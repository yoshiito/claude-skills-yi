# Systematic Troubleshooting Framework

A structured approach to root cause analysis that prevents jumping to conclusions and ensures thorough investigation.

## The RIVV Framework

**R**eproduce → **I**solate → **V**erify hypothesis → **V**alidate fix

### 1. Reproduce

**Goal**: Confirm the issue exists and understand the conditions that trigger it.

#### Questions to Answer
- Can you reproduce the issue consistently?
- What exact steps trigger it?
- Does it happen in all environments or specific ones?
- Does it affect all users or specific users/configurations?

#### Reproduction Checklist
- [ ] Gather exact reproduction steps from reporter
- [ ] Attempt reproduction in development environment
- [ ] If can't reproduce locally, try staging
- [ ] Document exact conditions (user, data, timing)
- [ ] Note any intermittent behavior

#### When You Can't Reproduce
- Timing-dependent (race condition)
- Data-dependent (specific user data)
- Environment-dependent (production config)
- Load-dependent (only under stress)

**Actions**:
- Review logs from when it occurred
- Check for differences between environments
- Add more logging for next occurrence
- Set up monitoring/alerts

### 2. Isolate

**Goal**: Narrow down which component/layer is causing the problem.

#### Layer-by-Layer Investigation

```
User Interface (Frontend)
         ↓
    API Gateway
         ↓
  Application Logic
         ↓
    Database/Cache
         ↓
 External Services
```

**For each layer, ask**:
- Does data look correct entering this layer?
- Does data look correct leaving this layer?
- If not, the problem is in this layer

#### Isolation Techniques

| Technique | When to Use |
|-----------|-------------|
| Binary search | Large codebase, narrow by halves |
| Component bypass | Replace component to see if issue persists |
| Input validation | Check data at each boundary |
| Logging injection | Add temporary logging at suspected points |
| Time correlation | Match timestamps across systems |

#### Common Isolation Questions

**Frontend issues**:
- Does the API return correct data? (Check Network tab)
- Is rendering logic handling data correctly?
- Is state management working as expected?

**API issues**:
- Is the request being received correctly?
- Is business logic executing properly?
- Is the database returning expected data?

**Database issues**:
- Is the query correct?
- Is the data in expected state?
- Are indexes being used?

**External service issues**:
- Is the service reachable?
- Is the request formatted correctly?
- Is the response being parsed correctly?

### 3. Verify Hypothesis

**Goal**: Confirm your suspected root cause before implementing a fix.

#### Forming Hypotheses

Based on isolation, form specific hypotheses:
- ❌ "Something is wrong with the database" (too vague)
- ✅ "The query is missing a WHERE clause, returning all rows instead of filtered results"

#### Testing Hypotheses

| Method | Description |
|--------|-------------|
| Code review | Read the suspected code path |
| Logging | Add logging to confirm execution path |
| Debugger | Step through code |
| Data inspection | Query database directly |
| Unit test | Write failing test that proves the bug |

#### Hypothesis Validation Checklist
- [ ] Hypothesis explains all observed symptoms
- [ ] Hypothesis explains why it only happens under certain conditions
- [ ] You can predict behavior based on hypothesis
- [ ] Code review confirms hypothesis

#### Multiple Causes

Sometimes there are multiple contributing factors:
1. Primary cause (what's broken)
2. Contributing factors (why it wasn't caught)
3. Triggering condition (why it happened now)

Example:
- **Primary**: Missing null check
- **Contributing**: No unit test for edge case
- **Trigger**: New user signup with empty optional field

### 4. Validate Fix

**Goal**: Confirm the fix works and doesn't introduce new problems.

#### Fix Validation Checklist
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Original reproduction case now passes
- [ ] Related edge cases tested
- [ ] No regression in existing functionality
- [ ] Fix deployed to test environment first
- [ ] Monitoring confirms issue is resolved

#### After Deployment
- Monitor error rates for 24-48 hours
- Check Sentry for recurrence
- Confirm with original reporter

## Root Cause Categories

### Code Bugs

| Type | Example | Detection |
|------|---------|-----------|
| Logic error | Off-by-one, wrong operator | Code review, unit tests |
| Null/undefined | Missing null check | Stack trace, type checking |
| Type mismatch | String vs number comparison | Stack trace, TypeScript |
| Race condition | Concurrent modification | Intermittent failures |
| Memory leak | Growing memory usage | Monitoring, profiling |

### Configuration Issues

| Type | Example | Detection |
|------|---------|-----------|
| Missing config | Environment variable not set | Startup errors |
| Wrong value | Pointing to wrong database | Data inconsistencies |
| Secret rotation | Expired API key | Auth failures |
| Feature flag | Flag not enabled for environment | Feature not working |

### Data Issues

| Type | Example | Detection |
|------|---------|-----------|
| Invalid data | Malformed email, negative price | Validation errors |
| Missing data | Required field null | Query failures |
| Stale data | Cache not invalidated | Inconsistent results |
| Migration gap | Old data doesn't match new schema | Format errors |

### External Dependencies

| Type | Example | Detection |
|------|---------|-----------|
| Service down | Third-party API unavailable | Connection errors |
| Rate limited | Too many requests | 429 responses |
| API change | Breaking change in response format | Parse errors |
| Network | DNS, firewall, timeout | Connection timeouts |

### Resource Exhaustion

| Type | Example | Detection |
|------|---------|-----------|
| Memory | Out of memory | OOM errors |
| Disk | No space left | Write failures |
| Connections | Pool exhausted | Connection timeouts |
| CPU | 100% utilization | Slow responses |

## Troubleshooting Anti-Patterns

### Avoid These

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Guessing | Random changes without evidence | Follow RIVV framework |
| Shotgun debugging | Change many things at once | Change one thing at a time |
| Blame shifting | "It's not my code" | Focus on facts, not ownership |
| Premature optimization | Fix performance before root cause | Fix correctness first |
| Magic fixes | "Restart fixed it" | Understand why restart helped |

### Red Flags

- "It works on my machine" → Environment difference
- "It just started happening" → Recent change (deploy, data, config)
- "It's intermittent" → Race condition, resource, or external dependency
- "Only some users affected" → Data-dependent, A/B test, feature flag

## Documentation Template

After resolving an issue, document:

```markdown
## Issue: [Brief description]

### Symptoms
- What users experienced
- Error messages observed

### Root Cause
[Specific technical explanation]

### Investigation Path
1. [First thing checked]
2. [What it revealed]
3. [How root cause was identified]

### Resolution
- [Fix applied]
- [PR/commit reference]

### Prevention
- [How to prevent recurrence]
- [Tests added]
- [Monitoring added]
```

## Quick Reference: Common Issues

| Symptom | First Check |
|---------|-------------|
| 500 errors | Server logs, stack traces |
| Slow response | Database queries, external calls |
| Intermittent failures | Race conditions, resource limits |
| Wrong data displayed | API response, data transformation |
| Feature not working | Feature flags, permissions |
| Auth failures | Token expiration, secret rotation |
| Cannot connect | Network, DNS, firewall, service status |
