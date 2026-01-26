# Ticket Templates

**Project Coordinator enforces these templates.** Each template includes Definition of Ready (DoR) for creation and Definition of Done (DoD) for completion.

## Template Overview

| Level | Template | Content From | Use Case |
|-------|----------|--------------|----------|
| **Epic** | `[Feature]` | TPO | Feature-level container |
| **Story/Task** | `[Backend]`/`[Frontend]` | SA | Container for implementation activities |
| **Bug** | `[Bug]` | Support Engineer | Container for bug fix activities |
| **Activity** | `[Dev]` | SA | Implementation subtask |
| **Activity** | `[Code Review]` | SA | Code review subtask |
| **Activity** | `[Test]` | SA | Testing subtask (QA writes all tests) |
| **Activity** | `[Docs]` | SA | Documentation subtask |
| **Activity** | `[SA Review]` | SA | Solutions Architect technical acceptance |
| **Activity** | `[UAT]` | SA | TPO user acceptance testing |
| **Communication** | `[Query]` | Any Role | Cross-team/intra-team gap discovery |

**Note**: All tickets are created by **Project Coordinator**. The "Content From" column indicates which role provides the ticket content when invoking PC.

---

## Ticket Hierarchy Model

**INVEST requires each ticket to be Testable.** Every Story/Task/Bug is a **container** with explicit activity subtasks for full lifecycle tracking.

### Story/Task/Bug Level (Container with Activities)

```
[Backend] Add password reset endpoint        ← Container (groups all activities)
├── [Dev] Add password reset endpoint        ← Implementation
├── [Code Review] Add password reset endpoint ← Code review
├── [Test] Add password reset endpoint       ← Testing (QA writes all tests)
├── [Docs] Add password reset endpoint       ← Documentation
├── [SA Review] Add password reset endpoint  ← SA technical acceptance
└── [UAT] Add password reset endpoint        ← TPO user acceptance
```

Each Story/Task/Bug includes ALL lifecycle activities as explicit subtasks:

| Step | Subtask | Worker | Purpose |
|------|---------|--------|---------|
| 1 | `[Dev]` | Developer | Implementation |
| 2 | `[Code Review]` | Code Reviewer | Review implementation |
| 3 | `[Test]` | Tester | Unit + functional tests |
| 4 | `[Docs]` | Tech Doc Writer | Documentation |
| 5 | `[SA Review]` | Solutions Architect | Technical/architecture validation |
| 6 | `[UAT]` | TPO | User/business acceptance |

### Epic Level (Cross-Cutting)

In addition to story-level activities, each Epic has cross-cutting tickets:

```
Epic: Password Reset Feature
├── [Backend] Add reset endpoint
│   ├── [Dev], [Code Review], [Test], [Docs], [SA Review], [UAT]
├── [Frontend] Add reset form
│   ├── [Dev], [Code Review], [Test], [Docs], [SA Review], [UAT]
├── [Bug] Fix validation edge case
│   ├── [Dev], [Code Review], [Test], [Docs], [SA Review], [UAT]
├── [Query] API rate limit unclear (Backend)  ← Communication (no subtasks)
│   └── (relatesTo: [Frontend] Add reset form, blocks its [Dev])
├── [Test] Password Reset E2E Regression      ← Epic-level activity
├── [Docs] Password Reset Feature Guide       ← Epic-level activity
├── [SA Review] Password Reset Architecture   ← Epic-level activity
└── [UAT] Password Reset Feature Acceptance   ← Epic-level activity
```

| Epic-Level Ticket | Purpose |
|-------------------|---------|
| `[Query] {Subject} ({Target Team})` | Cross-team/intra-team gap discovery and resolution |
| `[Test] {Feature} E2E Regression` | Full feature integration/regression testing |
| `[Docs] {Feature} Guide` | Comprehensive feature documentation |
| `[SA Review] {Feature} Architecture` | SA validates architecture compliance across all stories |
| `[UAT] {Feature} Acceptance` | TPO acceptance of complete feature |

