# GitHub Projects Ticketing

GitHub Projects-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Critical: GitHub Has Native Relationship Fields via GraphQL

GitHub provides **native parent-child and blocking relationships** through the GraphQL Sub-Issues API (beta feature).

**IMPORTANT**: These relationships are NOT available via CLI flags (`--parent`, `--add-blocked-by` do NOT exist). You must use GraphQL mutations.

| Relationship | Purpose | GraphQL Mutation |
|--------------|---------|------------------|
| **Parent** | Links sub-issue to parent issue | `addSubIssue` |
| **Blocked By** | Issues that must complete before this one | `addBlockedBy` |
| **Remove Parent** | Unlinks sub-issue from parent | `removeSubIssue` |
| **Remove Blocked By** | Removes blocking relationship | `removeBlockedBy` |

### Required: Relationship Checklist

Before creating any sub-issue, complete this checklist:

- [ ] **Parent relationship set** via `addSubIssue` GraphQL mutation
- [ ] **Blocked By set** via `addBlockedBy` GraphQL mutation for any dependencies
- [ ] **Beta header included** in all GraphQL calls: `-H "GraphQL-Features: sub_issues"`
- [ ] **Node IDs obtained** using `gh api repos/OWNER/REPO/issues/NUMBER --jq '.node_id'`
- [ ] **Relationships NOT in issue body** - all relationships use native GraphQL API only

### Setting Relationships via GraphQL

**Step 1: Get Node IDs (Required)**

```bash
# Get repository owner and name from current directory
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# Get parent issue node ID
PARENT_NODE=$(gh api repos/$REPO/issues/101 --jq '.node_id')

# Get child issue node ID
CHILD_NODE=$(gh api repos/$REPO/issues/102 --jq '.node_id')
```

**Step 2: Set Parent-Child Relationship**

```bash
# Add sub-issue relationship (102 becomes child of 101)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: {
    issueId: "'"$PARENT_NODE"'"
    subIssueId: "'"$CHILD_NODE"'"
  }) {
    issue {
      number
      title
    }
    subIssue {
      number
      title
    }
  }
}'
```

**Step 3: Set Blocked-By Relationship**

```bash
# Get blocking issue node ID
BLOCKING_NODE=$(gh api repos/$REPO/issues/100 --jq '.node_id')

# Add blocked-by relationship (102 is blocked by 100)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: {
    issueId: "'"$CHILD_NODE"'"
    blockingIssueId: "'"$BLOCKING_NODE"'"
  }) {
    issue {
      number
      title
    }
  }
}'
```

### Complete Workflow: Create Issues and Set Relationships

```bash
# 1. Create parent issue
parent_num=$(gh issue create \
  --title "[Feature] Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Acceptance Criteria
- [ ] User can request password reset
- [ ] Email sent with reset link
- [ ] User can set new password
EOF
)" | grep -oP '\d+')

# 2. Create sub-issue
child_num=$(gh issue create \
  --title "[Backend] Password reset API" \
  --body "..." | grep -oP '\d+')

# 3. Get repository info
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# 4. Get node IDs
parent_node=$(gh api repos/$REPO/issues/$parent_num --jq '.node_id')
child_node=$(gh api repos/$REPO/issues/$child_num --jq '.node_id')

# 5. Set parent-child relationship
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$child_node"'"
  }) {
    issue { number title }
    subIssue { number title }
  }
}'
```

## Hierarchy Mapping

| Core Term | GitHub Term | How to Implement |
|-----------|-------------|------------------|
| Initiative | Project (board) | GitHub Project board groups related work |
| Project | Milestone or Label | Use milestone for time-bound; label for categorical |
| Issue | Issue | Standard GitHub issue |
| Sub-Issue | Issue with Parent relationship | Separate issue linked via GraphQL `addSubIssue` mutation |

```
Project Board: "Q1 User Growth"
└── Milestone: "User Authentication System"
    └── Issue #101: "Implement Password Reset" (parent)
        ├── Issue #102: "[Backend] Password reset API" (parent: #101)
        ├── Issue #103: "[Frontend] Reset form UI" (parent: #101, blockedBy: #102)
        └── Issue #104: "[Docs] Password reset guide" (parent: #101, blockedBy: #102)
```

## Ticket ID Format

`#XXX` or `GH-XXX` (e.g., `#123`, `GH-123`)

## Git Workflow

See `git-workflow.md` for complete Git workflow including base branch confirmation.

**Key point**: Always ask the user which branch to branch from and merge back to. Do not assume `main`.

### Branch Pattern

```
feature/platform/GH-101-password-reset-api
fix/portal/GH-102-login-validation
docs/platform/GH-103-api-reference
```

### Commit Pattern

```
[GH-123] Brief description

Closes #123
```

Or use GitHub's auto-linking:

```
Add password reset endpoint

Fixes #123
```

## Pre-Creation Confirmation

**CRITICAL**: Before creating any issue, explicitly confirm the GitHub context with the user.

### Step 1: Fetch Available Options

```bash
# Verify repository
gh repo view

# List projects (boards)
gh project list

# List milestones
gh milestone list

# List labels
gh label list
```

