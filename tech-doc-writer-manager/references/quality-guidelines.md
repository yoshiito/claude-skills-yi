# Documentation Quality Guidelines

This reference contains standards for producing high-quality technical documentation.

## Metadata Schema Reference

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | string | Human-readable document title | "User Authentication API" |
| `doc_type` | enum | Document category | api, integration, testing, architecture, runbook, guide |
| `version` | semver | Document version | "1.2.0" |
| `status` | enum | Publication status | draft, review, published, deprecated |
| `created` | date | Creation date | "2024-01-15" |
| `last_updated` | date | Last modification | "2024-03-20" |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `author` | string | Primary author |
| `reviewers` | array | List of reviewers |
| `related_docs` | array | Cross-referenced documents |
| `tags` | array | Searchable tags |
| `deprecated_by` | string | Path to replacement doc |

### Status Lifecycle

```
draft → review → published → deprecated
  ↑       │
  └───────┘ (revisions)
```

**draft**: Initial creation, not ready for use
**review**: Awaiting technical review
**published**: Approved and current
**deprecated**: Superseded or no longer relevant

## Writing Standards

### Document Structure

1. **Title**: Clear, specific, searchable
2. **Overview**: 1-2 paragraphs explaining purpose
3. **Prerequisites**: What reader needs before starting
4. **Main Content**: Logical sections with examples
5. **Troubleshooting**: Common issues and solutions
6. **See Also**: Related documentation links

### Language Guidelines

**Do:**
- Use active voice: "The API returns a JSON response"
- Use imperative mood for instructions: "Configure the environment variables"
- Define acronyms on first use: "Content Delivery Network (CDN)"
- Include concrete examples for abstract concepts

**Avoid:**
- Passive constructions: "A JSON response is returned"
- Vague language: "It might be necessary to..."
- Undefined jargon
- Assumptions about reader knowledge

### Code Examples

Always include:
- Language identifier in code blocks
- Complete, runnable examples where possible
- Expected output or response
- Error handling patterns

```python
# Good: Complete with context
def fetch_user(user_id: str) -> dict:
    """Fetch user by ID from the API."""
    response = requests.get(f"{API_URL}/users/{user_id}")
    response.raise_for_status()
    return response.json()

# Usage
user = fetch_user("usr_abc123")
print(user["email"])  # Output: user@example.com
```

## Staleness Thresholds

| Doc Type | Review Frequency | Stale Threshold |
|----------|------------------|-----------------|
| api | Quarterly | 90 days |
| integration | Quarterly | 90 days |
| runbook | Monthly | 60 days |
| architecture | Semi-annually | 180 days |
| testing | Quarterly | 90 days |
| guide | Semi-annually | 180 days |

## Cross-Reference Format

Use relative paths for internal links:

```markdown
See [Authentication Guide](../guides/authentication.md) for setup instructions.
```

In metadata:

```yaml
related_docs:
  - path: "../guides/authentication.md"
    relationship: "references"
  - path: "./deprecated-v1.md"
    relationship: "supersedes"
```

### Relationship Types

- **extends**: Builds upon the referenced doc
- **implements**: Provides implementation for spec
- **references**: General reference
- **supersedes**: Replaces deprecated doc
