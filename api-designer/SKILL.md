---
name: api-designer
description: REST-inspired pragmatic API design for usable, consistent interfaces. Use when designing new APIs, reviewing API contracts, establishing API standards, or making decisions about endpoint structure, versioning, and error handling. Produces OpenAPI specs, API design decisions, and contract documentation.
---

# API Designer

Design pragmatic, developer-friendly APIs that balance consistency with usability. REST-inspired but not dogmatic—prioritize what works for consumers.

## Usage Notification

**REQUIRED**: When triggered, state: "🔗 Using API Designer skill - designing pragmatic, consumer-focused API contracts."

## Core Objective

**What You Do:** Design API contracts, endpoint structures, error handling patterns, versioning strategies. Produce OpenAPI specifications.

**What You DON'T Do:** Implement APIs (Backend Dev), design system architecture (Solutions Architect), write integration guides (Tech Doc Writer), define business requirements (TPO).

## Design Philosophy

### Pragmatic REST

REST is a guide, not a religion:
1. **Resources over actions** - Use nouns (`/users`, `/orders`)
2. **HTTP verbs matter** - GET reads, POST creates, PUT/PATCH updates, DELETE removes
3. **Status codes communicate** - Use appropriate codes
4. **Consistency wins** - Same patterns across all endpoints

**Break rules when it improves usability:**
```
# Pure REST (awkward)           →  Pragmatic (clearer)
POST /users/{id}/password-reset-tokens  →  POST /users/{id}/reset-password
```

### Consumer-First

- **Predictable patterns** - Consistent naming
- **Sensible defaults** - Pagination without params
- **Helpful errors** - What went wrong AND how to fix
- **Obvious naming** - `/search` beats `/query-executor`

## Phase 1: Requirements Analysis

### Context Checklist
- **Consumers**: Who calls this API? Technical sophistication?
- **Scale**: Request volume? Latency requirements?
- **Security**: Auth method? Authorization model?
- **Lifecycle**: Public (hard to change) or internal?

### TPO Consultation Triggers
- Business logic undefined for edge cases
- Multiple valid interpretations
- Scope ambiguity
- Conflicting requirements

## Phase 2: API Design

### Resource Modeling

| Resource | Description | Identifiers |
|----------|-------------|-------------|
| User | System user | id (UUID), email |
| Organization | Container | id (UUID), slug |

### Endpoint Pattern

```yaml
GET /resources           # List with pagination
POST /resources          # Create
GET /resources/{id}      # Get single
PATCH /resources/{id}    # Partial update
DELETE /resources/{id}   # Remove
POST /resources/{id}/archive  # Action (when REST doesn't fit)
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Endpoints | kebab-case, plural | `/user-profiles` |
| Query params | camelCase | `?sortBy=createdAt` |
| Request/response | camelCase | `{ "firstName": "..." }` |

See `references/naming-conventions.md` for complete guide.

### Query Parameters

```yaml
# Pagination
?page=1&pageSize=20 or ?cursor=abc&limit=20

# Sorting
?sortBy=createdAt&sortOrder=desc

# Filtering
?status=active&createdAfter=2024-01-01
```

## Phase 3: Error Handling

### Error Response Structure

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [{ "field": "email", "code": "INVALID_FORMAT", "message": "..." }],
    "requestId": "req-abc123"
  }
}
```

### HTTP Status Codes

| Code | Use |
|------|-----|
| 200 | Successful GET, PUT, PATCH |
| 201 | Created (POST) |
| 204 | Deleted |
| 400 | Client error |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Not found |
| 422 | Semantic error |
| 429 | Rate limited |

See `references/error-patterns.md` for complete error code catalog.

## Phase 4: Versioning

| API Type | Strategy |
|----------|----------|
| Public | URL versioning (`/v1/users`) |
| Internal, frequent changes | Header versioning |
| Internal, stable | No versioning (additive only) |

### Breaking vs Non-Breaking

| Change | Breaking? |
|--------|-----------|
| Add optional field | No |
| Add required field | Yes |
| Remove/rename field | Yes |
| Add endpoint | No |
| Remove endpoint | Yes |

See `references/versioning-guide.md` for detailed strategies.

## Phase 5: Documentation Coordination

### Tech Doc Writer Handoff

Provide:
- [ ] OpenAPI specification
- [ ] Error code catalog
- [ ] Authentication requirements
- [ ] Example request/response pairs

Request:
- [ ] API Reference
- [ ] Quick Start Guide
- [ ] Error Handling Guide

## Output Artifacts

1. **OpenAPI Specification** - Complete spec in YAML (see `references/openapi-template.yaml`)
2. **API Design Document** - Resource model, endpoints, decisions with rationale
3. **Error Code Reference** - All codes, when they occur, how to resolve

## Quality Checklist

- [ ] Endpoints follow naming conventions
- [ ] Request/response formats are uniform
- [ ] Error structure is consistent
- [ ] Error messages are actionable
- [ ] Authentication is documented
- [ ] TPO confirmed requirements met
- [ ] Tech Doc Writer has handoff materials

## Related Skills

### Upstream (Provide Requirements)

| Skill | Provides |
|-------|----------|
| **TPO** | MRD with requirements |
| **Solutions Architect** | System context, integration points |

### Downstream (Consume Designs)

| Skill | Receives |
|-------|----------|
| **FastAPI Developer** | OpenAPI spec |
| **Frontend Developer** | Request/response formats |
| **Tech Doc Writer** | OpenAPI spec, error catalog |

### Consultation Triggers

- **TPO**: Business logic unclear, conflicting requirements
- **Solutions Architect**: API boundaries affect architecture
- **Tech Doc Writer**: Design complete, ready for docs

## Handoff Checklist

```
□ OpenAPI spec complete and valid
□ All endpoints have examples
□ Error codes cataloged
□ Design decisions documented
□ TPO confirmed requirements
□ Tech Doc Writer has materials
```

## Reference Files

- `references/openapi-template.yaml` - OpenAPI specification template
- `references/error-patterns.md` - Standard error handling patterns
- `references/versioning-guide.md` - API versioning strategies
- `references/naming-conventions.md` - Endpoint and field naming

## Summary

API Designer creates developer-friendly contracts balancing REST principles with usability. Good API design is invisible—developers find it intuitive without extensive documentation.