**Note**: `[Query]` has no activity subtasks. It is resolved through human discussion, not implementation.

### blockedBy Relationships (Activity Chain)

| Subtask | blockedBy |
|---------|-----------|
| `[Dev]` | None (starts first) + any open `[Query]` blockers |
| `[Code Review]` | `[Dev]` |
| `[Test]` | `[Code Review]` |
| `[Docs]` | `[Test]` |
| `[SA Review]` | `[Docs]` |
| `[UAT]` | `[SA Review]` |
| Parent container | All activity subtasks |

### Query as Dynamic Blocker

When a `[Query]` ticket is created:
1. **PC auto-links** the Query to the originating ticket's `[Dev]` subtask via `blockedBy`
2. **`[Dev]` cannot be marked Done** while any linked Query is open
3. **Query resolution** removes the blocker relationship automatically

| Epic-Level | blockedBy |
|------------|-----------|
| Epic `[Test]` | All Story/Task/Bug containers |
| Epic `[Docs]` | Epic `[Test]` |
| Epic `[SA Review]` | Epic `[Docs]` |
| Epic `[UAT]` | Epic `[SA Review]` |

---

## 1. Epic Template

**Content from**: Technical Product Owner
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

## Branch Information
- **Epic Branch**: `[USER MUST SPECIFY]`

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
| **Epic Branch** | **User-specified branch name** | ✅ Enforced |
| Team assigned | From project's `Team Slug` in claude.md | ✅ Auto (from config) |

**Epic Branch Requirement**: User MUST specify the branch all Story/Task/Bug work will target. This cannot be assumed or defaulted. See "Branch Confirmation Protocol" below.

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

## 2. Story/Task Template (Container)

**Content from**: Solutions Architect
**Title format**: `[Backend]` or `[Frontend]` prefix
**Note**: This is a CONTAINER ticket. SA creates 6 activity subtasks for each container.

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
| Title prefix | `[Backend]` or `[Frontend]` | ✅ Enforced |
| Story | User story format | ⚠️ Manual |
| Context | Not empty | ⚠️ Manual |
| Technical Spec | `<technical-spec>` with `<must>` section | ✅ Enforced |
| Gherkin scenarios | `Given`/`When`/`Then` keywords present | ✅ Enforced |
| Testing Notes | Section exists | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| Parent specified | `Parent: #NUM` in request | ✅ Enforced |
| **Activity subtasks specified** | All 6 subtasks defined | ✅ Enforced |
| INVEST compliant | See checklist below | ⚠️ Manual |

**Activity Subtasks (SA creates all 6):**
- [ ] `[Dev]` - Implementation subtask
- [ ] `[Code Review]` - Code review subtask
- [ ] `[Test]` - Testing subtask
- [ ] `[Docs]` - Documentation subtask (if user-facing)
- [ ] `[SA Review]` - SA technical acceptance subtask
- [ ] `[UAT]` - TPO user acceptance subtask

**INVEST Checklist (SA verifies before invoking PC):**
- [ ] **I**ndependent: Can start without waiting (or `blockedBy` set)
- [ ] **N**egotiable: Approach flexible, criteria fixed
- [ ] **V**aluable: Moves feature toward "Done"
- [ ] **E**stimable: Bounded scope, known files, clear end state
- [ ] **S**mall: Single logical change (one PR, one concern)
- [ ] **T**estable: Technical Spec + Gherkin verifiable; all activity subtasks specified

### DoD: Definition of Done (Before Closing)

#### For `[Backend]` and `[Frontend]` Containers

**These are now CONTAINERS.** They are Done when ALL activity subtasks are Done.

