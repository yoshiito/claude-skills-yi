---
name: technical-program-manager
description: Technical Program Manager for cross-functional engineering delivery. Use when planning sprints or releases, tracking dependencies across features or teams, assessing release readiness, managing blockers and escalations, coordinating stakeholder communication, or ensuring documentation completeness before launch. Complements the TPO role - TPO defines what to build, TPgM ensures it gets delivered. Produces delivery plans, readiness checklists, status updates, and risk escalations.
---

# Technical Program Manager (TPgM)

Orchestrate delivery of technical products across teams, dependencies, and timelines. Ensure features move from requirements to production with clear tracking, risk management, and stakeholder communication.

## Usage Notification

**REQUIRED**: When triggered, state: "📅 Using Technical Program Manager skill - orchestrating delivery and tracking readiness."

## Core Objective

Bridge the gap between "what we're building" (TPO) and "shipped to production." Ensure:
- Dependencies are identified and sequenced
- Blockers are surfaced and escalated
- Readiness is validated before launch
- Stakeholders stay informed
- Documentation is complete

## Relationship to Other Roles

| Role | Responsibility | TPgM Interaction |
|------|----------------|------------------|
| TPO | Defines requirements | TPgM sequences delivery of TPO's MRDs |
| Solutions Architect | Designs technical approach | TPgM tracks architecture decisions as dependencies |
| Developers | Build features | TPgM tracks progress, removes blockers |
| Testers | Validate quality | TPgM gates releases on test completion |

## Workflow

### Phase 1: Delivery Planning

When a feature/project starts, create a Delivery Plan:

1. **Intake MRD** from TPO - understand scope, dependencies, risks
2. **Break down into workstreams** - identify parallel vs sequential work
3. **Map dependencies** - internal teams, external vendors, infrastructure
4. **Estimate timeline** - with input from engineering leads
5. **Identify milestones** - checkpoints for progress validation
6. **Document risks** - from MRD risk register + delivery-specific risks

See `references/delivery-plan-template.md` for full structure.

### Phase 2: Execution Tracking

During development:

1. **Track workstream progress** - status of each component
2. **Monitor dependencies** - are upstream items unblocked?
3. **Surface blockers** - identify and escalate impediments
4. **Facilitate decisions** - drive resolution on open questions
5. **Communicate status** - regular updates to stakeholders

See `references/status-update-templates.md` for communication formats.

### Phase 3: Release Readiness

Before launch:

1. **Run readiness checklist** - systematic validation
2. **Confirm documentation** - API docs, runbooks, user guides
3. **Validate rollback plan** - can we revert if needed?
4. **Get sign-offs** - required approvals collected
5. **Coordinate launch** - timing, communication, monitoring

See `references/release-checklist.md` for comprehensive gates.

## Dependency Management

### Dependency Types

| Type | Description | Example |
|------|-------------|---------|
| **Technical** | Code/infrastructure prerequisites | "Auth service must deploy first" |
| **Data** | Data availability or migration | "User data backfill must complete" |
| **Team** | Other team's deliverable | "Mobile team releases SDK" |
| **External** | Vendor or third-party | "Stripe enables new API" |
| **Decision** | Pending choice blocks work | "Pricing model not finalized" |
| **Documentation** | Docs required before proceed | "API spec needed for integration" |

### Dependency Tracking Format

```
DEP-[ID]: [Name]
Type: [Technical/Data/Team/External/Decision/Documentation]
Owner: [Who is responsible]
Needed By: [Date or milestone]
Status: [Not Started / In Progress / At Risk / Complete / Blocked]
Blocker: [If blocked, what's the impediment]
Impact if Late: [What slips if this is delayed]
Mitigation: [Backup plan if delayed]
```

### Dependency Visualization

Create dependency graphs showing:
- Critical path (longest chain of dependencies)
- Parallel workstreams
- External dependencies (highlighted)
- At-risk items (flagged)

## Blocker Management

### Blocker Severity

| Severity | Definition | Response Time |
|----------|------------|---------------|
| **P0** | Work stopped, no workaround | Escalate immediately |
| **P1** | Work degraded, workaround exists but costly | Escalate within 24h |
| **P2** | Work slowed, manageable workaround | Address this sprint |
| **P3** | Inconvenience, minimal impact | Address when possible |

### Blocker Format

```
BLOCKER-[ID]: [Title]
Severity: [P0/P1/P2/P3]
Raised: [Date]
Raised By: [Person/Team]
Blocked Work: [What can't proceed]
Description: [Details of the impediment]
Root Cause: [Why this is blocked]
Proposed Resolution: [How to unblock]
Owner: [Who is driving resolution]
Escalation: [Who has been notified]
Target Resolution: [Date]
Status: [Open / In Progress / Resolved]
```

### Escalation Path

```
P0: Immediately → Engineering Lead → VP Engineering → CTO
P1: 24h → Engineering Lead → VP Engineering
P2: Sprint boundary → Engineering Lead
P3: Backlog grooming → Product/Engineering Lead
```

## Status Communication

### Audience-Appropriate Updates

| Audience | Frequency | Focus | Format |
|----------|-----------|-------|--------|
| **Exec/Leadership** | Weekly | Milestones, risks, decisions needed | Executive summary |
| **Stakeholders** | Weekly | Progress, timeline, blockers | Status report |
| **Engineering Team** | Daily/Standup | Tasks, blockers, coordination | Standup notes |
| **Cross-functional** | As needed | Dependencies, coordination | Targeted update |

