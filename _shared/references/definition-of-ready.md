# Definition of Ready (DoR)

**Universal checklist for ticket readiness.** Project Coordinator enforces this at ticket creation time.

## Who Uses This

| Role | Uses DoR For |
|------|--------------|
| **Project Coordinator** | **ENFORCES** - rejects ticket creation if DoR not met |
| **Solutions Architect** | Prepares sub-issues to pass DoR checks |
| **TPO** | Prepares parent issues to pass DoR checks |
| **PM** | Additional validation before Drive Mode |
| **Workers** | Understands what "ready" looks like |

## Enforcement Point

**Project Coordinator is the enforcer.** When any role invokes `[PROJECT_COORDINATOR] Create`, the coordinator:
1. Parses the provided content
2. Verifies ALL required elements exist
3. **REJECTS with specific gaps** if checks fail
4. Only creates ticket if ALL checks pass

**Roles cannot bypass this gate.** Fix the content and retry.

## Definition of Ready Checklist

### For Parent Issues (Content from TPO)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Feature] {name}` format |
| MRD in description | ✅ | Problem, users, success criteria defined |
| **UAT criteria defined** | ✅ | What TPO will verify before accepting |
| Team assigned | ✅ | From project's `Team Slug` in claude.md |
| No open questions | ✅ | All clarifications resolved |

**UAT Criteria**: TPO must define specific, verifiable criteria that they will check before accepting the feature as complete. Project Coordinator will provide template guidance if missing.

### For Sub-Issues (Content from SA)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Type] {description}` - Type: Backend/Frontend/Bug/Docs/Test |
| Parent linked | ✅ | Native field, not body text |
| Technical Spec | ✅ | MUST/MUST NOT/SHOULD constraints |
| Gherkin scenarios | ✅ | Given/When/Then for validation |
| Testing Notes | ✅ | What tests to write, edge cases to cover |
| Dependencies | ✅ | `blockedBy` set via native field (or explicitly "None") |
| Skill prefix | ✅ | `[Backend]`, `[Frontend]`, `[Bug]`, `[Docs]`, `[Test]` |
| No open questions | ✅ | All clarifications resolved in ticket |
| INVEST passed | ✅ | See checklist below |
| **Activity subtasks specified** | ✅ | All 6 activity subtasks for implementation containers |

### For Story/Task/Bug Completeness (Verified by SA)

**INVEST requires each ticket to be Testable.** Every implementation ticket is a **container** with **6 mandatory activity subtasks**:

| Parent Type | Required Activity Subtasks |
|-------------|---------------------------|
| `[Backend]` | `[Dev]`, `[Code Review]`, `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]` |
| `[Frontend]` | `[Dev]`, `[Code Review]`, `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]` |
| `[Bug]` | `[Dev]`, `[Code Review]`, `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]` |

**Activity Subtask Purposes:**

| Subtask | Worker | Purpose | Creates PR |
|---------|--------|---------|------------|
| `[Dev]` | Developer | Implementation | ✅ Yes |
| `[Code Review]` | Code Reviewer | Review implementation | No |
| `[Test]` | Tester | Unit + functional tests | ✅ Yes |
| `[Docs]` | Tech Doc Writer | Documentation | ✅ Yes |
| `[SA Review]` | Solutions Architect | Technical acceptance | No |
| `[UAT]` | TPO | User acceptance | No |

**blockedBy relationships (activity chain):**
- `[Dev]` → None (starts first)
- `[Code Review]` → `[Dev]`
- `[Test]` → `[Code Review]`
- `[Docs]` → `[Test]`
- `[SA Review]` → `[Docs]`
- `[UAT]` → `[SA Review]`
- Container → All 6 activity subtasks

**No exceptions.** If ANY activity subtask is missing, the ticket violates INVEST and is NOT ready.

### For Epic-Level Completeness (Verified by SA/PM)

**In addition to story-level activity subtasks**, each Epic MUST have cross-cutting tickets:

