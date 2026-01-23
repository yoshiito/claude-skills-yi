# Definition of Done (DoD)

**Universal checklist for ticket completion.** Project Coordinator enforces this when updating status to "Done".

## Who Uses This

| Role | Uses DoD For |
|------|--------------|
| **Project Coordinator** | **ENFORCES** - rejects status=done if DoD not met |
| **TPgM** | Additional verification after coordinator accepts |
| **Workers** | Understands what "complete" means before claiming done |
| **Code Reviewer** | Validates implementation quality |

## Enforcement Point

**Project Coordinator is the enforcer.** When any role invokes `[PROJECT_COORDINATOR] Update #NUM: Status=done`, the coordinator:
1. Fetches the actual ticket from the system
2. Reads comments and description for evidence
3. **REJECTS with specific gaps** if checks fail
4. Only updates status if ALL checks pass

**Workers cannot mark done without evidence.** Add PR link, review confirmation, test results to ticket comments first.

## Definition of Done Checklist

### For Implementation Sub-Issues (`[Backend]`, `[Frontend]`)

| Check | Required | Validation |
|-------|----------|------------|
| PR created | ✅ | Link provided in completion message |
| PR reviewed by Code Reviewer | ✅ | Review completed, issues addressed |
| **PR merged to target branch** | ✅ | Code is in target branch, not just approved |
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

### For Parent Issues (`[Feature]`)

**Parent issues have a DIFFERENT DoD than sub-issues.** All sub-issues being complete does NOT mean the parent is done.

| Check | Required | Validation |
|-------|----------|------------|
| All sub-issues completed | ✅ | Every child sub-issue marked Done |
| UAT criteria verified by TPO | ✅ | TPO has verified each UAT criterion |
| Feature works end-to-end | ✅ | Integration verified in target environment |
| Documentation complete | ✅ | User-facing docs updated (if applicable) |

**CRITICAL**: Only TPO can mark a parent issue as Done after UAT verification.

## DoD Enforcement

### First Line: Project Coordinator (Automatic)

When worker invokes `[PROJECT_COORDINATOR] Update #NUM: Status=done`:

```
[PROJECT_COORDINATOR] - 🔍 Verifying Definition of Done for #NUM...

Fetching ticket from system...
Reading comments for completion evidence...

| Check | Status | Evidence |
|-------|--------|----------|
| PR created | ✅ / ❌ | [link or "Not found"] |
| PR merged | ✅ / ❌ | [merged status or "Not merged"] |
| Code reviewed | ✅ / ❌ | [reviewer or "Not found"] |
| Tests documented | ✅ / ❌ | [mention or "Not found"] |
```

**If checks fail**: REJECT with missing items, do NOT update status.

### Second Line: TPgM (Drive Mode)

In Drive Mode, TPgM may do additional verification after Project Coordinator accepts:

```
[TPgM] - ✅ [TICKET-ID] verified complete

Project Coordinator accepted completion.
All Definition of Done checks passed.
```

### If DoD Fails at Project Coordinator

```
[PROJECT_COORDINATOR] - ❌ REJECTED: Definition of Done not met.

**Operation**: Update #123 to Done
**Ticket**: "[Backend] User API"

**Missing Items**:
- [ ] PR Link: No pull request URL found in comments
- [ ] Code Review: No Code Reviewer approval found

**Action Required**: Add completion evidence to ticket comments, then retry.

Returning control to [CALLING_ROLE] for correction.
```

**Ticket remains In Progress.** Worker must add evidence and retry.

### Parent Issue Closure (TPO Only)

When TPO invokes `[PROJECT_COORDINATOR] Update #NUM: Status=done` for a parent issue:

```
[PROJECT_COORDINATOR] - 🔍 Verifying Parent Issue DoD for #NUM...

Fetching parent issue and all sub-issues...
Checking UAT verification status...

| Check | Status | Evidence |
|-------|--------|----------|
| All sub-issues done | ✅ / ❌ | [X of Y complete] |
| UAT verified by TPO | ✅ / ❌ | [TPO comment or "Not found"] |
| End-to-end verified | ✅ / ❌ | [verification note or "Not found"] |
```

**If checks fail**: REJECT - parent issue cannot be closed until UAT complete.

**TPO must add UAT verification comment** before closing:
```markdown
✅ **UAT Complete**
- [x] User receives reset email within 2 minutes
- [x] Reset link expires after 24 hours
- [x] New password works on next login
- [x] Invalid/expired links show helpful error

Feature accepted.
```

## Common Gaps

| Gap | Resolution |
|-----|------------|
| No PR link | Worker must provide PR link |
| PR not merged | Worker must merge PR after approval |
| No code review | Worker must invoke Code Reviewer |
| Tests missing | Worker must write tests per Gherkin scenarios |
| Tests failing | Worker must fix failures |
| Spec not met | Worker must address MUST/MUST NOT violations |
| Sub-issues incomplete | Complete all sub-issues before closing parent |
| UAT not verified | TPO must verify UAT criteria and add comment |

## Related References

- `definition-of-ready.md` - Pre-work checklist
- `ticket-templates.md` - Ticket body templates
- `code-reviewer/SKILL.md` - Code review process
