# API Naming Conventions

Consistent naming patterns for API endpoints, parameters, and response fields.

## Quick Reference

| Element | Convention | Example |
|---------|------------|---------|
| Endpoint paths | kebab-case, plural nouns | `/user-profiles` |
| Path parameters | camelCase | `/{userId}` |
| Query parameters | camelCase | `?sortBy=createdAt` |
| Request body fields | camelCase | `{ "firstName": "..." }` |
| Response fields | camelCase | `{ "createdAt": "..." }` |
| HTTP headers | Title-Case | `X-Request-Id` |
| Error codes | SCREAMING_SNAKE_CASE | `VALIDATION_ERROR` |

## Endpoint Naming

### Use Nouns, Not Verbs

```yaml
# ✓ CORRECT: Nouns representing resources
GET /users           # Get users (the verb is GET)
POST /users          # Create user (the verb is POST)
GET /orders          # Get orders
DELETE /orders/{id}  # Delete order

# ✗ WRONG: Verbs in path
GET /getUsers
POST /createUser
GET /fetchOrders
POST /deleteOrder
```

### Use Plural Nouns

```yaml
# ✓ CORRECT: Plural for collections
GET /users
GET /users/{id}
GET /products
GET /products/{id}

# ✗ WRONG: Singular
GET /user
GET /user/{id}
GET /product
GET /product/{id}
```

### Use kebab-case for Multi-Word Resources

```yaml
# ✓ CORRECT: kebab-case
GET /user-profiles
GET /order-items
GET /api-keys

# ✗ WRONG: Other case styles
GET /userProfiles      # camelCase
GET /user_profiles     # snake_case
GET /UserProfiles      # PascalCase
```

### Nest Related Resources Appropriately

```yaml
# ✓ CORRECT: Logical nesting (1-2 levels max)
GET /users/{userId}/orders
GET /orders/{orderId}/items
POST /teams/{teamId}/members

# ⚠ CAUTION: Deep nesting (hard to use)
GET /organizations/{orgId}/teams/{teamId}/projects/{projectId}/tasks
# Consider: GET /tasks?projectId={projectId}

# ✗ WRONG: Unrelated nesting
GET /users/{userId}/settings/{settingId}/logs
# These aren't naturally hierarchical
```

### Action Endpoints (When REST Doesn't Fit)

For operations that don't map cleanly to CRUD:

```yaml
# Use verb as sub-resource for actions
POST /users/{id}/activate        # State change
POST /users/{id}/deactivate
POST /orders/{id}/cancel
POST /documents/{id}/publish
POST /reports/{id}/generate

# Bulk operations
POST /users/bulk-delete
POST /orders/bulk-update

# Complex queries (when GET params aren't enough)
POST /users/search
POST /analytics/query

# ✗ WRONG: Verb in main path
POST /activateUser/{id}
POST /cancelOrder/{id}
```

## Query Parameters

### Use camelCase

```yaml
# ✓ CORRECT: camelCase
?sortBy=createdAt
?pageSize=20
?includeDeleted=true
?startDate=2024-01-01

# ✗ WRONG: Other case styles
?sort_by=createdAt     # snake_case
?PageSize=20           # PascalCase
?INCLUDE_DELETED=true  # SCREAMING_CASE
```

### Standard Parameters

```yaml
# Pagination
page: 1              # Page number (1-indexed)
pageSize: 20         # Items per page (default: 20)
limit: 20            # Alternative to pageSize
offset: 0            # Alternative to page
cursor: abc123       # For cursor-based pagination

# Sorting
sortBy: createdAt    # Field to sort by
sortOrder: desc      # asc or desc
sort: -createdAt     # Combined (- for desc, + for asc)

# Filtering
status: active       # Exact match
search: keyword      # Full-text search
q: keyword           # Shorthand for search

# Date ranges
createdAfter: 2024-01-01
createdBefore: 2024-12-31
startDate: 2024-01-01
endDate: 2024-12-31

# Includes/expands
include: author,comments   # Include related resources
fields: id,name,email      # Sparse fieldsets (only these fields)
expand: organization       # Expand nested objects
```

### Boolean Parameters

```yaml
# ✓ CORRECT: Use true/false strings
?active=true
?includeArchived=false

# Also acceptable: presence-based
?archived          # Presence means true
# Absence means false

# ✗ WRONG: Numeric booleans
?active=1
?archived=0
```

## Request/Response Body Fields

### Use camelCase

```yaml
# ✓ CORRECT: camelCase for all fields
{
  "id": "123",
  "firstName": "Jane",
  "lastName": "Doe",
  "emailAddress": "jane@example.com",
  "createdAt": "2024-01-15T10:30:00Z",
  "isActive": true,
  "orderCount": 5
}

# ✗ WRONG: Other case styles
{
  "first_name": "Jane",      # snake_case
  "FirstName": "Jane",       # PascalCase
  "FIRST_NAME": "Jane"       # SCREAMING_CASE
}
```

### Naming Patterns for Common Fields