| Check | Required | PC Validates |
|-------|----------|--------------|
| `[Dev]` subtask done | ✅ | ✅ Enforced |
| `[Code Review]` subtask done | ✅ | ✅ Enforced |
| `[Test]` subtask done | ✅ | ✅ Enforced |
| `[Docs]` subtask done | ✅ (if user-facing) | ✅ Enforced |
| `[SA Review]` subtask done | ✅ | ✅ Enforced |
| `[UAT]` subtask done | ✅ | ✅ Enforced |
| Technical Spec satisfied | All MUST/MUST NOT met | ⚠️ Manual |

**Container Completion Comment:**
```markdown
✅ **Story/Task Complete**
- All 6 activity subtasks: Done
- [Dev] #{num}: ✅
- [Code Review] #{num}: ✅
- [Test] #{num}: ✅
- [Docs] #{num}: ✅
- [SA Review] #{num}: ✅
- [UAT] #{num}: ✅
```

**Note**: Container tickets track overall progress. Actual work happens in activity subtasks.

---

## 3. Bug Template

**Content from**: Support Engineer
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

### Mandatory Activity Subtasks

Like Story/Task, every Bug MUST have all 6 activity subtasks:

| Subtask | Required | Purpose |
|---------|----------|---------|
| `[Dev]` | ✅ ALWAYS | Implement the fix |
| `[Code Review]` | ✅ ALWAYS | Review the fix |
| `[Test]` | ✅ ALWAYS | Regression test for the fix |
| `[Docs]` | If user-facing | Document behavior change |
| `[SA Review]` | ✅ ALWAYS | Technical validation |
| `[UAT]` | ✅ ALWAYS | TPO acceptance |

### DoD: Definition of Done (Before Closing)

**Bugs are now CONTAINERS.** They are Done when ALL activity subtasks are Done.

| Check | Required | PC Validates |
|-------|----------|--------------|
| `[Dev]` subtask done | ✅ | ✅ Enforced |
| `[Code Review]` subtask done | ✅ | ✅ Enforced |
| `[Test]` subtask done | ✅ | ✅ Enforced |
| `[Docs]` subtask done | If user-facing | ⚠️ Conditional |
| `[SA Review]` subtask done | ✅ | ✅ Enforced |
| `[UAT]` subtask done | ✅ | ✅ Enforced |
| Root cause documented | In `[Dev]` comment | ⚠️ Manual |

**Container Completion Comment:**
```markdown
✅ **Bug Fixed**
- Root cause: [Brief explanation]
- All activity subtasks: Done
- [Dev] #{num}: ✅
- [Code Review] #{num}: ✅
- [Test] #{num}: ✅
- [Docs] #{num}: ✅ / N/A
- [SA Review] #{num}: ✅
- [UAT] #{num}: ✅
```

---

## 4. Query Template (Communication Protocol)

**Content from**: Any role discovering a gap
**Title format**: `[Query] {Subject} ({Target Team})`
**Purpose**: Formalize discovery gaps that require cross-team or intra-team resolution

### Hierarchy Position

Query is at the **same level as Story/Task/Bug** - a child of Epic:

```
[Feature] Password Reset (Epic)
├── [Backend] Add reset endpoint (Story)
├── [Frontend] Add reset form (Story)  ← Gap discovered here
├── [Bug] Fix validation (Bug)
└── [Query] API rate limit unclear (Backend Team)  ← Sibling to Story/Task/Bug
```

**Key differences from Story/Task/Bug:**
- **No activity subtasks** - Query is resolved through discussion, not implementation
- **Has "Originating Ticket" link** - Separate from parent; links to the ticket where gap was found
- **Blocks originating ticket's `[Dev]`** - Dynamic blocker until resolved

### When to Use

| Situation | Use [Query]? |
|-----------|--------------|
| Frontend discovers Backend API limitation | ✅ Yes |
| Dev finds unclear spec during implementation | ✅ Yes |
| Tester identifies missing edge case coverage | ✅ Yes |
| SA needs clarification from another domain | ✅ Yes |
| Simple bug in own team's code | ❌ No - use `[Bug]` |
| Missing requirement | ❌ No - route to TPO |

