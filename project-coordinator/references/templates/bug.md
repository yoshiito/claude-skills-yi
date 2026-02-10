# Bug Template

**Content from**: Support Engineer
**Title format**: `[Bug] {description}`

## Template Structure

```markdown
## Execution Rules

**This ticket IS the work. Do not reframe.**

- Execute each checklist item exactly as written
- Each item is discrete—do not combine or skip
- Do not add work not listed here
- Mark items complete IN this ticket as you go
- If unclear, ask—do not assume

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

## Execution Steps

**CRITICAL**: Each step MUST specify the role and concrete checklist items for THIS bug. Steps are discrete and sequential—do not combine or skip.

### Development
- **Role**: `[developer-skill-name]`
- **Checklist**:
  - [ ] [Fix item 1 based on root cause]
  - [ ] [Fix item 2 based on root cause]
  - [ ] PR created targeting feature branch
  - [ ] Comment on ticket with verbose summary. [Describe: root cause fix, files modified, approach used]
  - [ ] Edit ticket body to check off this phase's completed items
  - [ ] Hand off to Code Reviewer

### Code Review
- **Role**: `code-reviewer`
- **Checklist**:
  - [ ] [Verify fix addresses root cause]
  - [ ] [Verify no regression in related code]
  - [ ] PR approved
  - [ ] PR merged into feature branch
  - [ ] Source branch deleted
  - [ ] Comment on ticket with verbose summary. [Describe: items checked, issues found and resolved]
  - [ ] Edit ticket body to check off this phase's completed items
  - [ ] Hand off to [Tester role]

### Test
- **Role**: `[tester-skill-name]`
- **Checklist**:
  - [ ] [Test the specific bug scenario is fixed]
  - [ ] [Regression test related functionality]
  - [ ] All tests passing
  - [ ] Comment on ticket with verbose summary. [Describe: number of tests, regression scenarios covered]
  - [ ] Edit ticket body to check off this phase's completed items
  - [ ] Hand off to Solutions Architect

### SA Review
- **Role**: `solutions-architect`
- **Checklist**:
  - [ ] [Verify fix doesn't introduce architectural issues]
  - [ ] Architecture compliance verified
  - [ ] Comment on ticket with verbose summary. [Describe: architectural impact assessed, patterns validated]
  - [ ] Edit ticket body to check off this phase's completed items
  - [ ] Hand off to TPO

### UAT
- **Role**: `technical-product-owner`
- **Checklist**:
  - [ ] [Verify bug is fixed from user perspective]
  - [ ] All acceptance criteria verified
  - [ ] Comment on ticket with verbose summary. [Describe: bug scenario validated, user impact resolved]
  - [ ] Edit ticket body to check off this phase's completed items
  - [ ] Bug complete
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Bug]` | ✅ Enforced |
| Execution Rules section | Present verbatim | ✅ Enforced |
| Environment | OS/Browser/App version specified | ✅ Enforced |
| Steps to Reproduce | Numbered steps present | ✅ Enforced |
| Actual Result | Described | ✅ Enforced |
| Expected Result | Described | ✅ Enforced |
| Impact | Severity specified | ⚠️ Manual |
| Execution Steps | Each step has Role + Checklist items | ✅ Enforced |
| Checklist items | Each item fully specified | ✅ Enforced |
| **Self-contained** | **All info to complete work is IN this ticket** | ✅ Enforced |

## DoD: Definition of Done (Before Closing)

**Bugs are Done when ALL execution steps are complete.**

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

## Execution Steps
- [x] Development: PR #{num} merged
- [x] Code Review: Approved by {reviewer}
- [x] Test: Regression tests passing
- [x] Docs: Updated / N/A
- [x] SA Review: Validated
- [x] UAT: Accepted by TPO
```
