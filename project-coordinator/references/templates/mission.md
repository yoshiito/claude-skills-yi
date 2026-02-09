# Mission Template

**Content from**: Technical Product Owner
**Title format**: `[Mission] {name}`

## Template Structure

```markdown
## Problem Statement
[What user problem are we solving?]

## Target Users
[Who experiences this problem? Include estimates if available.]

## Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

## UAT Criteria

Before this feature can be marked complete, TPO will verify:
- [ ] [Specific user flow works end-to-end]
- [ ] [Specific data displays correctly]
- [ ] [Error handling behaves as expected]
- [ ] [Performance meets requirements]

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
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Mission]` | ✅ Enforced |
| Problem Statement | Not empty, describes user problem | ✅ Enforced |
| Target Users | Identified | ✅ Enforced |
| Success Criteria | Measurable outcomes listed | ✅ Enforced |
| UAT Criteria | Checklist with specific verifiable items | ✅ Enforced |
| Out of Scope | Defined (can be "N/A") | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| **Mission Branch** | **User-specified branch name** | ✅ Enforced |
| Team assigned | From project's `Team Slug` in claude.md | ✅ Auto (from config) |

**Mission Branch Requirement**: User MUST specify the branch all Feature work will target. This cannot be assumed or defaulted.

## DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| All Features done | Every child Feature marked Done | ✅ Enforced |
| Mission-level tickets done | `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]` complete | ✅ Enforced |
| UAT verified by TPO | Comment with "UAT Complete" + checked items | ✅ Enforced |
| Mission works E2E | Integration verified | ⚠️ Manual |
| Caller is TPO | Only TPO can close Missions | ✅ Enforced |

**UAT Verification Comment Format:**
```markdown
✅ **Mission UAT Complete**
- [x] [Criterion 1 from UAT Criteria]
- [x] [Criterion 2 from UAT Criteria]
- [x] [Criterion 3 from UAT Criteria]

Mission accepted.
```
