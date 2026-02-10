# Mission Template

**Content from**: Technical Product Owner
**Title format**: `[Mission] {name}`

## Template Structure

```markdown
## Execution Rules

**This ticket IS the work. Do not reframe.**

- Execute each checklist item exactly as written
- Each item is discrete—do not combine or skip
- Do not add work not listed here
- Mark items complete IN this ticket as you go
- If unclear, ask—do not assume

## Problem Statement
[What user problem are we solving?]

## Target Users
[Who experiences this problem? Include estimates if available.]

## Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

## Out of Scope
- [What this feature does NOT include]
- [Future phases]

## Open Questions
- [ ] [Any unresolved questions - MUST be empty before creation]

## Branch Information
- **Mission Branch**: `[USER MUST SPECIFY]`

## References
- Initiative: [Related strategic initiative]
- Research: [Links to research, competitor analysis]

## Execution Steps

**Note**: Mission-level steps happen AFTER all child Features are complete. Steps are discrete and sequential—do not combine or skip.

### Integration Test
- **Role**: `[tester-skill-name]`
- **Checklist**:
  - [ ] [E2E test scenario 1 - features work together]
  - [ ] [E2E test scenario 2 - cross-feature flows]
  - [ ] All integration tests passing
  - [ ] Comment on ticket with test results
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Tech Doc Writer

### Docs (if user-facing changes)
- **Role**: `tech-doc-writer-manager`
- **Checklist**:
  - [ ] [Mission-level doc update 1]
  - [ ] [... more mission-level doc items]
  - [ ] All docs updated
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Solutions Architect

### SA Review
- **Role**: `solutions-architect`
- **Checklist**:
  - [ ] [Verify overall architecture coherence]
  - [ ] [Verify integration patterns correct]
  - [ ] Architecture compliance verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to TPO

### UAT
- **Role**: `technical-product-owner`
- **Checklist**:
  - [ ] [Specific user flow works end-to-end]
  - [ ] [Specific data displays correctly]
  - [ ] [Error handling behaves as expected]
  - [ ] [Performance meets requirements]
  - [ ] All acceptance criteria verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Mission complete
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Mission]` | ✅ Enforced |
| Execution Rules section | Present verbatim | ✅ Enforced |
| Problem Statement | Not empty, describes user problem | ✅ Enforced |
| Target Users | Identified | ✅ Enforced |
| Success Criteria | Measurable outcomes listed | ✅ Enforced |
| Out of Scope | Defined (can be "N/A") | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| **Mission Branch** | **User-specified branch name** | ✅ Enforced |
| Execution Steps | Integration Test + Docs + SA Review + UAT with Role + Checklist | ✅ Enforced |
| Checklist items | Each item fully specified | ✅ Enforced |
| **Self-contained** | **All info to complete work is IN this ticket** | ✅ Enforced |
| Team assigned | From project's `Team Slug` in claude.md | ✅ Auto (from config) |

**Mission Branch Requirement**: User MUST specify the branch all Feature work will target. This cannot be assumed or defaulted.

## DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| All Features done | Every child Feature marked Done | ✅ Enforced |
| All execution steps complete | Integration Test, Docs, SA Review, UAT checked off | ✅ Enforced |
| UAT verified by TPO | Comment with "UAT Complete" + checked items | ✅ Enforced |
| Caller is TPO | Only TPO can close Missions | ✅ Enforced |

**Mission Completion Comment Format:**
```markdown
✅ **Mission Complete**

## Execution Steps
- [x] Integration Test: E2E tests passing
- [x] Docs: Updated [list pages] / N/A
- [x] SA Review: Architecture validated
- [x] UAT: Accepted by TPO

## Success Criteria
- [x] [Criterion 1 verified]
- [x] [Criterion 2 verified]
- [x] [Criterion 3 verified]

Mission accepted.
```
