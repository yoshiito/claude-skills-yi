# Definition of Ready (DoR)

**Universal checklist for ticket readiness.** All roles use this to determine if a ticket is ready for work.

## Who Uses This

| Role | Uses DoR For |
|------|--------------|
| **Solutions Architect** | Validates sub-issues before creation |
| **TPO** | Validates parent issues before handoff |
| **TPgM** | Gates Drive Mode - cannot drive incomplete work |
| **Workers** | Understands what "ready" looks like |

## Definition of Ready Checklist

### For Parent Issues (Created by TPO)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Feature] {name}` format |
| MRD in description | ✅ | Problem, users, success criteria defined |
| Team assigned | ✅ | Valid team in ticket system |
| No open questions | ✅ | All clarifications resolved |

### For Sub-Issues (Created by SA)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Type] {description}` - Type: Backend/Frontend/Docs/Test |
| Parent linked | ✅ | Native field, not body text |
| Technical Spec | ✅ | MUST/MUST NOT/SHOULD constraints |
| Gherkin scenarios | ✅ | Given/When/Then for validation |
| Testing Notes | ✅ | What tests to write, edge cases to cover |
| Dependencies | ✅ | `blockedBy` set via native field (or explicitly "None") |
| Skill prefix | ✅ | `[Backend]`, `[Frontend]`, `[Docs]`, `[Test]` |
| No open questions | ✅ | All clarifications resolved in ticket |
| INVEST passed | ✅ | See checklist below |

### For Feature-Level Completeness (Verified by SA/TPgM)

**MANDATORY**: Before a feature can be driven, ALL of these must exist:

| Sub-Issue Type | Required | Purpose |
|----------------|----------|---------|
| Implementation (`[Backend]`/`[Frontend]`) | ✅ ALWAYS | Core functionality |
| Test sub-issue (`[Test]`) | ✅ ALWAYS | Validate implementation against Gherkin scenarios |
| Documentation (`[Docs]`) | ✅ ALWAYS for user-facing | API docs, guides, runbooks |

**No exceptions.** If `[Test]` sub-issue is missing, the feature is NOT ready.

**Why Testing is Mandatory:**
- Gherkin scenarios define WHAT to validate
- `[Test]` sub-issue ensures scenarios are ACTUALLY validated
- Without `[Test]`, Gherkin scenarios are just documentation, not enforcement

**Why Documentation is Mandatory (for user-facing):**
- Users need to know how to use what we build
- API consumers need updated docs
- Without `[Docs]`, feature is incomplete even if code works

**If missing**: SA must create the sub-issue before TPgM can drive.

### INVEST Checklist (Sub-Issues Only)

- [ ] **I**ndependent: Can start without waiting (or `blockedBy` set)
- [ ] **N**egotiable: Approach flexible, criteria fixed
- [ ] **V**aluable: Moves feature toward "Done"
- [ ] **E**stimable: Bounded scope with known files and clear end state
- [ ] **S**mall: Single logical change (one PR, one concern)
- [ ] **T**estable: Technical Spec + Gherkin scenarios verifiable

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

### When Entering Drive Mode (TPgM)

Before driving, verify ALL tickets pass DoR. If any fail:

```
[TPgM] - ⛔ Cannot enter Drive Mode

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
| Technical Spec | Solutions Architect |
| Gherkin scenarios | Solutions Architect |
| Dependencies | Solutions Architect |
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

## Related References

- `ticket-templates.md` - Full ticket body templates
- `ticketing-core.md` - INVEST checklist details, workflow rules
