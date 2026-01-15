# API Versioning Strategies

Guide for choosing and implementing API versioning strategies.

## Versioning Decision Framework

```
Is this a public API with external consumers?
├── YES → Use URL versioning (most explicit)
│         GET /v1/users
│         GET /v2/users
│
└── NO → Is it an internal API between your own services?
         ├── YES → Is breaking change frequency expected to be high?
         │         ├── YES → Use header versioning
         │         │         Accept: application/vnd.api.v2+json
         │         │
         │         └── NO → Consider no versioning
         │                  Use additive changes only
         │
         └── NO (partner API) → Use URL versioning
                                Explicit versions for contracts
```

## Strategy Comparison

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| URL versioning | Explicit, easy to understand, cacheable | URL pollution, harder redirects | Public APIs |
| Header versioning | Clean URLs, flexible | Less discoverable, harder to test | Internal APIs |
| Query param | Simple to implement | Looks hacky, caching issues | Quick prototypes |
| No versioning | Simplest | Breaking changes are hard | Rapidly evolving internal |

## Strategy 1: URL Versioning (Recommended for Public APIs)

### Implementation

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

### Pros
- **Explicit**: Version is visible in every request
- **Easy testing**: Can test in browser, curl, Postman without headers
- **Cacheable**: Different URLs = different cache entries
- **Clear documentation**: Each version has distinct API docs

### Cons
- Multiple URLs for same resource
- Harder to redirect clients to new versions
- API URLs can become long with nested resources

### Best Practices

```yaml
# Version only the base path, not every segment
# ✓ CORRECT
/v1/users/{userId}/projects

# ✗ WRONG
/v1/users/v1/{userId}/v1/projects

# Use major versions only (v1, v2, not v1.1)
# ✓ CORRECT
/v1/users

# ✗ WRONG
/v1.2.3/users

# Keep legacy versions running during transition
# Document sunset dates clearly
```

### Version Lifecycle

```
v1 (current)     -> v2 (new)
     │                │
     │   Migration    │
     │   Period       │
     ▼   (6 months)   ▼
Deprecated ---------> Active
     │
     │   Sunset
     │   (6 months)
     ▼
  Removed
```

## Strategy 2: Header Versioning

### Implementation

```http
GET /users HTTP/1.1
Host: api.example.com
Accept: application/vnd.example.v2+json
```

### Pros
- Clean, version-free URLs
- Single URL for conceptual resource
- Flexible (can version different parts independently)

### Cons
- Less discoverable
- Harder to test (need to set headers)
- Some proxies/caches may not handle correctly

### Header Options

```http
# Option A: Accept header with custom media type
Accept: application/vnd.example.v2+json

# Option B: Custom version header
X-API-Version: 2

# Option C: Accept header with parameter
Accept: application/json; version=2
```

### Best Practices

```yaml
# Always default to latest stable version
# If no version header, use v1 (or current stable)

# Return version in response headers
X-API-Version: 2
X-API-Version-Deprecated: false
X-API-Version-Sunset: 2025-06-01  # if applicable

# Document supported versions clearly
```

## Strategy 3: Query Parameter Versioning

### Implementation

```
GET /users?version=2
GET /users?api-version=2024-01-15
```

### Pros
- Simple to implement
- Easy to test
- Works with all HTTP clients

### Cons
- Looks unofficial/hacky
- Caching complications
- Mixes versioning with filtering

### Use Cases

Generally **not recommended** except for:
- Quick prototypes
- Date-based versioning (Azure style)
- Gradual migration from no versioning

```yaml
# Date-based versioning (Azure pattern)
GET /users?api-version=2024-01-15

# Useful when you want to pin to exact API behavior
# New features added only in newer date versions
```

## Breaking vs Non-Breaking Changes

### Non-Breaking Changes (No new version needed)

| Change Type | Example | Notes |
|-------------|---------|-------|
| Add optional field | Add `middleName` to user | Existing clients ignore it |
| Add endpoint | Add `GET /analytics` | Doesn't affect existing |
| Add optional parameter | Add `?include=metadata` | Default maintains behavior |
| Add enum value | Add `status: "archived"` | Existing clients may need update |
| Increase limit | Raise max `pageSize` from 100 to 200 | Backwards compatible |
| Add header | Add `X-Request-Id` response header | Clients can ignore |

### Breaking Changes (New version required)