### Template Structure

```markdown
## Originating Context
- **Originating Ticket**: [TICKET-ID] - [Title]
- **Originating Role**: [Role that discovered the gap]
- **Discovery Phase**: [Planning / Dev / Test / Review]

## Target
- **Target Team**: [Team slug or name]
- **Target Domain**: [Backend API / Frontend / Data / Infrastructure / etc.]

## Gap Description

### What We Found
[Describe the technical gap or limitation discovered]

### What We Expected
[What the originating team expected to exist or work]

### Why This Matters
[Impact on the originating work - why this blocks progress]

## Technical Details
[Include relevant code snippets, API calls, error messages, specs referenced]

## Questions for Target Team
1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3]

## Proposed Solutions (Optional)
[If the originating team has suggestions]

## References
- Related ADR: [Link if applicable]
- Related API Spec: [Link if applicable]
```

### DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title format | `[Query] {Subject} ({Target Team})` | ✅ Enforced |
| Parent (Epic) | Linked via native parent field | ✅ Enforced |
| Originating Ticket | Linked via `relatesTo` field (separate from parent) | ✅ Enforced |
| Target Team | Specified in body | ✅ Enforced |
| Gap Description | "What We Found" not empty | ✅ Enforced |
| Technical Details | Section exists | ✅ Enforced |
| At least one question | Questions section not empty | ✅ Enforced |

### DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Resolution provided | Target team answered questions | ✅ Enforced |
| Resolution Summary comment | Structured summary added | ✅ Enforced |
| Caller is resolver | Human in the loop closes after resolution | ✅ Enforced |

**Resolution Summary Comment Format:**
```markdown
✅ **Query Resolved**

## Resolution
[Technical answer to the gap/questions]

## Decision
[What was decided - proceed as-is, change needed, workaround, etc.]

## Spec/ADR Updates
- [Link to updated spec/ADR if applicable]
- [Or "No updates required" with rationale]

## Impact on Originating Ticket
[How the originating work should proceed given this resolution]

Resolved by: [Name/role]
```

### Automatic Blocker Behavior

**When PC creates a `[Query]` ticket:**

1. Set parent to the Epic (same parent as originating Story/Task/Bug)
2. Set `relatesTo` link to the originating Story/Task/Bug
3. **Add Query to originating ticket's `[Dev]` subtask's `blockedBy` list**
4. Log the blocker relationship

**Workflow Constraint**: No `[Dev]` subtask can be marked "Done" if it has an open `[Query]` blocker.

**When PC marks a `[Query]` as Done:**

1. **Remove Query from `[Dev]`'s `blockedBy` list**
2. Verify Resolution Summary comment exists
3. Mark Query as Done

---

## 5. Activity Subtask Templates

**Content from**: Solutions Architect (during work breakdown)
**SA creates all 6 activity subtasks** for each Story/Task/Bug container.

---

### 5.1 `[Dev]` - Implementation Subtask

**Assigned to**: Developer (Backend/Frontend)

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| Parent container exists | ✅ | - |
| Technical Spec available | ✅ | - |
| **Epic Branch confirmed** | ✅ (BLOCKING) | - |
| PR created | - | ✅ Link in comment |
| PR targets Epic Branch | - | ✅ Verified |
| Technical Spec satisfied | - | ✅ Confirmed in comment |

**⛔ Branch Confirmation Protocol (BLOCKING)**

Before starting ANY work, prompt user:

```
⛔ BRANCH CONFIRMATION REQUIRED

I cannot proceed without knowing the target branch.

Please confirm:
  Epic Branch: _________________ (e.g., feature/password-reset)

This branch will be the PR target for this work.

Waiting for your response...
```

**Do NOT proceed until user provides explicit branch name.**

