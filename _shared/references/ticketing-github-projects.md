# GitHub Projects Ticketing

GitHub Projects-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Critical: GitHub Projects Has Native Relationship Fields

GitHub Projects has built-in relationship fields that MUST be used for issue relationships.

| Relationship | Purpose | CLI Flag |
|--------------|---------|----------|
| **Parent** | Links sub-issue to parent issue | `--parent ISSUE_NUMBER` |
| **Blocked By** | Issues that must complete before this one | `--add-blocked-by ISSUE_NUMBER` |
| **Blocks** | Issues that depend on this one completing | `--add-blocks ISSUE_NUMBER` |

### Required: Relationship Checklist

Before creating any sub-issue, complete this checklist:

- [ ] **Parent relationship set** via `--parent` flag or `gh issue edit --add-parent`
- [ ] **Blocked By set** via `--add-blocked-by` for any dependencies
- [ ] **Blocks set** via `--add-blocks` if this issue blocks others
- [ ] **Relationships NOT in issue body** - all relationships use native fields only

### Setting Relationships via CLI

```bash
# Set parent relationship (sub-issue → parent)
gh issue edit ISSUE_NUMBER --add-parent PARENT_ISSUE_NUMBER

# Set blocking relationship (this issue blocks another)
gh issue edit ISSUE_NUMBER --add-blocks BLOCKED_ISSUE_NUMBER

# Set blocked-by relationship (this issue is blocked by another)
gh issue edit ISSUE_NUMBER --add-blocked-by BLOCKING_ISSUE_NUMBER

# View issue relationships
gh issue view ISSUE_NUMBER --json parent,blockedBy,blocks
```

### Creating Sub-Issues with Relationships

```bash
# Create a sub-issue with parent relationship
gh issue create \
  --title "[Backend] Password reset API" \
  --body "$(cat <<'EOF'
## Story
As a user, I want to reset my password via API...

## Acceptance Criteria
...
EOF
)" \
  --parent 101

# Then add blocking relationships if needed
gh issue edit 102 --add-blocked-by 100
```

## Hierarchy Mapping

| Core Term | GitHub Term | How to Implement |
|-----------|-------------|------------------|
| Initiative | Project (board) | GitHub Project board groups related work |
| Project | Milestone or Label | Use milestone for time-bound; label for categorical |
| Issue | Issue | Standard GitHub issue |
| Sub-Issue | Issue with Parent relationship | Separate issue linked via `--parent` flag |

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
# Create parent issue with milestone and labels
gh issue create \
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
  --label "feature"
# Returns: Created issue #101

# Create sub-issue with parent relationship (REQUIRED)
gh issue create \
  --title "[Backend] Password reset API" \
  --parent 101 \
  --label "backend" \
  --body "..."
# Returns: Created issue #102

# Create another sub-issue with parent AND blocking relationship
gh issue create \
  --title "[Frontend] Reset form UI" \
  --parent 101 \
  --label "frontend" \
  --body "..."
# Returns: Created issue #103

# Add blocking relationship (Frontend blocked by Backend)
gh issue edit 103 --add-blocked-by 102
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

## Sub-Issues (Native Parent Relationship)

GitHub has native parent-child relationships. Create sub-issues using the `--parent` flag.

### Creating Sub-Issues with Parent Relationship

```bash
# 1. Create parent issue first
gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Acceptance Criteria
- [ ] User can request password reset
- [ ] Email sent with reset link
- [ ] User can set new password
EOF
)"
# Returns: Created issue #101

# 2. Create sub-issues with parent relationship
gh issue create \
  --title "[Backend] Password reset API" \
  --parent 101 \
  --body "..."
# Returns: Created issue #102

gh issue create \
  --title "[Frontend] Reset form UI" \
  --parent 101 \
  --body "..."
# Returns: Created issue #103

# 3. Add blocking relationships between sub-issues
gh issue edit 103 --add-blocked-by 102
```

### Viewing Parent-Child Relationships

```bash
# View sub-issues of a parent
gh issue view 101 --json subIssues

# View parent of a sub-issue
gh issue view 102 --json parent
```

## Dependencies (Native Relationship Fields)

**MANDATORY**: Use GitHub's native relationship fields for all dependencies.

### Setting Dependencies via CLI

```bash
# Mark issue 102 as blocked by issue 101
gh issue edit 102 --add-blocked-by 101

# Mark issue 101 as blocking issues 102 and 103
gh issue edit 101 --add-blocks 102
gh issue edit 101 --add-blocks 103

# View all relationships for an issue
gh issue view 102 --json parent,blockedBy,blocks

# Remove a blocking relationship
gh issue edit 102 --remove-blocked-by 101
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
# 1. Query issue relationships via native fields
gh issue view ISSUE_NUMBER --json state,blockedBy

# 2. Check if any blockers exist and are still open
# Example output: {"state":"OPEN","blockedBy":[{"number":101,"state":"OPEN"}]}

# 3. If blockedBy array has items with state != "CLOSED", skip to next task
# 4. If no open blockers, execute the task
```

**DO NOT parse issue body for dependencies** - always use the native `blockedBy` field.

## GitHub-Specific Notes

- **Native parent/sub-issues**: Use `--parent` flag to create parent-child relationships
- **Native blocking/blocked-by**: Use `--add-blocked-by` and `--add-blocks` for dependencies
- **Issue types**: Classify issues as bugs, features, tasks, etc.
- **Auto-close**: PRs with `Closes #123` auto-close issues on merge
- **Projects vs Milestones**: Projects are Kanban boards; Milestones are time-boxed
- **Task lists**: `- [ ] Task` in issue body for simple checklists (not sub-issues)
- **Cross-repo**: Use `owner/repo#123` to link issues across repositories
- **Advanced search**: Support for complex queries using `and` and `or`
