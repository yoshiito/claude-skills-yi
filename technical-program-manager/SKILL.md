---
name: technical-program-manager
description: Technical Program Manager for cross-functional engineering delivery. Use when planning sprints or releases, tracking dependencies across features or teams, assessing release readiness, managing blockers and escalations, coordinating stakeholder communication, or ensuring documentation completeness before launch. Complements the TPO role - TPO defines what to build, TPgM ensures it gets delivered. Produces delivery plans, readiness checklists, status updates, and risk escalations. Integrates with Linear MCP for issue tracking.
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

## Linear MCP Integration

**CRITICAL**: Use the Linear MCP server for all issue tracking and project management.

### When to Use Linear

| Action | Linear MCP Tool |
|--------|-----------------|
| Create epic/project | `create_issue` with parent project |
| Create tasks | `create_issue` for each workstream item |
| Track progress | `update_issue` to change status |
| Log blockers | `create_issue` with "Blocked" label |
| Search issues | `search_issues` to find related work |
| Get status | `get_issue` for current state |

### Linear Workflow

```
1. Create Project in Linear (epic-level)
2. Create issues for each workstream
3. Link dependencies between issues
4. Update status as work progresses
5. Use labels for tracking (P0, P1, Blocked, At-Risk)
```

### Before Creating Issues in Linear

**STOP** - Consult Plan Registry and Integration Catalog first:

```
1. Read docs/plans/_registry.json
   - Is this plan registered? (if not, TPO must create it first)
   - Is the plan status "approved"? (don't create tickets for drafts)
   - What are the dependencies on other plans?

2. Read docs/integrations/_catalog.json
   - What integrations does this feature use?
   - Are any integrations deprecated? (may need migration work)
   - Are API versions current?
```

**Then** ensure all relevant skills have provided input:

1. **TPO Sign-off** - Are requirements complete? (MRD approved, in registry)
2. **Solutions Architect Sign-off** - Is architecture defined? (ADRs written, integrations cataloged)
3. **Data Platform Engineer** - Data dependencies identified? (if applicable)
4. **Developer Input** - Effort estimates provided?
5. **Tester Input** - Test strategy defined?

**Pre-Flight Checklist**:
```
□ Plan exists in docs/plans/_registry.json with status "approved"
□ MRD from TPO is complete and approved
□ Architecture from Solutions Architect is documented
□ Required integrations are in docs/integrations/_catalog.json
□ Data requirements from Data Platform Engineer are clear (if applicable)
□ Backend Developer has reviewed feasibility
□ Frontend Developer has reviewed feasibility
□ Test strategy is outlined
□ Documentation needs identified (Tech Doc Writer)
```

Only create Linear issues after this checklist passes.

## Relationship to Other Roles

| Role | Responsibility | TPgM Interaction | Consult Before |
|------|----------------|------------------|----------------|
| **TPO** | Defines requirements | TPgM sequences delivery of TPO's MRDs | Creating any issues |
| **Solutions Architect** | Designs technical approach | TPgM tracks architecture decisions as dependencies | Technical breakdown |
| **Backend Developer** | Implements APIs | TPgM tracks backend progress | Backend estimates |
| **Frontend Developer** | Implements UI | TPgM tracks frontend progress | Frontend estimates |
| **Backend Tester** | Validates API quality | TPgM gates on test completion | Test strategy |
| **Frontend Tester** | Validates UI quality | TPgM gates on test completion | Test strategy |
| **Data Platform Engineer** | Data infrastructure | TPgM tracks data dependencies | Data-related work |
| **Tech Doc Writer** | Documentation | TPgM ensures docs complete | Release readiness |
| **UX Designer** | User experience | TPgM tracks design dependencies | UI/UX work |

### Cross-Skill Consultation Triggers

**Before creating Linear issues, consult if:**

| Trigger | Consult Skill |
|---------|---------------|
| New feature request | TPO (for MRD) |
| Technical complexity unclear | Solutions Architect (for ADR) |
| Database changes needed | Data Platform Engineer |
| New API endpoints | Backend Developer + Backend Tester |
| New UI components | Frontend Developer + Frontend Tester + UX Designer |
| Documentation needs | Tech Doc Writer |
| AI/ML features | AI Integration Engineer |
| MCP server needed | MCP Server Developer |

