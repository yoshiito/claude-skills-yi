# Linear MCP Workflow

Integration patterns for using Linear MCP server in delivery management.

## Linear MCP Tools Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `create_issue` | Create new issue | New tasks, bugs, features |
| `update_issue` | Modify existing issue | Status changes, assignments |
| `get_issue` | Fetch issue details | Checking current state |
| `search_issues` | Find issues | Discovery, reporting |
| `list_issues` | List issues in project | Status overview |
| `create_comment` | Add comment to issue | Updates, discussions |

## Pre-Flight Checklist

**Before creating ANY issues in Linear, verify:**

### Requirements Phase
```
□ TPO has produced MRD
□ MRD has been reviewed and approved
□ User stories have acceptance criteria
□ Edge cases are documented
□ NFRs are defined with thresholds
```

### Architecture Phase
```
□ Solutions Architect has reviewed requirements
□ ADRs are written for key decisions
□ System diagrams are current
□ API contracts are defined (if applicable)
□ Data flow is documented
```

### Implementation Planning
```
□ Backend Developer has reviewed and estimated backend work
□ Frontend Developer has reviewed and estimated frontend work
□ Data Platform Engineer has reviewed data requirements (if applicable)
□ AI Integration Engineer has reviewed AI requirements (if applicable)
□ MCP Server Developer has reviewed MCP requirements (if applicable)
```

### Test Planning
```
□ Backend Tester has outlined test strategy for APIs
□ Frontend Tester has outlined test strategy for UI
□ Performance test approach defined
□ Security review planned
```

### Documentation Planning
```
□ Tech Doc Writer has identified documentation needs
□ API documentation planned
□ User documentation planned
□ Runbook/operational docs planned
```

## Issue Creation Workflow

### Step 1: Create Project/Epic

```
Linear Action: create_issue (type: Project or Epic)

Title: [Feature Name]
Description: Link to MRD, high-level scope
Labels: Epic, [Team]
```

### Step 2: Create Workstream Issues

For each workstream identified in planning:

**Backend Issues:**
```
Title: [API] [Feature] - [Specific Task]
Description:
- Requirements: Link to MRD section
- Architecture: Link to ADR
- Acceptance Criteria: From MRD
Labels: Backend, [Priority]
Parent: [Epic ID]
```

**Frontend Issues:**
```
Title: [UI] [Feature] - [Specific Task]
Description:
- Requirements: Link to MRD section
- Designs: Link to Figma/designs
- Components: Atomic level (Atom/Molecule/Organism)
Labels: Frontend, [Priority]
Parent: [Epic ID]
```

**Data Issues:**
```
Title: [Data] [Feature] - [Specific Task]
Description:
- Schema changes
- Migration requirements
- Data dependencies
Labels: Data, [Priority]
Parent: [Epic ID]
```

**Test Issues:**
```
Title: [Test] [Feature] - [Test Type]
Description:
- Test strategy link
- Coverage requirements
Labels: Testing, [Priority]
Parent: [Epic ID]
Blocked By: [Implementation issues]
```

**Documentation Issues:**
```
Title: [Docs] [Feature] - [Doc Type]
Description:
- Documentation requirements
- Audience
Labels: Documentation, [Priority]
Parent: [Epic ID]
```

### Step 3: Link Dependencies

```
Linear Action: update_issue

Add "Blocked By" relationships:
- Frontend blocked by Backend API
- Tests blocked by Implementation
- Docs blocked by Feature completion
- Release blocked by all above
```

### Step 4: Assign and Prioritize

```
Linear Action: update_issue

Assign owners based on skill area:
- Backend tasks → Backend Developer
- Frontend tasks → Frontend Developer
- Data tasks → Data Platform Engineer
- Test tasks → Testers
- Docs → Tech Doc Writer
```

## Status Tracking

### Status Mapping

| Linear Status | TPgM Indicator | Meaning |
|---------------|----------------|---------|
| Backlog | ⚪ Not Started | Not yet begun |
| Todo | ⚪ Not Started | Ready to start |
| In Progress | 🟢 On Track | Work ongoing |
| In Review | 🟢 On Track | PR/Review stage |
| Blocked | 🔴 Blocked | Impediment exists |
| Done | 🔵 Complete | Finished |
| Canceled | ⬛ Canceled | Not proceeding |

### Daily Standup Query

```
Search: project:[Project] AND status:["In Progress", "Blocked", "In Review"]
Sort: priority, updated

Check:
- What moved to "In Progress"?
- What's been "In Review" > 2 days?
- What's "Blocked"? (Escalate immediately)
```

### Weekly Status Query

```
Search: project:[Project]
Group by: status

Report:
- Completed this week (moved to Done)
- In flight (In Progress, In Review)
- At risk (Blocked, or no updates > 3 days)
- Not started (Backlog, Todo)
```

## Blocker Management

### Creating Blocker Issues

```
Linear Action: create_issue

Title: [BLOCKED] [Issue Title]
Description:
- Blocked Issue: Link to blocked issue
- Blocker: What's preventing progress
- Impact: What can't proceed
- Proposed Resolution: How to unblock
Labels: Blocked, [Priority P0-P3]
```

### Escalation via Linear

For P0/P1 blockers:

```
Linear Action: create_comment on blocker issue

Comment:
🚨 ESCALATION

Severity: P0/P1
Impact: [What's affected]
Escalated to: @[Leadership]
Decision needed by: [Date]

Options:
1. [Option A]
2. [Option B]

Recommendation: [Preferred option]
```

## Release Checklist Integration

### Pre-Release Query

```
Search: project:[Project] AND label:["Release Blocker"] AND status:NOT["Done"]
```

If any results, release is NOT ready.

### Release Readiness Issue

Create a release checklist issue:

```
Title: [Release] v[X.X.X] Readiness Checklist
Description:
## Code Complete
- [ ] All feature issues Done
- [ ] No critical bugs open
- [ ] Code reviews approved

## Testing Complete
- [ ] All test issues Done
- [ ] Coverage meets threshold
- [ ] No P0/P1 bugs open

## Documentation Complete
- [ ] All doc issues Done
- [ ] API docs current
- [ ] Runbook ready

## Operations Ready
- [ ] Monitoring configured
- [ ] Rollback tested
- [ ] On-call briefed

## Approvals
- [ ] TPO sign-off
- [ ] Engineering sign-off
- [ ] Security sign-off (if applicable)

Labels: Release, [Version]
```

## Best Practices

### Issue Hygiene

1. **Update status daily** - Don't let issues go stale
2. **Link dependencies** - Make blockers explicit
3. **Use labels consistently** - Enable accurate reporting
4. **Add context in comments** - Don't just change status

### Avoiding Common Mistakes

**Don't:**
- Create issues before requirements are clear
- Skip the pre-flight checklist
- Leave blocked issues without escalation
- Let issues sit in "In Review" > 3 days

**Do:**
- Get sign-off from relevant skills first
- Link issues to MRD/ADR documentation
- Update issues as work progresses
- Escalate blockers immediately

### Reporting

**For Stakeholders:**
- Use Linear's project views
- Export weekly status from queries
- Include completion % and risks

**For Engineering:**
- Daily: Blocked issues, PRs needing review
- Weekly: Velocity, upcoming work
- Sprint: Planned vs delivered
