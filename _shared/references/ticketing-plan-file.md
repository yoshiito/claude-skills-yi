# Plan File Ticketing

Tracking work without an external ticket system. See `ticketing-core.md` for universal rules.

## ⚠️ ENFORCEMENT WARNING

**This file is ONLY for projects where `Ticket System: none` in claude.md.**

### DO NOT USE Plan Files If:

| Condition | What to Do Instead |
|-----------|-------------------|
| Project has `Ticket System: linear` | Use Linear MCP commands (see `ticketing-linear.md`) |
| Project has `Ticket System: github` | Use GitHub Issues (see `ticketing-github-projects.md`) |
| Linear/GitHub MCP is "unavailable" | STOP and ask user to fix connection - do NOT fall back |
| You think markdown is "faster" | NO. Use the configured system. |

**If you're reading this file but the project uses Linear or GitHub, STOP and use the correct system.**

## When to Use (Legitimate Cases ONLY)

- `Ticket System: none` is explicitly set in project's claude.md
- Small teams without formal project management
- Personal projects
- Open source with minimal process
- Documentation-only projects

## Hierarchy Mapping

| Core Term | Plan File Equivalent | Where Tracked |
|-----------|---------------------|---------------|
| Initiative | Project goal | `docs/plans/` or README |
| Project | Plan document | `docs/plans/{feature}.md` |
| Issue | Section in plan | H2 heading in plan file |
| Sub-Issue | Checklist item | `- [ ]` in plan file |

```
docs/plans/
├── user-authentication.md    # Project plan
│   ├── ## Password Reset     # Issue (feature)
│   │   ├── - [ ] Backend API # Sub-task
│   │   ├── - [ ] Frontend UI # Sub-task
│   │   └── - [ ] Documentation
│   └── ## Login Flow
└── _registry.json            # Plan index
```

## Tracking Format

No ticket IDs. Use descriptive references instead.

### Branch Pattern

```
feature/platform/password-reset-api
fix/portal/login-validation
docs/platform/api-reference
```

### Commit Pattern

```
Add password reset endpoint

Part of: user-authentication plan
Related: docs/plans/user-authentication.md
```

## Plan File Template

Create `docs/plans/{feature-name}.md`:

```markdown
# {Feature Name} Plan

## Overview
[Brief description of the feature]

## Status
- [ ] In Progress / Complete

## Tasks

### {Component 1}
- [ ] Sub-task 1
- [ ] Sub-task 2 (blockedBy: Sub-task 1)

### {Component 2}
- [ ] Sub-task 1 (blockedBy: {Component 1} Sub-task 2)
- [ ] Sub-task 2 (blockedBy: Sub-task 1)

## Progress Log

### YYYY-MM-DD
- Started: {what was started}
- Completed: {what was finished}
- Notes: {any blockers or decisions}

## Related
- PR: #{number} (when created)
- ADR: docs/adr/{number}.md
```

**Note**: Use `(blockedBy: ...)` for dependencies. Omit `@assignee` for AI agent execution.

## Progress Tracking

Without a ticket system, track progress in these locations:

### 1. Plan File (Primary)

Update the plan file as work progresses:

```markdown
## Progress Log

### 2025-01-16
🚀 **Started**: Backend password reset API
- Branch: `feature/platform/password-reset-api`
- Approach: REST endpoint with email service

### 2025-01-17
✅ **Completed**: Backend password reset API
- PR: #456
- Files: `app/api/auth.py`
```

### 2. PR Description (Required)

Include full context since there's no ticket to reference:

```markdown
## Summary
Implements password reset API endpoint.

## Context
Part of User Authentication plan.
See: docs/plans/user-authentication.md

## Changes
- Added POST /api/v1/auth/reset
- Added email notification service

## Checklist
- [x] Tests included
- [x] Documentation updated
- [x] Plan file updated
```

### 3. Commit Messages (Descriptive)

Without ticket IDs, commits must be self-documenting:

```
Add password reset endpoint with email notification

- Implement POST /api/v1/auth/reset
- Add PasswordResetService with token generation
- Integrate with EmailService for reset links
- Add rate limiting (5 requests/hour per email)

Part of: user-authentication plan
```

## AI Agent Execution Mode

**When an AI agent is executing planned work, these rules apply:**

### No Sprints or Arbitrary Assignments

- ❌ DO NOT create sprint assignments
- ❌ DO NOT assign work to team members (@alice, @bob)
- ❌ DO NOT batch tasks into "phases" or "iterations"
- ✅ Execute tasks sequentially in the order listed
- ✅ Respect explicit `blockedBy` dependencies only
- ✅ Mark each task complete before moving to the next

### Execution Sequence

```
1. Read the plan file
2. Find the first unchecked task: `- [ ]`
3. Check if it has a `blockedBy` that is still incomplete
   - If blocked: skip to next unblocked task
   - If unblocked: execute it
4. Mark task complete: `- [x]`
5. Repeat until all tasks done
```

### Plan File Format for AI Execution

```markdown
## Tasks

### Backend
- [ ] Password reset API
- [ ] Rate limiting (blockedBy: Password reset API)

### Frontend
- [ ] Reset form (blockedBy: Password reset API)

### Documentation
- [ ] Password reset guide (blockedBy: Reset form)
```

**Note**: The `(blockedBy: ...)` annotation is the ONLY coordination mechanism needed. No sprints, no assignees, no phases.

### Progress Updates During Execution

As the agent works, update the plan file:

```markdown
## Tasks

### Backend
- [x] Password reset API ✓ 2025-01-16
- [ ] Rate limiting (blockedBy: Password reset API)
```

## Human Team Coordination (Optional)

**Only use this section if multiple humans are coordinating work.**

### Assign Work

Use plan file with names:

```markdown
## Tasks

### Backend
- [ ] Password reset API - @alice (in progress)
- [ ] Rate limiting - @bob

### Frontend
- [ ] Reset form - @charlie
```

### Track Dependencies

Note dependencies in plan file:

```markdown
## Dependencies

| Task | Blocked By | Status |
|------|------------|--------|
| Frontend reset form | Backend API | Waiting |
| Documentation | Backend + Frontend | Waiting |
```

### Status Updates

Add dated entries to progress log:

```markdown
## Progress Log

### 2025-01-16
**Status Update**
- Backend: 80% complete, PR in review
- Frontend: Blocked on backend
- Blockers: None
- ETA: Backend done tomorrow, frontend can start
```

## Worker Completion Checklist

Before marking work as done:

- [ ] Plan file updated with completion entry
- [ ] PR description includes full context
- [ ] Commits are descriptive (no ticket ID to reference)
- [ ] Related documentation updated
- [ ] Plan file checklist item marked complete

## Limitations

Without a ticket system:

- ❌ No automatic linking between commits and requirements
- ❌ No dashboards or burndown charts
- ❌ Manual status tracking required
- ❌ Harder to search history

Mitigate by:

- ✅ Detailed commit messages
- ✅ Comprehensive PR descriptions
- ✅ Regular plan file updates
- ✅ Good branch naming