| Epic-Level Ticket | Required | Purpose |
|-------------------|----------|---------|
| `[Test] {Feature} E2E Regression` | ✅ ALWAYS | Full feature integration/regression testing |
| `[Docs] {Feature} Guide` | ✅ ALWAYS for user-facing | Comprehensive feature documentation |
| `[SA Review] {Feature} Architecture` | ✅ ALWAYS | Architecture compliance across all stories |
| `[UAT] {Feature} Acceptance` | ✅ ALWAYS | Feature acceptance by TPO |

**blockedBy relationships:**
- Epic `[Test]` → blockedBy all Story/Task/Bug containers
- Epic `[Docs]` → blockedBy Epic `[Test]`
- Epic `[SA Review]` → blockedBy Epic `[Docs]`
- Epic `[UAT]` → blockedBy Epic `[SA Review]`

### Why This Hierarchy?

**Story-Level Activities:**
- Each ticket is independently testable (INVEST - Testable)
- Full lifecycle tracking: Dev → Code Review → Test → Docs → SA Review → UAT
- QA writes unit + functional tests for each specific change
- Each activity is a visible, trackable subtask

**Epic-Level Cross-Cutting:**
- Integration/E2E testing across all stories
- Regression testing for the whole feature
- Architecture compliance verification across all stories
- Feature acceptance by TPO
- Catches issues that only appear when components interact

**If missing**: SA must create the activity subtasks/epic tickets before PM can drive.

### INVEST Checklist (Sub-Issues Only)

- [ ] **I**ndependent: Can start without waiting (or `blockedBy` set)
- [ ] **N**egotiable: Approach flexible, criteria fixed
- [ ] **V**aluable: Moves feature toward "Done"
- [ ] **E**stimable: Bounded scope with known files and clear end state
- [ ] **S**mall: Single logical change (one PR, one concern)
- [ ] **T**estable: Technical Spec + Gherkin verifiable; all 6 activity subtasks exist

## DoR Enforcement

### When Creating Tickets (SA)

Before `create_issue`, verify ALL checks pass. If any fail:

```
❌ TICKET CREATION BLOCKED

Title: "[Backend] User API"

Missing:
- Technical Spec: Not defined
- Gherkin scenarios: Missing
- Parent: Not linked

Action: Complete these before creating ticket.
```

### When Entering Drive Mode (PM)

Before driving, verify ALL tickets pass DoR. If any fail:

```
[PM] - ⛔ Cannot enter Drive Mode

Definition of Ready not met:

| Ticket | Missing | Route To |
|--------|---------|----------|
| [ID-1] | Technical Spec | SA |
| [ID-2] | Gherkin scenarios | SA |

Fix these gaps, then invoke Drive Mode again.
```

### Routing When DoR Fails

| Missing Item | Route To |
|--------------|----------|
| MRD/Requirements | TPO |
| UAT criteria | TPO |
| Technical Spec | Solutions Architect |
| Gherkin scenarios | Solutions Architect |
| Dependencies | Solutions Architect |
| Activity subtasks (`[Dev]`, `[Code Review]`, `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]`) | Solutions Architect |
| Epic-level tickets (`[Test]`, `[Docs]`, `[SA Review]`, `[UAT]`) | Solutions Architect |
| Test strategy | Tester |
| Documentation plan | Tech Doc Writer |

## Common Issues

| Issue | Fix |
|-------|-----|
| Vague acceptance criteria | Add MUST/MUST NOT/SHOULD constraints |
| Missing dependencies | SA reviews task ordering |
| No Gherkin scenarios | SA adds Given/When/Then |
| Open questions in ticket | Resolve via comments, then update ticket |
| Title missing prefix | Use `[Backend]`, `[Frontend]`, etc. |
| No UAT criteria (parent) | TPO adds verifiable UAT checklist |

## Related References

- `definition-of-done.md` - Completion checklist
- `project-coordinator/SKILL.md` - Ticket operations and quality enforcement
