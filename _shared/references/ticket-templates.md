# Ticket Templates

Standard templates for creating well-structured tickets. These templates ensure consistency and completeness across different ticket types.

**MANDATORY**: All sub-issues MUST use these templates. Solutions Architect creates tickets, TPO reviews, TPgM validates.

## Story/Task Template

Use this template for implementation sub-issues created by Solutions Architect.

### Template Structure

| Section | Content |
|---------|---------|
| **Assigned Role** | Skill/role that should complete this work |
| **Story** | As a [user type], I want [capability] so that [benefit]. |
| **Context** | Background for someone unfamiliar (see below) |
| **Acceptance Criteria & Technical Spec** | Technical constraints + Gherkin scenarios (see below) |
| **NFRs** | Performance, security requirements (or "N/A") |
| **Implementation Notes** | Technical guidance, patterns, code references |
| **Infrastructure Notes** | DB changes, env vars, deployment (or "N/A") |
| **Testing Notes** | Added by Tester after review |

### Context Section Guidelines

Context should provide enough background for someone unfamiliar with the product:
- Why this work exists (business driver)
- How it fits into the larger feature
- What the user is trying to accomplish
- Any relevant domain knowledge needed

Include **References** at the end:
- Parent Issue: [TICKET-ID - Parent feature name]
- ADR: [Link if applicable]
- API Spec: [Link if applicable]
- Design: [Link if applicable]

### Acceptance Criteria Format (Hybrid: Spec + Gherkin)

Acceptance Criteria has two parts that serve different purposes:

| Component | Purpose | Consumer |
|-----------|---------|----------|
| **Technical Specification** | Hard constraints, guardrails, red-lines | AI Coding Agents (Cursor, Copilot, Claude Code) |
| **Gherkin Scenarios** | Behavioral validation, testable outcomes | Agent Testers, QA automation |

**Why this hybrid approach?**
- Technical Specs provide **guardrails** for AI Coding Agents - they define what MUST or MUST NOT be done
- Gherkin provides **validation** for Agent Testers - they define how to verify the implementation works

#### Technical Specification

Define hard constraints using `<technical-spec>` tags or markdown lists. Include:

- **MUST**: Required behaviors or constraints (non-negotiable)
- **MUST NOT**: Prohibited approaches or patterns (red-lines)
- **SHOULD**: Preferred approaches (negotiable with justification)
- **Tools/Libraries**: Specific technologies required

```xml
<technical-spec>
  <must>
    - Use Redis for caching (not in-memory)
    - Validate currency codes against ISO-4217
    - Return amounts as integers (cents, not decimals)
  </must>
  <must-not>
    - Do NOT call external APIs synchronously in the request path
    - Do NOT store prices as floating point numbers
  </must-not>
  <should>
    - Prefer async/await over callbacks
    - Use existing ExternalPricingClient class
  </should>
</technical-spec>
```

#### Gherkin Scenarios

Write behavioral scenarios for testing:

```gherkin
Feature: [Feature name]

  Scenario: [Happy path scenario]
    Given [initial context]
    When [action taken]
    Then [expected outcome]

  Scenario: [Edge case or error scenario]
    Given [initial context]
    When [action taken]
    Then [expected outcome]
```

### Section Ownership

| Section | Written By | Purpose |
|---------|------------|---------|
| Assigned Role | Solutions Architect | Who implements this |
| Story | Solutions Architect | User-centric description |
| Context | Solutions Architect | Background for anyone to understand |
| Acceptance Criteria (Tech Spec) | Solutions Architect | Guardrails for AI Coding Agents |
| Acceptance Criteria (Gherkin) | Solutions Architect | Behavioral scenarios for validation |
| NFRs | Solutions Architect | Performance/security requirements |
| Implementation Notes | Solutions Architect | Technical guidance |
| Infrastructure Notes | Solutions Architect | Deployment considerations |
| Testing Notes | Tester | Additional test scenarios after review |

---

## Example: Story/Task

**Title:** `[Backend] Pricing API`

---

**Assigned Role:** Backend Developer

---

**Story:**

As a subscriber, I want to see current pricing for my subscription plan so that I can understand what I'm paying before making changes.

---

**Context:**

AMC+ is expanding to support multiple pricing tiers. Users currently have no way to see their current price or compare it to other plans. This API will power the pricing display on the Account Settings page.

The pricing data comes from App Store (iOS) and Play Store (Android) via their respective APIs. We need to cache this data to avoid rate limits and improve response times.

This is part of the larger "Subscription Management" feature where users can view and modify their subscriptions.

