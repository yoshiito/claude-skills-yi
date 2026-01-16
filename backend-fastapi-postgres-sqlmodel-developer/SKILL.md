---
name: backend-fastapi-postgres-sqlmodel-developer
description: Systematic workflow for designing and implementing CRUD APIs using FastAPI, PostgreSQL, and SQLModel ORM. Use when creating new REST API endpoints, designing database schemas, implementing CRUD operations, or adding new resources to existing FastAPI applications. Guides through requirements gathering, pattern exploration, planning, documentation-first development, implementation, and verification with comprehensive test coverage. Includes guidance on when to use raw SQL vs ORM.
---

# FastAPI + PostgreSQL + SQLModel Developer

Build production-ready CRUD APIs following a systematic, documentation-first workflow.

## Tech Stack

- **FastAPI**: Python web framework with automatic OpenAPI docs
- **PostgreSQL**: Relational database with strong consistency
- **SQLModel**: Pydantic-based ORM combining SQLAlchemy and Pydantic
- **Pytest**: Testing framework with async support

## Raw SQL vs ORM Decision

**DEFAULT**: Use SQLModel ORM for 95% of operations.

| Use SQLModel ORM | Use Raw SQL |
|------------------|-------------|
| Standard CRUD | Complex aggregations (window functions) |
| Simple filters | PostgreSQL-specific (JSONB, full-text) |
| Joins with relationships | Bulk operations (1000+ rows) |
| Type-safe queries | Performance-critical with N+1 issues |

See `references/raw-sql-vs-orm.md` for detailed decision framework and examples.

## Workflow Overview

Follow these phases in order:

1. **Requirements Gathering** - Resource, fields, relationships, constraints
2. **Explore Existing Patterns** - Review codebase architecture
3. **Create Plan File** - Document design in `.plan/` directory
4. **Documentation First** - Update API docs before implementation
5. **Implementation** - Model → DDL → Routes → Tests
6. **Verification** - Run comprehensive checklist

## Phase 1: Requirements Gathering

### Resource Identity
- Resource name (singular/plural)
- Primary use case
- User story

### Fields and Schema
For each field: Name, Type, Required?, Constraints, Defaults, Arrays?, Enums?

### Ownership Model
- Profile-scoped (user-owned)
- Account-scoped (org-shared)
- Public (no restrictions)

### Delete Behavior
- Soft delete (deleted_at timestamp)
- Hard delete
- Cascade behavior

### Relationships
- Foreign keys
- One-to-many / Many-to-many
- Cascading rules

## Phase 2: Explore Existing Patterns

**CRITICAL**: Review codebase for consistency before implementing.

| File | Look For |
|------|----------|
| `sql/schema.sql` | Table naming, constraints |
| `app/models/*.py` | SQLModel patterns, base classes |
| `app/api/v1/routes/*.py` | Auth patterns, pagination |
| `tests/test_*.py` | Test structure, fixtures |
| `doc/api.md` | Documentation format |

## Phase 3: Create Plan File

Create `.plan/<resource>-api.md` with:
1. **Product**: User story, acceptance criteria, non-goals
2. **Development**: Files, DDL, models, endpoints, examples
3. **Testing**: Test cases with Test Intent Validation

## Phase 4: Documentation First

Update `doc/api.md` BEFORE implementing:
- HTTP method and path
- Authentication requirements
- Request parameters/body with types
- Success and error responses
- Validation rules

## Phase 5: Implementation Order

Follow strictly:
1. SQLModel classes (`app/models/<resource>.py`)
2. DDL (`sql/schema.sql`)
3. Drop statement (`sql/drop_all_tables.sql`)
4. Service layer (if needed)
5. Routes (`app/api/v1/routes/<resource>.py`)
6. Register router (`app/main.py`)
7. Tests (`tests/test_<resource>.py`)
8. Run migration
9. Run tests

See `references/code-patterns.md` for complete code examples.

## Phase 6: Verification Checklist

### Documentation
- [ ] `doc/api.md` updated
- [ ] Request/response examples included
- [ ] Error responses documented

### Database
- [ ] DDL in `sql/schema.sql` with indexes
- [ ] `sql/drop_all_tables.sql` updated
- [ ] Migration applied successfully

### Models
- [ ] SQLModel classes follow pattern (Base, Table, Create, Update, Response)
- [ ] All fields properly typed

