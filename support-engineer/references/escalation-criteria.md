# Escalation Criteria and Procedures

Clear guidelines for when and how to escalate issues beyond standard support handling.

## Escalation Decision Framework

### When to Escalate Immediately

**Escalate without delay if ANY of these apply**:

| Condition | Reason |
|-----------|--------|
| Data integrity at risk | Potential data loss, corruption, or inconsistency |
| Security vulnerability | Potential unauthorized access, data exposure |
| System-wide outage | All users affected, core functionality unavailable |
| Payment/billing failure | Financial impact to users or business |
| Legal/compliance risk | GDPR, PCI-DSS, or other regulatory concerns |
| Cannot contain | Issue spreading or worsening |

### Severity Levels

| Severity | Definition | Response Time | Escalation |
|----------|------------|---------------|------------|
| **Critical** | System down, data loss risk, security breach | Immediate | Always escalate |
| **High** | Major feature broken, many users affected | < 4 hours | Escalate if not resolved quickly |
| **Medium** | Feature degraded, workaround exists | < 24 hours | Escalate if blocked |
| **Low** | Minor inconvenience, edge case | Next sprint | Track in backlog |

### Escalation Triggers by Category

#### Technical Escalation

**Escalate to Tech Lead / Senior Engineer when**:
- Root cause requires architectural knowledge
- Fix requires changes across multiple systems
- Issue involves unfamiliar codebase area
- Performance impact requires optimization expertise
- Database schema changes needed

#### Security Escalation

**Escalate to Security Team when**:
- Potential unauthorized data access
- Suspected credential compromise
- Vulnerability discovered in dependencies
- Unusual access patterns detected
- Compliance-related data exposure

#### Business Escalation

**Escalate to Product/Business when**:
- Decision needed on user-facing changes
- Customer communication required
- Feature behavior unclear (is it bug or intended?)
- Impact affects key accounts/revenue
- Workaround affects user experience significantly

## Escalation Procedures

### Step 1: Gather Information

Before escalating, document:

```markdown
## Escalation Summary

### Issue Description
[One-line summary]

### Impact
- Users affected: [number/scope]
- Duration: [how long has this been happening]
- Severity: [Critical/High/Medium/Low]

### Investigation So Far
- What was tried:
- What was ruled out:
- Current hypothesis:

### Why Escalating
[Specific reason - blocked, expertise needed, severity]

### Urgency
[Why this can't wait]
```

### Step 2: Choose Escalation Path

| If Issue Involves... | Escalate To |
|---------------------|-------------|
| Code/architecture | Tech Lead |
| Security | Security contact |
| Infrastructure | DevOps/SRE |
| Customer impact | Product Owner |
| Business decision | Business stakeholder |
| External service | Vendor support |

### Step 3: Communicate Clearly

**For synchronous escalation (Slack/call)**:
1. Lead with severity and impact
2. State what you need (decision, expertise, access)
3. Provide context link (ticket, Sentry issue)
4. Confirm acknowledgment

**For async escalation (ticket/email)**:
1. Use clear subject with severity
2. Include all gathered information
3. Specify response needed and timeline
4. Tag appropriate people

### Step 4: Track and Follow Up

- Create Linear ticket if not already tracked
- Link escalation to original issue
- Update status as escalation progresses
- Close loop when resolved

## Communication Templates

### Slack/Immediate Escalation

```
🔴 [CRITICAL/HIGH] Need immediate help

Issue: [One-line description]
Impact: [Who/what affected, since when]
Link: [Sentry/Linear link]

I've tried: [Brief summary]
Blocked because: [Why you need help]

Can someone from [team/role] assist?
```

### Linear Ticket Escalation

```markdown
## Summary
[Escalated] [Original issue title]

## Severity
[Critical/High/Medium/Low]

## Impact
- Affected: [users/features]
- Duration: [time]
- Business impact: [if known]

## Investigation Summary
[What was done, what was found]

## Escalation Reason
[Why escalating - blocked, expertise, severity]

## Needed From
[Who needs to act and what they need to do]

## Links
- Original issue: [link]
- Sentry: [link]
- Related: [links]
```

## Escalation Anti-Patterns

### Don't Do This

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Escalate without investigation | Wastes expert time | Do basic triage first |
| Vague escalation | "Something's broken" | Be specific about symptoms and impact |
| Wrong channel | Using email for critical issue | Match urgency to channel |
| No follow-up | Escalate and forget | Track to resolution |
| Over-escalate | Everything is "critical" | Reserve severity for true emergencies |
| Under-escalate | Hesitate on real emergencies | When in doubt, escalate up |

## Post-Escalation

### After Resolution

1. **Update original ticket** with resolution
2. **Thank escalation recipients** - acknowledge their help
3. **Document learnings** - what could have caught this earlier?
4. **Update runbooks** if needed
5. **Consider prevention** - monitoring, tests, process changes

### Escalation Review Questions

- Was escalation necessary? (Did we try enough first?)
- Was escalation timely? (Did we wait too long?)
- Was right person/team engaged?
- What can we do to handle similar issues without escalation?

## Quick Reference

### Escalation Checklist

- [ ] Issue documented with symptoms and impact
- [ ] Investigation summary prepared
- [ ] Root cause hypothesis (even if uncertain)
- [ ] Clear ask for escalation recipient
- [ ] Appropriate urgency/channel selected
- [ ] Ticket created/linked
- [ ] Acknowledgment received

### Severity Quick Guide

| If this is true... | Severity |
|--------------------|----------|
| Users can't use the product at all | Critical |
| Major feature broken, no workaround | High |
| Feature degraded, workaround exists | Medium |
| Edge case, minor impact | Low |

### Channel Selection

| Urgency | Channel |
|---------|---------|
| Need response in minutes | Phone/Slack call |
| Need response in hours | Slack DM/channel |
| Need response in 1-2 days | Linear ticket + mention |
| Can wait for next sprint | Linear ticket |
