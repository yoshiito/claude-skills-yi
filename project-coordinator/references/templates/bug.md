# Bug Template

**Content from**: Support Engineer
**Title format**: `[Bug] {description}`

## Template Structure

```markdown
## Environment
- OS: [e.g., iOS 17.2, Windows 11]
- Browser/App: [e.g., Chrome 120, App v5.4.1]
- Environment: [Production/Staging/Dev]

## Impact
**Severity**: [Critical/High/Medium/Low]
**Business Impact**: [Description of business impact]

## User Scope
[How many users affected, percentage of user base]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Actual Result
[What happens - include error messages, screenshots]

## Expected Result
[What should happen]

## Root Cause (if known)
[Technical root cause from investigation]

## Testing Notes
[How to verify the fix]

## Additional Notes
- Workaround: [If any]
- Related: [Related tickets]
- Logs: [Relevant log snippets]

## Workflow Phases

**CRITICAL**: Each phase MUST specify the role and concrete checklist items for THIS bug.

### Development
- **Role**: `[developer-skill-name]`
- **Checklist**:
  - [ ] [Fix item 1 based on root cause]
  - [ ] [Fix item 2 based on root cause]
  - [ ] All checklist items complete, PR created
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Code Reviewer

### Code Review
- **Role**: `code-reviewer`
- **Checklist**:
  - [ ] [Verify fix addresses root cause]
  - [ ] [Verify no regression in related code]
  - [ ] All items verified, PR approved
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to [Tester role]

### Test
- **Role**: `[tester-skill-name]`
- **Checklist**:
  - [ ] [Test the specific bug scenario is fixed]
  - [ ] [Regression test related functionality]
  - [ ] All tests passing
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Solutions Architect

### SA Review
- **Role**: `solutions-architect`
- **Checklist**:
  - [ ] [Verify fix doesn't introduce architectural issues]
  - [ ] Architecture compliance verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to TPO

### UAT
- **Role**: `technical-product-owner`
- **Checklist**:
  - [ ] [Verify bug is fixed from user perspective]
  - [ ] All acceptance criteria verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Bug complete
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Bug]` | ✅ Enforced |
| Environment | OS/Browser/App version specified | ✅ Enforced |
| Steps to Reproduce | Numbered steps present | ✅ Enforced |
| Actual Result | Described | ✅ Enforced |
| Expected Result | Described | ✅ Enforced |
| Impact | Severity specified | ⚠️ Manual |
| Workflow Phases | Each phase has Role + Checklist items | ✅ Enforced |

## DoD: Definition of Done (Before Closing)

**Bugs are Done when ALL workflow phases are complete.**

| Check | Required | PC Validates |
|-------|----------|--------------|
| Development complete | PR created | ✅ PR link in comment |
| Code Review complete | PR approved and merged | ✅ Merge confirmed |
| Test complete | Regression tests passing | ✅ Test completion comment |
| Docs complete | Documentation updated (if user-facing) | ⚠️ Conditional |
| SA Review complete | Technical validation | ✅ SA approval comment |
| UAT complete | TPO accepted | ✅ UAT approval comment |
| Root cause documented | In completion comment | ⚠️ Manual |
| Dev subtasks done | All `[Dev]` children complete (if any) | ✅ Enforced |

**Bug Completion Comment:**
```markdown
✅ **Bug Fixed**

## Root Cause
[Technical explanation of the bug]

## Fix
[Brief description of the solution]

## Workflow Phases
- [x] Development: PR #{num} merged
- [x] Code Review: Approved by {reviewer}
- [x] Test: Regression tests passing
- [x] Docs: Updated / N/A
- [x] SA Review: Validated
- [x] UAT: Accepted by TPO
```
