# Sentry MCP Integration Guide

This guide covers how to effectively use Sentry MCP tools for error triage and investigation.

## Available Sentry MCP Tools

The Sentry MCP server provides these tools:

| Tool | Purpose |
|------|---------|
| `list_organizations` | List available Sentry organizations |
| `list_projects` | List projects in an organization |
| `list_issues` | Query issues with filters |
| `get_issue` | Get detailed issue information |
| `get_latest_event` | Get most recent event for an issue |
| `resolve_issue` | Mark an issue as resolved |

## Common Investigation Workflows

### 1. Initial Triage - Recent Unresolved Issues

Start by listing unresolved issues to understand the current state:

```
list_issues(
  project="your-project",
  query="is:unresolved",
  sort_by="date"
)
```

**Key filters for query parameter**:
- `is:unresolved` - Only open issues
- `is:resolved` - Closed issues
- `firstSeen:-24h` - New in last 24 hours
- `lastSeen:-1h` - Active in last hour
- `times_seen:>100` - High frequency
- `level:error` - Only errors (not warnings)

### 2. Investigating a Specific Issue

Once you identify an issue to investigate:

```
# Get issue details
get_issue(issue_id="ISSUE_ID")

# Get the latest occurrence with full context
get_latest_event(issue_id="ISSUE_ID")
```

**Information to extract**:

From `get_issue`:
- Issue title and culprit (where it originated)
- First seen / last seen timestamps
- Event count and user count affected
- Tags (environment, release, browser, etc.)
- Assigned user (if any)

From `get_latest_event`:
- Full stack trace
- Breadcrumbs (actions before the error)
- Request data (URL, method, headers)
- User context (if captured)
- Custom tags and extra data

### 3. Filtering by Environment

When investigating environment-specific issues:

```
# Production only
list_issues(
  project="your-project",
  query="is:unresolved environment:production"
)

# Specific release
list_issues(
  project="your-project",
  query="is:unresolved release:v2.1.0"
)
```

### 4. Finding User-Specific Issues

When a specific user reports a problem:

```
list_issues(
  project="your-project",
  query="user.id:user_123"
)
```

Or by email if captured:
```
query="user.email:user@example.com"
```

## Reading Stack Traces

### Python/FastAPI Stack Traces

Look for these patterns:
1. **Bottom of trace** = Where error was raised
2. **Top of trace** = Entry point (request handler)
3. **Middle** = Call chain

Example:
```
File "app/api/routes/users.py", line 45, in get_user
    user = await user_service.get_by_id(user_id)
File "app/services/user_service.py", line 23, in get_by_id
    return await self.repository.find_one(id=user_id)
File "app/repositories/base.py", line 67, in find_one
    raise NotFoundError(f"Entity not found: {id}")
```

**Reading order**: Start from bottom, trace upward to understand call chain.

### JavaScript/React Stack Traces

Look for:
1. **Your code** vs **library code** (node_modules)
2. **Source maps** - Sentry should show original TypeScript/JSX
3. **Component tree** in React errors

### Common Error Patterns

| Error Type | Common Causes |
|------------|---------------|
| `NoneType has no attribute` | Null reference, missing data |
| `KeyError` / `AttributeError` | Missing field, API contract change |
| `ConnectionError` | Database/external service down |
| `TimeoutError` | Slow query, network issues |
| `ValidationError` | Bad input data |
| `PermissionError` | Auth/authz issue |

## Using Breadcrumbs

Breadcrumbs show what happened before the error:

```json
[
  {"category": "http", "message": "GET /api/users/123", "timestamp": "..."},
  {"category": "query", "message": "SELECT * FROM users WHERE id = ?", "timestamp": "..."},
  {"category": "ui.click", "message": "button#submit", "timestamp": "..."}
]
```

**What to look for**:
- HTTP requests that preceded the error
- Database queries (N+1 problems, slow queries)
- User actions that triggered the flow
- Console logs if captured

## Issue Management

### Resolving Issues

After fixing an issue:

```
resolve_issue(
  issue_id="ISSUE_ID",
  status="resolved"
)
```

**Resolution states**:
- `resolved` - Fixed, should not recur
- `ignored` - Known issue, intentionally not fixing
- `unresolved` - Reopen if it recurs

### Best Practices

1. **Don't resolve without verification** - Wait for deployment and confirm the fix works
2. **Use release tracking** - Link issues to releases to track regression
3. **Add context via comments** - Document investigation findings
4. **Tag for categorization** - Use consistent tags for analysis

## Query Language Reference

### Time-Based Queries
```
firstSeen:-7d          # New in last 7 days
lastSeen:-1h           # Active in last hour
firstSeen:>2025-01-01  # After specific date
```

### Frequency Queries
```
times_seen:>100        # Seen more than 100 times
times_seen:1           # Seen exactly once (potentially new)
```

### User Impact
```
user.id:specific_user  # Specific user affected
users:>10              # Affecting more than 10 users
```

### Combining Filters
```
is:unresolved environment:production level:error firstSeen:-24h
```

## Sentry Setup Recommendations

### For Effective Debugging

1. **Enable source maps** (JavaScript) for readable stack traces
2. **Capture user context** to correlate issues with users:
   ```python
   sentry_sdk.set_user({"id": user.id, "email": user.email})
   ```
3. **Add custom tags** for filtering:
   ```python
   sentry_sdk.set_tag("feature", "checkout")
   ```
4. **Use breadcrumbs** for context:
   ```python
   sentry_sdk.add_breadcrumb(message="Processing payment", category="payment")
   ```

### Performance Considerations

- **Sample rate**: Don't capture 100% in high-traffic production
- **Ignore common errors**: Filter out expected/handled errors
- **PII scrubbing**: Ensure sensitive data is redacted

## Troubleshooting Sentry Issues

### Issue: Events not appearing
- Check DSN is correct
- Verify network connectivity to Sentry
- Check sample rate isn't too low
- Look for SDK initialization errors

### Issue: Stack traces unreadable
- Upload source maps for JavaScript
- Ensure debug symbols for native code
- Check that source code context is enabled

### Issue: Too many events
- Implement rate limiting in SDK
- Filter out non-actionable errors
- Use `before_send` hook to drop events