### Step 2: Present Options to User

```
Before creating this issue, please confirm the GitHub context:

Issue: "[Title of the issue]"

**Repository**: (from gh repo view)
- owner/repo-name

**Project Board** (Initiative level):
1. Q1 User Growth
2. Platform Reliability
3. [Create new project]
4. [None]

**Milestone** (Project level):
1. User Authentication System
2. v2.0 Release
3. [Create new milestone]
4. [None]

**Labels**:
1. feature
2. backend
3. frontend
4. [Other]

Which options should I use?
```

### Step 3: Create After Confirmation

Only create issues after user confirms:
- Repository is correct
- Project board selected (or none)
- Milestone selected (or none)
- Labels selected

If project or milestone doesn't exist, create it first:

```bash
# Create new project
gh project create --title "New Project Name"

# Create new milestone
gh milestone create --title "New Milestone"
```

---

## CLI Commands

### Fetch Options

```bash
# Verify repository
gh repo view

# List milestones
gh milestone list

# List labels
gh label list

# List projects (boards)
gh project list

# View project details
gh project view PROJECT_NUMBER
```

### Create Issues

```bash
# Step 1: Create parent issue with milestone and labels
parent_num=$(gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Acceptance Criteria
- [ ] User can request password reset
- [ ] Email sent with reset link
- [ ] User can set new password
EOF
)" \
  --milestone "User Authentication" \
  --label "feature" | grep -oP '\d+')
# Returns issue number: 101

# Step 2: Create sub-issues (without relationships yet)
backend_num=$(gh issue create \
  --title "[Backend] Password reset API" \
  --label "backend" \
  --body "..." | grep -oP '\d+')
# Returns: 102

frontend_num=$(gh issue create \
  --title "[Frontend] Reset form UI" \
  --label "frontend" \
  --body "..." | grep -oP '\d+')
# Returns: 103

# Step 3: Get repository info and node IDs
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
parent_node=$(gh api repos/$REPO/issues/$parent_num --jq '.node_id')
backend_node=$(gh api repos/$REPO/issues/$backend_num --jq '.node_id')
frontend_node=$(gh api repos/$REPO/issues/$frontend_num --jq '.node_id')

# Step 4: Set parent-child relationships via GraphQL
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  backend: addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$backend_node"'"
  }) {
    issue { number }
    subIssue { number }
  }
  frontend: addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$frontend_node"'"
  }) {
    issue { number }
    subIssue { number }
  }
}'

# Step 5: Add blocking relationship (Frontend blocked by Backend)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: {
    issueId: "'"$frontend_node"'"
    blockingIssueId: "'"$backend_node"'"
  }) {
    issue { number title }
  }
}'
```

### Update Issues

```bash
# Add to project board
gh project item-add PROJECT_NUMBER --url ISSUE_URL

# Update project item status
gh project item-edit --project-id PROJECT_ID --id ITEM_ID --field-id STATUS_FIELD_ID --single-select-option-id OPTION_ID

# Add labels
gh issue edit 123 --add-label "in-progress"

# Remove labels
gh issue edit 123 --remove-label "todo"

# Assign
gh issue edit 123 --add-assignee @username

# Close issue
gh issue close 123
```

### Progress Comments

```bash
# Started comment (include base branch)
gh issue comment 123 --body "$(cat <<'EOF'
🚀 **Started**
- Branch: `feature/platform/GH-123-password-api`
- Base: `{base_branch}` (confirmed with user)
- Approach: Implementing REST endpoint with email service
EOF
)"

# Completed comment
gh issue comment 123 --body "$(cat <<'EOF'
✅ **Completed**
- PR: #456 (targeting {base_branch})
- Files: `app/api/auth.py`, `app/services/email.py`
EOF
)"
```

### Query Issues

```bash
# My issues
gh issue list --assignee @me

# Issues by milestone
gh issue list --milestone "User Authentication"

# Issues by label
gh issue list --label "in-progress"

# Issues in project
gh project item-list PROJECT_NUMBER

# View issue details
gh issue view 123
```

### Pull Requests

```bash
# Create PR linking to issue
gh pr create \
  --title "[GH-123] Add password reset endpoint" \
  --body "$(cat <<'EOF'
## Summary
Implements password reset API endpoint.

Closes #123

## Changes
- Added POST /api/v1/auth/reset
- Added email notification service

## Test Plan
- [ ] Unit tests pass
- [ ] Manual test: request reset, receive email
EOF
)"

# Link PR to issue (auto-close on merge)
# Use keywords in PR body: Closes #123, Fixes #123, Resolves #123
```

## Status Mapping via Labels

| Stage | Recommended Label |
|-------|-------------------|
| Created | `backlog` or `todo` |
| Work started | `in-progress` |
| PR created | `in-review` |
| PR merged | (Issue closed automatically) |

## Project Board Status Fields

Configure custom status field in GitHub Project:

| Status | When |
|--------|------|
| 📋 Backlog | Issue created, not started |
| 🏃 In Progress | Work started |
| 👀 In Review | PR created |
| ✅ Done | PR merged, issue closed |

