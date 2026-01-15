# Escalation Templates

Templates for blocker escalation, risk escalation, and decision requests.

## Blocker Escalation

### Blocker Report Format

```markdown
# 🚧 BLOCKER: [Title]

**ID**: BLOCKER-[XXX]
**Severity**: [P0 / P1 / P2 / P3]
**Project**: [Project name]
**Raised**: [Date]
**Raised By**: [Name]

## What's Blocked
[Specific work/task/feature that cannot proceed]

## Blocking Issue
[Clear description of the impediment]

## Root Cause
[Why this blocker exists - technical, resource, decision, external, etc.]

## Impact

**Immediate**:
- [What's stopped right now]

**Timeline**:
- Days blocked so far: [X]
- Projected delay if unresolved: [X] days/weeks

**Dependencies**:
- [Other work waiting on this]

## Resolution Options

**Option A**: [Description]
- Effort: [X days]
- Pros: [List]
- Cons: [List]

**Option B**: [Description]
- Effort: [X days]
- Pros: [List]
- Cons: [List]

**Option C**: Do nothing / Wait
- Pros: [List]
- Cons: [List]

## Recommendation
[Which option and why]

## Action Needed
- [ ] [Specific action] - Owner: [Name] - By: [Date]

## Escalation History
| Date | Escalated To | Response |
|------|--------------|----------|
| [Date] | [Name] | [Response/Action] |
```

### Severity-Specific Templates

#### P0 - Critical (Work Stopped)

```markdown
🚨 **P0 BLOCKER - IMMEDIATE ATTENTION REQUIRED**

**Issue**: [One-line summary]
**Project**: [Project]
**Impact**: [What's completely stopped]

**The Problem**:
[2-3 sentences max - be direct]

**Why P0**:
- Work is completely stopped
- No workaround exists
- [X] engineers blocked
- [X] days already lost

**We Need**:
[Specific ask - be concrete]

**Decision/Action Needed By**: [Time/Date - should be hours, not days]

**Contact**: [Name] - [Phone] - [Slack]
```

#### P1 - High (Work Degraded)

```markdown
⚠️ **P1 BLOCKER - Action Needed Within 24h**

**Issue**: [One-line summary]
**Project**: [Project]
**Impact**: [What's degraded/slowed]

**Situation**:
[Brief description]

**Current Workaround**:
[What we're doing to keep moving, and why it's not sustainable]

**Cost of Workaround**:
- [Extra effort/time]
- [Technical debt]
- [Other costs]

**Resolution Needed**:
[What we need to fully unblock]

**Timeline**: Need resolution by [Date] to avoid [consequence]
```

---

## Risk Escalation

### Risk Escalation Format

```markdown
# 🚨 RISK ESCALATION: [Title]

**Severity**: [Critical / High / Medium]
**Project**: [Project name]
**Date**: [Today]
**Escalated By**: [Name]
**Escalated To**: [Names/Roles]

## Situation
[What's happening - facts only, no blame]

## Risk
[What bad outcome might occur if not addressed]

## Probability
[High / Medium / Low] - [Why this probability]

## Impact If Realized

**Timeline**:
- [Effect on dates]

**Scope**:
- [Effect on deliverables]

**Resources**:
- [Effect on team/budget]

**External Commitments**:
- [Effect on customer/partner promises]

## Contributing Factors
- [Factor 1]
- [Factor 2]
- [Factor 3]

## Options

### Option 1: [Name]
**Description**: [What we would do]
**Pros**: 
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Cost/Effort**: [Estimate]

### Option 2: [Name]
**Description**: [What we would do]
**Pros**: 
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Cost/Effort**: [Estimate]

### Option 3: Accept Risk
**Description**: Continue current path, accept potential outcome
**Pros**: 
- No change required
- May not materialize
**Cons**:
- [Potential bad outcome]
**Contingency if risk materializes**: [What we'd do]

## Recommendation
[Which option and clear rationale]

## Decision Needed By
[Date] - [What happens if no decision by then]

## Supporting Information
- [Link to data/analysis]
- [Link to related documents]
```

### Timeline Slip Escalation

