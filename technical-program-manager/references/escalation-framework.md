# Escalation Framework

Structured approach to identifying, documenting, and escalating blockers and risks.

---

## Blocker Identification

### What Constitutes a Blocker

A blocker is anything that:
- Prevents work from starting or continuing
- Cannot be resolved by the immediate team
- Will cause timeline slip if not resolved quickly
- Requires decision-making authority beyond the team

### Blocker vs. Impediment

| Type | Definition | Resolution |
|------|------------|------------|
| **Impediment** | Slows work but doesn't stop it | Team can work around it |
| **Blocker** | Stops work completely | Requires external resolution |

### Blocker Categories

| Category | Examples | Typical Resolver |
|----------|----------|------------------|
| **Resource** | Key person unavailable, capacity shortage | Manager, HR |
| **Technical** | Unexpected complexity, system limitation, bug in dependency | Tech Lead, Architect |
| **Dependency** | Upstream team delayed, API not ready, data unavailable | TPgM, upstream team |
| **Decision** | Waiting on stakeholder decision, unclear requirements | Product, Leadership |
| **Access** | Missing permissions, credentials, environments | IT, Security, DevOps |
| **External** | Vendor delay, third-party outage, contract pending | Vendor manager, Legal |
| **Process** | Approval bottleneck, compliance requirement | Process owner |

---

## Blocker Documentation

### Blocker Record Format

```
BLOCKER-[ID]: [Descriptive Title]
═══════════════════════════════════════════════════════════════

Created:     [Date]
Reporter:    @name
Status:      [New / Investigating / Escalated / Resolved]
Priority:    [P1-Critical / P2-High / P3-Medium / P4-Low]

────────────────────────────────────────────────────────────────
IMPACT
────────────────────────────────────────────────────────────────
What's Blocked:
- [Story/Task/Feature being blocked]
- [Additional items affected]

Timeline Impact:
- [X days/weeks delay if not resolved by Y date]

People Affected:
- [Team members who cannot proceed]

────────────────────────────────────────────────────────────────
DETAILS
────────────────────────────────────────────────────────────────
Description:
[Detailed explanation of the blocker]

Root Cause:
[Why this blocker exists]

Discovered:
[How/when the blocker was identified]

────────────────────────────────────────────────────────────────
RESOLUTION
────────────────────────────────────────────────────────────────
Owner:        @name (person who can resolve)
Resolver:     @name (person actively working on it)

Resolution Path:
1. [Step 1]
2. [Step 2]
3. [Step 3]

ETA:          [Expected resolution date]

Workaround:
[Temporary workaround if available, or "None"]

────────────────────────────────────────────────────────────────
ESCALATION
────────────────────────────────────────────────────────────────
Current Level: [L0-Team / L1-Lead / L2-Manager / L3-Director / L4-VP]
Escalated To:  @name
Escalated On:  [Date]
Reason:        [Why escalation was needed]

────────────────────────────────────────────────────────────────
HISTORY
────────────────────────────────────────────────────────────────
[Date] - [Update]
[Date] - [Update]
[Date] - [Update]
```

### Blocker Priority Definitions

| Priority | Definition | Response Time | Update Frequency |
|----------|------------|---------------|------------------|
| **P1 - Critical** | Complete work stoppage for multiple people/teams | 2 hours | Every 2 hours |
| **P2 - High** | Significant impact, critical path affected | 4 hours | Daily |
| **P3 - Medium** | Moderate impact, workaround available | 1 day | Every 2-3 days |
| **P4 - Low** | Minor impact, can defer without timeline risk | Best effort | Weekly |

---

## Escalation Levels

### Level Definitions

| Level | Who | When to Escalate | Authority |
|-------|-----|------------------|-----------|
| **L0 - Team** | Team members | Initial identification | Self-resolution |
| **L1 - Lead** | Tech Lead / Team Lead | Cannot resolve in 24h | Prioritize team work, reassign |
| **L2 - Manager** | Engineering Manager | 24-48h unresolved, cross-team | Resource allocation, cross-team coordination |
| **L3 - Director** | Director / Senior Manager | 48h+ or high business impact | Budget, scope changes, vendor decisions |
| **L4 - VP/Exec** | VP / C-level | Critical path blocked, strategic impact | Strategic decisions, major scope/timeline |

