# GitHub Projects Ticketing

GitHub Projects-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Hierarchy Mapping

| Core Term | GitHub Term | How to Implement |
|-----------|-------------|------------------|
| Initiative | Project (board) | GitHub Project board groups related work |
| Project | Milestone or Label | Use milestone for time-bound; label for categorical |
| Issue | Issue | Standard GitHub issue |
| Sub-Issue | Task list or Linked issue | Checklist in body, or separate issue with `parent: #123` label |

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

Or use GitHub's auto-linking:

```
Add password reset endpoint

Fixes #123
```

## CLI Commands

### Fetch Options (Pre-Creation)

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
# Started comment
gh issue comment 123 --body "$(cat <<'EOF'
🚀 **Started**
- Branch: `feature/platform/GH-123-password-api`
- Approach: Implementing REST endpoint with email service
EOF
)"

# Completed comment
gh issue comment 123 --body "$(cat <<'EOF'
✅ **Completed**
- PR: #456
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

## GitHub-Specific Notes

- **No native sub-issues**: Use task lists in issue body or linked issues with labels
- **Auto-close**: PRs with `Closes #123` auto-close issues on merge
- **Projects vs Milestones**: Projects are Kanban boards; Milestones are time-boxed
- **Task lists**: `- [ ] Task` in issue body creates trackable checkboxes
- **Cross-repo**: Use `owner/repo#123` to link issues across repositories

## Task List for Sub-Issues

When sub-issues are small, use task list in parent issue body:

```markdown
## Sub-tasks
- [ ] [Backend] Password reset API @developer1
- [ ] [Frontend] Reset form UI @developer2
- [ ] [Docs] Password reset guide @writer

Track progress by checking off items as completed.
```

For larger sub-issues, create separate issues with linking:

```bash
# In sub-issue body, reference parent
Parent: #101

# Or use a label
gh issue create --label "parent:#101"
```