```markdown
# 📅 TIMELINE ESCALATION: [Project] Delay

**Project**: [Name]
**Original Target**: [Date]
**New Projection**: [Date]
**Slip**: [X weeks]
**Escalated To**: [Names]

## What Happened
[Brief, factual explanation of why timeline slipped]

## Contributing Factors
| Factor | Impact | Controllable |
|--------|--------|--------------|
| [Factor 1] | [X days] | [Yes/No] |
| [Factor 2] | [X days] | [Yes/No] |
| [Factor 3] | [X days] | [Yes/No] |

## Impact

**Internal**:
- [Other projects affected]
- [Team morale/burnout risk]

**External**:
- [Customer commitments]
- [Partner dependencies]
- [Marketing/Sales plans]

## Options to Recover

### Option A: Extend Timeline
- New target: [Date]
- Scope: Unchanged
- Risk: [External commitment impact]

### Option B: Reduce Scope
- Timeline: Original [Date]
- Cut: [Features to remove]
- Risk: [Product impact]

### Option C: Add Resources
- Timeline: [Date] (partial recovery)
- Add: [X engineers for Y weeks]
- Risk: [Ramp time, budget, coordination]

### Option D: Combination
- Timeline: [Date]
- Cut: [Limited scope reduction]
- Add: [Limited resource increase]

## Recommendation
[Option and rationale]

## Lessons Learned
[What we'll do differently - briefly]
```

---

## Decision Request

### Decision Request Format

```markdown
# 🔔 DECISION REQUIRED: [Title]

**Project**: [Name]
**Requested By**: [Name]
**Decision Makers**: [Names/Roles]
**Decision Needed By**: [Date]
**Urgency**: [Critical / High / Normal]

## Context
[Background information needed to make the decision]

## The Question
[Clear, specific question requiring a decision]

## Why This Matters
[Stakes - what's at risk, what's the opportunity]

## Why Now
[Why this decision is needed at this time]

## Options

### Option A: [Name]
**Description**: [What this option means]
**Pros**:
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Cost**: [Time/money/resources]
**Reversibility**: [Easy / Moderate / Difficult / Irreversible]

### Option B: [Name]
**Description**: [What this option means]
**Pros**:
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Cost**: [Time/money/resources]
**Reversibility**: [Easy / Moderate / Difficult / Irreversible]

### Option C: Defer Decision
**Description**: Wait for more information
**What we'd learn**: [Information we'd gain]
**Cost of waiting**: [What we lose by deferring]
**Defer until**: [Trigger/date for revisiting]

## Recommendation
**Recommended Option**: [A/B/C]
**Rationale**: [Clear reasoning]

## If No Decision By [Date]
[What happens - default action, continued uncertainty, etc.]

## Supporting Information
- [Link to analysis]
- [Link to related decisions]
```

### Quick Decision Request (Slack/Email)

```markdown
🔔 **Decision Needed**: [One-line question]

**Context**: [1-2 sentences]

**Options**:
A) [Option A - brief]
B) [Option B - brief]

**Recommendation**: [A or B] because [one sentence]

**Need answer by**: [Date/Time]

**Impact of delay**: [What happens if we don't decide]

Full analysis: [Link if applicable]
```

---

## Escalation Paths

### Standard Escalation Matrix

| Severity | First Escalation | Second Escalation | Final Escalation |
|----------|------------------|-------------------|------------------|
| P0 | Engineering Lead (immediately) | VP Engineering (1h) | CTO (2h) |
| P1 | Engineering Lead (4h) | VP Engineering (24h) | CTO (48h) |
| P2 | Engineering Lead (24h) | VP Engineering (1 week) | - |
| P3 | Sprint planning | Engineering Lead (2 weeks) | - |

### Escalation by Type

| Type | Primary Contact | Escalation Path |
|------|-----------------|-----------------|
| Technical blocker | Tech Lead | → Engineering Manager → VP Engineering |
| Resource constraint | TPgM | → Engineering Manager → VP Engineering |
| Scope/priority conflict | Product Owner | → Product Director → CPO |
| External dependency | TPgM | → Partnership/Vendor contact → VP |
| Budget/spend | TPgM | → Finance partner → CFO |
| Security concern | Security Lead | → CISO → CTO |
| Legal/compliance | Legal contact | → General Counsel → CEO |

### Escalation Communication Channels

| Urgency | Channel | Response Expectation |
|---------|---------|---------------------|
| P0 | Phone + Slack DM + Email | Minutes |
| P1 | Slack DM + Email | Hours |
| P2 | Slack channel + Email | Same day |
| P3 | Email + JIRA | This week |

### Escalation Etiquette

**Do**:
- State facts clearly
- Provide options with trade-offs
- Make a recommendation
- Specify deadline for decision
- Follow up in writing after verbal escalation

**Don't**:
- Assign blame
- Escalate without attempting resolution first
- Surprise people (give a heads-up when possible)
- Escalate the same issue repeatedly without new information
- Skip levels without reason