```yaml
# Identifiers
id: "uuid-or-string"           # Primary identifier
externalId: "partner-123"      # External system ID
slug: "my-resource"            # URL-friendly identifier

# Timestamps (always ISO-8601)
createdAt: "2024-01-15T10:30:00Z"
updatedAt: "2024-01-15T10:30:00Z"
deletedAt: "2024-01-15T10:30:00Z"   # For soft deletes
publishedAt: "2024-01-15T10:30:00Z"
expiresAt: "2024-01-15T10:30:00Z"

# Booleans (use is/has/can prefix)
isActive: true
isVerified: false
hasChildren: true
canEdit: true
allowNotifications: true

# Counts
count: 10              # Generic count
totalCount: 100        # Total (for pagination)
itemCount: 5           # Specific item count
orderCount: 3          # Domain-specific count

# Related resources
userId: "user-123"     # Foreign key (ID only)
user: { ... }          # Embedded object
users: [ ... ]         # Collection

# Metadata
metadata: { ... }      # Generic key-value
tags: ["tag1", "tag2"] # Labels/tags
attributes: { ... }    # Custom attributes
```

### Nested Objects

```yaml
# ✓ CORRECT: Flat when possible
{
  "id": "order-123",
  "customerName": "Jane Doe",
  "customerEmail": "jane@example.com",
  "shippingStreet": "123 Main St",
  "shippingCity": "San Francisco"
}

# ✓ ALSO CORRECT: Nested for logical grouping
{
  "id": "order-123",
  "customer": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "shipping": {
    "street": "123 Main St",
    "city": "San Francisco"
  }
}

# Choose based on:
# - Reusability (nested if address is reused)
# - Complexity (flat for simple cases)
# - API consistency (match existing patterns)
```

## HTTP Headers

### Custom Headers

```yaml
# Use X- prefix (though deprecated, still common)
# Use Title-Case
X-Request-Id: "req-abc123"
X-Correlation-Id: "corr-xyz789"
X-Api-Version: "2"
X-Rate-Limit-Remaining: "95"

# Standard headers (follow spec)
Content-Type: application/json
Authorization: Bearer token123
Accept: application/json
Cache-Control: no-cache
```

### Request ID Pattern

```yaml
# Always return request ID for debugging
# Request:
X-Request-Id: "client-provided-id"  # Optional, client can provide

# Response:
X-Request-Id: "req-abc123"          # Server always returns one
```

## Error Codes

### Use SCREAMING_SNAKE_CASE

```yaml
# ✓ CORRECT: SCREAMING_SNAKE_CASE
VALIDATION_ERROR
RESOURCE_NOT_FOUND
AUTH_TOKEN_EXPIRED
PERMISSION_DENIED
RATE_LIMIT_EXCEEDED

# ✗ WRONG: Other styles
ValidationError          # PascalCase
validation_error         # snake_case
validation-error         # kebab-case
```

### Hierarchical Codes

```yaml
# Group related codes with prefixes
AUTH_TOKEN_MISSING
AUTH_TOKEN_INVALID
AUTH_TOKEN_EXPIRED

VALIDATION_REQUIRED_FIELD
VALIDATION_INVALID_FORMAT
VALIDATION_OUT_OF_RANGE

RESOURCE_NOT_FOUND
RESOURCE_ALREADY_EXISTS
RESOURCE_LOCKED
```

## Consistency Rules

### Be Consistent Within Your API

```yaml
# If you use createdAt, always use createdAt
# ✗ WRONG: Mixing timestamp names
{
  "createdAt": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",  # Inconsistent
  "deleted": "2024-01-15T10:30:00Z"       # Inconsistent
}

# ✓ CORRECT: Consistent pattern
{
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z",
  "deletedAt": "2024-01-15T10:30:00Z"
}
```

### Match Industry Conventions

```yaml
# Common conventions to follow:
id: "string"           # Not: identifier, uuid, key
email: "user@..."      # Not: emailAddress, mail
name: "string"         # Not: title (for person names)
createdAt: "ISO-8601"  # Not: created, createTime, dateCreated
status: "active"       # Not: state (unless state machine context)
type: "invoice"        # Not: kind, category (for discriminators)
```

### Document Your Conventions

Create a style guide for your API:

```markdown
## Our API Conventions

### Timestamps
- All timestamps use ISO-8601 format with UTC timezone
- Field names end with `At` suffix: createdAt, updatedAt, deletedAt

### Identifiers
- Primary IDs are UUIDs stored as strings
- Foreign keys use `{resource}Id` format: userId, orderId

### Booleans
- Prefix with `is`, `has`, `can`, or `allow`
- Examples: isActive, hasAccess, canEdit, allowNotifications

### Collections
- Always use plural nouns: users, orders, items
- Pagination uses `page` and `pageSize` parameters
```

## Anti-Patterns to Avoid

```yaml
# ✗ Inconsistent casing
GET /user-profiles    # kebab-case
GET /orderItems       # camelCase (inconsistent!)

# ✗ Verbs in resource names
GET /getUserById/{id}
POST /createNewOrder

# ✗ Unnecessary nesting
GET /api/v1/resources/users/profiles/{id}/details/extended

# ✗ Ambiguous names
GET /data             # What data?
GET /items            # What items?
GET /list             # List of what?

# ✗ Abbreviations (unless universal)
GET /usrs             # Not clear
GET /prods            # Not clear
# OK: id, url, api (universally understood)

# ✗ Redundant resource type in name
{
  "userId": "123",
  "userName": "jane",     # Just use "name"
  "userEmail": "..."      # Just use "email"
}
```