**Completion Comment:**
```markdown
✅ **[Dev] Complete**
- PR: [link] (targets `{epic-branch}`)
- Branch: `{story-branch}`
- Files: [Key files changed]
- Technical Spec: All MUST/MUST NOT met
- Ready for: Code Review
```

**Note**: PR merging happens AFTER Code Review approval (Code Reviewer merges to Epic branch).

---

### 5.2 `[Code Review]` - Code Review Subtask

**Assigned to**: Code Reviewer

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| `[Dev]` subtask done | ✅ | - |
| PR link available | ✅ | - |
| PR targets Epic Branch | ✅ | - |
| Review completed | - | ✅ |
| **All issues resolved** | - | ✅ (none remain) |
| Approved | - | ✅ |
| **PR merged to Epic Branch** | - | ✅ |

**No issues pass through.** Code Reviewer MUST reject PRs with ANY unresolved issues (Critical, High, Medium, or Minor). Fix and re-review until clean.

**Code Reviewer Merge Responsibility:**

After approval, Code Reviewer merges the PR to Epic branch:

```bash
gh pr merge {PR_NUMBER} --squash --delete-branch
```

**Completion Comment:**
```markdown
✅ **[Code Review] Complete**
- PR: [link]
- Status: Approved and Merged
- Merged to: `{epic-branch}`
- Issues found: [X] (all resolved)
- Ready for: Testing
```

**Note**: Code Reviewer merges Story/Task/Bug PRs to Epic branch. User merges Epic branch to main.

---

### 5.3 `[Test]` - Testing Subtask

**Assigned to**: Tester (QA writes ALL tests - unit + functional)

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| `[Code Review]` subtask done | ✅ | - |
| Gherkin scenarios available | ✅ | - |
| Unit tests written | - | ✅ |
| Functional tests written | - | ✅ |
| All tests passing | - | ✅ |
| Test PR created | - | ✅ Link in comment |

**Completion Comment:**
```markdown
✅ **[Test] Complete**
- PR: [link]
- Unit tests: [X] tests
- Functional tests: [Y] scenarios
- Coverage: [Z]%
- All passing: ✅
- Ready for: User to merge, then Documentation
```

**Note**: User merges test PR. Agent DoD is test code written and passing.

---

### 5.4 `[Docs]` - Documentation Subtask

**Assigned to**: Tech Doc Writer

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| `[Test]` subtask done | ✅ | - |
| Implementation complete | ✅ | - |
| Documentation created | - | ✅ |
| Matches implementation | - | ✅ |
| Review completed | - | ✅ |
| Docs PR created | - | ✅ Link in comment |

**Completion Comment:**
```markdown
✅ **[Docs] Complete**
- PR: [link]
- Docs updated: [list pages/sections]
- Reviewed by: [reviewer]
- Ready for: User to merge, then SA Review
```

**Note**: User merges docs PR. Agent DoD is documentation written and reviewed.

---

### 5.5 `[SA Review]` - SA Technical Acceptance Subtask

**Assigned to**: Solutions Architect

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| `[Docs]` subtask done | ✅ | - |
| All PRs merged | ✅ | - |
| Architecture compliance verified | - | ✅ |
| ADR requirements met | - | ✅ |
| No technical debt introduced | - | ✅ |
| **Query resolutions integrated** | - | ✅ (if any Queries were raised) |

**Query Integration Verification**: If any `[Query]` tickets were raised against this container during development, SA must verify:
- Query resolutions were incorporated into the implementation
- Any spec/ADR updates from Query resolutions are reflected in the code
- No outstanding gaps remain from Query discussions

**Completion Comment:**
```markdown
✅ **[SA Review] Complete**
- Architecture compliance: ✅
- ADR requirements: Met
- Technical debt: None introduced
- Query integration: [N/A / Verified - X queries resolved and incorporated]
- Issues: [None / List]
- Ready for: UAT
```

