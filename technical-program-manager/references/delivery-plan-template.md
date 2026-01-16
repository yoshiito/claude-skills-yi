# Delivery Plan Template

Comprehensive structure for project/feature delivery plans with task breakdown, dependencies, and quality gates.

## Development Philosophy

Every task follows these principles:
- **Tests written with implementation** - Code + tests as definition of done
- **Documentation updated with each task** - Not deferred to the end
- **Regression tests run after each feature** - Gate before merging
- **Dependencies explicitly mapped** - No hidden blockers

---

## Delivery Plan Structure

```markdown
# Delivery Plan: [Project/Feature Name]

## Overview

| Field | Value |
|-------|-------|
| **Project** | [Name] |
| **MRD** | [Link to MRD from TPO] |
| **Architecture** | [Link to ADR from SA] |
| **Linear Project** | [Link to Linear project] |
| **TPgM Owner** | [Name] |
| **Status** | 🟢 On Track / 🟡 At Risk / 🔴 Off Track |

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

---

## Task Hierarchy

Epic → Feature → Task structure for Linear:

```
[Epic] Project Name
├── [Feature] Component/Module 1
│   ├── [Task] Schema/data model changes
│   ├── [Task] Backend implementation (incl. tests)
│   ├── [Task] Frontend implementation (incl. tests)
│   ├── [Task] Documentation updates
│   └── [Task] Regression gate
│
├── [Feature] Component/Module 2
│   ├── [Task] ...
│   └── ...
│
└── [Feature] Final Validation
    ├── [Task] Full regression suite
    ├── [Task] Documentation review
    └── [Task] Release readiness checklist
```

---

## Task Breakdown Table

### Feature: [Feature Name]

| Task ID | Task Name | Blocked By | Tests Required | Docs to Update | Branch |
|---------|-----------|------------|----------------|----------------|--------|
| [PRE]-1 | [Task description] | - | [Test type/count] | [Doc file] | `[branch-pattern]` |
| [PRE]-2 | [Task description] | [PRE]-1 | [Test type/count] | [Doc file] | `[branch-pattern]` |
| [PRE]-3 | [Task description] | [PRE]-1, [PRE]-2 | [Test type/count] | - | `[branch-pattern]` |

**Acceptance Criteria - [PRE]-1:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

**Tests Required - [PRE]-2:**
| Test Case | Type | Description |
|-----------|------|-------------|
| `test_name_happy_path` | Happy | [What it verifies] |
| `test_name_error_case` | Error | [What it verifies] |
| `test_name_edge_case` | Edge | [What it verifies] |

**Regression Gate - [PRE]-N:**
- [ ] All existing tests pass
- [ ] All new tests pass
- [ ] No new failures introduced

---

## Dependency Graph

```
[Task A] ──────────────────┐
                           ├──► [Task C] ──┐
[Task B] ──────────────────┘               │
                                           ├──► [Integration] ──► [Release]
[Task D] ──► [Task E] ────────────────────┘
```

---

## Branching Strategy

```
main
│
├── feat/{team}/{ID}-{feature-1}
│   └── PR → main (after regression)
│
├── feat/{team}/{ID}-{feature-2}
│   ├── Depends on: feature-1 merged
│   └── PR → main (after regression)
│
└── feat/{team}/{ID}-cleanup
    ├── Depends on: All above merged
    └── PR → main
```

---

## Documentation Updates Summary

| Document | Tasks That Update It | Changes |
|----------|---------------------|---------|
| `[file path]` | [Task IDs] | [Description of changes] |
| `[file path]` | [Task IDs] | [Description of changes] |

---

## Test Coverage Summary

| Feature | Tasks | Tests Written | Coverage Target |
|---------|-------|---------------|-----------------|
| [Feature 1] | N | NN pytest | [%] |
| [Feature 2] | N | NN pytest | [%] |
| **TOTAL** | **N** | **NN pytest** | **[%]** |

---

## Risks & Dependencies

### Internal Dependencies
| ID | Dependency | Owner | Needed By | Status | Impact if Late |
|----|------------|-------|-----------|--------|----------------|
| D1 | [Dependency] | [Team] | [Task ID] | [Status] | [Impact] |

### External Dependencies
| ID | Dependency | Vendor | Needed By | Status | Mitigation |
|----|------------|--------|-----------|--------|------------|
| E1 | [Dependency] | [Vendor] | [Task ID] | [Status] | [Mitigation] |

### Risks
| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|-------------|--------|------------|-------|
| R1 | [Risk] | H/M/L | H/M/L | [Mitigation] | [Name] |

---

## Linear Import Summary

| ID | Type | Title | Parent | Blocked By | Branch |
|----|------|-------|--------|------------|--------|
| EPIC-1 | Epic | [Project Name] | - | - | - |
| FEAT-1 | Feature | [Feature Name] | EPIC-1 | - | feat/... |
| [PRE]-1 | Task | [Task Name] | FEAT-1 | - | feat/... |
| [PRE]-2 | Task | [Task Name] | FEAT-1 | [PRE]-1 | feat/... |

---

## Appendix

### Related Documents
- MRD: [link]
- Architecture/ADR: [link]
- API Contract: [link]
- Test Strategy: [link]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial plan |
```

---

## Task Breakdown Principles

### INVEST Compliance

Every task must be:

| Principle | Validation Question |
|-----------|---------------------|
| **I**ndependent | Can start without waiting? (If not, set `blockedBy`) |
| **N**egotiable | Is approach flexible, criteria fixed? |
| **V**aluable | Does it move feature toward "Done"? |
| **E**stimable | Bounded scope with known files and clear end state? |
| **S**mall | Single logical change (one PR, one concern)? |
| **T**estable | Are acceptance criteria verifiable? |

### Standard Task Types

| Task Type | Contains | Example |
|-----------|----------|---------|
| Schema/Data | DDL, migrations | "Create users table" |
| Backend | API + unit tests | "Implement user CRUD API" |
| Frontend | UI + component tests | "Build user form component" |
| Integration | E2E tests | "End-to-end user flow tests" |
| Documentation | API docs, guides | "Update API_DOCUMENTATION.md" |
| Regression Gate | Full test suite | "Run full regression" |

### Task Granularity Decision

Granularity is determined collaboratively by TPM, SA, and domain experts:

**Fine-grained (single focused change):**
- When tests need dedicated focus (complex edge cases)
- When multiple reviewers needed
- When parallelization benefits

**Coarse-grained (multiple related changes in one PR):**
- When implementation + tests naturally go together
- When single developer owns end-to-end
- Default for most work

**Rule**: Each task must have clear completion comment documenting what was done.

---

## Regression Gates

Every feature ends with a regression gate task:

```markdown
**Regression Gate - [FEAT]-N:**
- [ ] All existing tests pass (`pytest tests/ -v` or equivalent)
- [ ] All new tests pass
- [ ] Integration tests pass (if applicable)
- [ ] No new test failures introduced
- [ ] Documentation updated
```

**Gate Failure Protocol:**
1. Do NOT merge to main
2. Create blocking issue for failure
3. Assign to responsible developer
4. Re-run gate after fix

---

## Final Validation Feature

Every delivery plan includes a Final Validation feature:

```markdown
### Feature: Final Validation

| Task ID | Task Name | Blocked By | Description |
|---------|-----------|------------|-------------|
| VAL-1 | Full regression | [All features] | Run complete test suite |
| VAL-2 | Documentation review | VAL-1 | Verify all docs current |
| VAL-3 | Release readiness | VAL-2 | Complete release checklist |
```

See `release-checklist.md` for comprehensive readiness gates.