## Scope Boundaries

**CRITICAL**: TPgM coordinates across all domains but does NOT define work for domains. Scope ownership is project-specific.

### Pre-Action Checklist

```
1. Check if project's claude.md has "Project Scope" section
   → If NOT defined: Prompt user to set up scope (see below)
   → If defined: Continue to step 2

2. Read project scope definition in project's claude.md
3. Identify domain owners for each workstream
4. Before creating any issue:
   → Has the domain owner defined this work? → Proceed to create/track
   → Is this undefined work? → Route to domain owner first
```

### If Project Scope Is Not Defined

Prompt the user:

```
I notice this project doesn't have scope boundaries defined in claude.md yet.

Before I coordinate delivery or track work, I need to understand:

1. **What domains/workstreams exist?** (Frontend, Backend, Data, etc.)
2. **Who owns each domain?** (e.g., "SA owns architecture, Dev Team owns implementation")
3. **Linear context?** (Which Team/Project for tracking?)

Would you like me to help set up a Project Scope section in claude.md?
```

After user responds, update `claude.md` with scope, then proceed.

### What TPgM CAN Do Across All Domains

- Track progress and status of all workstreams
- Identify blockers and dependencies
- Facilitate communication between domain owners
- Escalate risks and timeline concerns
- Coordinate cross-domain meetings
- Maintain delivery plans and readiness checklists

### What TPgM CANNOT Do Outside Coordination Scope

