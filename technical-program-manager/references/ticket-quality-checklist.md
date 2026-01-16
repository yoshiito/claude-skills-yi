# Ticket Quality Checklist

**ENFORCEMENT**: Block ticket creation until ALL required fields pass. No exceptions.

## Pre-Creation Gate

Before calling `create_issue`, verify every required field is present and complete.

---

## Required Fields by Ticket Type

### Epic/Project Ticket

| Field | Required | Validation |
|-------|----------|------------|
| Title | ✅ | Descriptive, matches MRD feature name |
| Description | ✅ | Links to MRD, high-level scope |
| Team | ✅ | Valid Linear team |
| Project | ✅ | Existing or newly created project |

### Feature Ticket (Parent Issue)

| Field | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Feature] {name}` format |
| Description | ✅ | See template below |
| Team | ✅ | Valid Linear team |
| Parent | ✅ | Link to Epic |
| Labels | ✅ | At minimum: type label (Feature/Bug/etc.) |

**Description Template:**
```markdown
## Overview
[1-2 sentences describing the feature]

## Context
- MRD: [link]
- Architecture: [link to ADR]
- Design: [link if applicable]

## Success Criteria
- [ ] [Measurable outcome]
- [ ] [Measurable outcome]

## Out of Scope
- [What this feature does NOT include]
```

### Task Ticket (Sub-Issue)

| Field | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Type] {description}` - Type: Backend/Frontend/Docs/Test |
| Description | ✅ | See template below |
| Team | ✅ | Valid Linear team |
| Parent | ✅ | Link to Feature |
| Blocked By | ⚠️ | Required if dependencies exist |
| Labels | ✅ | Type label (Backend/Frontend/etc.) |

**Description Template:**
```markdown
## Description
[Clear description of implementation work]

## Context
- Parent: [LIN-XXX - Feature name]
- ADR: [link if applicable]
- API Spec: [link if applicable]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Tests written and passing]
- [ ] [Documentation updated if applicable]

## Dependencies
[List upstream tasks that must complete first, or "None"]

## Testing Requirements
[What tests must be written/pass]
```

### Bug Ticket

| Field | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Bug] {brief description}` |
| Description | ✅ | See template below |
| Team | ✅ | Valid Linear team |
| Labels | ✅ | `Bug` + priority label |
| Priority | ✅ | P0-P3 based on impact |

**Description Template:**
```markdown
## Environment
[Platform, version, environment]

## Impact
[Critical/High/Medium/Low + description]

## Steps to Reproduce
1. [Step]
2. [Step]

## Actual Result
[What happens]

## Expected Result
[What should happen]

## Testing Notes
[How to verify the fix]
```

---

## Quality Gate Checklist

Run this checklist before ANY `create_issue` call:

### Structural Checks
- [ ] Title follows naming convention (`[Type] description`)
- [ ] Description is not empty
- [ ] Team is specified and valid
- [ ] Parent is set (for Features and Tasks)

### Content Checks
- [ ] Acceptance criteria are specific and testable
- [ ] Dependencies are explicitly stated (or marked "None")
- [ ] Context links are provided (MRD, ADR, API spec)
- [ ] Testing requirements are defined

### Dependency Checks
- [ ] All `blockedBy` issues exist in Linear
- [ ] Circular dependencies checked (A blocks B blocks A)
- [ ] Dependency graph is documented in delivery plan

### INVEST Validation (for Tasks)
- [ ] **I**ndependent: Can start without waiting (or `blockedBy` set)
- [ ] **N**egotiable: Approach flexible, criteria fixed
- [ ] **V**aluable: Moves feature toward "Done"
- [ ] **E**stimable: Bounded scope with known files and clear end state
- [ ] **S**mall: Single logical change (one PR, one concern)
- [ ] **T**estable: Criteria can be verified

---

## Enforcement Protocol

### When Check Fails

1. **STOP** - Do not create the ticket
2. **Report** - List all missing/invalid fields
3. **Route** - Direct to appropriate owner:
   - Missing requirements → TPO
   - Missing architecture → Solutions Architect
   - Missing test strategy → Tester
   - Missing documentation plan → Tech Doc Writer
4. **Wait** - Only proceed when ALL fields complete

### Example Rejection

```
❌ TICKET CREATION BLOCKED

Title: "[Backend] User API"

Missing required fields:
- Description: Empty
- Acceptance Criteria: Not defined
- Testing Requirements: Not specified
- Parent: Not linked to Feature

Action Required:
- Solutions Architect: Define acceptance criteria
- Backend Developer: Specify testing requirements
- Link to parent Feature issue

Ticket will NOT be created until all fields are complete.
```

---

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Vague acceptance criteria | Add specific, testable conditions |
| Missing dependencies | Consult SA for task ordering |
| No test requirements | Consult domain tester |
| Missing context links | Link MRD, ADR, API spec |
| Title doesn't follow convention | Use `[Type] description` format |

---

## Post-Creation Verification

After ticket creation, verify:

- [ ] Ticket appears in correct project
- [ ] `blockedBy`/`blocks` relations are set
- [ ] Assignee is set (or deliberately left unassigned)
- [ ] Labels are applied
- [ ] Priority is set (if specified)

---

## Related References

- `_shared/references/ticket-templates.md` - Full ticket templates
- `_shared/references/linear-ticket-traceability.md` - Lifecycle workflow
- `delivery-plan-template.md` - Task breakdown structure
