# Linear Operations

Internal reference for Project Coordinator. Handles Linear via MCP commands.

## Key Advantage: Native Relationship Support

Linear supports `parentId` and `blockedBy` at creation time - no separate step needed.

---

## Operation: Create Ticket

### Parent Issue

```python
mcp.create_issue(
    title="[Feature] Password Reset Flow",
    team="Platform Team",
    project="User Authentication",
    description="...",
    labels=["feature"]
)
```

### Sub-Issue with Relationships

```python
mcp.create_issue(
    title="[Backend] Password reset API",
    team="Platform Team",
    parentId="parent-issue-id",      # Sets parent relationship
    blockedBy=["LIN-101", "LIN-102"], # Sets blocker relationships
    assignee="developer@email.com",
    description="..."
)
```

**Note**: Relationships are set AT CREATION TIME. No separate step needed.

---

## Operation: Update Ticket

### Update Status

```python
mcp.update_issue(
    id="LIN-123",
    state="In Progress"  # Backlog, Todo, In Progress, In Review, Done
)
```

### Update Fields

```python
mcp.update_issue(
    id="LIN-123",
    title="New Title",           # optional
    description="New body",       # optional
    assignee="dev@email.com",     # optional
    labels=["backend", "urgent"]  # optional
)
```

### Add Comment

```python
mcp.create_comment(
    issueId="LIN-123",
    body="Comment text with **markdown** support"
)
```

---

## Operation: Set Relationships

### Set Parent (on existing issue)

```python
mcp.update_issue(
    id="LIN-456",
    parentId="LIN-123"
)
```

### Add Blocker (on existing issue)

```python
# Get current blockers first
issue = mcp.get_issue(id="LIN-456")
current_blockers = issue.get("blockedBy", [])

# Add new blocker
mcp.update_issue(
    id="LIN-456",
    blockedBy=current_blockers + ["LIN-789"]
)
```

### Remove Blocker

```python
# Get current blockers
issue = mcp.get_issue(id="LIN-456")
current_blockers = issue.get("blockedBy", [])

# Remove specific blocker
new_blockers = [b for b in current_blockers if b != "LIN-789"]
mcp.update_issue(
    id="LIN-456",
    blockedBy=new_blockers
)
```

---

## Operation: Verify Relationships

```python
issue = mcp.get_issue(id="LIN-456")

# Check parent
parent_id = issue.get("parent", {}).get("id")
if parent_id != expected_parent:
    # FAIL: Parent not set correctly
    pass

# Check blockers
blockers = [b["id"] for b in issue.get("blockedBy", [])]
for expected_blocker in expected_blockers:
    if expected_blocker not in blockers:
        # FAIL: Missing blocker
        pass
```

---

## Pre-Creation: Fetch Options

Before creating issues, fetch available options:

```python
# List teams
teams = mcp.list_teams()

# List projects (optionally filtered)
projects = mcp.list_projects(team="Platform Team")

# List issue statuses
statuses = mcp.list_issue_statuses(team="Platform Team")

# List labels
labels = mcp.list_issue_labels(team="Platform Team")
```

---

## Status Mapping

| Status | Linear State | Notes |
|--------|-------------|-------|
| Backlog | `Backlog` | Default for new issues |
| In Progress | `In Progress` | Work started |
| In Review | `In Review` | PR created |
| Done | `Done` | Work complete |

---

## Progress Comments

### Started

```python
mcp.create_comment(
    issueId="LIN-123",
    body="🚀 **Started**\n- Branch: `feature/platform/LIN-123-password-api`"
)
```

### Completed

```python
mcp.create_comment(
    issueId="LIN-123",
    body="✅ **Completed**\n- PR: [link]\n- Files: `app/api/auth.py`"
)
```

---

## Ticket ID Format

`LIN-XXX` (e.g., `LIN-123`)

---

## Linear-Specific Notes

- **Initiatives** require Enterprise/Plus plan (use Project if unavailable)
- **Sub-issues** are created by setting `parentId`
- **Dependencies** use `blockedBy` field (array of issue IDs)
- **Auto-close**: Parent can auto-close when all sub-issues complete (if configured in Linear)
