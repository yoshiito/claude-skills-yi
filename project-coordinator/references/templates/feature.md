# Feature Template (Quality-Bounded Work Unit)

**Content from**: Solutions Architect
**Title format**: `[Backend]` or `[Frontend]` prefix
**Note**: This is a FEATURE ticket - the primary unit of work. Quality phases happen at this level, not as subtasks. Dev subtasks are OPTIONAL.

## Template Structure

```markdown
## Mission Statement
[ONE clear statement defining what "done" looks like for this Feature]

## Story
As a [user type], I want [capability] so that [benefit].

## Context
[Background for someone unfamiliar. Include why this work matters.]

## References
- Parent Mission: [TICKET-ID] - [Mission title]
- Feature Branch: [USER MUST SPECIFY]
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

## Workflow Phases

**CRITICAL**: Each phase MUST specify the role and concrete checklist items for THIS ticket.

### Development
- **Role**: `[exact-skill-name]`
- **Checklist**:
  - [ ] [Concrete work item 1 for THIS ticket]
  - [ ] [Concrete work item 2 for THIS ticket]
  - [ ] [... more ticket-specific work items]
  - [ ] All checklist items complete, PR created
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Code Reviewer

### Code Review
- **Role**: `code-reviewer`
- **Checklist**:
  - [ ] [Specific verification item 1 for THIS ticket]
  - [ ] [Specific verification item 2 for THIS ticket]
  - [ ] [... more ticket-specific review items]
  - [ ] All items verified, PR approved
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to [Tester role]

### Test
- **Role**: `[backend-fastapi-pytest-tester or frontend-tester]`
- **Checklist**:
  - [ ] [Specific test case 1 from Gherkin scenarios]
  - [ ] [Specific test case 2 from Gherkin scenarios]
  - [ ] [... more ticket-specific test items]
  - [ ] All tests passing
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Tech Doc Writer

### Docs (if user-facing changes)
- **Role**: `tech-doc-writer-manager`
- **Checklist**:
  - [ ] [Specific doc update 1 for THIS ticket]
  - [ ] [... more ticket-specific doc items]
  - [ ] All docs updated
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to Solutions Architect

### SA Review
- **Role**: `solutions-architect`
- **Checklist**:
  - [ ] [Specific architecture check for THIS ticket]
  - [ ] Architecture compliance verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Hand off to TPO

### UAT
- **Role**: `technical-product-owner`
- **Checklist**:
  - [ ] [Acceptance criterion 1 from Gherkin]
  - [ ] [Acceptance criterion 2 from Gherkin]
  - [ ] All acceptance criteria verified
  - [ ] Comment on ticket with completion evidence
  - [ ] Check off completed checklist items in ticket
  - [ ] Feature complete

## Open Questions
- [ ] [Any unresolved questions - MUST be empty before creation]
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title prefix | `[Backend]` or `[Frontend]` | ✅ Enforced |
| Mission Statement | ONE clear "done" definition | ✅ Enforced |
| Story | User story format | ⚠️ Manual |
| Context | Not empty | ⚠️ Manual |
| Technical Spec | `<technical-spec>` with `<must>` section | ✅ Enforced |
| Gherkin scenarios | `Given`/`When`/`Then` keywords present | ✅ Enforced |
| Testing Notes | Section exists | ✅ Enforced |
| Workflow Phases | Each phase has Role + Checklist items | ✅ Enforced |
| Open Questions | **EMPTY** (all resolved) | ✅ Enforced |
| Parent Mission | `Parent Mission: #NUM` in request | ✅ Enforced |
| **Feature Branch** | **User-specified branch name (BLOCKING)** | ✅ Enforced |
| Quality-bounded | See checklist below | ⚠️ Manual |

**Workflow Phases Requirement (SA specifies before invoking PC):**
- [ ] Each phase has `Role:` with exact skill slug
- [ ] Each phase has `Checklist:` with concrete items for THIS ticket
- [ ] Checklist items are ticket-specific (not generic "implement feature")
- [ ] Each phase ends with hand-off to next role
- [ ] Development checklist items derived from Technical Spec
- [ ] Test checklist items derived from Gherkin scenarios
- [ ] Code Review checklist items specify what to verify for THIS ticket

**Role-Phase Validation (PC enforces - BLOCKING):**

| Phase Type | Valid Roles | Invalid Assignment = REJECT |
|------------|-------------|----------------------------|
| Development | `backend-*-developer`, `frontend-*-engineer`, `mcp-server-developer`, `data-platform-engineer`, `ai-integration-engineer`, `api-designer`, `ux-designer`, `svg-designer` | Tester, Doc Writer, Reviewer |
| Code Review | `code-reviewer` | Any other role |
| Test | `backend-*-tester`, `frontend-tester` | Developer, Doc Writer |
| Docs | `tech-doc-writer-manager` | Developer, Tester |
| SA Review | `solutions-architect` | Any other role |
| UAT | `technical-product-owner` | Any other role |
| Subtask Complete | `project-coordinator` | Any other role |

**PC MUST read the assigned role's SKILL.md** to verify the phase work falls within that role's `authorizedActions`. If not → REJECT with specific boundary violation.

**Dev Subtasks (OPTIONAL - only if implementation needs breakdown):**
- [ ] `[Dev]` subtasks specified if implementation is complex

**Quality Boundary Checklist (SA verifies before invoking PC):**
- [ ] **Reviewable**: Code review can validate comprehensively in one session
- [ ] **Testable**: Tests can cover this feature completely
- [ ] **UAT-able**: TPO can verify outcome in one pass
- [ ] **Architecturally coherent**: SA can review compliance holistically
- [ ] **Mission-driven**: ONE clear statement of what "done" looks like
- [ ] **Feature branch**: User has provided branch name

## DoD: Definition of Done (Before Closing)

**Features are Done when ALL workflow phases are complete.**

| Check | Required | PC Validates |
|-------|----------|--------------|
| Development complete | PR created | ✅ PR link in comment |
| Code Review complete | PR approved and merged | ✅ Merge confirmed |
| Test complete | Tests written and passing | ✅ Test completion comment |
| Docs complete | Documentation updated (if user-facing) | ⚠️ Conditional |
| SA Review complete | Architecture validated | ✅ SA approval comment |
| UAT complete | TPO accepted | ✅ UAT approval comment |
| Technical Spec satisfied | All MUST/MUST NOT met | ⚠️ Manual |
| Dev subtasks done | All `[Dev]` children complete (if any) | ✅ Enforced |

**Feature Completion Comment:**
```markdown
✅ **Feature Complete**

## Mission Statement
[Restated mission - confirmed achieved]

## Workflow Phases
- [x] Development: PR #{num} merged
- [x] Code Review: Approved by {reviewer}
- [x] Test: {X} tests passing
- [x] Docs: Updated [list pages]
- [x] SA Review: Architecture validated
- [x] UAT: Accepted by TPO

## Technical Spec
All MUST/MUST NOT requirements satisfied.
```

**Note**: Quality phases are tracked within the Feature ticket via comments and checklists.
