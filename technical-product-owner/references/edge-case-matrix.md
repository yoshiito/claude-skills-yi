# Edge Case Matrix

Comprehensive patterns for documenting unhappy paths, empty states, and extreme states.

## Unhappy Paths

### Format
```
UNHAPPY-[ID]: [Name]
Trigger: [What causes this state]
User Impact: [What the user experiences]
System Behavior: [What the system does]
Recovery Path: [How user recovers]
Error Code: [ERR_CODE]
Error Message: "[User-facing message]"
```

### Common Categories

#### Input Validation Failures

UNHAPPY-V01: Missing Required Field
Trigger: User submits form without required field
User Impact: Cannot proceed with action
System Behavior: Reject request, return 422, highlight field
Recovery Path: Fill in required field and resubmit
Error Code: ERR_FIELD_REQUIRED
Error Message: "[Field name] is required"

UNHAPPY-V02: Invalid Format
Trigger: User enters data in wrong format (email, phone, date)
User Impact: Cannot proceed with action
System Behavior: Reject request, return 422, show format hint
Recovery Path: Correct format and resubmit
Error Code: ERR_INVALID_FORMAT
Error Message: "Please enter a valid [field type]"

UNHAPPY-V03: Value Out of Range
Trigger: Numeric value outside allowed bounds
User Impact: Cannot proceed with action
System Behavior: Reject request, return 422, show allowed range
Recovery Path: Enter value within range
Error Code: ERR_OUT_OF_RANGE
Error Message: "[Field] must be between [min] and [max]"

UNHAPPY-V04: Exceeds Maximum Length
Trigger: Text input exceeds character limit
User Impact: Cannot proceed with action
System Behavior: Reject request (or truncate with warning)
Recovery Path: Shorten input
Error Code: ERR_TOO_LONG
Error Message: "[Field] must be [max] characters or less"

UNHAPPY-V05: Duplicate Entry
Trigger: User creates resource that already exists (unique constraint)
User Impact: Cannot create duplicate
System Behavior: Reject request, return 409
Recovery Path: Use different value or edit existing resource
Error Code: ERR_DUPLICATE
Error Message: "A [resource] with this [field] already exists"

#### Authentication Failures

UNHAPPY-A01: Invalid Credentials
Trigger: Wrong username or password
User Impact: Cannot log in
System Behavior: Reject request, return 401, increment failure count
Recovery Path: Retry with correct credentials or reset password
Error Code: ERR_INVALID_CREDENTIALS
Error Message: "Invalid email or password"

UNHAPPY-A02: Account Locked
Trigger: Too many failed login attempts
User Impact: Cannot log in even with correct credentials
System Behavior: Reject request, return 403
Recovery Path: Wait for lockout period or contact support
Error Code: ERR_ACCOUNT_LOCKED
Error Message: "Account locked. Try again in [X] minutes or reset password"

UNHAPPY-A03: Session Expired
Trigger: User's session times out
User Impact: Current action fails, must re-authenticate
System Behavior: Return 401, redirect to login
Recovery Path: Log in again
Error Code: ERR_SESSION_EXPIRED
Error Message: "Your session has expired. Please log in again"

UNHAPPY-A04: Token Invalid/Expired
Trigger: Reset token, invite token, or API token invalid
User Impact: Cannot complete token-based action
System Behavior: Reject request, return 400 or 401
Recovery Path: Request new token
Error Code: ERR_TOKEN_INVALID / ERR_TOKEN_EXPIRED
Error Message: "This link is invalid or has expired"

#### Authorization Failures

UNHAPPY-Z01: Insufficient Permissions
Trigger: User attempts action their role doesn't allow
User Impact: Action blocked
System Behavior: Reject request, return 403, log attempt
Recovery Path: Request elevated permissions or contact admin
Error Code: ERR_FORBIDDEN
Error Message: "You don't have permission to perform this action"

UNHAPPY-Z02: Resource Not Owned
Trigger: User attempts to access/modify another user's resource
User Impact: Cannot access resource
System Behavior: Return 404 (not 403, to avoid enumeration)
Recovery Path: Access own resources only
Error Code: N/A (returns 404)
Error Message: "[Resource] not found"

UNHAPPY-Z03: Quota Exceeded
Trigger: User attempts action that exceeds plan limits
User Impact: Cannot create more resources
System Behavior: Reject request, return 403
Recovery Path: Upgrade plan or delete existing resources
Error Code: ERR_QUOTA_EXCEEDED
Error Message: "You've reached your limit of [X] [resources]. Upgrade to create more"

#### Resource State Failures

UNHAPPY-R01: Resource Not Found
Trigger: Requested resource doesn't exist or was deleted
User Impact: Cannot view/edit resource
System Behavior: Return 404
Recovery Path: Verify URL, return to list view
Error Code: N/A (returns 404)
Error Message: "[Resource] not found"