- Create implementation issues without domain owner definition
- Define technical approach or architecture
- Assign work to teams without domain owner input
- Make scope decisions (what's in/out)
- Define acceptance criteria for features

### TPgM Boundary Examples

```
✅ WITHIN TPgM SCOPE:
- "Frontend sub-issue LIN-101 is blocked by Backend LIN-100"
- "Backend team estimates 3 days for API endpoint"
- "Escalating: Data pipeline dependency at risk"
- "Release checklist: Code complete ✅, Tests ✅, Docs pending"

❌ OUTSIDE TPgM SCOPE:
- "Frontend should use React Query for state management"
- Creating [Backend] sub-issue without SA definition
- "Let's skip the caching layer to save time"
- Defining what API endpoints are needed
```

### Cross-Domain Gap Handling

When you identify missing work definition:

```markdown
## Work Definition Gap

**Identified By**: TPgM
**Domain**: [Backend/Frontend/Data/etc.]
**Project**: [Project Name]

### Gap Description
[What work appears to be missing from the plan]

### Impact on Delivery
[Timeline risk, dependency blocked, etc.]

### Requested Action
Domain owner [Name/Role] to define:
1. [What needs to be defined]
2. [Scope and acceptance criteria]

### Urgency
[When this blocks other work]
```

See `_shared/references/scope-boundaries.md` for the complete framework.

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

## Registry Updates (TPgM Responsibility)

TPgM is responsible for updating registry statuses during delivery:

### Plan Registry Updates

| Trigger | Update |
|---------|--------|
| Work starts on plan | Update status to `in_progress`, add `linear_project_id` |
| Plan delivered | Update status to `completed`, add `completed_date` |

```python
# When starting work
registry["plans"][idx]["status"] = "in_progress"
registry["plans"][idx]["linear_project_id"] = "proj_xxx"

# When completing
registry["plans"][idx]["status"] = "completed"
registry["plans"][idx]["completed_date"] = "2024-03-15"
```

### Integration Catalog Updates

| Trigger | Update |
|---------|--------|
| New integration goes live | Update status `planned` → `active` |
| Integration issues found | Flag for SA review |

See `_shared/references/plan-registry-schema.md` and `_shared/references/integration-catalog-schema.md` for full schemas.

## Reference Files

- `references/delivery-plan-template.md` - Full delivery plan structure
- `references/status-update-templates.md` - Templates by audience
- `references/release-checklist.md` - Comprehensive readiness gates
- `references/escalation-framework.md` - Blocker and risk escalation formats
- `references/linear-workflow.md` - Linear MCP integration patterns
- `_shared/references/plan-registry-schema.md` - Plan Registry schema (TPO owns, TPgM updates status)
- `_shared/references/integration-catalog-schema.md` - Integration Catalog schema (SA owns)

## Related Skills

The TPgM coordinates with these skills throughout the delivery lifecycle:

| Phase | Skills to Engage |
|-------|------------------|
| **Planning** | TPO, Solutions Architect |
| **Breakdown** | Backend Developer, Frontend Developer, Data Platform Engineer |
| **Estimation** | All developers, Testers |
| **Execution** | All implementation skills |
| **Testing** | Backend Tester, Frontend Tester |
| **Documentation** | Tech Doc Writer, Solutions Architect |
| **Release** | All skills for sign-off |

### Skill Ecosystem

```
                    ┌─────────────────┐
                    │       TPO       │
                    │  (Requirements) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Solutions    │
                    │    Architect    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────────┐ ┌───▼───┐ ┌───────▼───────┐
     │    Backend      │ │ Data  │ │   Frontend    │
     │    Developer    │ │Platform│ │   Developer   │
     └────────┬────────┘ └───┬───┘ └───────┬───────┘
              │              │              │
     ┌────────▼────────┐     │     ┌───────▼───────┐
     │ Backend Tester  │     │     │Frontend Tester│
     └────────┬────────┘     │     └───────┬───────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Tech Doc      │
                    │   Writer        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │      TPgM       │◄──── Linear MCP
                    │   (Delivery)    │      (Issue Tracking)
                    └─────────────────┘
```

## Linear Ticket Traceability Verification

**CRITICAL**: Before closing any parent Issue, verify code-to-ticket traceability.

### Hierarchy Model

```
Initiative (Company Objective)
└── Project (Deliverable/Feature Set)
     └── Issue (Parent - Feature/Story) ← TPO creates
          └── Sub-Issue (Task - Implementation Unit) ← Solutions Architect creates
```

### Traceability Verification Checklist

Before marking a parent Issue as Done:

**Sub-Issue Completion**:
- [ ] All sub-issues are in "Done" status
- [ ] Each sub-issue has completion comment with PR link
- [ ] No orphaned sub-issues (all linked to parent)

**Commit Traceability**:
- [ ] All commits reference `[LIN-XXX]` in message
- [ ] PR titles include ticket references
- [ ] Branch names follow `feature/LIN-XXX-description` pattern

**Progress Documentation**:
- [ ] Each sub-issue has start comment
- [ ] Each sub-issue has completion comment
- [ ] Test coverage documented in comments
- [ ] Implementation decisions noted

### Verification Commands

```python
# Get parent Issue with all sub-issues
parent = mcp.get_issue(id="LIN-XXX", includeRelations=True)

# List all sub-issues
sub_issues = mcp.list_issues(parentId="LIN-XXX")

# Check comments on each sub-issue
for sub in sub_issues:
    comments = mcp.list_comments(issueId=sub.id)
    # Verify start and completion comments exist
```

### Parent Issue Status Update

When all sub-issues are verified:

```python
mcp.create_comment(
    issueId="LIN-XXX",  # Parent Issue
    body="""## Delivery Status - COMPLETE

### Sub-issue Status
| Issue | Assignee | Status | PR |
|-------|----------|--------|-----|
| LIN-101 [Backend] | @backend-dev | ✅ Done | PR #45 |
| LIN-102 [Frontend] | @frontend-dev | ✅ Done | PR #47 |
| LIN-103 [Docs] | @tech-writer | ✅ Done | PR #48 |

### Traceability Verified
- ✅ All commits reference tickets
- ✅ All PRs linked
- ✅ Test coverage documented
- ✅ All sub-issues have completion comments

### Ready for Release
Feature verified and ready for deployment.
"""
)

# Update parent to Done (auto-closes when all sub-issues done)
mcp.update_issue(id="LIN-XXX", state="Done")
```

See `_shared/references/linear-ticket-traceability.md` for full workflow details.

## Summary

The TPgM ensures features move from "defined" to "shipped" by:
- **Consulting all relevant skills** before creating Linear issues
- Planning delivery with clear milestones and dependencies
- Tracking progress in Linear and surfacing blockers early
- Validating readiness before launch
- Communicating status to the right audience
- Escalating risks before they become crises

**Remember**: Before pushing any work to Linear, ensure voices from all relevant roles have been heard. This prevents rework and ensures alignment.

A good TPgM makes delivery predictable and keeps surprises to a minimum.