---

### 5.6 `[UAT]` - TPO User Acceptance Subtask

**Assigned to**: Technical Product Owner

| Check | DoR (Before Start) | DoD (Before Done) |
|-------|-------------------|-------------------|
| `[SA Review]` subtask done | ✅ | - |
| All previous activities complete | ✅ | - |
| Acceptance criteria verified | - | ✅ |
| User flows work as expected | - | ✅ |
| Business requirements met | - | ✅ |

**Completion Comment:**
```markdown
✅ **[UAT] Complete**
- Acceptance criteria: All met
- User flows: ✅ Working as expected
- Business requirements: ✅ Satisfied
- Story/Task/Bug: Ready to close
```

---

### Activity Subtask Summary

| Subtask | Worker | blockedBy | Creates PR |
|---------|--------|-----------|------------|
| `[Dev]` | Developer | None | ✅ Yes |
| `[Code Review]` | Code Reviewer | `[Dev]` | No |
| `[Test]` | Tester | `[Code Review]` | ✅ Yes |
| `[Docs]` | Tech Doc Writer | `[Test]` | ✅ Yes |
| `[SA Review]` | Solutions Architect | `[Docs]` | No |
| `[UAT]` | TPO | `[SA Review]` | No |

---

## Assigned Role Values

### Container Tickets

| Ticket Prefix | Created By | Purpose |
|---------------|------------|---------|
| `[Backend]` | SA | Backend implementation container |
| `[Frontend]` | SA | Frontend implementation container |
| `[Bug]` | Support Engineer | Bug fix container |

### Communication Tickets (No Subtasks)

| Ticket Prefix | Created By | Purpose |
|---------------|------------|---------|
| `[Query]` | Any role | Cross-team/intra-team gap discovery (human-resolved)

### Activity Subtasks (Mandatory for each container)

| Subtask | Skill Name | Purpose |
|---------|------------|---------|
| `[Dev]` | `backend-fastapi-postgres-sqlmodel-developer` / `frontend-atomic-design-engineer` | Implementation |
| `[Code Review]` | `code-reviewer` | Code review |
| `[Test]` | `backend-fastapi-pytest-tester` / `frontend-tester` | Testing (QA writes all tests) |
| `[Docs]` | `tech-doc-writer-manager` | Documentation |
| `[SA Review]` | `solutions-architect` | Technical acceptance |
| `[UAT]` | `technical-product-owner` | User acceptance |

### Epic-Level Cross-Cutting Tickets

| Ticket | Skill Name | Purpose |
|--------|------------|---------|
| `[Test] {Feature} E2E Regression` | `backend-fastapi-pytest-tester` / `frontend-tester` | Full feature regression |
| `[Docs] {Feature} Guide` | `tech-doc-writer-manager` | Comprehensive feature docs |
| `[SA Review] {Feature} Architecture` | `solutions-architect` | Architecture compliance |
| `[UAT] {Feature} Acceptance` | `technical-product-owner` | Feature acceptance |

---

## Relationship Fields

**All relationships set via Project Coordinator** using native ticket system fields.

| System | Parent Field | Blocked By Field | Relates To Field |
|--------|--------------|------------------|------------------|
| Linear | `parentId` | `blockedBy` | `relatedIssues` |
| GitHub | `addSubIssue` GraphQL | `addBlockedBy` GraphQL | `convertedNoteToIssue` links |
| Plan Files | N/A | `(blockedBy: ...)` | `(relatesTo: ...)` |

**DO NOT** put relationship info in ticket body text. PC sets native fields.

### Query-Specific Relationships

When creating a `[Query]` ticket, PC sets:
1. **Parent**: Epic (same as originating Story/Task/Bug)
2. **Relates To**: The originating Story/Task/Bug where gap was discovered
3. **Blocked By (on target)**: PC adds Query to originating ticket's `[Dev]` subtask's blockedBy list

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
