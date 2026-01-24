# Ticket Templates

**Project Coordinator enforces these templates.** Each template includes Definition of Ready (DoR) for creation and Definition of Done (DoD) for completion.

| Template | Created By | Use Case |
|----------|------------|----------|
| **Epic** | TPO | Feature-level work with child sub-issues |
| **Story/Task** | SA | Implementation work (Backend, Frontend, Docs, Test) |
| **Bug** | Support Engineer | Defect tracking and fix |
| **Subtask** | Worker | Breakdown of a Story/Task (optional) |

---

## 1. Epic Template

**Created by**: Technical Product Owner
**Title format**: `[Feature] {name}`

### Template Structure

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

## References
- Initiative: [Related strategic initiative]
- Research: [Links to research, competitor analysis]
```

### DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Feature]` | ✅ Enforced |
| Problem Statement | Not empty, describes user problem | ✅ Enforced |
| Target Users | Identified | ✅ Enforced |
| Success Criteria | Measurable outcomes listed | ✅ Enforced |
| UAT Criteria | Checklist with specific verifiable items | ✅ Enforced |
| Out of Scope | Defined (can be "N/A") | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| Team assigned | From project's `Team Slug` in claude.md | ✅ Auto (from config) |

### DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| All sub-issues done | Every child marked Done | ✅ Enforced |
| UAT verified by TPO | Comment with "UAT Complete" + checked items | ✅ Enforced |
| Feature works E2E | Integration verified | ⚠️ Manual |
| Documentation complete | Docs sub-issue done | ✅ Via sub-issue |
| Caller is TPO | Only TPO can close epics | ✅ Enforced |

**UAT Verification Comment Format:**
```markdown
✅ **UAT Complete**
- [x] [Criterion 1 from UAT Criteria]
- [x] [Criterion 2 from UAT Criteria]
- [x] [Criterion 3 from UAT Criteria]

Feature accepted.
```

---

## 2. Story/Task Template

**Created by**: Solutions Architect
**Title format**: `[Backend]`, `[Frontend]`, `[Docs]`, or `[Test]` prefix

### Template Structure

```markdown
## Assigned Role
`[exact-skill-name]`

## Story
As a [user type], I want [capability] so that [benefit].

## Context
[Background for someone unfamiliar. Include why this work matters.]

## References
- Parent: [TICKET-ID] - [Parent title]
- ADR: [Link if architectural decisions involved]
- API Spec: [Link if API work involved]

## Acceptance Criteria

<technical-spec>
  <must>
    - [Required behavior 1 - non-negotiable]
    - [Required behavior 2 - non-negotiable]
  </must>
  <must-not>
    - [Prohibited approach 1 - red line]
    - [Prohibited approach 2 - red line]
  </must-not>
  <should>
    - [Preferred approach 1 - negotiable]
    - [Preferred approach 2 - negotiable]
  </should>
</technical-spec>

```gherkin
Feature: [Feature name]

  Scenario: [Happy path]
    Given [context]
    When [action]
    Then [outcome]

  Scenario: [Error case]
    Given [context]
    When [action]
    Then [outcome]
```

## NFRs
[Performance, security requirements or "N/A"]

## Implementation Notes
[Technical guidance, patterns to follow, files to modify]

## Infrastructure Notes
[DB changes, env vars, config changes or "N/A"]

## Testing Notes
[Edge cases to cover, test data requirements]

## Open Questions
- [ ] [Any unresolved questions - MUST be empty before creation]
```

### DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Backend]`, `[Frontend]`, `[Docs]`, or `[Test]` | ✅ Enforced |
| Assigned Role | Valid skill name | ⚠️ Manual |
| Story | User story format | ⚠️ Manual |
| Context | Not empty | ⚠️ Manual |
| Technical Spec | `<technical-spec>` with `<must>` section | ✅ Enforced |
| Gherkin scenarios | `Given`/`When`/`Then` keywords present | ✅ Enforced |
| Testing Notes | Section exists | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| Parent specified | `Parent: #NUM` in request | ✅ Enforced |
| INVEST compliant | See checklist below | ⚠️ Manual |

**INVEST Checklist (SA verifies before invoking PC):**
- [ ] **I**ndependent: Can start without waiting (or `blockedBy` set)
- [ ] **N**egotiable: Approach flexible, criteria fixed
- [ ] **V**aluable: Moves feature toward "Done"
- [ ] **E**stimable: Bounded scope, known files, clear end state
- [ ] **S**mall: Single logical change (one PR, one concern)
- [ ] **T**estable: Technical Spec + Gherkin scenarios verifiable

### DoD: Definition of Done (Before Closing)

#### For `[Backend]` and `[Frontend]` Sub-Issues

| Check | Required | PC Validates |
|-------|----------|--------------|
| PR created | Link in comment | ✅ Enforced |
| PR merged | Merged to target branch | ✅ Enforced |
| Branch deleted | Feature branch removed after merge | ✅ Enforced |
| Code reviewed | Code Reviewer approved | ✅ Enforced |
| Tests written | Covers Gherkin scenarios | ✅ Enforced |
| Tests pass | CI green or manual confirmation | ⚠️ Manual |
| Technical Spec satisfied | All MUST/MUST NOT met | ⚠️ Manual |
| No regressions | Existing tests pass | ⚠️ Manual |

