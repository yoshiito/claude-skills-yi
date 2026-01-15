# Delivery Plan Template

Complete structure for project/feature delivery plans.

```markdown
# Delivery Plan: [Project/Feature Name]

## Overview

**Project**: [Name]
**TPO/MRD**: [Link to MRD]
**TPgM**: [Owner name]
**Start Date**: [Date]
**Target Launch**: [Date]
**Status**: [🟢 On Track / 🟡 At Risk / 🔴 Off Track]

### Executive Summary
[2-3 sentences: what we're delivering, why it matters, key dates]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

---

## Scope

### In Scope
| Item | Description | Owner |
|------|-------------|-------|
| [Feature 1] | [Brief description] | [Team/Person] |
| [Feature 2] | [Brief description] | [Team/Person] |

### Out of Scope
| Item | Reason | Future Phase |
|------|--------|--------------|
| [Excluded 1] | [Why excluded] | [v2 / TBD / Never] |

### Scope Change Log
| Date | Change | Requested By | Approved By | Impact |
|------|--------|--------------|-------------|--------|
| [Date] | [Description] | [Name] | [Name] | [Timeline/effort impact] |

---

## Team

### Core Team
| Name | Role | Allocation | Responsibilities |
|------|------|------------|------------------|
| [Name] | TPgM | 50% | Delivery coordination, status reporting |
| [Name] | Tech Lead | 80% | Technical decisions, code review |
| [Name] | Backend Dev | 100% | API implementation |
| [Name] | Frontend Dev | 100% | UI implementation |
| [Name] | QA | 50% | Test planning, execution |

### Extended Team / Stakeholders
| Name | Role | Involvement |
|------|------|-------------|
| [Name] | Product Owner | Approvals, prioritization |
| [Name] | Design | UX consultation |
| [Name] | DevOps | Infrastructure, deployment |

### RACI Matrix
| Activity | TPgM | Tech Lead | Dev | QA | PO |
|----------|------|-----------|-----|----|----|
| Requirements | I | C | I | I | A/R |
| Architecture | I | A/R | C | I | I |
| Development | I | A | R | I | I |
| Testing | I | C | C | A/R | I |
| Deployment | A | R | C | C | I |
| Go/No-Go | R | C | I | C | A |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## Timeline

### Milestones
| Milestone | Target Date | Status | Exit Criteria |
|-----------|-------------|--------|---------------|
| M1: Kickoff | [Date] | 🔵 | Team aligned, plan approved |
| M2: Design Complete | [Date] | [Status] | Architecture doc, UI mocks approved |
| M3: Dev Complete | [Date] | [Status] | All features coded, unit tests pass |
| M4: QA Complete | [Date] | [Status] | All test cases pass, bugs resolved |
| M5: Release Ready | [Date] | [Status] | Readiness checklist complete |
| M6: Launch | [Date] | [Status] | Production deployment, monitoring green |

### Phase Breakdown

**Phase 1: Planning (Week 1-2)**
- [ ] Finalize requirements with TPO
- [ ] Complete architecture design
- [ ] Set up project infrastructure
- [ ] Create detailed task breakdown

**Phase 2: Development (Week 3-6)**
- [ ] Backend API implementation
- [ ] Frontend UI implementation
- [ ] Integration development
- [ ] Unit test coverage

**Phase 3: Testing (Week 7-8)**
- [ ] Integration testing
- [ ] E2E testing
- [ ] Performance testing
- [ ] Security testing
- [ ] Bug fixes

**Phase 4: Launch Prep (Week 9)**
- [ ] Documentation complete
- [ ] Runbook prepared
- [ ] Monitoring configured
- [ ] Rollback tested
- [ ] Go/no-go decision

**Phase 5: Launch (Week 10)**
- [ ] Production deployment
- [ ] Smoke testing
- [ ] Monitoring validation
- [ ] Stakeholder communication

### Gantt View
```
Week:        1    2    3    4    5    6    7    8    9    10
Planning:    ████████
Design:      ░░░░████████
Backend:              ████████████████████
Frontend:                  ████████████████████
Integration:                         ████████████
Testing:                                  ████████████
Launch Prep:                                        ████
Launch:                                                  ██
```

---

## Dependencies

### Internal Dependencies
| ID | Dependency | Owner | Needed By | Status | Impact if Late |
|----|------------|-------|-----------|--------|----------------|
| D1 | Auth service v2 | Platform | Week 3 | 🟢 | Block all API work |
| D2 | Design system components | Design | Week 2 | 🟡 | Delay frontend |
| D3 | Database migration | DBA | Week 4 | 🟢 | Block data features |

### External Dependencies
| ID | Dependency | Vendor | Needed By | Status | Mitigation |
|----|------------|--------|-----------|--------|------------|
| E1 | Stripe webhook setup | Stripe | Week 5 | 🟢 | Manual fallback |
| E2 | CDN configuration | Cloudflare | Week 8 | ⚪ | Use origin direct |

### Decision Dependencies
| ID | Decision | Owner | Needed By | Status | Options |
|----|----------|-------|-----------|--------|---------|
| X1 | Pricing tiers | Product | Week 2 | 🟡 | A: 3 tiers, B: Usage-based |
| X2 | Launch regions | Legal | Week 6 | ⚪ | US-only vs Global |

### Dependency Graph
```
[Auth Service v2] ──┐
                    ├──► [Backend API] ──┐
