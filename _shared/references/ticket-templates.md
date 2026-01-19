# Ticket Templates

**MANDATORY**: All sub-issues MUST use these templates. Solutions Architect creates sub-issues, TPO reviews, TPgM validates.

## Story/Task Template

For implementation sub-issues created by Solutions Architect.

| Section | Content |
|---------|---------|
| **Assigned Role** | Skill that should complete this work |
| **Story** | As a [user type], I want [capability] so that [benefit] |
| **Context** | Background + References (Parent Issue, ADR, API Spec) |
| **Acceptance Criteria** | Technical Spec + Gherkin Scenarios |
| **NFRs** | Performance, security requirements (or "N/A") |
| **Implementation Notes** | Technical guidance, patterns |
| **Infrastructure Notes** | DB changes, env vars (or "N/A") |
| **Testing Notes** | Added by Tester after review |

### Acceptance Criteria Format (Hybrid)

| Component | Purpose | Consumer |
|-----------|---------|----------|
| **Technical Spec** | Hard constraints, guardrails | AI Coding Agents |
| **Gherkin Scenarios** | Behavioral validation | Agent Testers |

#### Technical Spec

```xml
<technical-spec>
  <must>
    - Required behaviors (non-negotiable)
  </must>
  <must-not>
    - Prohibited approaches (red-lines)
  </must-not>
  <should>
    - Preferred approaches (negotiable)
  </should>
</technical-spec>
```

#### Gherkin Scenarios

```gherkin
Feature: [Feature name]

  Scenario: [Happy path]
    Given [context]
    When [action]
    Then [outcome]

  Scenario: [Error case]
    Given [context]
    When [action]
    Then [outcome]
```

### Section Ownership

| Section | Written By |
|---------|------------|
| Story, Context, Tech Spec, Gherkin, NFRs, Implementation/Infrastructure Notes | Solutions Architect |
| Testing Notes | Tester (after review) |

---

## Example: Story/Task

**Title:** `[Backend] Pricing API`

**Assigned Role:** `backend-fastapi-postgres-sqlmodel-developer`

**Story:** As a subscriber, I want to see current pricing so I can understand what I'm paying.

**Context:** AMC+ needs pricing display on Account Settings. Data comes from App Store/Play Store APIs, cached in Redis.

**References:**
- Parent: LIN-456 - Pricing Display Feature
- ADR: /docs/adr/005-pricing-api-design.md

**Acceptance Criteria:**

```xml
<technical-spec>
  <must>
    - Use Redis for caching
    - Return amounts as integers (cents)
    - Use ExternalPricingClient
  </must>
  <must-not>
    - Do NOT call store APIs synchronously in request path
    - Do NOT store prices as floats
  </must-not>
</technical-spec>
```

```gherkin
Feature: Pricing API

  Scenario: Retrieve iOS pricing
    Given App Store API is available
    When GET /api/v1/pricing/ios
    Then 200 with currency, amount, billing_period

  Scenario: External API timeout with cache
    Given App Store API unavailable
    And cached data exists
    When GET /api/v1/pricing/ios
    Then 200 with cached data
```

**NFRs:** Response < 200ms (p95), cache hit rate > 80%

**Implementation Notes:** Use `ExternalPricingClient`, follow repository pattern

**Infrastructure Notes:** Add `PRICING_CACHE_TTL` env var

---

## Assigned Role Values

| Skill Name | When to Assign |
|------------|----------------|
| `backend-fastapi-postgres-sqlmodel-developer` | FastAPI endpoints, services, DB |
| `frontend-atomic-design-engineer` | React UI components |
| `tech-doc-writer-manager` | Documentation |
| `backend-fastapi-pytest-tester` | Backend tests |
| `frontend-tester` | Frontend/E2E tests |
| `data-platform-engineer` | Data pipelines |
| `api-designer` | API contract design |

---

## Bug Template

| Section | Content |
|---------|---------|
| **Environment** | OS, browser, app version, environment |
| **Impact** | Critical/High/Medium/Low + business impact |
| **User Scope** | How many affected |
| **Steps to Reproduce** | Numbered steps |
| **Actual Result** | What happens |
| **Expected Result** | What should happen |
| **Testing Notes** | How to verify fix |
| **Additional Notes** | Workarounds, logs |

---

## Example: Bug

**Title:** `[Bug] iOS subscription cancellation fails silently`

**Environment:** iOS 17.2, App 5.4.1, Production

**Impact:** High - Users cannot cancel, causing support tickets and chargebacks

**User Scope:** 15% of subscriber base, 47 tickets in 24h

**Steps:**
1. Open app on iOS
2. Settings > Subscription > Cancel
3. Confirm in Apple popup

**Actual:** Shows success, subscription remains active

**Expected:** Subscription cancelled, confirmation email sent

**Testing Notes:** Verify Apple API propagation, test sandbox account

**Additional:** Workaround: Cancel via iOS Settings. Related: LIN-234

---

## Dependencies

Use ticket system's native fields. See `ticketing-*.md` for system-specific commands.

| System | Parent | Blocked By |
|--------|--------|------------|
| Linear | `parentId` | `blockedBy` |
| GitHub | `addSubIssue` GraphQL | `addBlockedBy` GraphQL |
| Plan Files | N/A | `(blockedBy: ...)` |

---

## Quality Checklist

Before submitting:

- [ ] Story written as user story
- [ ] Context provides background
- [ ] Technical Spec has MUST/MUST NOT/SHOULD
- [ ] Gherkin scenarios cover happy path + errors
- [ ] References linked (Parent, ADR, specs)
- [ ] Dependencies set via native fields (NOT in issue body)
- [ ] Assignee set