**Completion Comment Format:**
```markdown
✅ **Completed**
- PR merged: [link]
- Branch: `{branch-name}` deleted
- Code Review: Approved by [reviewer]
- Tests: [X] scenarios covered, all passing
- Files: [Key files changed]
```

#### For `[Test]` Sub-Issues

| Check | Required | PC Validates |
|-------|----------|--------------|
| All scenarios validated | Each Given/When/Then verified | ✅ Enforced |
| Edge cases covered | Testing Notes addressed | ⚠️ Manual |
| Test results documented | Pass/fail with evidence | ✅ Enforced |
| Regression suite updated | New tests added | ⚠️ Manual |

**Completion Comment Format:**
```markdown
✅ **Test Complete**
- Scenarios validated: [X/Y]
- Results:
  - [Scenario 1]: ✅ Pass
  - [Scenario 2]: ✅ Pass
  - [Scenario 3]: ✅ Pass
- Edge cases: [Covered/Notes]
```

#### For `[Docs]` Sub-Issues

| Check | Required | PC Validates |
|-------|----------|--------------|
| Documentation created | Link in comment | ✅ Enforced |
| Matches implementation | Reflects actual behavior | ⚠️ Manual |
| Review completed | Technical review done | ✅ Enforced |

**Completion Comment Format:**
```markdown
✅ **Documentation Complete**
- Doc link: [link]
- Reviewed by: [reviewer]
- Covers: [What's documented]
```

---

## 3. Bug Template

**Created by**: Support Engineer
**Title format**: `[Bug] {description}`

### Template Structure

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
```

### DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Bug]` | ✅ Enforced |
| Environment | OS/Browser/App version specified | ✅ Enforced |
| Steps to Reproduce | Numbered steps present | ✅ Enforced |
| Actual Result | Described | ✅ Enforced |
| Expected Result | Described | ✅ Enforced |
| Impact | Severity specified | ⚠️ Manual |

### DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| PR created | Link in comment | ✅ Enforced |
| PR merged | Merged to target branch | ✅ Enforced |
| Code reviewed | Code Reviewer approved | ✅ Enforced |
| Tests written | Regression test for bug | ✅ Enforced |
| Fix verified | Testing Notes followed | ⚠️ Manual |

**Completion Comment Format:**
```markdown
✅ **Bug Fixed**
- PR merged: [link]
- Code Review: Approved by [reviewer]
- Root cause: [Brief explanation]
- Fix: [What was changed]
- Regression test: Added to prevent recurrence
```

---

## 4. Subtask Template

**Created by**: Worker (during implementation)
**Title format**: `[Subtask] {description}`

Subtasks break down a Story/Task into smaller pieces. Use when a single Story/Task has multiple distinct work items.

### Template Structure

```markdown
## Parent Task
[TICKET-ID] - [Parent task title]

## Description
[What this subtask accomplishes]

## Acceptance Criteria
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]

## Notes
[Implementation details, files to modify]
```

### DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Subtask]` | ✅ Enforced |
| Parent specified | `Parent: #NUM` in request | ✅ Enforced |
| Description | Not empty | ⚠️ Manual |
| Acceptance Criteria | At least one item | ⚠️ Manual |

### DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Acceptance criteria met | All items checked | ⚠️ Manual |
| Parent updated | Progress noted on parent | ⚠️ Manual |

**Note**: Subtasks typically don't require separate PRs - they contribute to the parent task's PR.

---

## Assigned Role Values

| Skill Name | When to Assign | Ticket Prefix |
|------------|----------------|---------------|
| `backend-fastapi-postgres-sqlmodel-developer` | FastAPI endpoints, services, DB | `[Backend]` |
| `frontend-atomic-design-engineer` | React UI components | `[Frontend]` |
| `tech-doc-writer-manager` | Documentation | `[Docs]` |
| `backend-fastapi-pytest-tester` | Backend tests | `[Test]` |
| `frontend-tester` | Frontend/E2E tests | `[Test]` |
| `data-platform-engineer` | Data pipelines | `[Backend]` |
| `api-designer` | API contract design | `[Backend]` |

---

## Relationship Fields

**All relationships set via Project Coordinator** using native ticket system fields.

| System | Parent Field | Blocked By Field |
|--------|--------------|------------------|
| Linear | `parentId` | `blockedBy` |
| GitHub | `addSubIssue` GraphQL | `addBlockedBy` GraphQL |
| Plan Files | N/A | `(blockedBy: ...)` |

**DO NOT** put relationship info in ticket body text. PC sets native fields.

---

## Progress Comment Formats

Workers add structured comments at lifecycle points:

### When Starting Work
```markdown
🚀 **Started**
- Branch: `{branch-name}`
- Base: `{base_branch}` (confirmed with user)
- Approach: [Brief implementation approach]
```

### When PR Created
```markdown
🔍 **Ready for review**
- PR: [link] (targeting {base_branch})
- Changes: [Brief summary]
- Tests: [What's covered]
```

### When Complete
```markdown
✅ **Completed**
- PR merged: [link]
- Files: [Key files changed]
- Notes: [Anything for QA/next steps]
```
