# Definition of Done (DoD)

**Universal checklist for ticket completion.** TPgM uses this to verify work is actually complete before accepting "Done" status.

## Who Uses This

| Role | Uses DoD For |
|------|--------------|
| **TPgM** | Gates completion - cannot accept "Done" without verification |
| **Workers** | Understands what "complete" means before claiming done |
| **Code Reviewer** | Validates implementation quality |

## Definition of Done Checklist

### For Implementation Sub-Issues (`[Backend]`, `[Frontend]`)

| Check | Required | Validation |
|-------|----------|------------|
| PR created | ✅ | Link provided in completion message |
| PR reviewed by Code Reviewer | ✅ | Review completed, issues addressed |
| Tests written | ✅ | Covers Gherkin scenarios in ticket |
| Tests pass | ✅ | CI green or manual confirmation |
| Technical Spec satisfied | ✅ | All MUST/MUST NOT constraints met |
| No regressions introduced | ✅ | Existing tests still pass |

### For Test Sub-Issues (`[Test]`)

| Check | Required | Validation |
|-------|----------|------------|
| All Gherkin scenarios validated | ✅ | Each Given/When/Then verified |
| Edge cases covered | ✅ | Testing Notes from ticket addressed |
| Test results documented | ✅ | Pass/fail status with evidence |
| Regression suite updated | ✅ | New tests added to suite |

### For Documentation Sub-Issues (`[Docs]`)

| Check | Required | Validation |
|-------|----------|------------|
| Documentation created/updated | ✅ | PR or ticket system update |
| Matches implementation | ✅ | Reflects actual behavior |
| Reviewed for accuracy | ✅ | Technical review completed |

## DoD Enforcement

### When Worker Claims "Done"

TPgM MUST verify before accepting completion:

```
[TPgM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| PR created | ✅ / ❌ |
| Code reviewed | ✅ / ❌ |
| Tests written | ✅ / ❌ |
| Tests pass | ✅ / ❌ |
| Technical Spec satisfied | ✅ / ❌ |
| No regressions | ✅ / ❌ |
```

### If DoD Passes

```
[TPgM] - ✅ [TICKET-ID] verified complete

All Definition of Done checks passed.
Moving ticket to Done status.
```

### If DoD Fails

```
[TPgM] - ⛔ [TICKET-ID] NOT complete

Definition of Done not met:

| Missing | Action Required |
|---------|-----------------|
| Code review | Invoke Code Reviewer |
| Tests | Write tests for Gherkin scenarios |
| [other] | [action] |

Ticket remains In Progress until gaps addressed.
```

**DO NOT mark ticket Done.** Return to worker with specific gaps.

## Common Gaps

| Gap | Resolution |
|-----|------------|
| No PR link | Worker must provide PR link |
| No code review | Worker must invoke Code Reviewer |
| Tests missing | Worker must write tests per Gherkin scenarios |
| Tests failing | Worker must fix failures |
| Spec not met | Worker must address MUST/MUST NOT violations |

## Related References

- `definition-of-ready.md` - Pre-work checklist
- `ticket-templates.md` - Ticket body templates
- `code-reviewer/SKILL.md` - Code review process