**References:**
- Parent Issue: LIN-456 - AMC+ Pricing Display Feature
- ADR: /docs/adr/005-pricing-api-design.md
- API Spec: /docs/api/pricing.yaml

---

**Acceptance Criteria & Technical Spec:**

*Technical Specification (Guardrails for AI Coding Agents):*

```xml
<technical-spec>
  <must>
    - Use Redis for caching (PRICING_CACHE_TTL env var)
    - Validate currency codes against ISO-4217 standard
    - Return price amounts as integers in cents (not decimals)
    - Use existing ExternalPricingClient for store API calls
    - Cache responses with key prefix "pricing:"
  </must>
  <must-not>
    - Do NOT call App Store/Play Store APIs synchronously in request path
    - Do NOT store or return prices as floating point numbers
    - Do NOT implement custom HTTP clients (use ExternalPricingClient)
  </must-not>
  <should>
    - Follow repository pattern in app/repositories/
    - Use async/await for external API calls
    - Log cache hits/misses for monitoring
  </should>
</technical-spec>
```

*Gherkin Scenarios (Validation for Agent Testers):*

```gherkin
Feature: Pricing API

  Scenario: Retrieve iOS pricing successfully
    Given the App Store API is available
    When I request GET /api/v1/pricing/ios
    Then I receive a 200 response
    And the response includes currency, amount, and billing_period
    And the response is cached for 1 hour

  Scenario: Retrieve Android pricing successfully
    Given the Play Store API is available
    When I request GET /api/v1/pricing/android
    Then I receive a 200 response
    And the response includes currency, amount, and billing_period

  Scenario: Request pricing for unsupported platform
    When I request GET /api/v1/pricing/windows
    Then I receive a 404 response
    And the error message indicates unsupported platform

  Scenario: External API timeout with cache hit
    Given the App Store API is unavailable
    And cached pricing data exists
    When I request GET /api/v1/pricing/ios
    Then I receive a 200 response with cached data

  Scenario: External API timeout without cache
    Given the App Store API is unavailable
    And no cached pricing data exists
    When I request GET /api/v1/pricing/ios
    Then I receive a 503 response
```

---

**NFRs:**
- Response time < 200ms (p95)
- Cache hit rate > 80%
- Graceful degradation when external APIs fail

---

**Implementation Notes:**
- Use existing `ExternalPricingClient` for App Store/Play Store APIs
- Follow repository pattern in `app/repositories/`
- Price amounts should be stored as integers (cents)
- See `app/services/subscription_service.py` for similar patterns

---

**Infrastructure Notes:**
- Add `PRICING_CACHE_TTL` environment variable (default: 3600 seconds)
- Redis cache key prefix: `pricing:`
- No database migrations required

---

**Testing Notes:**

[To be added by Backend Tester after implementation review]

---

### Assigned Role Values

Use exact skill names from the skills library:

| Skill Name | When to Assign |
|------------|----------------|
| `backend-fastapi-postgres-sqlmodel-developer` | FastAPI endpoints, services, database operations |
| `frontend-atomic-design-engineer` | React UI components, pages, client-side logic |
| `tech-doc-writer-manager` | API documentation, guides, runbooks |
| `backend-fastapi-pytest-tester` | Dedicated backend test coverage |
| `frontend-tester` | Dedicated frontend/E2E test coverage |
| `data-platform-engineer` | Data pipelines, migrations, analytics |
| `api-designer` | API contract design (before implementation) |
| `ai-integration-engineer` | AI/LLM features, prompt design |
| `mcp-server-developer` | MCP server implementation |

---

## Bug Template

Use this template for bug reports.

### Template Structure

| Section | Content |
|---------|---------|
| **Environment/Platform** | OS, browser, app version, environment |
| **Impact** | Critical/High/Medium/Low with business impact |
| **User Scope** | How many users affected |
| **Steps to Reproduce** | Numbered steps |
| **Actual Result** | What happens |
| **Expected Result** | What should happen |
| **Testing Notes** | How to verify fix |
| **Additional Notes** | Workarounds, logs, related issues |

---

## Example: Bug

**Title:** `[Bug] iOS subscription cancellation fails silently`

---

**Environment/Platform:**
- iOS 17.2
- App Version 5.4.1
- Production

---

**Impact:**

**High** - Users cannot complete subscription cancellation, leading to support tickets and potential chargebacks.

---

**User Scope:**
- Affects iOS users who subscribed via Apple
- Estimated 15% of active subscriber base
- 47 support tickets in last 24 hours

---

