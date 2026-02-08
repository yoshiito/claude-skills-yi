# GitHub Operations

Internal reference for Project Coordinator. Handles GitHub Issues with GraphQL for relationships.

---

## ⛔ BLOCKING: Relationship Protocol for GitHub

**This section is NON-NEGOTIABLE. Read it EVERY TIME before creating a ticket with relationships.**

### What DOES vs DOES NOT Set Relationships

| Action | Sets Parent? | Sets Blockers? |
|--------|-------------|----------------|
| `gh project item-add` | ❌ NO | ❌ NO |
| Writing "Part of #X" in body | ❌ NO | ❌ NO |
| Writing "Blocked by #Y" in body | ❌ NO | ❌ NO |
| Writing "Parent: #X" in body | ❌ NO | ❌ NO |
| GraphQL `addSubIssue` mutation | ✅ YES | - |
| GraphQL `addBlockedBy` mutation | - | ✅ YES |

### ⛔ NEVER Do This

```markdown
## Body text that does NOTHING:
Parent: #262
Blocked by: #263, #264
Part of: #262
```

**This is cosmetic text. GitHub ignores it. The relationship is NOT set.**

### ✅ ALWAYS Do This

When a ticket specifies `Parent: #NUM`:
1. Create the issue (Step 1-2)
2. **Run GraphQL `addSubIssue` mutation** (Step 3) — MANDATORY
3. **Run verification query** (Step 5) — MANDATORY
4. **Confirm `parent.number` matches expected** — MANDATORY

**If you skip Steps 3-5, the relationship does NOT exist.**

### Atomic Operation Rule

Creating a ticket with relationships is ONE atomic operation:

```
Create Issue → Set Parent (GraphQL) → Set Blockers (GraphQL) → VERIFY → Report
     ↓              ↓                      ↓                    ↓
   Step 1-2       Step 3                 Step 4              Step 5
```

**If ANY step fails, the ENTIRE operation fails. Do not report success.**

---

---

## Operation: Create Ticket

### Step 1: Create the Issue

```bash
# Extract issue number from output
ISSUE_NUM=$(gh issue create \
  --title "[Type] Title" \
  --body "Body content" \
  --label "label1,label2" \
  2>&1 | grep -oE '[0-9]+$')
```

### Step 2: Get Node ID

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
ISSUE_NODE=$(gh api repos/$REPO/issues/$ISSUE_NUM --jq '.node_id')
```

### Step 3: Set Parent (for sub-issues)

```bash
# Get parent node ID
PARENT_NODE=$(gh api repos/$REPO/issues/$PARENT_NUM --jq '.node_id')

# Set parent relationship
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: { issueId: "'"$PARENT_NODE"'", subIssueId: "'"$ISSUE_NODE"'" }) {
    subIssue { number }
  }
}'
```

### Step 4: Set Blockers (if any)

```bash
# Get blocker node ID
BLOCKER_NODE=$(gh api repos/$REPO/issues/$BLOCKER_NUM --jq '.node_id')

# Set blocker relationship
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: { issueId: "'"$ISSUE_NODE"'", blockingIssueId: "'"$BLOCKER_NODE"'" }) {
    issue { number }
  }
}'
```

### Step 5: Verify Relationships

```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: '"$ISSUE_NUM"') {
      number
      title
      parent { number title }
      blockedByIssues(first: 10) { nodes { number title } }
    }
  }
}'
```

---

## Operation: Update Ticket

### Update Title/Body

```bash
gh issue edit $ISSUE_NUM --title "New Title"
gh issue edit $ISSUE_NUM --body "New Body"
```

### Update Labels

```bash
gh issue edit $ISSUE_NUM --add-label "in-progress"
gh issue edit $ISSUE_NUM --remove-label "backlog"
```

### Add Comment

```bash
gh issue comment $ISSUE_NUM --body "Comment text"
```

### Close Issue

```bash
gh issue close $ISSUE_NUM
```

---

## Operation: Set Relationships

### Set Parent

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
PARENT_NODE=$(gh api repos/$REPO/issues/$PARENT_NUM --jq '.node_id')
CHILD_NODE=$(gh api repos/$REPO/issues/$CHILD_NUM --jq '.node_id')

gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: { issueId: "'"$PARENT_NODE"'", subIssueId: "'"$CHILD_NODE"'" }) {
    subIssue { number }
  }
}'
```

### Add Blocker

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
BLOCKED_NODE=$(gh api repos/$REPO/issues/$BLOCKED_NUM --jq '.node_id')
BLOCKER_NODE=$(gh api repos/$REPO/issues/$BLOCKER_NUM --jq '.node_id')

gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: { issueId: "'"$BLOCKED_NODE"'", blockingIssueId: "'"$BLOCKER_NODE"'" }) {
    issue { number }
  }
}'
```

### Remove Blocker

```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  removeBlockedBy(input: { issueId: "'"$BLOCKED_NODE"'", blockingIssueId: "'"$BLOCKER_NODE"'" }) {
    issue { number }
  }
}'
```

---

## Operation: Verify Relationships

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
OWNER=$(echo $REPO | cut -d'/' -f1)
REPO_NAME=$(echo $REPO | cut -d'/' -f2)

gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query {
  repository(owner: "'"$OWNER"'", name: "'"$REPO_NAME"'") {
    issue(number: '"$ISSUE_NUM"') {
      number
      title
      parent { number title }
      subIssues(first: 20) { nodes { number title } }
      blockedByIssues(first: 20) { nodes { number title state } }
    }
  }
}'
```

**Verification checks:**
- `parent.number` should match expected parent
- `blockedByIssues.nodes` should contain expected blockers
- If either is wrong, relationships were NOT set correctly

---

## Status Mapping

| Status | Label | Command |
|--------|-------|---------|
| Backlog | `backlog` | `gh issue edit NUM --add-label backlog` |
| In Progress | `in-progress` | `gh issue edit NUM --add-label in-progress --remove-label backlog` |
| In Review | `in-review` | `gh issue edit NUM --add-label in-review --remove-label in-progress` |
| Done | (closed) | `gh issue close NUM` |

---

## Required Header

All GraphQL calls MUST include: `-H "GraphQL-Features: sub_issues"`

This is a beta feature flag. Without it, relationship queries/mutations will fail.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Could not resolve to a node" | Wrong node ID format | Re-fetch node ID via `gh api` |
| "Resource not accessible" | Permission issue | Check repo access |
| Empty parent/blockedBy | Mutation never ran | Run the GraphQL mutation |
| "Unknown field" on parent | Missing header | Add `-H "GraphQL-Features: sub_issues"` |
