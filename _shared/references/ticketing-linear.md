# Linear Ticketing

Linear-specific mappings and commands. See `ticketing-core.md` for universal rules.

## Hierarchy Mapping

| Core Term | Linear Term | Notes |
|-----------|-------------|-------|
| Initiative | Initiative | Enterprise/Plus only; use Project if unavailable |
| Project | Project | Time-bound deliverable |
| Issue | Issue (parent) | User-facing feature |
| Sub-Issue | Sub-Issue | Set via `parentId` |

## Ticket ID Format

`LIN-XXX` (e.g., `LIN-123`)

## Branch Pattern

```
feature/platform/LIN-101-password-reset-api
fix/portal/LIN-102-login-validation
docs/platform/LIN-103-api-reference
```

## Commit Pattern

```
[LIN-123] Brief description

Ticket: https://linear.app/team/issue/LIN-123
```

## MCP Commands

### Fetch Options (Pre-Creation)

```python
# List teams
teams = mcp.list_teams()

# List projects (optionally filtered)
projects = mcp.list_projects()
projects = mcp.list_projects(team="Platform Team")
projects = mcp.list_projects(state="started")

# Get project details
project = mcp.get_project(query="User Authentication")

# List issue statuses
statuses = mcp.list_issue_statuses(team="Platform Team")

# List labels
labels = mcp.list_issue_labels(team="Platform Team")
```

### Create Issues

```python
# Create parent issue
mcp.create_issue(
    title="Implement Password Reset Flow",
    team="Platform Team",
    project="User Authentication",
    description="...",
    labels=["feature"]
)

# Create sub-issue
mcp.create_issue(
    title="[Backend] Password reset API",
    team="Platform Team",
    parentId="parent-issue-id",
    assignee="developer@email.com",
    description="..."
)

# Create with dependencies
mcp.create_issue(
    title="[Frontend] Reset form UI",
    team="Platform Team",
    parentId="parent-issue-id",
    blockedBy=["LIN-101"],  # Backend must complete first
    description="..."
)
```

### Update Issues

```python
# Move to In Progress
mcp.update_issue(
    id="LIN-123",
    state="In Progress"
)

# Move to Done
mcp.update_issue(
    id="LIN-123",
    state="Done"
)

# Add assignee
mcp.update_issue(
    id="LIN-123",
    assignee="developer@email.com"
)
```

### Progress Comments

```python
# Started comment
mcp.create_comment(
    issueId="LIN-123",
    body="🚀 **Started**\n- Branch: `feature/platform/LIN-123-password-api`"
)

# Completed comment
mcp.create_comment(
    issueId="LIN-123",
    body="✅ **Completed**\n- PR: [link]\n- Files: `app/api/auth.py`"
)
```

### Query Issues

```python
# My issues
my_issues = mcp.list_issues(assignee="me")

# Team's in-progress issues
in_progress = mcp.list_issues(
    team="Platform Team",
    state="In Progress"
)

# Issues in a project
project_issues = mcp.list_issues(
    project="User Authentication"
)

# Get issue details
issue = mcp.get_issue(id="LIN-123")
```

## Status Mapping

| Stage | Linear Status |
|-------|---------------|
| Created | Backlog or Todo |
| Work started | In Progress |
| PR created | In Review |
| PR merged | Done |

## Linear-Specific Notes

- **Initiatives** require Enterprise/Plus plan
- **Sub-issues** are created by setting `parentId`
- **Dependencies** use `blockedBy` and `blocks` fields
- **Auto-close**: Parent can auto-close when all sub-issues complete (if configured)
