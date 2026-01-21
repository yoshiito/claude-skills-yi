# GitHub Projects Ticketing

GitHub-specific mappings and commands. See `ticketing-core.md` for universal rules. Blocks/BlockedBy and Parent Relationships are mandatory for our setup and must be defined as part of creating tickets.

## MANDATORY: Relationship Creation via GraphQL

**CLI flags `--parent`, `--add-blocked-by` DO NOT EXIST.** Use GraphQL only.

### Required Header

All GraphQL calls MUST include: `-H "GraphQL-Features: sub_issues"`

### Get Node IDs First

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
NODE=$(gh api repos/$REPO/issues/NUMBER --jq '.node_id')
```

### GraphQL Mutations

| Relationship | Mutation | Required Params |
|--------------|----------|-----------------|
| Set parent | `addSubIssue` | `issueId` (parent), `subIssueId` (child) |
| Set blocker | `addBlockedBy` | `issueId` (blocked), `blockingIssueId` (blocker) |
| Remove parent | `removeSubIssue` | `issueId` (parent), `subIssueId` (child) |
| Remove blocker | `removeBlockedBy` | `issueId` (blocked), `blockingIssueId` (blocker) |

### Mutation Templates

**Add sub-issue (set parent):**
```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation { addSubIssue(input: { issueId: "PARENT_NODE", subIssueId: "CHILD_NODE" }) { issue { number } subIssue { number } } }'
```

**Add blocker:**
```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation { addBlockedBy(input: { issueId: "BLOCKED_NODE", blockingIssueId: "BLOCKER_NODE" }) { issue { number } } }'
```

### Relationship Checklist (BLOCKING)

Before marking sub-issue creation complete:

- [ ] Parent set via `addSubIssue` GraphQL mutation
- [ ] Blockers set via `addBlockedBy` GraphQL mutation
- [ ] Header `-H "GraphQL-Features: sub_issues"` included
- [ ] Node IDs obtained (not issue numbers)
- [ ] Relationships NOT written in issue body text

**FAILURE TO SET RELATIONSHIPS = INCOMPLETE WORK**

---

## Hierarchy Mapping

| Core Term | GitHub Term | Implementation |
|-----------|-------------|----------------|
| Initiative | Project board | `gh project list` |
| Project | Milestone | `gh milestone list` |
| Issue | Issue | `gh issue create` |
| Sub-Issue | Issue + parent relationship | Create issue, then `addSubIssue` |

## Ticket ID Format

`#XXX` or `GH-XXX` (e.g., `#123`, `GH-123`)

## Branch Pattern

```
feature/platform/GH-101-password-reset-api
fix/portal/GH-102-login-validation
docs/platform/GH-103-api-reference
```

## Commit Pattern

```
[GH-123] Brief description

Closes #123
```

---

## CLI Commands

### Fetch Options

```bash
gh repo view                    # Verify repository
gh milestone list               # List milestones
gh label list                   # List labels
gh project list                 # List project boards
```

### Create Issues

```bash
# Create with milestone and labels
gh issue create \
  --title "[Feature] Title" \
  --body "Description" \
  --milestone "Milestone Name" \
  --label "feature"
```

### Update Issues

```bash
gh issue edit 123 --add-label "in-progress"
gh issue edit 123 --add-assignee @username
gh issue close 123
```

### Progress Comments

```bash
# Started
gh issue comment 123 --body "🚀 **Started** - Branch: \`feature/GH-123-name\`"

# Completed
gh issue comment 123 --body "✅ **Completed** - PR: #456"
```

### Query Issues

```bash
gh issue list --assignee @me
gh issue list --milestone "Milestone"
gh issue list --label "in-progress"
gh issue view 123
```

### Query Relationships (GraphQL)

```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query { repository(owner: "OWNER", name: "REPO") { issue(number: 123) {
  parent { number title }
  subIssues(first: 10) { nodes { number title } }
  blockedByIssues(first: 10) { nodes { number title state } }
} } }'
```

---

## Status Mapping via Labels

| Stage | Label |
|-------|-------|
| Created | `backlog` or `todo` |
| Work started | `in-progress` |
| PR created | `in-review` |
| PR merged | Issue closed via `Closes #123` |

---

## Complete Workflow Example

```bash
# 1. Create parent issue
parent=$(gh issue create --title "[Feature] Password Reset" --body "..." | grep -oP '\d+')

# 2. Create sub-issues
backend=$(gh issue create --title "[Backend] Reset API" --body "..." | grep -oP '\d+')
frontend=$(gh issue create --title "[Frontend] Reset UI" --body "..." | grep -oP '\d+')

# 3. Get node IDs
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
parent_node=$(gh api repos/$REPO/issues/$parent --jq '.node_id')
backend_node=$(gh api repos/$REPO/issues/$backend --jq '.node_id')
frontend_node=$(gh api repos/$REPO/issues/$frontend --jq '.node_id')

# 4. Set parent relationships (MANDATORY)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: { issueId: "'"$parent_node"'", subIssueId: "'"$backend_node"'" }) { subIssue { number } }
}'
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: { issueId: "'"$parent_node"'", subIssueId: "'"$frontend_node"'" }) { subIssue { number } }
}'

# 5. Set blocker (frontend blocked by backend) (MANDATORY if dependency exists)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: { issueId: "'"$frontend_node"'", blockingIssueId: "'"$backend_node"'" }) { issue { number } }
}'
```

---

## GitHub-Specific Notes

- **GraphQL required**: No CLI flags for relationships
- **Beta header required**: `-H "GraphQL-Features: sub_issues"`
- **Node IDs required**: Issue numbers alone won't work
- **Auto-close PRs**: Use `Closes #123` in PR body
- **Cross-repo links**: `owner/repo#123`
- **Task lists in body**: `- [ ] Task` for simple checklists only (not for tracked sub-issues)
