# Ticket Templates

Standard templates for creating well-structured tickets. These templates ensure consistency and completeness across different ticket types.

**MANDATORY**: All sub-issues MUST use these templates. Solutions Architect creates tickets, TPO reviews, TPgM validates.

## Story/Task Template

Use this template for implementation sub-issues created by Solutions Architect.

```markdown
## Assigned Role
[Skill/role that should complete this work - e.g., Backend Developer, Frontend Developer, Tech Doc Writer]

## Description
[Clear, concise description of what needs to be implemented]

## Context
- Parent Issue: [TICKET-ID - Parent feature name]
- ADR: [Link to architecture decision record if applicable]
- API Spec: [Link to OpenAPI spec if applicable]
- Design: [Link to Figma/design if applicable]

## Acceptance Criteria
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

## NFRs (Non-Functional Requirements)
[Performance, security, accessibility requirements, or "N/A" if none]

## Implementation Notes
[Technical guidance, patterns to follow, code references]

## Infrastructure Notes
[Database changes, environment variables, deployment considerations, or "N/A" if none]

## Testing
[Test scenarios to cover, edge cases to validate]

## Additional Notes
[Any other relevant information]
```

### Example: Story/Task

```markdown
## Assigned Role
Backend Developer

## Description
Backend API to retrieve pricing information for AMC+ from App Store/Play Store price points.

## Context
- Parent Issue: LIN-456 - AMC+ Pricing Display Feature
- ADR: /docs/adr/005-pricing-api-design.md
- API Spec: /docs/api/pricing.yaml

## Acceptance Criteria
- [ ] GET /api/v1/pricing/{platform} returns price points for iOS/Android
- [ ] Response includes currency, amount, and billing period
- [ ] Caches price data for 1 hour to reduce external API calls
- [ ] Returns 404 for unsupported platforms

## NFRs
- Response time < 200ms (p95)
- Cache hit rate > 80%

## Implementation Notes
- Use existing `ExternalPricingClient` for App Store/Play Store APIs
- Follow repository pattern in `app/repositories/`
- Price amounts should be stored as integers (cents)

## Infrastructure Notes
- Add `PRICING_CACHE_TTL` environment variable
- Redis cache key prefix: `pricing:`

## Testing
- Happy path: Valid platform returns prices
- Cache hit: Second request uses cached data
- Invalid platform: Returns 404
- External API timeout: Returns cached data or 503

## Additional Notes
- Price points may vary by region - initial implementation is US-only
```

### Assigned Role Values

| Role | When to Assign |
|------|----------------|
| Backend Developer | API endpoints, services, database operations |
| Frontend Developer | UI components, pages, client-side logic |
| Tech Doc Writer | API documentation, guides, runbooks |
| Backend Tester | Dedicated backend test coverage |
| Frontend Tester | Dedicated frontend/E2E test coverage |
| Data Platform Engineer | Data pipelines, migrations, analytics |
| API Designer | API contract design (before implementation) |

## Bug Template

Use this template for bug reports.

```markdown
## Environment/Platform
[e.g., iOS 17.2, Android 14, Web Chrome 120, Production/Staging]

## Impact
[Critical/High/Medium/Low - describe business impact]

## User Scope
[How many users affected? Specific user segments?]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

## Actual Result
[What happens - include error messages, screenshots if applicable]

## Expected Result
[What should happen]

## Testing Notes
[How to verify the fix, regression test scenarios]

## Additional Notes
[Workarounds, related issues, logs, stack traces]
```

### Example: Bug

```markdown
## Environment/Platform
- iOS 17.2
- App Version 5.4.1
- Production

## Impact
**High** - Users cannot complete subscription cancellation, leading to support tickets and potential chargebacks.

## User Scope
- Affects iOS users who subscribed via Apple
- Estimated 15% of active subscriber base
- 47 support tickets in last 24 hours

## Steps to Reproduce
1. Open app on iOS device
2. Navigate to Settings > Subscription
3. Tap "Cancel Subscription"
4. Confirm cancellation in Apple popup

## Actual Result
- App shows "Cancellation successful" message
- Subscription remains active in Apple settings
- User continues to be charged

## Expected Result
- Subscription is cancelled in Apple's system
- User receives confirmation email
- No further charges occur

## Testing Notes
- Verify cancellation propagates to Apple's API
- Check webhook handling for cancellation events
- Test with sandbox Apple account
- Regression: Verify new subscriptions still work

## Additional Notes
- Workaround: Users can cancel directly in iOS Settings > Apple ID > Subscriptions
- Related: LIN-234 (subscription webhook refactor)
- Logs show timeout on Apple API call at `SubscriptionService:145`
```

## Dependency Tracking

Use Linear's native dependency fields instead of adding dependency sections to descriptions:

```python
# When creating a sub-issue with dependencies
mcp.create_issue(
    title="[Frontend] Pricing display component",
    team="TeamName",
    parentId="parent-issue-id",
    blockedBy=["LIN-101"],  # Backend API must be complete first
    description="..."
)

# When creating a sub-issue that blocks others
mcp.create_issue(
    title="[Backend] Pricing API",
    team="TeamName",
    parentId="parent-issue-id",
    blocks=["LIN-102", "LIN-103"],  # Frontend and docs depend on this
    description="..."
)
```

### Dependency Types

| Relation | When to Use | Example |
|----------|-------------|---------|
| `blockedBy` | This issue cannot start until another completes | Frontend blocked by Backend API |
| `blocks` | Other issues cannot start until this completes | Backend API blocks Frontend |
| `relatedTo` | Issues are related but not dependent | Two features touching same code |
| `duplicateOf` | This issue duplicates another | Bug already reported |

## Template Selection Guide

| Ticket Type | Template | Created By |
|-------------|----------|------------|
| New feature sub-issue | Story/Task | Solutions Architect |
| Enhancement sub-issue | Story/Task | Solutions Architect |
| Refactoring sub-issue | Story/Task | Solutions Architect |
| Bug report | Bug | Anyone (usually TPO or QA) |
| Documentation sub-issue | Story/Task | Solutions Architect |

## Quality Checklist

Before submitting any ticket:

- [ ] **Description**: Clear and concise?
- [ ] **Context**: Links to parent/related docs included?
- [ ] **Acceptance Criteria**: Specific and testable?
- [ ] **Dependencies**: Set via `blockedBy`/`blocks` fields?
- [ ] **Assignee**: Appropriate person assigned?
- [ ] **Labels**: Correct labels applied?

Note: Estimates are added by TPgM during delivery planning, not by ticket creator.