### Routes
- [ ] All CRUD endpoints (POST, GET, GET/:id, PATCH, DELETE)
- [ ] Auth dependencies present
- [ ] Router registered

### Tests
- [ ] Happy path tests pass
- [ ] Validation errors (422) tested
- [ ] Auth (401) tested
- [ ] Authorization (403) tested
- [ ] Not found (404) tested
- [ ] Edge cases tested
- [ ] Coverage > 90%

### Test Intent Validation
- [ ] Product lens (user behavior)
- [ ] Developer lens (code coverage)
- [ ] Tester lens (independent, meaningful)

## Related Skills

### Upstream Skills (Provide Input)

| Skill | Provides |
|-------|----------|
| **TPO** | MRD with data entities, rules |
| **Solutions Architect** | API contracts, data models |
| **Data Platform Engineer** | Database patterns |

### Downstream/Parallel Skills

| Skill | Coordination |
|-------|-------------|
| **Backend Tester** | Test scenarios, edge cases |
| **Frontend Developer** | API contract alignment |
| **Tech Doc Writer** | OpenAPI spec, examples |
| **TPgM** | Progress tracking |

### Consultation Triggers

- **Data Platform Engineer**: Complex queries, schema performance, raw SQL review
- **Solutions Architect**: API contract changes, integration patterns
- **Backend Tester**: Test scenarios, edge cases

### Handoff Checklist

```
□ Solutions Architect's API contract implemented
□ Data Platform Engineer consulted on schema
□ Backend Tester has test strategy
□ OpenAPI docs current
□ TPgM updated on progress
```

## Linear Ticket Workflow

**CRITICAL**: When assigned a Linear sub-issue, follow this workflow to ensure traceability.

### Worker Workflow

```
1. Accept work → Move ticket to "In Progress"
2. Create branch → {type}/{team}/LIN-XXX-description (team from claude.md)
3. Do work → Commit with [LIN-XXX] prefix
4. Track progress → Add comment on ticket
5. Complete work → Create PR, move to "In Review"
6. PR merged → Move to "Done"
```

**Branch Pattern**: `{type}/{team}/{LIN-XXX}-{description}`
- `type`: `feature`, `fix`, `refactor`, `docs`, `test`
- `team`: From project's `claude.md` Team Context (e.g., `platform`)
- Example: `feature/platform/LIN-101-password-reset-api`

### Starting Work

When you begin work on an assigned sub-issue:

```python
# Update ticket status
mcp.update_issue(id="LIN-XXX", state="In Progress")

# Add start comment
mcp.create_comment(
    issueId="LIN-XXX",
    body="""🚀 **Started work**
- Branch: `feature/platform/LIN-XXX-password-reset-api`
- Approach: Implementing JWT-based reset tokens with 24h expiry
"""
)
```

### Commit Message Format

```
[LIN-XXX] Brief description of change

- Detail 1
- Detail 2

Ticket: https://linear.app/team/issue/LIN-XXX
```

### Completion Comment Template

When PR is ready for review:

```python
mcp.update_issue(id="LIN-XXX", state="In Review")

mcp.create_comment(
    issueId="LIN-XXX",
    body="""🔍 **Ready for review**
- PR: [link to PR]

## Implementation Summary
- Endpoint: POST /api/v1/auth/reset-password
- Token: JWT with 24h expiry
- Rate limit: 3 requests/email/hour

## Test Coverage
- Unit tests: 12 tests passing
- Integration tests: 5 tests passing
- Coverage: 94%

## Files Changed
- `app/api/v1/routes/auth.py`
- `app/services/password_reset.py`
- `tests/test_password_reset.py`
"""
)
```

### After PR Merge

```python
mcp.update_issue(id="LIN-XXX", state="Done")

mcp.create_comment(
    issueId="LIN-XXX",
    body="""✅ **Completed**
- PR merged: [link]
- Deployed to: staging
"""
)
```

See `_shared/references/linear-ticket-traceability.md` for full workflow details.

## Reference Files

- `references/raw-sql-vs-orm.md` - When to use ORM vs raw SQL with examples
- `references/code-patterns.md` - SQLModel, route, DDL, and test patterns

## Summary

This workflow ensures:
- Complete planning before coding
- Consistent patterns across APIs
- Documentation synchronized
- Comprehensive test coverage
- Security by default

**Remember**: Consult Data Platform Engineer for schema design and Backend Tester for test strategy.
