# API Contract Template

Specification format for defining API interfaces between systems.

## Contract Structure

```yaml
# API Contract: [Resource Name]
# Version: [X.Y.Z]
# Last Updated: [YYYY-MM-DD]
# Owner: [Team/Person]

base_path: /api/v1/[resource]

authentication:
  type: [Bearer JWT | API Key | None]
  header: [Authorization | X-API-Key]

endpoints:
  - name: [Operation Name]
    method: [GET | POST | PUT | PATCH | DELETE]
    path: [/path/{param}]
    description: [What this endpoint does]
    
    request:
      path_params:
        - name: [param_name]
          type: [string | uuid | integer]
          description: [What it is]
          
      query_params:
        - name: [param_name]
          type: [string | integer | boolean]
          required: [true | false]
          default: [value]
          description: [What it is]
          
      headers:
        - name: [Header-Name]
          required: [true | false]
          description: [Purpose]
          
      body:
        content_type: application/json
        schema:
          field_name:
            type: [string | integer | boolean | array | object]
            required: [true | false]
            constraints: [max_length, min, max, pattern, enum values]
            description: [What it is]
            
    response:
      success:
        status: [200 | 201 | 204]
        body:
          field_name:
            type: [type]
            description: [What it is]
            
      errors:
        - status: [4XX | 5XX]
          code: [ERR_CODE]
          when: [Condition that triggers this error]
          body:
            error: [code]
            message: [User-facing message]
            details: [Additional info if applicable]
```

---

## Full Example: User Resource

```yaml
# API Contract: Users
# Version: 1.0.0
# Last Updated: 2025-01-15
# Owner: Backend Team

base_path: /api/v1/users

authentication:
  type: Bearer JWT
  header: Authorization

rate_limiting:
  requests_per_minute: 100
  burst: 20

common_headers:
  request:
    - name: Authorization
      required: true
      format: "Bearer {jwt_token}"
    - name: Content-Type
      required: true
      value: application/json
    - name: X-Request-ID
      required: false
      description: Client-generated request ID for tracing
      
  response:
    - name: X-Request-ID
      description: Echoed from request or generated
    - name: X-RateLimit-Remaining
      description: Remaining requests in current window

# ============================================
# ENDPOINTS
# ============================================

endpoints:

  # ------------------------------------------
  # CREATE USER
  # ------------------------------------------
  - name: Create User
    method: POST
    path: /
    description: Register a new user account
    
    request:
      body:
        content_type: application/json
        schema:
          email:
            type: string
            required: true
            constraints:
              format: email
              max_length: 255
            description: User's email address (must be unique)
            example: "user@example.com"
            
          password:
            type: string
            required: true
            constraints:
              min_length: 12
              max_length: 128
              pattern: "Must contain uppercase, lowercase, number"
            description: User's password
            example: "SecurePass123!"
            
          name:
            type: string
            required: true
            constraints:
              min_length: 1
              max_length: 100
            description: User's display name
            example: "Jane Smith"
            
          metadata:
            type: object
            required: false
            description: Optional key-value metadata
            example: {"referral_code": "ABC123"}
    
    response:
      success:
        status: 201
        headers:
          Location: /api/v1/users/{id}
        body:
          id:
            type: uuid
            description: Unique user identifier
            example: "550e8400-e29b-41d4-a716-446655440000"
          email:
            type: string
            example: "user@example.com"
          name:
            type: string
            example: "Jane Smith"
          status:
            type: string
            enum: [pending, active, suspended]
            example: "pending"
          created_at:
            type: datetime
            format: ISO 8601
            example: "2025-01-15T10:30:00Z"
            
      errors:
        - status: 400
          code: ERR_VALIDATION
          when: Request body fails validation
          body:
            error: "ERR_VALIDATION"
            message: "Validation failed"
            details:
              - field: "email"
                message: "Invalid email format"
                
        - status: 409
          code: ERR_DUPLICATE_EMAIL
          when: Email already registered
          body:
            error: "ERR_DUPLICATE_EMAIL"
            message: "An account with this email already exists"
            
        - status: 429
          code: ERR_RATE_LIMITED
          when: Too many requests
          body:
            error: "ERR_RATE_LIMITED"
            message: "Too many requests. Please wait before trying again."

  # ------------------------------------------
  # GET USER
  # ------------------------------------------
  - name: Get User
    method: GET
    path: /{user_id}
    description: Retrieve user details by ID
    
    request:
      path_params:
        - name: user_id
          type: uuid
          description: User's unique identifier
          example: "550e8400-e29b-41d4-a716-446655440000"
          
      headers:
        - name: Authorization
          required: true
          
    response:
      success:
        status: 200
        body:
          id:
            type: uuid
          email:
            type: string
          name:
            type: string
          status:
            type: string
            enum: [pending, active, suspended]
          created_at:
            type: datetime
          updated_at:
            type: datetime
            
      errors:
        - status: 401
          code: ERR_UNAUTHORIZED
          when: Missing or invalid JWT
          body:
            error: "ERR_UNAUTHORIZED"
            message: "Authentication required"
            
        - status: 403
          code: ERR_FORBIDDEN
          when: User accessing another user's data (non-admin)
          body:
            error: "ERR_FORBIDDEN"
            message: "You don't have permission to access this resource"
            
        - status: 404
          code: ERR_NOT_FOUND
          when: User ID doesn't exist
          body:
            error: "ERR_NOT_FOUND"
            message: "User not found"

  # ------------------------------------------
  # LIST USERS
  # ------------------------------------------
  - name: List Users
    method: GET
    path: /
    description: List users with pagination and filtering (admin only)
    
    request:
      query_params:
        - name: page
          type: integer
          required: false
          default: 1
          constraints:
            min: 1
          description: Page number
          
        - name: per_page
          type: integer
          required: false
          default: 20
          constraints:
            min: 1
            max: 100
          description: Items per page
          
        - name: status
          type: string
          required: false
          constraints:
            enum: [pending, active, suspended]
          description: Filter by status
          
        - name: search
          type: string
          required: false
          constraints:
            min_length: 2
          description: Search by name or email
          
        - name: sort
          type: string
          required: false
          default: created_at
          constraints:
            enum: [created_at, name, email]
          description: Sort field
          
        - name: order
          type: string
          required: false
          default: desc
          constraints:
            enum: [asc, desc]
          description: Sort order
          
    response:
      success:
        status: 200
        body:
          data:
            type: array
            items:
              type: object
              properties:
                id: uuid
                email: string
                name: string
                status: string
                created_at: datetime
          pagination:
            type: object
            properties:
              page:
                type: integer
                example: 1
              per_page:
                type: integer
                example: 20
              total_items:
                type: integer
                example: 150
              total_pages:
                type: integer
                example: 8
              
      errors:
        - status: 401
          code: ERR_UNAUTHORIZED
          when: Missing or invalid JWT
          
        - status: 403
          code: ERR_FORBIDDEN
          when: Non-admin user

  # ------------------------------------------
  # UPDATE USER
  # ------------------------------------------
  - name: Update User
    method: PATCH
    path: /{user_id}
    description: Update user details (partial update)
    
    request:
      path_params:
        - name: user_id
          type: uuid
          
      body:
        content_type: application/json
        schema:
          name:
            type: string
            required: false
            constraints:
              min_length: 1
              max_length: 100
          metadata:
            type: object
            required: false
            
    response:
      success:
        status: 200
        body:
          id: uuid
          email: string
          name: string
          status: string
          updated_at: datetime
          
      errors:
        - status: 400
          code: ERR_VALIDATION
          when: Invalid field values
          
        - status: 401
          code: ERR_UNAUTHORIZED
          
        - status: 403
          code: ERR_FORBIDDEN
          
        - status: 404
          code: ERR_NOT_FOUND

  # ------------------------------------------
  # DELETE USER
  # ------------------------------------------
  - name: Delete User
    method: DELETE
    path: /{user_id}
    description: Soft delete a user account
    
    request:
      path_params:
        - name: user_id
          type: uuid
          
    response:
      success:
        status: 204
        body: null
        
      errors:
        - status: 401
          code: ERR_UNAUTHORIZED
          
        - status: 403
          code: ERR_FORBIDDEN
          
        - status: 404
          code: ERR_NOT_FOUND
```