### Escalation Criteria

**Escalate from L0 → L1 when:**
- Cannot resolve within 24 hours
- Need help from outside immediate team
- Uncertainty about resolution approach
- Impact becoming clearer and significant

**Escalate from L1 → L2 when:**
- Lead cannot resolve within 24 hours
- Cross-team coordination needed
- Resource conflict exists
- Technical decision beyond team authority

**Escalate from L2 → L3 when:**
- Manager cannot resolve within 48 hours
- Budget or contract implications
- Scope change may be required
- Multiple teams affected
- Vendor escalation needed

**Escalate from L3 → L4 when:**
- Strategic impact to project/company
- Major timeline or scope decision
- Customer/partner impact
- Legal or compliance implications
- Director cannot resolve within reasonable time

---

## Escalation Process

### Step-by-Step

1. **Document** the blocker completely (use format above)
2. **Attempt resolution** at current level
3. **Determine if escalation needed** based on criteria
4. **Prepare escalation** with context and options
5. **Escalate** to appropriate person/level
6. **Track** escalation status
7. **Communicate** resolution back down

### Escalation Communication Format

```markdown
Subject: [ESCALATION L{X}] BLOCKER-{ID}: {Title}

## Escalation Summary

**Blocker**: BLOCKER-{ID} - {Title}
**Escalation Level**: L{X} → L{Y}
**Escalating From**: @name
**Escalating To**: @name
**Urgency**: [Immediate / Today / This Week]

## Situation

[2-3 sentences: What's blocked, what's the impact, what's been tried]

## Impact

- **Timeline**: [X days/weeks delay]
- **Scope**: [What cannot be delivered]
- **Teams Affected**: [List]
- **Revenue/Customer Impact**: [If applicable]

## What's Been Tried

1. [Action taken, result]
2. [Action taken, result]
3. [Action taken, result]

## Options

### Option 1: [Name]
- **Action**: [What needs to happen]
- **Owner**: [Who does it]
- **Timeline**: [How long]
- **Tradeoffs**: [Pros/cons]

### Option 2: [Name]
- **Action**: [What needs to happen]
- **Owner**: [Who does it]
- **Timeline**: [How long]
- **Tradeoffs**: [Pros/cons]

### Option 3: Do Nothing
- **Result**: [What happens if we don't act]

## Recommendation

[Recommended option and why]

## Decision Needed By

[Date/Time] - because [reason]

## Meeting Request

[If needed: Proposed time, attendees, or "Async decision acceptable"]
```

---

## Escalation Scenarios

### Resource Conflict

```markdown
Subject: [ESCALATION L2] Resource Conflict: @engineer needed by 2 projects

## Situation
@engineer is required for both Project Alpha (critical path) and Project Beta (committed deadline). Cannot parallelize - both need focused attention.

## Impact
- Project Alpha: 2 week delay without @engineer
- Project Beta: Miss Feb 15 customer commitment without @engineer

## Options

### Option 1: Prioritize Alpha
@engineer focuses on Alpha. Beta slips 1 week.
- **Alpha Impact**: On track
- **Beta Impact**: Slip to Feb 22, customer negotiation needed

### Option 2: Prioritize Beta
@engineer focuses on Beta. Alpha slips 2 weeks.
- **Alpha Impact**: Slip to Mar 1
- **Beta Impact**: Meet Feb 15 commitment

### Option 3: Split Time
@engineer splits 50/50.
- **Alpha Impact**: Slip 1 week
- **Beta Impact**: Slip 3-4 days, might still miss Feb 15

## Recommendation
Option 1 - Alpha is revenue-critical. Beta customer has been flexible before.

## Decision Needed By
Tomorrow EOD to allow Beta customer communication.
```

### Vendor Dependency