## Sub-Issues (Native Parent Relationship via GraphQL)

GitHub has native parent-child relationships via the **GraphQL Sub-Issues API** (beta feature).

**IMPORTANT**: The CLI flags `--parent`, `--add-blocked-by`, `--add-blocks` do NOT exist. You must use GraphQL.

### Creating Sub-Issues with Parent Relationship

```bash
# 1. Create parent issue first
parent_num=$(gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Acceptance Criteria
- [ ] User can request password reset
- [ ] Email sent with reset link
- [ ] User can set new password
EOF
)" | grep -oP '\d+')
# Returns: 101

# 2. Create sub-issues (relationships set separately)
backend_num=$(gh issue create \
  --title "[Backend] Password reset API" \
  --body "..." | grep -oP '\d+')
# Returns: 102

frontend_num=$(gh issue create \
  --title "[Frontend] Reset form UI" \
  --body "..." | grep -oP '\d+')
# Returns: 103

# 3. Get repository info and node IDs
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
parent_node=$(gh api repos/$REPO/issues/$parent_num --jq '.node_id')
backend_node=$(gh api repos/$REPO/issues/$backend_num --jq '.node_id')
frontend_node=$(gh api repos/$REPO/issues/$frontend_num --jq '.node_id')

# 4. Set parent-child relationships via GraphQL
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  backend: addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$backend_node"'"
  }) {
    issue { number }
    subIssue { number }
  }
  frontend: addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$frontend_node"'"
  }) {
    issue { number }
    subIssue { number }
  }
}'

# 5. Set blocking relationship (Frontend blocked by Backend)
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: {
    issueId: "'"$frontend_node"'"
    blockingIssueId: "'"$backend_node"'"
  }) {
    issue { number title }
  }
}'
```

### Viewing Parent-Child Relationships

```bash
# View issue with relationships using GraphQL
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 102) {
      number
      title
      parent {
        number
        title
      }
      subIssues(first: 10) {
        nodes {
          number
          title
        }
      }
      blockedByIssues(first: 10) {
        nodes {
          number
          title
        }
      }
    }
  }
}'
```

## Dependencies (Native Relationship Fields via GraphQL)

**MANDATORY**: Use GitHub's GraphQL API for all dependency relationships.

### Setting Dependencies via GraphQL

```bash
# Get node IDs for both issues
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
blocked_node=$(gh api repos/$REPO/issues/102 --jq '.node_id')
blocking_node=$(gh api repos/$REPO/issues/101 --jq '.node_id')

# Mark issue 102 as blocked by issue 101
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: {
    issueId: "'"$blocked_node"'"
    blockingIssueId: "'"$blocking_node"'"
  }) {
    issue {
      number
      title
      blockedByIssues(first: 10) {
        nodes { number title }
      }
    }
  }
}'

# Remove a blocking relationship
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  removeBlockedBy(input: {
    issueId: "'"$blocked_node"'"
    blockingIssueId: "'"$blocking_node"'"
  }) {
    issue { number title }
  }
}'
```

### Dependency Status Notification

When a blocker is resolved, add a comment to notify:

```bash
gh issue comment 102 --body "$(cat <<'EOF'
🔓 **Unblocked**
- Blocker #101 is now complete
- Starting work
EOF
)"
```

### AI Agent Execution with Dependencies

For AI agents executing GitHub-tracked work:

```bash
# 1. Query issue relationships via GraphQL
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
issue_num=102

gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query {
  repository(owner: "'${REPO%/*}'", name: "'${REPO#*/}'") {
    issue(number: '$issue_num') {
      state
      blockedByIssues(first: 10) {
        nodes {
          number
          title
          state
        }
      }
    }
  }
}' --jq '.data.repository.issue'

# 2. Check if any blockers exist and are still open
# Example output: {"state":"OPEN","blockedByIssues":{"nodes":[{"number":101,"state":"OPEN"}]}}

# 3. If blockedByIssues.nodes array has items with state == "OPEN", skip to next task
# 4. If no open blockers, execute the task
```

**DO NOT parse issue body for dependencies** - always use GraphQL to query the native `blockedByIssues` field.

## GitHub-Specific Notes

- **Native parent/sub-issues**: Use GraphQL `addSubIssue` mutation with `-H "GraphQL-Features: sub_issues"` header
- **Native blocking/blocked-by**: Use GraphQL `addBlockedBy` mutation with the beta header
- **CLI flags DO NOT EXIST**: `--parent`, `--add-blocked-by`, `--add-blocks` are NOT valid gh CLI flags
- **Node IDs required**: Get via `gh api repos/OWNER/REPO/issues/NUMBER --jq '.node_id'`
- **Issue types**: Classify issues as bugs, features, tasks, etc.
- **Auto-close**: PRs with `Closes #123` auto-close issues on merge
- **Projects vs Milestones**: Projects are Kanban boards; Milestones are time-boxed
- **Task lists**: `- [ ] Task` in issue body for simple checklists (NOT for sub-issues - use GraphQL)
- **Cross-repo**: Use `owner/repo#123` to link issues across repositories
- **Advanced search**: Support for complex queries using `and` and `or`