UNHAPPY-R02: Resource Already Deleted
Trigger: Action on soft-deleted resource
User Impact: Cannot interact with deleted resource
System Behavior: Return 404 or 410 Gone
Recovery Path: Resource may be restorable by admin
Error Code: ERR_RESOURCE_DELETED
Error Message: "This [resource] has been deleted"

UNHAPPY-R03: Invalid State Transition
Trigger: Action not allowed in current state (e.g., publish draft that's already published)
User Impact: Cannot perform action
System Behavior: Reject request, return 409
Recovery Path: Take different action appropriate to state
Error Code: ERR_INVALID_TRANSITION
Error Message: "Cannot [action] a [resource] that is already [state]"

UNHAPPY-R04: Concurrent Modification Conflict
Trigger: Two users edit same resource simultaneously
User Impact: Second user's changes rejected
System Behavior: Return 409, include current version
Recovery Path: Reload current data and retry
Error Code: ERR_CONFLICT
Error Message: "This [resource] was modified by another user. Please refresh and try again"

#### External/System Failures

UNHAPPY-X01: Network Timeout
Trigger: Request takes too long (client or server side)
User Impact: Action fails or hangs
System Behavior: Return 504 or client timeout
Recovery Path: Retry action
Error Code: ERR_TIMEOUT
Error Message: "Request timed out. Please try again"

UNHAPPY-X02: External Service Unavailable
Trigger: Third-party dependency is down
User Impact: Dependent feature unavailable
System Behavior: Return 503 or degrade gracefully
Recovery Path: Wait and retry, or use fallback if available
Error Code: ERR_SERVICE_UNAVAILABLE
Error Message: "This feature is temporarily unavailable. Please try again later"

UNHAPPY-X03: Rate Limited
Trigger: Too many requests in time window
User Impact: Temporarily blocked
System Behavior: Return 429 with Retry-After header
Recovery Path: Wait and retry
Error Code: ERR_RATE_LIMITED
Error Message: "Too many requests. Please wait [X] seconds"

---

## Empty States

### Format
```
EMPTY-[ID]: [Name]
Context: [Where this empty state appears]
Condition: [When it's shown]
Display: [What the UI shows - illustration, message, etc.]
Action: [CTA or guidance provided]
```

### Common Patterns

EMPTY-001: First-Time User / No Resources
Context: Main list view (projects, documents, etc.)
Condition: User has zero resources of this type
Display: Welcome illustration, "No [resources] yet" heading
Action: Primary CTA "Create your first [resource]" + optional onboarding

EMPTY-002: Search No Results
Context: Search results page or filtered list
Condition: Search/filter returns zero matches
Display: Search illustration, "No results for '[query]'"
Action: Suggestions: "Try different keywords" / "Clear filters" / "Browse all"

EMPTY-003: Filtered List Empty
Context: List view with active filters
Condition: Filters exclude all items
Display: Filter illustration, "No [resources] match these filters"
Action: "Clear filters" button, show filter summary

EMPTY-004: Activity Feed Empty
Context: Activity/notification feed
Condition: No recent activity
Display: Activity illustration, "No recent activity"
Action: Contextual prompt based on what generates activity

EMPTY-005: Comments/Discussion Empty
Context: Comments section on resource
Condition: No comments yet
Display: Discussion illustration, "No comments yet"
Action: "Be the first to comment" with input field visible

EMPTY-006: Team Members Empty
Context: Team/organization member list
Condition: Only current user is member
Display: Team illustration, "You're the only member"
Action: "Invite team members" button

EMPTY-007: Integrations Empty
Context: Connected apps/integrations list
Condition: No integrations configured
Display: Integration illustration, "No connected apps"
Action: "Browse integrations" button + featured integrations

EMPTY-008: Deleted/Archived View Empty
Context: Trash/archive list view
Condition: No deleted/archived items
Display: Clean illustration, "No deleted [resources]"
Action: None or "Learn about deletion policy"

---

## Extreme States

### Format
```
EXTREME-[ID]: [Name]
Scenario: [The extreme condition]
Expected Volume: [Quantified - numbers, rates]
System Behavior: [How system handles this load]
Degradation Strategy: [What gets sacrificed to maintain stability]
User Communication: [How users are informed]
```

### Common Patterns

#### High Volume

EXTREME-HV01: Bulk Import
Scenario: User imports large dataset
Expected Volume: 10,000 - 100,000 records
System Behavior: Queue-based processing, background job, progress tracking
Degradation Strategy: Rate limit processing (1000/minute), allow partial success
User Communication: Progress bar, email notification on completion

EXTREME-HV02: Large List View
Scenario: User with many resources loads list
Expected Volume: 10,000+ items
System Behavior: Server-side pagination, virtual scrolling, lazy loading
Degradation Strategy: Limit to 100 items per page, require filters for full access
User Communication: "Showing 100 of 10,000" with filter prompts

EXTREME-HV03: Bulk Export
Scenario: User exports large dataset
Expected Volume: 100,000+ records
System Behavior: Background job, generate downloadable file, email link
Degradation Strategy: Limit export size, require date range filters
User Communication: "Export started. We'll email you when ready"

#### High Concurrency

EXTREME-HC01: Viral Content Spike
Scenario: Shared content goes viral, massive read traffic
Expected Volume: 10,000+ requests/second
System Behavior: CDN caching, read replicas, auto-scaling
Degradation Strategy: Serve cached content, delay real-time updates
User Communication: None visible if handled; "High traffic" notice if degraded

EXTREME-HC02: Simultaneous Editors
Scenario: Many users edit related resources simultaneously
Expected Volume: 100+ concurrent editors
System Behavior: Optimistic locking, conflict resolution, operational transforms
Degradation Strategy: Queue updates, show presence indicators, merge conflicts
User Communication: "[X] others editing", conflict resolution UI

EXTREME-HC03: Event-Driven Surge
Scenario: Scheduled event triggers mass simultaneous action
Expected Volume: 10,000+ users at T+0
System Behavior: Pre-warm capacity, queue-based processing, rate limiting
Degradation Strategy: Fair queuing, stagger processing, partial availability
User Communication: "High demand - you're in queue", estimated wait time

#### Edge Values

EXTREME-EV01: Maximum Text Length
Scenario: User enters maximum allowed characters
Expected Volume: 10,000+ characters in rich text field
System Behavior: Accept and store, may affect rendering performance
Degradation Strategy: Truncate preview, paginate content display
User Communication: Character counter, "Showing preview" indicator

EXTREME-EV02: Deep Nesting
Scenario: Deeply nested hierarchical data
Expected Volume: 50+ levels deep
System Behavior: Recursive queries with depth limits
Degradation Strategy: Limit display depth, "Show more" for deep levels
User Communication: "Showing 10 levels. Click to expand"

EXTREME-EV03: Many Relationships
Scenario: Single resource with many associations
Expected Volume: 10,000+ related items
System Behavior: Paginated relationship loading, count-only by default
Degradation Strategy: Lazy load relationships, limit inline display
User Communication: "1,234 related items" with "View all" link

#### Time-Based

EXTREME-TB01: Long-Running Operation
Scenario: Complex operation takes extended time
Expected Volume: 5+ minutes processing time
System Behavior: Background job, progress tracking, resumable
Degradation Strategy: Allow cancellation, checkpoint progress
User Communication: Progress indicator, estimated time, email on completion

EXTREME-TB02: Historical Data Request
Scenario: User requests very old data
Expected Volume: 5+ years historical data
System Behavior: Archive tier retrieval, may require async processing
Degradation Strategy: Longer retrieval time, limited query options
User Communication: "Retrieving archived data. This may take a few minutes"

---

## Error Message Registry

Centralize all error messages for consistency.

### Format
| Code | HTTP | User Message | Internal Log | Retry | Action |
|------|------|--------------|--------------|-------|--------|

### Example Registry

| Code | HTTP | User Message | Internal Log | Retry | Action |
|------|------|--------------|--------------|-------|--------|
| ERR_FIELD_REQUIRED | 422 | "[Field] is required" | "Missing required field: {field}" | No | Fix input |
| ERR_INVALID_FORMAT | 422 | "Please enter a valid [type]" | "Invalid format: {field}={value}" | No | Fix input |
| ERR_INVALID_CREDENTIALS | 401 | "Invalid email or password" | "Login failed: {email}" | No | Retry/reset |
| ERR_SESSION_EXPIRED | 401 | "Session expired. Please log in" | "Expired session: {session_id}" | No | Re-auth |
| ERR_FORBIDDEN | 403 | "You don't have permission" | "Forbidden: {user} -> {action}" | No | Get access |
| ERR_QUOTA_EXCEEDED | 403 | "Limit reached. Upgrade to continue" | "Quota exceeded: {user}, {resource}" | No | Upgrade |
| ERR_NOT_FOUND | 404 | "[Resource] not found" | "Not found: {resource_type}/{id}" | No | Navigate away |
| ERR_CONFLICT | 409 | "Modified by another user. Refresh" | "Conflict: {resource}/{id}, v{version}" | Yes | Refresh |
| ERR_DUPLICATE | 409 | "Already exists" | "Duplicate: {field}={value}" | No | Use different value |
| ERR_RATE_LIMITED | 429 | "Too many requests. Wait [X]s" | "Rate limit: {ip}/{endpoint}" | Yes | Wait |
| ERR_TIMEOUT | 504 | "Request timed out. Try again" | "Timeout: {endpoint}, {duration}ms" | Yes | Retry |
| ERR_SERVICE_UNAVAILABLE | 503 | "Temporarily unavailable" | "Service down: {service}" | Yes | Wait |
