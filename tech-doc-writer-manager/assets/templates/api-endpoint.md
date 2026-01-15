---
title: "[Endpoint Name] API"
doc_type: api
version: "1.0.0"
status: draft
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
author: ""
reviewers: []
related_docs: []
tags: [api, rest]
---

# [Endpoint Name] API

Brief description of what this endpoint does and its primary use case.

## Endpoint

```
[METHOD] /api/v1/[resource]
```

## Authentication

Describe authentication requirements (e.g., Bearer token, API key, OAuth).

## Request

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer token |
| `Content-Type` | Yes | `application/json` |

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Resource identifier |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 20 | Maximum results to return |
| `offset` | integer | No | 0 | Pagination offset |

### Request Body

```json
{
  "field_name": "string",
  "nested_object": {
    "property": "value"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | Yes | Description of field |
| `nested_object` | object | No | Optional nested data |

## Response

### Success Response (200 OK)

```json
{
  "id": "abc123",
  "field_name": "value",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `field_name` | string | Description |
| `created_at` | datetime | ISO 8601 creation timestamp |
| `updated_at` | datetime | ISO 8601 last update timestamp |

## Error Responses

### 400 Bad Request

Returned when request validation fails.

```json
{
  "error": "validation_error",
  "message": "Invalid request body",
  "details": [
    {
      "field": "field_name",
      "error": "Required field missing"
    }
  ]
}
```

### 401 Unauthorized

Returned when authentication fails or token is missing.

```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token"
}
```

### 404 Not Found

Returned when the requested resource does not exist.

```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error

Returned when an unexpected server error occurs.

```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred"
}
```

## Examples

### Example Request

```bash
curl -X POST https://api.example.com/api/v1/resource \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "field_name": "example value"
  }'
```

### Example Response

```json
{
  "id": "res_abc123",
  "field_name": "example value",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Rate Limits

| Tier | Requests/Minute | Burst |
|------|-----------------|-------|
| Free | 60 | 10 |
| Pro | 600 | 100 |
| Enterprise | 6000 | 1000 |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |

## See Also

- [Related Endpoint](./related-endpoint.md)
- [Authentication Guide](../guides/authentication.md)