[DB Migration] ─────┘                    │
                                         ├──► [Integration] ──► [Launch]
[Design System] ──► [Frontend UI] ──────┘
                                         │
[Stripe Setup] ─────────────────────────┘
```

---

## Workstreams

### Workstream 1: Backend API
**Lead**: [Name]
**Status**: [🟢/🟡/🔴]

| Task | Assignee | Estimate | Status | Notes |
|------|----------|----------|--------|-------|
| User endpoints | [Name] | 3d | 🔵 | Complete |
| Project endpoints | [Name] | 5d | 🟢 | In progress |
| Auth integration | [Name] | 2d | ⚪ | Blocked on D1 |

### Workstream 2: Frontend UI
**Lead**: [Name]
**Status**: [🟢/🟡/🔴]

| Task | Assignee | Estimate | Status | Notes |
|------|----------|----------|--------|-------|
| Component library | [Name] | 3d | 🟢 | In progress |
| User flows | [Name] | 5d | ⚪ | Waiting on design |
| Integration | [Name] | 3d | ⚪ | After API ready |

### Workstream 3: Testing
**Lead**: [Name]
**Status**: [🟢/🟡/🔴]

| Task | Assignee | Estimate | Status | Notes |
|------|----------|----------|--------|-------|
| Test plan | [Name] | 2d | 🔵 | Complete |
| Test cases | [Name] | 3d | 🟢 | In progress |
| Automation | [Name] | 5d | ⚪ | After dev complete |

---

## Risks

| ID | Risk | Probability | Impact | Mitigation | Owner | Status |
|----|------|-------------|--------|------------|-------|--------|
| R1 | Auth service delayed | Medium | High | Parallel mock development | Tech Lead | Monitoring |
| R2 | Design iterations extend | Medium | Medium | Time-box design phase | TPgM | Mitigated |
| R3 | Performance targets missed | Low | High | Early load testing | QA Lead | Monitoring |
| R4 | Key developer unavailable | Low | High | Cross-train team | TPgM | Accepted |

---

## Communication Plan

### Regular Meetings
| Meeting | Frequency | Attendees | Purpose |
|---------|-----------|-----------|---------|
| Standup | Daily | Core team | Progress, blockers |
| Sprint Review | Bi-weekly | Team + stakeholders | Demo, feedback |
| Status Update | Weekly | Stakeholders | Progress report |
| Risk Review | Weekly | TPgM + Leads | Risk assessment |

### Status Reports
- **Audience**: [Stakeholder list]
- **Frequency**: Weekly (Fridays)
- **Format**: See status-update-templates.md

### Escalation Contacts
| Severity | Contact | Method |
|----------|---------|--------|
| P0 | [VP Engineering] | Slack DM + Phone |
| P1 | [Engineering Manager] | Slack DM |
| P2 | [Tech Lead] | Slack channel |

---

## Budget / Resources

### Infrastructure Costs
| Item | Monthly Cost | Notes |
|------|--------------|-------|
| Staging environment | $500 | 2 months |
| CI/CD runners | $200 | Ongoing |
| Third-party APIs | $100 | Stripe, etc. |

### Total Estimated Cost: $1,600

### Resource Constraints
- [Name] available only 50% (other project commitment)
- No additional headcount approved
- Design team bandwidth limited in Week 4

---

## Appendix

### Related Documents
- MRD: [link]
- Architecture Doc: [link]
- Design Specs: [link]
- Test Plan: [link]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial plan |
| 1.1 | [Date] | [Name] | Updated timeline |
```
