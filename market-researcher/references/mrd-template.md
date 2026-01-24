# MRD Template

Market Requirements Document - focused exclusively on **What** and **Why**, backed by **current market research**.

**Critical**: MRD contains NO implementation details. No architecture, no data models, no UI designs, no API contracts. Those belong in the PRD, contributed by domain experts.

**Research Requirement**: All claims in the MRD should be backed by up-to-date market research using web search. Include source links for key data points.

```markdown
# MRD: [Feature Name]

## 1. Problem Statement

### What problem exists?
[Describe the problem in user/business terms. No technical framing.]
[Include market data/research that validates this problem exists]

### Who experiences this problem?
[Specific user roles or personas affected]
[Include data on market size/user segments if available]

### What is the impact?
[Quantify with market data: revenue loss, time wasted, user churn, etc.]
[Source: link to research/report]

### What happens if we don't solve this?
[Cost of inaction - business risk of leaving problem unsolved]
[Include competitive risk if competitors are addressing this]

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

## 5. Market Context

### Competitive Landscape
| Competitor | Offering | Strengths | Gaps |
|------------|----------|-----------|------|
| [Name] | [What they offer] | [Why users choose them] | [What's missing] |

[Source: competitor research links]

### Market Trends
- [Trend 1 affecting this space]
- [Trend 2]
[Source: industry report links]

### Why Now?
[What makes this urgent? Market pressure, competitor move, customer demand, etc.]
[Include specific timing factors from market research]

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

**Research Quality:**
- [ ] Used web search for up-to-date market data
- [ ] Multiple sources consulted (not single-source)
- [ ] Research is current (within last 6-12 months)
- [ ] Source URLs provided for key claims
- [ ] Competitive analysis covers major players

**Content Quality:**
- [ ] Problem is described in business/user terms only
- [ ] No technical solution prescribed
- [ ] Success metrics are measurable and market-informed
- [ ] Scope boundaries are clear
- [ ] "Why now" is compelling with market evidence
- [ ] Risks are business-level, not technical
- [ ] No TBD placeholders
- [ ] **No open questions** - all questions resolved before finalizing
