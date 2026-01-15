# Status Update Templates

Templates for different audiences and communication needs.

## Status Indicators

Use consistently across all communications:

```
🟢 On Track - Proceeding as planned, no concerns
🟡 At Risk - Issues identified, mitigation in progress, needs attention
🔴 Off Track - Timeline/scope impacted, requires escalation/decision
⚪ Not Started - Work has not begun
🔵 Complete - Finished and validated
⏸️ Paused - Intentionally on hold
🚫 Blocked - Cannot proceed, waiting on dependency
```

---

## Executive Summary (Leadership)

**Audience**: VP+, C-suite
**Frequency**: Weekly
**Length**: <1 page
**Focus**: Milestones, risks, decisions needed

```markdown
# [Project Name] - Executive Status
**Week of**: [Date]
**Overall Status**: [🟢/🟡/🔴]

## Summary
[2-3 sentences: Where we are, key progress, main concern if any]

## Milestones
| Milestone | Target | Status |
|-----------|--------|--------|
| [M1] | [Date] | [🔵/🟢/🟡/🔴] |
| [M2] | [Date] | [🔵/🟢/🟡/🔴] |
| [M3] | [Date] | [🔵/🟢/🟡/🔴] |

## Key Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [H/M/L] | [Action] |

## Decisions Needed
- [ ] [Decision 1] - Needed by [Date]

## Next Week
- [Key activity 1]
- [Key activity 2]
```

---

## Stakeholder Status Report

**Audience**: Product, Design, Business stakeholders
**Frequency**: Weekly
**Length**: 1-2 pages
**Focus**: Progress, timeline, blockers, upcoming work

```markdown
# [Project Name] - Weekly Status
**Report Date**: [Date]
**Prepared By**: [TPgM Name]
**Overall Status**: [🟢/🟡/🔴]

## This Week's Highlights
- ✅ [Accomplishment 1]
- ✅ [Accomplishment 2]
- ✅ [Accomplishment 3]

## Progress by Workstream

### Backend [🟢/🟡/🔴]
- Completed: [items]
- In Progress: [items]
- Blocked: [items if any]

### Frontend [🟢/🟡/🔴]
- Completed: [items]
- In Progress: [items]
- Blocked: [items if any]

### Testing [🟢/🟡/🔴]
- Completed: [items]
- In Progress: [items]
- Blocked: [items if any]

## Timeline Update

**Original Target**: [Date]
**Current Projection**: [Date]
**Variance**: [None / +X days / -X days]

| Milestone | Original | Current | Status |
|-----------|----------|---------|--------|
| [M1] | [Date] | [Date] | [Status] |
| [M2] | [Date] | [Date] | [Status] |

## Blockers & Risks

### Active Blockers
| Blocker | Impact | Owner | ETA |
|---------|--------|-------|-----|
| [Blocker 1] | [Impact] | [Name] | [Date] |

### Risks Being Monitored
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Action] |

## Dependencies Update
| Dependency | Owner | Status | Notes |
|------------|-------|--------|-------|
| [Dep 1] | [Team] | [Status] | [Notes] |

## Next Week's Plan
- [ ] [Planned item 1]
- [ ] [Planned item 2]
- [ ] [Planned item 3]

## Needs / Asks
- [Request 1 - from whom]
- [Request 2 - from whom]

## Questions / Discussion Items
- [Topic needing discussion]
```

---

## Engineering Team Update

**Audience**: Development team, Tech leads
**Frequency**: Daily standup + weekly summary
**Length**: Brief
**Focus**: Tasks, blockers, coordination

### Daily Standup Format

```markdown
## Standup - [Date]

### [Name 1]
**Yesterday**: [What was done]
**Today**: [What's planned]
**Blockers**: [None / Description]

### [Name 2]
**Yesterday**: [What was done]
**Today**: [What's planned]
**Blockers**: [None / Description]

---
**Team Blockers**: [Summary of blockers needing attention]
**Coordination Needed**: [Any sync requirements]
```

### Weekly Engineering Summary

```markdown
# [Project] - Engineering Weekly
**Week of**: [Date]

## Velocity
- Story Points Committed: [X]
- Story Points Completed: [Y]
- Completion Rate: [Y/X]%

## Completed This Week
- [PR #123] - [Description]
- [PR #124] - [Description]
- [PR #125] - [Description]

## In Progress
| Item | Assignee | Status | ETA |
|------|----------|--------|-----|
| [Task 1] | [Name] | [X]% | [Date] |
| [Task 2] | [Name] | [X]% | [Date] |

## Technical Debt / Issues
- [Issue 1] - [Priority]
- [Issue 2] - [Priority]

## Blockers
| Blocker | Owner | Escalated To | ETA |
|---------|-------|--------------|-----|
| [Blocker] | [Name] | [Name] | [Date] |

## Next Week Focus
- [Priority 1]
- [Priority 2]

## Risks to Flag
- [Risk requiring attention]
```

