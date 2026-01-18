# GitHub Projects Ticketing

GitHub Projects-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Hierarchy Mapping

| Core Term | GitHub Term | How to Implement |
|-----------|-------------|------------------|
| Initiative | Project (board) | GitHub Project board groups related work |
| Project | Milestone or Label | Use milestone for time-bound; label for categorical |
| Issue | Issue | Standard GitHub issue |
| Sub-Issue | Task list item | Checklist items in issue body (`- [ ] task`) |

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

## Sub-Issues (Task Lists)

**⚠️ GitHub does NOT have native parent-child issue relationships like Linear.**

Use **task lists** within an issue body to track sub-tasks:

### Creating Sub-Tasks in Issue Body

```bash
gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "$(cat <<'EOF'
## Description
Implement password reset functionality.

## Sub-tasks
- [ ] [Backend] Password reset API
- [ ] [Frontend] Reset form UI
- [ ] [Docs] Password reset guide

Track progress by checking off items as completed.
EOF
)"
```

### Linking Related Issues (Manual)

For more complex tracking, create separate issues and link them manually:

```bash
# Create parent issue
gh issue create \
  --title "[Feature] Implement Password Reset Flow" \
  --body "## Sub-issues
- #102 [Backend] Password reset API
- #103 [Frontend] Reset form UI
- #104 [Docs] Password reset guide"

# Create child issue with reference to parent
gh issue create \
  --title "[Backend] Password reset API" \
  --body "Parent: #101

## Description
..."
```

**Note**: These are just text references - GitHub does not track or enforce these relationships.

## Dependencies (Manual Tracking)

**⚠️ GitHub does NOT have native dependency fields like Linear's `blockedBy`/`blocks`.**

Track dependencies manually using issue body text or comments:

### Document Dependencies in Issue Body

```markdown
## Dependencies

**Blocked by:**
- #101 - Backend API must be complete first

**Blocks:**
- #103 - Frontend needs this API
- #104 - Docs need the API spec
```

### Track Dependency Status

When a blocker is resolved, add a comment:

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

1. Read the issue body for `Blocked by:` section
2. Check if blocking issues are closed: `gh issue view 101 --json state`
3. If blockers are open, skip to next unblocked task
4. If unblocked, execute the task

## GitHub-Specific Notes

- **NO native sub-issues**: Use task lists in issue body or manual linking
- **NO native dependencies**: Document in issue body, track manually
- **Issue types**: Classify issues as bugs, features, tasks, etc.
- **Auto-close**: PRs with `Closes #123` auto-close issues on merge
- **Projects vs Milestones**: Projects are Kanban boards; Milestones are time-boxed
- **Task lists**: `- [ ] Task` in issue body creates trackable checkboxes
- **Cross-repo**: Use `owner/repo#123` to link issues across repositories
- **Advanced search**: Support for complex queries using `and` and `or`
