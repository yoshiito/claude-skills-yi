# Plan File Ticketing

Tracking work without an external ticket system. See `ticketing-core.md` for universal rules.

## When to Use

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
- [ ] Sub-task 1 - @assignee
- [ ] Sub-task 2 - @assignee

### {Component 2}
- [ ] Sub-task 1 - @assignee
- [ ] Sub-task 2 - @assignee

## Progress Log

### YYYY-MM-DD
- Started: {what was started}
- Completed: {what was finished}
- Notes: {any blockers or decisions}

## Related
- PR: #{number} (when created)
- ADR: docs/adr/{number}.md
```

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

## Coordination Without Tickets

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
