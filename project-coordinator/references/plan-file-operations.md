# Plan File Operations

Internal reference for Project Coordinator. Handles local plan files when no ticket system is configured.

## When to Use

**ONLY when `Ticket System: none` in project's claude.md.**

If Linear or GitHub is configured, DO NOT use plan files. Use the appropriate handler.

---

## File Structure

```
docs/plans/
├── {feature-name}.md    # Plan document
└── _registry.json       # Plan index (optional)
```

---

## Operation: Create Ticket

### Parent Issue (Plan Document)

Create `docs/plans/{feature-name}.md`:

```markdown
# {Feature Name}

## Overview
[Brief description]

## Status
In Progress

## Tasks

### {Component 1}
- [ ] Sub-task 1
- [ ] Sub-task 2 (blockedBy: Sub-task 1)

### {Component 2}
- [ ] Sub-task 1 (blockedBy: {Component 1})

## Progress Log

### YYYY-MM-DD
- Started: {feature name}
```

### Sub-Issue (Checklist Item)

Add to existing plan file under appropriate section:

```markdown
### {Component}
- [ ] {Task description}
- [ ] {Task description} (blockedBy: {Other task})
```

---

## Operation: Update Ticket

### Update Status

Mark checklist item:

```markdown
- [x] Password reset API ✓ 2025-01-16
```

### Add Comment (Progress Log)

Add entry to Progress Log section:

```markdown
## Progress Log

### 2025-01-16
🚀 **Started**: Backend password reset API
- Branch: `feature/platform/password-reset-api`

### 2025-01-17
✅ **Completed**: Backend password reset API
- PR: #456
```

---

## Operation: Set Relationships

### Set Parent

Sub-tasks are implicitly children of their H3 section, which is a child of the plan document.

### Set Blocker

Add `(blockedBy: {task})` annotation:

```markdown
- [ ] Frontend form (blockedBy: Backend API)
```

### Remove Blocker

Remove the `(blockedBy: ...)` annotation.

---

## Operation: Verify Relationships

Check plan file for:
- Task exists under correct section (parent)
- `(blockedBy: ...)` annotation present for blocked tasks
- Blocking task exists in file

---

## Tracking Without IDs

Plan files don't have ticket IDs. Use descriptive references.

### Branch Pattern

```
feature/platform/password-reset-api
fix/portal/login-validation
```

### Commit Pattern

```
Add password reset endpoint

Part of: user-authentication plan
Related: docs/plans/user-authentication.md
```

---

## Progress Comments

### Started

Add to Progress Log:

```markdown
### YYYY-MM-DD
🚀 **Started**: {Task name}
- Branch: `{branch-name}`
- Approach: {brief description}
```

### Completed

Add to Progress Log and mark task:

```markdown
### YYYY-MM-DD
✅ **Completed**: {Task name}
- PR: #{number}
- Files: {key files}
```

Mark task in checklist:
```markdown
- [x] {Task name} ✓ YYYY-MM-DD
```

---

## Limitations

Without a ticket system:
- No automatic linking
- No dashboards
- Manual status tracking
- Harder to search history

Mitigate by:
- Detailed commit messages
- Comprehensive PR descriptions
- Regular plan file updates
