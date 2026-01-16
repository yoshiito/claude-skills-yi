# GitHub Projects Ticketing

GitHub Projects-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Hierarchy Mapping

| Core Term | GitHub Term | How to Implement |
|-----------|-------------|------------------|
| Initiative | Project (board) | GitHub Project board groups related work |
| Project | Milestone or Label | Use milestone for time-bound; label for categorical |
| Issue | Issue | Standard GitHub issue |
| Sub-Issue | Sub-issue (native) | Use GitHub's native sub-issues feature (GA April 2025) |

```
Project Board: "Q1 User Growth"
└── Milestone: "User Authentication System"
    └── Issue #101: "Implement Password Reset"
        ├── Task: [ ] Backend: Password reset API
        ├── Task: [ ] Frontend: Reset form UI
        └── Task: [ ] Docs: Password reset guide
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
# Create issue with milestone and labels
gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Acceptance Criteria
- [ ] User can request password reset
- [ ] Email sent with reset link
- [ ] User can set new password

## Sub-tasks
- [ ] [Backend] Password reset API
- [ ] [Frontend] Reset form UI
- [ ] [Docs] Password reset guide
EOF
)" \
  --milestone "User Authentication" \
  --label "feature,backend"

# Create linked sub-issue
gh issue create \
  --title "[Backend] Password reset API" \
  --body "Parent: #101" \
  --label "backend,sub-task"
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

## Sub-Issues (Native Support)

GitHub now has native sub-issues support (GA as of April 2025). Sub-issues create a parent-child hierarchy for tasks.

### Creating Sub-Issues

```bash
# Create parent issue first
gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "## Description
Implement password reset functionality."

# Create sub-issue linked to parent
# Use the GitHub web UI or API to create sub-issues under a parent
# The gh CLI support for sub-issues may require the --parent flag (check current gh version)
```

### Via GitHub Web UI

1. Open the parent issue
2. Click "Add sub-issue" in the sub-issues section
3. Create or link existing issues as sub-issues

### Sub-Issue Features

- **Automatic progress tracking**: Parent issue shows completion % based on sub-issues
- **Tree visualization**: View hierarchical structure of issues
- **Inherited context**: Sub-issues inherit project/milestone from parent

## Dependencies (Native Support)

GitHub now has native issue dependencies (GA as of August 2025). Dependencies define blocking relationships between issues.

### Creating Dependencies

```bash
# Via GitHub web UI or API:
# 1. Open an issue
# 2. In the "Development" section, click "Add dependency"
# 3. Choose "blocked by" or "blocks" relationship
# 4. Search and select the related issue
```

### Dependency Types

| Relationship | Meaning |
|--------------|---------|
| **Blocked by** | This issue cannot start until the blocking issue is resolved |
| **Blocks** | This issue is blocking other issues from starting |

### Example Dependency Setup

For a password reset feature:

```
#101 [Backend] Password reset API
  └── blocks: #102, #103

#102 [Frontend] Reset form UI
  └── blocked by: #101

#103 [Docs] Password reset guide
  └── blocked by: #101
```

### Tracking Dependencies

When starting work on a blocked issue:

```bash
# Check if blocker is resolved via web UI or:
gh issue view 101 --json state

# Once unblocked, start work and add comment
gh issue comment 102 --body "$(cat <<'EOF'
🔓 **Unblocked**
- Blocker #101 is now complete
- Starting work
EOF
)"
```

## GitHub-Specific Notes

- **Native sub-issues**: Create hierarchical issue relationships (GA April 2025)
- **Native dependencies**: Define blocking relationships (GA August 2025)
- **Issue types**: Classify issues as bugs, features, tasks, etc.
- **Auto-close**: PRs with `Closes #123` auto-close issues on merge
- **Projects vs Milestones**: Projects are Kanban boards; Milestones are time-boxed
- **Task lists**: `- [ ] Task` in issue body creates trackable checkboxes
- **Cross-repo**: Use `owner/repo#123` to link issues across repositories
- **Advanced search**: Support for complex queries using `and` and `or`

## Legacy: Task List for Sub-Issues

For simple sub-tasks or repositories not using native sub-issues, use task lists in issue body:

```markdown
## Sub-tasks
- [ ] [Backend] Password reset API @developer1
- [ ] [Frontend] Reset form UI @developer2
- [ ] [Docs] Password reset guide @writer

Track progress by checking off items as completed.
```
