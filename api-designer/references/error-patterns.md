# API Error Handling Patterns

Standard patterns for consistent, helpful error responses across APIs.

## Error Response Structure

Every error response follows this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [],
    "requestId": "req-xxx",
    "documentation": "https://..."
  }
}
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `code` | Yes | Machine-readable error code (SCREAMING_SNAKE_CASE) |
| `message` | Yes | Human-readable explanation |
| `details` | No | Array of specific field/validation errors |
| `requestId` | Yes | Unique ID for support/debugging |
| `documentation` | No | Link to error documentation |

## Standard Error Codes

### Authentication Errors (401)

```yaml
AUTH_TOKEN_MISSING:
  message: "No authentication token provided"
  action: "Include Authorization header with Bearer token"
  example:
    error:
      code: "AUTH_TOKEN_MISSING"
      message: "No authentication token provided. Include an Authorization header with your request."
      requestId: "req-abc123"

AUTH_TOKEN_INVALID:
  message: "Token is malformed or signature is invalid"
  action: "Check token format, obtain a new token"
  example:
    error:
      code: "AUTH_TOKEN_INVALID"
      message: "The provided authentication token is invalid. Please obtain a new token."
      requestId: "req-abc123"

AUTH_TOKEN_EXPIRED:
  message: "Token has expired"
  action: "Refresh token or re-authenticate"
  example:
    error:
      code: "AUTH_TOKEN_EXPIRED"
      message: "Your authentication token has expired. Please refresh your token or log in again."
      requestId: "req-abc123"
```

### Authorization Errors (403)

```yaml
PERMISSION_DENIED:
  message: "User lacks required permission"
  action: "Request access from administrator"
  example:
    error:
      code: "PERMISSION_DENIED"
      message: "You don't have permission to access this resource. Required permission: projects.write"
      requestId: "req-abc123"

RESOURCE_ACCESS_DENIED:
  message: "User cannot access this specific resource"
  action: "Verify you have access to this resource"
  example:
    error:
      code: "RESOURCE_ACCESS_DENIED"
      message: "You don't have access to project 'secret-project'. Contact the project owner for access."
      requestId: "req-abc123"

ORGANIZATION_REQUIRED:
  message: "Action requires organization membership"
  action: "Join an organization or create one"
  example:
    error:
      code: "ORGANIZATION_REQUIRED"
      message: "This action requires organization membership. Please join or create an organization."
      requestId: "req-abc123"
```

### Validation Errors (400)

```yaml
VALIDATION_ERROR:
  message: "Request validation failed"
  action: "Check details array for specific field errors"
  example:
    error:
      code: "VALIDATION_ERROR"
      message: "Request validation failed"
      details:
        - field: "email"
          code: "INVALID_FORMAT"
          message: "Must be a valid email address"
        - field: "age"
          code: "OUT_OF_RANGE"
          message: "Must be between 18 and 120"
      requestId: "req-abc123"

INVALID_JSON:
  message: "Request body is not valid JSON"
  action: "Check JSON syntax"
  example:
    error:
      code: "INVALID_JSON"
      message: "Request body contains invalid JSON. Check for syntax errors."
      requestId: "req-abc123"

MISSING_REQUIRED_FIELD:
  message: "Required field is missing"
  action: "Include the required field"
  example:
    error:
      code: "MISSING_REQUIRED_FIELD"
      message: "Required field 'name' is missing"
      details:
        - field: "name"
          code: "REQUIRED_FIELD"
          message: "This field is required"
      requestId: "req-abc123"
```

### Field-Level Error Codes (in details array)