---

## Cross-Functional Update

**Audience**: Other teams with dependencies
**Frequency**: As needed (dependency changes, coordination required)
**Length**: Targeted, specific
**Focus**: What they need to know, what you need from them

```markdown
# [Project] Update for [Team Name]

**Date**: [Date]
**From**: [Your name], [Project] TPgM
**Re**: [Specific topic - dependency, coordination, etc.]

## Context
[1-2 sentences: Why you're reaching out]

## What's Changed
[Specific update relevant to this team]

## Impact on You
[How this affects their work/timeline]

## What We Need
- [ ] [Specific ask 1] - by [Date]
- [ ] [Specific ask 2] - by [Date]

## What We're Providing
- [What you'll deliver to them]
- [Timeline for your deliverable]

## Questions?
Contact: [Name] via [Slack/email]
```

---

## Sprint Report

**Audience**: Product Owner, Stakeholders
**Frequency**: End of each sprint
**Length**: 1-2 pages
**Focus**: What was delivered, what wasn't, why, next sprint

```markdown
# Sprint [X] Report - [Project Name]
**Sprint Dates**: [Start] - [End]
**Sprint Goal**: [What we aimed to achieve]
**Goal Met**: [Yes / Partially / No]

## Delivered This Sprint
| Item | Story Points | Demo Link |
|------|--------------|-----------|
| [Feature 1] | [X] | [Link] |
| [Feature 2] | [X] | [Link] |
| [Bug fix 1] | [X] | - |

**Total Points Delivered**: [X] / [Y] committed ([Z]%)

## Not Completed (Carried Over)
| Item | Reason | New Target |
|------|--------|------------|
| [Item 1] | [Why not done] | Sprint [X+1] |
| [Item 2] | [Why not done] | Sprint [X+1] |

## Sprint Metrics
- **Velocity**: [X] points (avg: [Y])
- **Bugs Found**: [X] (Critical: [Y], High: [Z])
- **Bugs Fixed**: [X]
- **Tech Debt Items**: [X] addressed

## Blockers Encountered
| Blocker | Duration | Resolution |
|---------|----------|------------|
| [Blocker 1] | [X] days | [How resolved] |

## Retrospective Summary
**What went well**:
- [Item 1]
- [Item 2]

**What to improve**:
- [Item 1] - Action: [Who will do what]
- [Item 2] - Action: [Who will do what]

## Next Sprint Plan
**Sprint [X+1] Goal**: [Goal statement]

| Item | Points | Owner |
|------|--------|-------|
| [Item 1] | [X] | [Name] |
| [Item 2] | [X] | [Name] |

**Total Committed**: [X] points

## Release Burndown
[If tracking toward release]
- Remaining work: [X] points
- Sprints remaining: [Y]
- Required velocity: [X/Y] points/sprint
- Current velocity: [Z] points/sprint
- Projection: [On track / At risk / Off track]
```

---

## Change Communication

**Audience**: All affected parties
**Frequency**: When significant changes occur
**Focus**: What changed, why, impact, next steps

```markdown
# [Project] - Important Update

**Date**: [Date]
**From**: [TPgM Name]
**Severity**: [🟡 Schedule Change / 🔴 Scope Change / 🔴 Launch Delay]

## What's Changing
[Clear statement of the change]

## Why
[Brief explanation - be honest but professional]

## Impact

**Timeline**:
- Previous target: [Date]
- New target: [Date]
- Delay: [X weeks]

**Scope** (if applicable):
- Removed: [Items cut]
- Deferred: [Items moved to future]
- Added: [Items added, if any]

**Resources** (if applicable):
- [Resource changes]

## What This Means For You

**[Team/Role 1]**:
- [Specific impact]
- [Action needed]

**[Team/Role 2]**:
- [Specific impact]
- [Action needed]

## Mitigation
[What we're doing to minimize impact]

## Next Steps
1. [Action 1] - [Owner] - [Date]
2. [Action 2] - [Owner] - [Date]

## Questions
Please direct questions to [Name] via [channel].

Updated delivery plan: [Link]
```
