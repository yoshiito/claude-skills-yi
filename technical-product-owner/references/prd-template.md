# PRD Template

Collaborative Product Requirements Document. TPO is accountable for completion; domain experts contribute their sections.

**Prerequisite**: MRD must be approved before PRD elaboration begins.

```markdown
# PRD: [Feature Name]

**MRD Reference**: [Link to approved MRD]
**Status**: [Draft | In Review | Approved]

## Contributors

| Section | Contributor | Role | Status |
|---------|-------------|------|--------|
| Business Requirements | [name] | TPO | [Pending/Complete] |
| Technical Design | [name] | Solutions Architect | [Pending/Complete] |
| User Experience | [name] | UX Designer | [Pending/Complete] |
| Data Design | [name] | Data Platform Engineer | [Pending/Complete] |
| API Specification | [name] | API Designer | [Pending/Complete] |
| Test Strategy | [name] | Tester | [Pending/Complete] |
| Delivery Plan | [name] | TPgM | [Pending/Complete] |

*Add/remove contributors based on feature scope.*

---

## 1. Overview (from MRD)

*Copied from approved MRD for reference. Do not modify without MRD amendment.*

### 1.1 Problem Statement
[From MRD]

### 1.2 North Star Goal
[From MRD]

### 1.3 Success Metrics
[From MRD]

### 1.4 Scope
[From MRD]

---

## 2. Users and Personas
**Contributor: TPO**

### 2.1 Primary Users
| Persona | Role | Goals | Pain Points |
|---------|------|-------|-------------|
| [Name] | [Role] | [What they want] | [Current frustrations] |

### 2.2 User Journey Context
[Where does this feature fit in the user's workflow? What happens before/after?]

---

## 3. Business Requirements
**Contributor: TPO**

### 3.1 User Stories

[P0] AS A [role]
I WANT TO [action]
SO THAT [measurable benefit]
Acceptance Criteria: AC-001, AC-002

[P1] AS A [role]
I WANT TO [action]
SO THAT [measurable benefit]
Acceptance Criteria: AC-003

### 3.2 Business Rules

RULE-001: [Name]
Condition: [When this is true]
Constraint: [This must/must not happen]
Error: [ERR_CODE] - "[User message]"

### 3.3 Acceptance Criteria

AC-001: [Descriptive Name]

Scenario: [Specific scenario]
  Given [precondition]
  And [additional context]
  When [action]
  Then [outcome]
  And [additional outcome]

### 3.4 Edge Cases (Business Logic)

EDGE-001: [Name]
Trigger: [What causes this]
Expected Behavior: [What should happen]
Error Message: "[User-facing message]"

---

## 4. User Experience
**Contributor: UX Designer**

### 4.1 User Flows
[Diagrams or descriptions of user interactions]

### 4.2 Wireframes
[Links to wireframes or embedded images]

### 4.3 Empty States
| State | Context | Display | Action |
|-------|---------|---------|--------|
| [name] | [where] | [what shows] | [CTA] |

### 4.4 Error States
[How errors are presented to users]

---

## 5. Technical Design
**Contributor: Solutions Architect**

### 5.1 Architecture Overview
[System diagram, component interactions]

### 5.2 Integration Points
| System | Direction | Protocol | Purpose |
|--------|-----------|----------|---------|
| [system] | [in/out] | [REST/Event/etc] | [why] |

### 5.3 Non-Functional Requirements Solutions

NFR from MRD: [e.g., "sub-200ms response time"]
Solution: [e.g., "Redis caching layer + CDN for static assets"]

### 5.4 Security Design
[Authentication, authorization, data protection approach]

### 5.5 ADR References
- [Link to ADR-001: Technology choice]
- [Link to ADR-002: Integration pattern]

---

## 6. Data Design
**Contributor: Data Platform Engineer**

### 6.1 Data Model

ENTITY: [EntityName]

| Field | Type | Required | Constraints | PII | Notes |
|-------|------|----------|-------------|-----|-------|
| id | UUID | Yes | Primary key | No | Auto-generated |
| [field] | [type] | [Yes/No] | [constraints] | [Yes/No] | [notes] |

### 6.2 Indexes and Relationships
[Index strategy, foreign keys, cascade behavior]

### 6.3 Data Retention and Privacy
[Retention policy, PII handling, encryption requirements]

---

## 7. API Specification
**Contributor: API Designer**

### 7.1 Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/[resource] | Create [resource] |
| GET | /api/v1/[resource]/{id} | Get [resource] by ID |

### 7.2 Request/Response Contracts
[OpenAPI spec or detailed contracts]

### 7.3 Error Responses
| Code | HTTP | Message | When |
|------|------|---------|------|
| [ERR_X] | [4XX] | "[message]" | [condition] |

---

## 8. Test Strategy
**Contributor: Tester**

### 8.1 Test Approach
[Unit, integration, E2E, performance, security testing plan]

### 8.2 Coverage Requirements
| Type | Target | Tool |
|------|--------|------|
| Unit | >80% | [tool] |
| Integration | [scope] | [tool] |
| E2E | [critical paths] | [tool] |

### 8.3 Performance Test Plan
[Load testing approach for NFRs]

---

## 9. Dependencies and Delivery
**Contributor: TPgM**

### 9.1 Dependencies

| Dependency | Type | Owner | Status | Mitigation |
|------------|------|-------|--------|------------|
| [name] | [upstream/downstream/external] | [team] | [status] | [fallback] |

### 9.2 Milestones
| Milestone | Description | Dependencies |
|-----------|-------------|--------------|
| M1 | [description] | [what must complete first] |

### 9.3 Risks
| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| [risk] | [L/M/H] | [L/M/H] | [strategy] | [who] |

---

## 10. Definition of Done

### Code Complete
- [ ] All user stories implemented
- [ ] All business rules enforced
- [ ] All acceptance criteria passing

### Testing Complete
- [ ] Test strategy executed
- [ ] NFRs validated
- [ ] Security testing passed

### Documentation Complete
- [ ] API documentation published
- [ ] User docs updated
- [ ] Runbook created

### Approvals
- [ ] TPO sign-off
- [ ] SA sign-off (technical design)
- [ ] UX sign-off (if applicable)

---

## 11. Appendix

### 11.1 Glossary
| Term | Definition |
|------|------------|
| [term] | [definition] |

### 11.2 Related Documents
- [Link to MRD]
- [Link to ADRs]
- [Link to designs]

### 11.3 Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial draft |
```

## PRD Completion Checklist

TPO validates before marking PRD as approved:

- [ ] All required contributors have completed their sections
- [ ] No "Pending" status in Contributors table
- [ ] No TBD placeholders anywhere
- [ ] MRD reference is linked and approved
- [ ] All acceptance criteria are testable
- [ ] Technical design reviewed by SA
- [ ] Dependencies identified and owners assigned