**Steps to Reproduce:**
1. Open app on iOS device
2. Navigate to Settings > Subscription
3. Tap "Cancel Subscription"
4. Confirm cancellation in Apple popup

---

**Actual Result:**
- App shows "Cancellation successful" message
- Subscription remains active in Apple settings
- User continues to be charged

---

**Expected Result:**
- Subscription is cancelled in Apple's system
- User receives confirmation email
- No further charges occur

---

**Testing Notes:**
- Verify cancellation propagates to Apple's API
- Check webhook handling for cancellation events
- Test with sandbox Apple account
- Regression: Verify new subscriptions still work

---

**Additional Notes:**
- Workaround: Users can cancel directly in iOS Settings > Apple ID > Subscriptions
- Related: LIN-234 (subscription webhook refactor)
- Logs show timeout on Apple API call at `SubscriptionService:145`

---

## Dependency Tracking

How to set dependencies varies by ticket system. Use the correct method for your system.

| System | Method | Parent | Blocked By | Blocks |
|--------|--------|--------|------------|--------|
| **Linear** | Native fields (MCP) | `parentId` | `blockedBy` | `blocks` |
| **GitHub** | GraphQL mutations | `addSubIssue` mutation | `addBlockedBy` mutation | (inverse of blockedBy) |
| **Plan Files** | Inline text | N/A | `(blockedBy: ...)` | N/A |

### Linear (Native Fields)

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

| Relation | When to Use | Example |
|----------|-------------|---------|
| `parentId` | Links sub-issue to parent | Sub-issue belongs to parent feature |
| `blockedBy` | This issue cannot start until another completes | Frontend blocked by Backend API |
| `blocks` | Other issues cannot start until this completes | Backend API blocks Frontend |
| `relatedTo` | Issues are related but not dependent | Two features touching same code |

### GitHub Projects (Native Relationship Fields via GraphQL)

GitHub provides native relationship fields via GraphQL Sub-Issues API (beta feature).

**IMPORTANT**: CLI flags like `--parent`, `--add-blocked-by` do NOT exist. Use GraphQL mutations.

```bash
# Create issues first
parent_num=$(gh issue create --title "[Feature] Password Reset" --body "..." | grep -oP '\d+')
child_num=$(gh issue create --title "[Frontend] Reset form UI" --body "..." | grep -oP '\d+')

# Get node IDs
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
parent_node=$(gh api repos/$REPO/issues/$parent_num --jq '.node_id')
child_node=$(gh api repos/$REPO/issues/$child_num --jq '.node_id')

# Set parent-child relationship
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addSubIssue(input: {
    issueId: "'"$parent_node"'"
    subIssueId: "'"$child_node"'"
  }) {
    issue { number }
    subIssue { number }
  }
}'

# Set blocking relationship
blocker_node=$(gh api repos/$REPO/issues/102 --jq '.node_id')
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation {
  addBlockedBy(input: {
    issueId: "'"$child_node"'"
    blockingIssueId: "'"$blocker_node"'"
  }) {
    issue { number }
  }
}'
```

| Relationship | GraphQL Mutation |
|--------------|------------------|
| `parent` | `addSubIssue` (requires node IDs + beta header) |
| `blockedBy` | `addBlockedBy` (requires node IDs + beta header) |
| `remove parent` | `removeSubIssue` |
| `remove blockedBy` | `removeBlockedBy` |

See `ticketing-github-projects.md` for full GitHub GraphQL workflow.

### Plan Files (Inline Annotation)

Use inline `(blockedBy: ...)` annotations:

```markdown
- [ ] Backend API
- [ ] Frontend form (blockedBy: Backend API)
- [ ] Documentation (blockedBy: Frontend form)
```

See `ticketing-plan-file.md` for plan file patterns.

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

- [ ] **Story**: Written as user story (As a... I want... so that...)?
- [ ] **Context**: Enough background for someone unfamiliar to understand?
- [ ] **Technical Spec**: MUST/MUST NOT/SHOULD constraints defined for AI agents?
- [ ] **Gherkin Scenarios**: Behavioral tests written in Given/When/Then format?
- [ ] **References**: Parent issue, ADR, specs linked?
- [ ] **Dependencies set correctly for your system**:
  - Linear: `parentId`, `blockedBy`, `blocks` native fields via MCP
  - GitHub: GraphQL `addSubIssue`, `addBlockedBy` mutations (NOT CLI flags)
  - Plan files: `(blockedBy: ...)` inline annotation
- [ ] **Assignee**: Appropriate person assigned?
- [ ] **Labels**: Correct labels applied?

Note: Estimates are added by TPgM during delivery planning, not by ticket creator.
