# MRD Template

Complete structure for Master Requirement Documents.

```markdown
# MRD: [Feature Name]

## 1. Overview

### 1.1 Problem Statement
[What problem exists? Who experiences it? What's the cost of not solving it?]

### 1.2 North Star Goal
[Single sentence: the one outcome this feature must achieve]

### 1.3 Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [metric] | [baseline] | [goal] | [how measured] |

### 1.4 Scope

#### In Scope
- [Capability 1]
- [Capability 2]

#### Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

---

## 2. Users and Personas

### 2.1 Primary Users
| Persona | Role | Goals | Pain Points |
|---------|------|-------|-------------|
| [Name] | [Role] | [What they want] | [Current frustrations] |

### 2.2 Secondary Users
[Users who interact with feature indirectly]

### 2.3 User Journey Context
[Where does this feature fit in the user's workflow? What happens before/after?]

---

## 3. Requirements

### 3.1 User Stories

[P0] AS A [role]
I WANT TO [action]
SO THAT [measurable benefit]
Acceptance Criteria: AC-001, AC-002

[P1] AS A [role]
I WANT TO [action]
SO THAT [measurable benefit]
Acceptance Criteria: AC-003

### 3.2 Functional Rules

RULE-001: [Name]
Condition: [When this is true]
Constraint: [This must/must not happen]
Enforcement: [Frontend/Backend/Both]
Error: [ERR_CODE] - "[User message]"

RULE-002: [Name]
Condition: [When this is true]
Constraint: [This must/must not happen]
Enforcement: [Frontend/Backend/Both]
Error: [ERR_CODE] - "[User message]"

### 3.3 Acceptance Criteria

AC-001: [Descriptive Name]

Scenario: [Specific scenario]
  Given [precondition]
  And [additional context]
  When [action]
  Then [outcome]
  And [additional outcome]

AC-002: [Descriptive Name]

Scenario: [Specific scenario]
  Given [precondition]
  When [action]
  Then [outcome]

### 3.4 Data Requirements

ENTITY: [EntityName]

| Field | Type | Required | Constraints | PII | Notes |
|-------|------|----------|-------------|-----|-------|
| id | UUID | Yes | Primary key | No | Auto-generated |
| [field] | [type] | [Yes/No] | [constraints] | [Yes/No] | [notes] |

INDEXES:
- [field] (unique/non-unique)
- [field, field] (composite)

RELATIONSHIPS:
- [field] -> [other_table.field] (CASCADE/SET NULL/RESTRICT)

RETENTION:
- [Retention policy description]

SECURITY:
- PII fields: [list]
- Encryption: [requirements]
- Audit logging: [requirements]

### 3.5 Non-Functional Requirements

NFR-PERF-001: API Response Time
- p50: < [X]ms
- p95: < [X]ms
- p99: < [X]ms

NFR-SCALE-001: Concurrent Users
- Normal load: [X] users
- Peak load: [X] users
- Degradation threshold: [X] users

NFR-A11Y-001: Accessibility
- Level: WCAG 2.1 [A/AA/AAA]
- Screen reader: [requirement]
- Keyboard: [requirement]
- Color contrast: [ratio]

NFR-SEC-001: Security
- Session timeout: [duration]
- Rate limiting: [threshold]
- [Other requirements]

---

## 4. Edge Cases and Error Handling

### 4.1 Unhappy Paths

UNHAPPY-001: [Name]
Trigger: [What causes this]
User Impact: [What user experiences]
System Behavior: [What system does]
Recovery Path: [How user recovers]
Error Code: [ERR_CODE]
Error Message: "[User-facing message]"

### 4.2 Empty States

EMPTY-001: [Name]
Context: [Where this appears]
Condition: [When shown]
Display: [What UI shows]
Action: [CTA or guidance]

### 4.3 Extreme States

EXTREME-001: [Name]
Scenario: [The extreme condition]
Expected Volume: [Numbers]
System Behavior: [How handled]
Degradation Strategy: [What's sacrificed]

### 4.4 Error Messages

| Code | HTTP | User Message | Internal Log | Retry |
|------|------|--------------|--------------|-------|
| [ERR_X] | [4XX] | "[message]" | "[log detail]" | [Yes/No] |

---

## 5. Dependencies

### 5.1 Upstream Dependencies

DEP-UP-001: [Name]
Type: [Service/Data/Feature/Infrastructure]
Owner: [Team]
Status: [Available/In Progress/Blocked]
Required By: [Date]
Fallback: [If unavailable]

### 5.2 Downstream Dependencies

DEP-DOWN-001: [Name]
Dependent Feature: [What needs this]
Integration Point: [API/Event/Data]
Timeline Impact: [Effect of delays]

### 5.3 External Dependencies

DEP-EXT-001: [Name]
Vendor: [Company/Service]
Purpose: [Why needed]
SLA: [Availability]
Fallback: [If unavailable]
Cost: [Pricing model]

### 5.4 Dependency Risk Assessment

| Dependency | Probability | Impact | Mitigation |
|------------|-------------|--------|------------|
| [name] | [L/M/H] | [L/M/H/Critical] | [strategy] |

---

## 6. Definition of Done

### Code Complete
- [ ] All user stories implemented
- [ ] All functional rules enforced
- [ ] All acceptance criteria passing
- [ ] Edge cases handled per specification

### Testing Complete
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Performance tests meet NFRs
- [ ] Security testing (OWASP top 10)
- [ ] Accessibility testing (WCAG)

### Documentation Complete
- [ ] API documentation (OpenAPI)
- [ ] User-facing docs updated
- [ ] Runbook for operations

### Review Complete
- [ ] Code review approved
- [ ] Security review (if required)
- [ ] UX review approved
- [ ] Product Owner sign-off

### Deployment Ready
- [ ] Feature flag configured
- [ ] Monitoring/alerting configured
- [ ] Rollback plan documented
- [ ] Database migrations tested

---

## 7. Risk Register

| ID | Risk | Prob | Impact | Mitigation | Owner | Status |
|----|------|------|--------|------------|-------|--------|
| R1 | [risk] | [L/M/H] | [L/M/H/C] | [strategy] | [who] | [status] |

---

## 8. Open Questions

| ID | Question | Owner | Due Date | Resolution |
|----|----------|-------|----------|------------|
| Q1 | [question] | [who] | [date] | [answer when resolved] |

---

## 9. Appendix

### 9.1 Glossary
| Term | Definition |
|------|------------|
| [term] | [definition] |

### 9.2 Related Documents
- [Link to design doc]
- [Link to architecture doc]
- [Link to prior art]

### 9.3 Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial draft |
```