---

## Error Response Standard

All errors follow this format:

```json
{
  "error": "ERR_CODE",
  "message": "Human-readable message",
  "details": {
    // Optional additional context
  },
  "request_id": "uuid-for-tracing"
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| ERR_VALIDATION | 400 | Request validation failed |
| ERR_MALFORMED | 400 | Request body is not valid JSON |
| ERR_UNAUTHORIZED | 401 | Authentication required or invalid |
| ERR_TOKEN_EXPIRED | 401 | JWT has expired |
| ERR_FORBIDDEN | 403 | Authenticated but not authorized |
| ERR_NOT_FOUND | 404 | Resource doesn't exist |
| ERR_METHOD_NOT_ALLOWED | 405 | HTTP method not supported |
| ERR_CONFLICT | 409 | Resource state conflict |
| ERR_DUPLICATE | 409 | Unique constraint violation |
| ERR_GONE | 410 | Resource permanently deleted |
| ERR_UNPROCESSABLE | 422 | Semantic validation error |
| ERR_RATE_LIMITED | 429 | Too many requests |
| ERR_INTERNAL | 500 | Unexpected server error |
| ERR_SERVICE_UNAVAILABLE | 503 | Temporary outage |
| ERR_TIMEOUT | 504 | Upstream timeout |

---

## Pagination Standard

### Request Parameters

```yaml
page:
  type: integer
  default: 1
  min: 1
  
per_page:
  type: integer
  default: 20
  min: 1
  max: 100
```

### Response Format

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Versioning

### URL Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

### Breaking Change Policy

Increment major version when:
- Removing endpoints
- Removing required fields from response
- Adding required fields to request
- Changing field types
- Changing authentication mechanism

Non-breaking changes (same version):
- Adding optional request fields
- Adding response fields
- Adding new endpoints
- Adding new error codes
