# MRD Template

Market Requirements Document - focused exclusively on **What** and **Why**.

**Critical**: MRD contains NO implementation details. No architecture, no data models, no UI designs, no API contracts. Those belong in the PRD, contributed by domain experts.

```markdown
# MRD: [Feature Name]

## 1. Problem Statement

### What problem exists?
[Describe the problem in user/business terms. No technical framing.]

### Who experiences this problem?
[Specific user roles or personas affected]

### What is the impact?
[Quantify if possible: revenue loss, time wasted, user churn, support tickets, etc.]

### What happens if we don't solve this?
[Cost of inaction - business risk of leaving problem unsolved]

---

## 2. Target Users

### Primary Users
| Persona | Role | Current Pain |
|---------|------|--------------|
| [Name] | [Role] | [What frustrates them today] |

### User Goals
[What do these users want to accomplish? Focus on outcomes, not features.]

---

## 3. Success Metrics

### North Star
[Single most important outcome this feature must achieve]

### Measurable Targets
| Metric | Current Baseline | Target | How Measured |
|--------|------------------|--------|--------------|
| [metric] | [current] | [goal] | [measurement method] |

### Leading Indicators
[Early signals that we're on track]

---

## 4. Scope

### In Scope
- [Capability 1 - what the system will do]
- [Capability 2]

### Out of Scope
- [Explicitly excluded 1 - and why]
- [Explicitly excluded 2 - and why]

### Future Considerations
[Things we might do later, but not now. Not a commitment.]

---

## 5. Business Context

### Why Now?
[What makes this urgent? Market pressure, competitor move, customer demand, etc.]

### Business Constraints
- [Constraint 1: e.g., must launch before Q2]
- [Constraint 2: e.g., budget limit of $X]

### Dependencies (Business Level)
[Other initiatives, teams, or decisions this depends on - NOT technical dependencies]

---

## 6. Risks

### Business Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk] | [L/M/H] | [L/M/H] | [what we'll do] |

### Open Questions
[Questions that must be answered before MRD approval - NOT technical questions]

---

## 7. Approval

| Role | Name | Date | Decision |
|------|------|------|----------|
| Product Lead | | | Approved / Rejected |
| Stakeholder | | | Approved / Rejected |

**Approval means:** Scope is agreed, problem is validated, we proceed to PRD elaboration.
```

## What Does NOT Belong in MRD

- Technical architecture or system design
- Database schemas or data models
- API endpoints or contracts
- UI wireframes or mockups
- Implementation estimates or timelines
- Test strategies
- Deployment plans

These all belong in the **PRD**, contributed by the appropriate domain experts after MRD approval.

## MRD Quality Checklist

Before seeking approval:

- [ ] Problem is described in business/user terms only
- [ ] No technical solution prescribed
- [ ] Success metrics are measurable
- [ ] Scope boundaries are clear
- [ ] "Why now" is compelling
- [ ] Risks are business-level, not technical
- [ ] No TBD placeholders