```yaml
REQUIRED_FIELD:
  message: "Field is required"

INVALID_FORMAT:
  message: "Field format is invalid"
  examples:
    - "email: Must be a valid email address"
    - "url: Must be a valid URL"
    - "uuid: Must be a valid UUID"

INVALID_TYPE:
  message: "Field type is wrong"
  examples:
    - "age: Must be a number"
    - "active: Must be a boolean"

OUT_OF_RANGE:
  message: "Value is outside allowed range"
  examples:
    - "age: Must be between 0 and 150"
    - "pageSize: Must be between 1 and 100"

TOO_SHORT:
  message: "String is too short"
  examples:
    - "password: Must be at least 8 characters"
    - "name: Must be at least 1 character"

TOO_LONG:
  message: "String is too long"
  examples:
    - "description: Must be at most 1000 characters"
    - "name: Must be at most 255 characters"

INVALID_ENUM:
  message: "Value not in allowed set"
  examples:
    - "status: Must be one of: active, inactive, pending"
    - "priority: Must be one of: low, medium, high, urgent"

INVALID_PATTERN:
  message: "Value doesn't match required pattern"
  examples:
    - "slug: Must contain only lowercase letters, numbers, and hyphens"
    - "phone: Must match format +1-XXX-XXX-XXXX"
```

### Resource Errors (404, 409)

```yaml
RESOURCE_NOT_FOUND:
  status: 404
  message: "Resource does not exist"
  example:
    error:
      code: "RESOURCE_NOT_FOUND"
      message: "User with ID 'user-123' was not found"
      requestId: "req-abc123"

RESOURCE_ALREADY_EXISTS:
  status: 409
  message: "Resource with identifier already exists"
  example:
    error:
      code: "RESOURCE_ALREADY_EXISTS"
      message: "A user with email 'user@example.com' already exists"
      requestId: "req-abc123"

RESOURCE_CONFLICT:
  status: 409
  message: "Request conflicts with current state"
  example:
    error:
      code: "RESOURCE_CONFLICT"
      message: "Cannot delete project with active tasks. Archive or delete tasks first."
      requestId: "req-abc123"

RESOURCE_LOCKED:
  status: 409
  message: "Resource is locked for modification"
  example:
    error:
      code: "RESOURCE_LOCKED"
      message: "This document is locked for editing by another user"
      requestId: "req-abc123"

VERSION_CONFLICT:
  status: 409
  message: "Optimistic locking conflict"
  example:
    error:
      code: "VERSION_CONFLICT"
      message: "Resource was modified since you last fetched it. Refresh and try again."
      requestId: "req-abc123"
```

### Business Logic Errors (422)

```yaml
OPERATION_NOT_ALLOWED:
  status: 422
  message: "Operation not allowed in current state"
  example:
    error:
      code: "OPERATION_NOT_ALLOWED"
      message: "Cannot publish a draft that has validation errors"
      requestId: "req-abc123"

LIMIT_EXCEEDED:
  status: 422
  message: "Account limit reached"
  example:
    error:
      code: "LIMIT_EXCEEDED"
      message: "You've reached the maximum of 5 projects on the free plan. Upgrade to create more."
      requestId: "req-abc123"

DEPENDENCY_ERROR:
  status: 422
  message: "Cannot complete due to dependency"
  example:
    error:
      code: "DEPENDENCY_ERROR"
      message: "Cannot delete this label as it's used by 15 tasks"
      requestId: "req-abc123"

INVALID_STATE_TRANSITION:
  status: 422
  message: "Invalid state change"
  example:
    error:
      code: "INVALID_STATE_TRANSITION"
      message: "Cannot move task from 'done' to 'in_progress'. Valid transitions: done -> reopened"
      requestId: "req-abc123"
```

### Rate Limiting Errors (429)

```yaml
RATE_LIMIT_EXCEEDED:
  status: 429
  message: "Too many requests"
  headers:
    Retry-After: 60
    X-RateLimit-Limit: 100
    X-RateLimit-Remaining: 0
    X-RateLimit-Reset: 1705312800
  example:
    error:
      code: "RATE_LIMIT_EXCEEDED"
      message: "Rate limit exceeded. Please wait 60 seconds before retrying."
      requestId: "req-abc123"

QUOTA_EXCEEDED:
  status: 429
  message: "Monthly/daily quota exceeded"
  example:
    error:
      code: "QUOTA_EXCEEDED"
      message: "Monthly API quota exceeded. Quota resets on February 1st or upgrade your plan."
      requestId: "req-abc123"
```

### Server Errors (500, 502, 503)