| Change Type | Example | Impact |
|-------------|---------|--------|
| Remove field | Remove `legacyId` | Clients expecting it will break |
| Rename field | `userName` → `username` | Clients using old name break |
| Change type | `age: "25"` → `age: 25` | Type parsing breaks |
| Remove endpoint | Delete `GET /legacy/users` | Clients using it break |
| Add required field | Require `phone` on create | Existing create calls fail |
| Change URL structure | `/user/{id}` → `/users/{id}` | All clients break |
| Change auth method | API key → OAuth | All clients break |

### Gray Area Changes

```yaml
# Adding required field to response
# Technically non-breaking, but...
{
  "id": "123",
  "name": "Test",
  "createdAt": "2024-01-15"  # New required field
}
# Impact: Clients with strict schemas may fail

# Recommendation: Treat as non-breaking but communicate clearly

# Changing error response format
# May break client error handling
# Recommendation: Version error format with API version
```

## Migration Strategies

### Parallel Running

Run both versions simultaneously during migration:

```yaml
Timeline:
  Day 0: v2 launches, v1 still active
  Month 3: v1 deprecated (warnings added)
  Month 6: v1 sunset announced
  Month 12: v1 removed

Communication:
  - Deprecation header: Deprecation: true
  - Sunset header: Sunset: Sat, 15 Jun 2025 00:00:00 GMT
  - Link to migration guide
```

### Gradual Rollout

```yaml
# Phase 1: v2 available but opt-in
/v1/users  # default
/v2/users  # opt-in, beta

# Phase 2: v2 becomes default, v1 deprecated
/v2/users  # default
/v1/users  # deprecated, still works

# Phase 3: v1 removed
/v2/users  # only version
```

### Client Migration Support

```python
# Provide migration helpers
# Document exact changes needed

# Example migration checklist:
"""
## Migrating from v1 to v2

### Breaking Changes
1. `userName` field renamed to `username`
   - Update: Change all references from `response.userName` to `response.username`

2. `created` field now returns ISO-8601 instead of Unix timestamp
   - Update: Use date parser instead of integer multiplication

3. `GET /user/{id}` moved to `GET /users/{id}`
   - Update: Change endpoint path (note: plural 'users')

### New Features in v2
- Pagination now supports cursor-based navigation
- New `include` parameter for embedding related resources
"""
```

## Deprecation Communication

### Response Headers

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 15 Jun 2025 00:00:00 GMT
Link: <https://api.example.com/docs/migration/v1-to-v2>; rel="deprecation"
X-API-Warn: "API version v1 is deprecated. Please migrate to v2."
```

### Documentation

```markdown
## API Version Status

| Version | Status | Sunset Date | Notes |
|---------|--------|-------------|-------|
| v3 | Current | - | Recommended |
| v2 | Supported | 2025-12-01 | Security updates only |
| v1 | Deprecated | 2025-06-01 | No updates, migrate ASAP |

## Migration Guides
- [v1 to v2 Migration Guide](/docs/migration/v1-v2)
- [v2 to v3 Migration Guide](/docs/migration/v2-v3)
```

### Email/Notification

```
Subject: [Action Required] API v1 Sunset on June 15, 2025

Dear Developer,

Our API v1 will be sunset on June 15, 2025. After this date,
all v1 endpoints will return 410 Gone.

Your application "MyApp" made 15,234 requests to v1 endpoints
in the past month.

Action Required:
1. Review the migration guide: [link]
2. Update your integration to use v2
3. Test in our sandbox environment
4. Deploy before June 15, 2025

Need help? Contact api-support@example.com

Timeline:
- Now: v1 deprecated, v2 current
- April 15, 2025: v1 requests return warning headers
- June 15, 2025: v1 endpoints return 410 Gone
```

## Best Practices Summary

### Do

- **Choose one strategy** and stick with it
- **Document versions clearly** in API docs
- **Communicate deprecations** well in advance (6+ months)
- **Provide migration guides** with specific change details
- **Run versions in parallel** during migration
- **Use semantic versioning** principles (major.minor for internal tracking)
- **Default to stable version** when version is omitted

### Don't

- **Mix versioning strategies** (URL + header)
- **Create too many versions** (aim for 2-3 active max)
- **Break without versioning** (even "small" changes)
- **Remove versions abruptly** (always sunset period)
- **Version for every change** (batch breaking changes)
- **Forget backwards compatibility** in non-breaking changes