```markdown
Subject: [ESCALATION L3] Vendor Delay: Stripe SDK blocking EU launch

## Situation
Stripe promised SDK v10.0 by Jan 15 for 3D Secure 2.0 compliance. Now saying "late January" with no firm date. EU launch requires this for compliance.

## Impact
- EU launch delayed from Feb 1 to TBD
- Compliance deadline: Mar 1 (regulatory)
- Revenue impact: ~$200K/month EU revenue delayed

## What's Been Tried
1. Contacted Stripe account manager - no firm date
2. Technical team evaluated API-only approach - 3 weeks additional work
3. Legal reviewed compliance deadline - no flexibility

## Options

### Option 1: Wait for Stripe
- Wait for SDK, launch when ready
- Risk: Unknown timeline, may miss compliance deadline

### Option 2: Build API Integration
- 3 weeks engineering effort
- Guaranteed timeline, no Stripe dependency
- Technical debt: Maintain custom integration

### Option 3: Executive Escalation to Stripe
- Engage Stripe executive contact
- Request expedited SDK or temporary workaround
- May get commitment or alternatives

## Recommendation
Option 3 first (low cost), fallback to Option 2 if no resolution by Jan 20.

## Decision Needed By
Jan 17 - need to start API work by Jan 20 if going that route.
```

### Decision Blocker

```markdown
Subject: [ESCALATION L2] Decision Needed: Pricing model for enterprise tier

## Situation
Enterprise tier development blocked waiting on pricing model decision. Three stakeholders have different opinions, no consensus after 2 weeks of discussion.

## Impact
- Enterprise feature development blocked
- 3 engineers waiting (partial work on other tasks)
- Sales team cannot quote enterprise deals

## What's Been Tried
1. Meeting with Product, Sales, Finance - no consensus
2. Async decision doc - conflicting comments
3. Proposed compromise rejected by Finance

## Options

### Option 1: Force Decision Meeting
- Schedule 1-hour decision meeting with decision-maker authority
- Someone must leave with final answer

### Option 2: Launch with Simple Model
- Launch with simple per-seat pricing (lowest risk)
- Commit to revisit in 90 days with data

### Option 3: A/B Test Models
- Additional 2 weeks development
- Launch both models, let data decide

## Recommendation
Option 2 - unblock development, gather real data, revisit with evidence.

## Decision Needed By
Tomorrow - engineers being reassigned Friday if no decision.
```

---

## Escalation Tracking

### Escalation Dashboard

| ID | Title | Level | Owner | Status | Age | Next Action |
|----|-------|-------|-------|--------|-----|-------------|
| BLOCKER-001 | API dependency | L2 | @manager | Active | 3d | Meeting Fri |
| BLOCKER-002 | Vendor delay | L3 | @director | Active | 5d | Exec call Mon |
| BLOCKER-003 | Resource conflict | L2 | @manager | Resolved | 2d | - |

### Weekly Escalation Review

```markdown
# Escalation Review - Week of [Date]

## Active Escalations
| ID | Title | Level | Days Open | Trend |
|----|-------|-------|-----------|-------|
| BLOCKER-XXX | [Title] | L[X] | [N] | ↑↓→ |

## Resolved This Week
- BLOCKER-XXX: [Resolution summary]

## New Escalations
- BLOCKER-YYY: [Brief description]

## Escalation Metrics
- **Average Resolution Time**: [X] days
- **Escalations Opened**: [N]
- **Escalations Closed**: [N]
- **Currently Open**: [N]

## Patterns Observed
[Any recurring themes suggesting systemic issues]

## Action Items
- [Systemic fix needed]
```

---

## De-escalation

### When to De-escalate

- Blocker resolved
- Workaround found that removes urgency
- Impact reduced (no longer critical path)
- Decision made at higher level, execution at lower level

### De-escalation Communication

```markdown
Subject: [RESOLVED] BLOCKER-{ID}: {Title}

## Resolution Summary

**Blocker**: BLOCKER-{ID}
**Status**: Resolved
**Resolution Date**: [Date]
**Time to Resolution**: [X] days

## What Was Done
[How the blocker was resolved]

## Outcome
- [Impact on timeline]
- [Any remaining follow-up work]

## Lessons Learned
- [What we learned]
- [What we'd do differently]

## Thank You
Thanks to @person1, @person2 for help resolving this.
```
