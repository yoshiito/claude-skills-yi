# Dev Subtask Template (OPTIONAL)

**Content from**: Solutions Architect (during work breakdown)
**Title format**: `[Dev] {component description}`
**Only create `[Dev]` subtasks if implementation needs breakdown.**

## `[Dev]` - Implementation Subtask

**Assigned to**: Developer (Backend/Frontend)
**Use when**: Implementation is complex and needs to be broken into independent components

## Template Structure

```markdown
## Execution Rules

**This ticket IS the work. Do not reframe.**

- Execute each checklist item exactly as written
- Each item is discrete—do not combine or skip
- Do not add work not listed here
- Mark items complete IN this ticket as you go
- If unclear, ask—do not assume

## Context

[Everything needed to understand this task - no external reading required]

## Technical Constraints

[Patterns to follow, files to modify, dependencies, edge cases]

## References

- Parent Feature: [TICKET-ID]
- Feature Branch: [branch-name]

## Execution Steps

**CRITICAL**: Each step MUST specify the role and concrete checklist items for THIS subtask. Steps are discrete and sequential—do not combine or skip.

### Development
- **Role**: `[exact-skill-name]`
- **Checklist**:
  - [ ] [Fully specified task 1 - what, where, how]
  - [ ] [Fully specified task 2 - what, where, how]
  - [ ] [... each item self-explanatory]
  - [ ] All checklist items complete, PR created
  - [ ] PR targets feature branch
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Code Reviewer

### Code Review
- **Role**: `code-reviewer`
- **Checklist**:
  - [ ] [Specific verification item 1 for THIS subtask]
  - [ ] [Specific verification item 2 for THIS subtask]
  - [ ] [... more subtask-specific review items]
  - [ ] All items verified, PR approved
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to [Tester role]

### Test
- **Role**: `[backend-fastapi-pytest-tester or frontend-tester]`
- **Checklist**:
  - [ ] [Specific test case 1 for THIS subtask]
  - [ ] [Specific test case 2 for THIS subtask]
  - [ ] [... more subtask-specific test items]
  - [ ] All tests passing
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Tech Doc Writer

### Docs (if user-facing changes)
- **Role**: `tech-doc-writer-manager`
- **Checklist**:
  - [ ] [Specific doc update 1 for THIS subtask]
  - [ ] [... more subtask-specific doc items]
  - [ ] All docs updated
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Solutions Architect

### SA Review
- **Role**: `solutions-architect`
- **Checklist**:
  - [ ] [Specific architecture check for THIS subtask]
  - [ ] Architecture compliance verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to TPO

### UAT
- **Role**: `technical-product-owner`
- **Checklist**:
  - [ ] [Acceptance criterion 1 for THIS subtask]
  - [ ] [Acceptance criterion 2 for THIS subtask]
  - [ ] All acceptance criteria verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Subtask complete
```

## DoR: Definition of Ready (Before Start)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Parent Feature exists | ✅ | ✅ Enforced |
| **Feature Branch confirmed** | ✅ (BLOCKING) | ✅ Enforced |
| Execution Rules section | Present verbatim | ✅ Enforced |
| Context | Sufficient to understand without external reading | ✅ Enforced |
| Technical Constraints | Patterns, files, dependencies specified | ✅ Enforced |
| Execution Steps | All steps (Dev, Review, Test, Docs, SA, UAT) with Role + Checklist | ✅ Enforced |
| Checklist items | Each item fully specified (what, where, how) | ✅ Enforced |
| **Self-contained** | **All info to complete work is IN this ticket** | ✅ Enforced |

## DoD: Definition of Done (Before Complete)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Development complete | All checklist items checked off | ✅ Enforced |
| PR created | Link in comment | ✅ Enforced |
| PR targets Feature Branch | Verified | ✅ Enforced |
| Code Review complete | PR approved and merged | ✅ Enforced |
| Test complete | Tests written and passing | ✅ Test completion comment |
| Docs complete | Documentation updated (if user-facing) | ⚠️ Conditional |
| SA Review complete | Architecture validated | ✅ SA approval comment |
| UAT complete | TPO accepted | ✅ UAT approval comment |

## Branch Confirmation Protocol (BLOCKING)

Before starting ANY work, prompt user:

```
⛔ BRANCH CONFIRMATION REQUIRED

I cannot proceed without knowing the target branch.

Please confirm:
  Feature Branch: _________________ (e.g., feature/password-reset-backend)

This branch will be the PR target for this work.

Waiting for your response...
```

**Do NOT proceed until user provides explicit branch name.**

## Completion Comment Format

```markdown
✅ **[Dev] Subtask Complete**

## Component
[What this subtask implemented]

## Execution Steps
- [x] Development: PR #{num} merged
- [x] Code Review: Approved by {reviewer}
- [x] Test: {X} tests passing
- [x] Docs: Updated [list pages]
- [x] SA Review: Architecture validated
- [x] UAT: Accepted by TPO

## Files Changed
[Key files]
```

## When to Create Dev Subtasks

| Situation | Create `[Dev]` Subtasks? |
|-----------|-------------------------|
| Multiple independent components | ✅ Yes |
| Different expertise needed for parts | ✅ Yes |
| Large implementation needing breakdown | ✅ Yes |
| Simple, straightforward implementation | ❌ No |
| Single developer can complete in one session | ❌ No |
| No natural component boundaries | ❌ No |

## Example: When to Use Dev Subtasks

```
[Backend] Add password reset endpoint        ← Feature
├── [Dev] Token generation and validation    ← Complex crypto logic
├── [Dev] Email integration                  ← Separate service integration
└── [Dev] Rate limiting                      ← Distinct security component
```

Each `[Dev]` subtask is a complete work unit with its own execution steps (Development → Code Review → Test → Docs → SA Review → UAT).