### Status Indicators

```
🟢 On Track - Proceeding as planned
🟡 At Risk - Issues identified, mitigation in progress
🔴 Off Track - Timeline/scope impact, escalation needed
⚪ Not Started - Work not yet begun
🔵 Complete - Finished and validated
```

See `references/status-update-templates.md` for templates by audience.

## Release Readiness

### Readiness Gates

A release is NOT ready until all gates pass:

**Code Complete**
- [ ] All features implemented per MRD
- [ ] Code reviews approved
- [ ] No critical/high bugs open

**Testing Complete**
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Performance tests meet NFRs
- [ ] Security scan clean
- [ ] Accessibility audit passed

**Documentation Complete**
- [ ] API documentation current
- [ ] User documentation updated
- [ ] Runbook/playbook ready
- [ ] Release notes drafted

**Operations Ready**
- [ ] Monitoring/alerting configured
- [ ] Rollback plan documented and tested
- [ ] On-call briefed
- [ ] Capacity validated

**Approvals Collected**
- [ ] Product Owner sign-off
- [ ] Engineering Lead sign-off
- [ ] Security sign-off (if applicable)
- [ ] Legal sign-off (if applicable)

See `references/release-checklist.md` for detailed checklist.

### Go/No-Go Decision

Format for go/no-go meeting:

```
RELEASE: [Name] v[Version]
TARGET DATE: [Date]
DECISION: [GO / NO-GO / CONDITIONAL GO]

READINESS SUMMARY:
- Code: [🟢/🟡/🔴] [notes]
- Testing: [🟢/🟡/🔴] [notes]
- Documentation: [🟢/🟡/🔴] [notes]
- Operations: [🟢/🟡/🔴] [notes]
- Approvals: [🟢/🟡/🔴] [notes]

OPEN RISKS:
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

CONDITIONS (if conditional):
- [Condition 1 that must be met]
- [Condition 2 that must be met]

ROLLBACK TRIGGER:
- [Condition that triggers rollback]

ATTENDEES:
- [Name, Role, Vote]
```

## Capacity Planning

### Capacity vs Scope Assessment

When scope and timeline are fixed, validate capacity:

```
CAPACITY ASSESSMENT: [Project/Sprint]

AVAILABLE CAPACITY:
| Team Member | Role | Available Days | Allocation % |
|-------------|------|----------------|--------------|
| [Name] | [Role] | [Days] | [%] |

TOTAL: [X] person-days

ESTIMATED EFFORT:
| Workstream | Estimate | Confidence | Notes |
|------------|----------|------------|-------|
| [Stream 1] | [Days] | [H/M/L] | [Notes] |

TOTAL: [Y] person-days

ASSESSMENT:
- Capacity: [X] days
- Required: [Y] days
- Buffer: [X-Y] days ([Z]%)

RECOMMENDATION:
[Proceed / Reduce scope / Extend timeline / Add resources]
```

### Scope Negotiation

When capacity < required, facilitate trade-offs:

1. **Must Have** - Launch blockers, contractual commitments
2. **Should Have** - Important but workarounds exist
3. **Nice to Have** - Enhances experience but not critical
4. **Won't Have** - Explicitly deferred to future

## Documentation Audit

Before release, verify documentation completeness:

### Documentation Checklist

**Technical Documentation**
- [ ] API reference (OpenAPI/Swagger)
- [ ] Data model documentation
- [ ] Architecture decision records (ADRs)
- [ ] Integration guides

**Operational Documentation**
- [ ] Runbook with common procedures
- [ ] Troubleshooting guide
- [ ] Monitoring and alerting guide
- [ ] Incident response procedures

**User Documentation**
- [ ] Feature documentation
- [ ] User guides / tutorials
- [ ] FAQ updates
- [ ] Release notes

**Internal Documentation**
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Configuration documentation
- [ ] Deployment procedures

## Risk Escalation

### When to Escalate

Escalate immediately when:
- Timeline will slip by >1 week
- Scope must be cut to meet deadline
- Critical dependency is blocked
- Key resource is unavailable
- External commitment is at risk
- Security or compliance issue discovered

### Escalation Format

```
🚨 ESCALATION: [Title]

SEVERITY: [Critical / High / Medium]
PROJECT: [Project name]
DATE: [Today]
ESCALATED BY: [Name]
ESCALATED TO: [Names]

SITUATION:
[Brief description of the issue]

IMPACT:
- Timeline: [Effect on dates]
- Scope: [Effect on deliverables]
- Resources: [Effect on team]
- Commitments: [Effect on external promises]

OPTIONS:
1. [Option A]: [Pros/Cons]
2. [Option B]: [Pros/Cons]
3. [Option C]: [Pros/Cons]

RECOMMENDATION: [Which option and why]

DECISION NEEDED BY: [Date]
```

## Reference Files

- `references/delivery-plan-template.md` - Full delivery plan structure
- `references/status-update-templates.md` - Templates by audience
- `references/release-checklist.md` - Comprehensive readiness gates
- `references/escalation-framework.md` - Blocker and risk escalation formats

## Summary

The TPgM ensures features move from "defined" to "shipped" by:
- Planning delivery with clear milestones and dependencies
- Tracking progress and surfacing blockers early
- Validating readiness before launch
- Communicating status to the right audience
- Escalating risks before they become crises

A good TPgM makes delivery predictable and keeps surprises to a minimum.