```yaml
INTERNAL_ERROR:
  status: 500
  message: "Unexpected server error"
  example:
    error:
      code: "INTERNAL_ERROR"
      message: "An unexpected error occurred. Our team has been notified. Please try again later."
      requestId: "req-abc123"

SERVICE_UNAVAILABLE:
  status: 503
  message: "Service temporarily unavailable"
  example:
    error:
      code: "SERVICE_UNAVAILABLE"
      message: "Service is temporarily unavailable for maintenance. Please try again in a few minutes."
      requestId: "req-abc123"

DEPENDENCY_FAILURE:
  status: 502
  message: "Upstream service failed"
  example:
    error:
      code: "DEPENDENCY_FAILURE"
      message: "Unable to process request due to a temporary service issue. Please try again."
      requestId: "req-abc123"
```

## Error Response Patterns

### Pattern 1: Simple Error

For errors without field-level details:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 'user-123' was not found",
    "requestId": "req-abc123"
  }
}
```

### Pattern 2: Validation Error with Details

For validation failures with multiple field errors:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Must be at least 8 characters"
      }
    ],
    "requestId": "req-abc123"
  }
}
```

### Pattern 3: Error with Nested Field

For validation errors in nested objects:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "address.zipCode",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid 5-digit ZIP code"
      },
      {
        "field": "contacts[0].email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req-abc123"
  }
}
```

### Pattern 4: Error with Recovery Guidance

For errors that can be resolved by the user:

```json
{
  "error": {
    "code": "LIMIT_EXCEEDED",
    "message": "You've reached the maximum of 5 projects on the free plan",
    "details": [
      {
        "code": "UPGRADE_AVAILABLE",
        "message": "Upgrade to Pro plan to create unlimited projects"
      }
    ],
    "requestId": "req-abc123",
    "documentation": "https://api.example.com/docs/pricing"
  }
}
```

## Implementation Guidelines

### 1. Always Include Request ID

Every error response MUST include a `requestId` for debugging:

```python
# Generate at request entry point
request_id = f"req-{uuid.uuid4().hex[:12]}"
# Include in all logs and error responses
```

### 2. Don't Leak Internal Details

```python
# ✗ WRONG: Exposes internal implementation
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "PostgreSQL connection failed: FATAL: password authentication failed"
  }
}

# ✓ CORRECT: User-friendly message, details logged server-side
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "requestId": "req-abc123"
  }
}
# Server logs: "req-abc123: PostgreSQL connection failed: FATAL: ..."
```

### 3. Be Specific About What's Wrong

```python
# ✗ WRONG: Vague error
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request"
  }
}

# ✓ CORRECT: Specific and actionable
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address. Example: user@example.com"
      }
    ]
  }
}
```

### 4. Use Consistent Status Codes

| Code | Use For |
|------|---------|
| 400 | Malformed request, validation errors |
| 401 | Missing or invalid authentication |
| 403 | Valid auth but insufficient permissions |
| 404 | Resource doesn't exist |
| 409 | Conflict with current state |
| 422 | Valid syntax but semantic error |
| 429 | Rate limiting |
| 500 | Unexpected server error |

### 5. Provide Documentation Links

For complex errors, link to documentation:

```json
{
  "error": {
    "code": "WEBHOOK_SIGNATURE_INVALID",
    "message": "Webhook signature verification failed",
    "documentation": "https://api.example.com/docs/webhooks#signature-verification",
    "requestId": "req-abc123"
  }
}
```

## Error Logging Best Practices

### Log Levels by Error Type

| Error Type | Log Level | Example |
|------------|-----------|---------|
| Validation (400) | INFO | User submitted invalid data |
| Auth (401/403) | WARN | Potential security issue |
| Not Found (404) | DEBUG | Normal for some flows |
| Conflict (409) | INFO | Expected business condition |
| Rate Limit (429) | WARN | May indicate abuse |
| Server Error (500) | ERROR | Requires investigation |

### Structured Logging

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "ERROR",
  "requestId": "req-abc123",
  "userId": "user-456",
  "method": "POST",
  "path": "/api/v1/projects",
  "statusCode": 500,
  "errorCode": "INTERNAL_ERROR",
  "errorMessage": "Database connection timeout",
  "stackTrace": "...",
  "duration_ms": 5023
}
```
