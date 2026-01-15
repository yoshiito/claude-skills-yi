---
name: fastapi-postgres-sqlmodel-developer
description: Systematic workflow for designing and implementing CRUD APIs using FastAPI, PostgreSQL, and SQLModel ORM. Use when creating new REST API endpoints, designing database schemas, implementing CRUD operations, or adding new resources to existing FastAPI applications. Guides through requirements gathering, pattern exploration, planning, documentation-first development, implementation, and verification with comprehensive test coverage. Includes guidance on when to use raw SQL vs ORM.
---

# FastAPI + PostgreSQL + SQLModel Developer

Build production-ready CRUD APIs following a systematic, documentation-first workflow. This skill ensures consistency, comprehensive testing, and maintainable code through structured planning and validation.

## Tech Stack

- **FastAPI**: Modern Python web framework with automatic OpenAPI docs
- **PostgreSQL**: Relational database with strong consistency
- **SQLModel**: Pydantic-based ORM combining SQLAlchemy and Pydantic
- **Pytest**: Testing framework with async support

## Raw SQL vs SQLModel ORM: Decision Framework

**DEFAULT**: Use SQLModel ORM for standard CRUD operations. Only use raw SQL when you have a specific, justified reason.

### When to Use SQLModel ORM (Default)

Use SQLModel for 95% of operations:

**Standard CRUD operations**:
```python
# Create
user = User(name="John", email="john@example.com")
db.add(user)
db.commit()

# Read
user = db.exec(select(User).where(User.id == user_id)).first()

# Update
user.name = "Jane"
db.add(user)
db.commit()

# Delete
db.delete(user)
db.commit()
```

**Simple queries with filters**:
```python
# Filter by single field
users = db.exec(select(User).where(User.status == "active")).all()

# Multiple conditions
users = db.exec(
    select(User)
    .where(User.status == "active")
    .where(User.created_at > start_date)
).all()

# Ordering and pagination
users = db.exec(
    select(User)
    .order_by(User.created_at.desc())
    .offset(skip)
    .limit(limit)
).all()
```

**Joins and relationships**:
```python
# Join with relationship
statement = (
    select(Project, User)
    .join(User)
    .where(Project.status == "active")
)
results = db.exec(statement).all()
```

**Benefits of ORM**:
- Type safety with Pydantic validation
- Automatic SQL injection protection
- IDE autocomplete for fields
- Easier to test and mock
- Cleaner, more maintainable code
- Automatic handling of relationships

### When to Use Raw SQL

Use raw SQL only in these specific scenarios:

#### 1. Complex Aggregations

**When**: Multiple GROUP BY, HAVING clauses, complex aggregations, window functions

```python
# ORM gets too verbose/complex
query = """
    SELECT 
        DATE_TRUNC('day', created_at) as date,
        status,
        COUNT(*) as count,
        AVG(amount) as avg_amount,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median_amount
    FROM orders
    WHERE created_at >= :start_date
    GROUP BY DATE_TRUNC('day', created_at), status
    HAVING COUNT(*) > 10
    ORDER BY date DESC, status
"""
results = db.exec(text(query), {"start_date": start_date}).all()
```

#### 2. PostgreSQL-Specific Features

**When**: Using JSONB operations, full-text search, array operations, CTEs, or other PostgreSQL-specific features

```python
# JSONB operations
query = """
    SELECT * FROM resources
    WHERE metadata @> :filter_json
    AND metadata->'tags' ?| :tags
"""

# Full-text search
query = """
    SELECT *, ts_rank(search_vector, query) as rank
    FROM articles, plainto_tsquery(:search_term) query
    WHERE search_vector @@ query
    ORDER BY rank DESC
"""

# Array operations
query = """
    SELECT * FROM projects
    WHERE :tag_id = ANY(tag_ids)
"""

# Common Table Expressions (CTEs)
query = """
    WITH active_users AS (
        SELECT id, name FROM users WHERE last_login > NOW() - INTERVAL '30 days'
    ),
    user_stats AS (
        SELECT user_id, COUNT(*) as project_count
        FROM projects
        GROUP BY user_id
    )
    SELECT u.*, s.project_count
    FROM active_users u
    LEFT JOIN user_stats s ON u.id = s.user_id
"""
```

#### 3. Bulk Operations

**When**: Inserting/updating thousands of rows at once

```python
# Bulk insert with ON CONFLICT
query = """
    INSERT INTO cache_entries (key, value, expires_at)
    VALUES (:key, :value, :expires_at)
    ON CONFLICT (key) 
    DO UPDATE SET value = EXCLUDED.value, expires_at = EXCLUDED.expires_at
"""
db.exec(text(query), params_list)

# Bulk update with complex logic
query = """
    UPDATE resources
    SET status = CASE
        WHEN expires_at < NOW() THEN 'expired'
        WHEN usage_count > threshold THEN 'over_limit'
        ELSE 'active'
    END
    WHERE owner_id = :owner_id
"""
```

#### 4. Performance-Critical Queries

**When**: Query has performance issues with ORM due to N+1 queries or inefficient SQL generation

```python
# Instead of N+1 queries with ORM
query = """
    SELECT 
        p.*,
        COALESCE(
            JSON_AGG(
                JSON_BUILD_OBJECT('id', t.id, 'name', t.name)
            ) FILTER (WHERE t.id IS NOT NULL),
            '[]'
        ) as tags
    FROM projects p
    LEFT JOIN project_tags pt ON p.id = pt.project_id
    LEFT JOIN tags t ON pt.tag_id = t.id
    WHERE p.owner_id = :owner_id
    GROUP BY p.id
"""
```

#### 5. Database Maintenance Operations

**When**: Running migrations, maintenance tasks, or database administration

```python
# Vacuum, analyze, reindex
query = "VACUUM ANALYZE resources"

# Update statistics
query = "ANALYZE resources"

# Create indexes concurrently
query = "CREATE INDEX CONCURRENTLY idx_name ON table(column)"
```

### Raw SQL Guidelines

When you do use raw SQL, follow these rules:

**1. Always use parameterized queries** (NEVER string interpolation):
```python
# ✓ CORRECT - parameterized
query = "SELECT * FROM users WHERE id = :user_id"
result = db.exec(text(query), {"user_id": user_id})

# ✗ WRONG - SQL injection vulnerability
query = f"SELECT * FROM users WHERE id = {user_id}"  # NEVER DO THIS
```

**2. Document why raw SQL is necessary**:
```python
# Use raw SQL for complex aggregation with window functions
# ORM would generate inefficient subqueries
query = """
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY score DESC) as rank
    FROM products
"""
```

**3. Keep SQL in constants or separate files**:
```python
# For complex queries, extract to constant
DAILY_STATS_QUERY = """
    SELECT 
        DATE_TRUNC('day', created_at) as date,
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE status = 'completed') as completed
    FROM orders
    WHERE created_at >= :start_date
    GROUP BY DATE_TRUNC('day', created_at)
    ORDER BY date
"""

def get_daily_stats(start_date: datetime, db: Session):
    """Get daily order statistics."""
    return db.exec(text(DAILY_STATS_QUERY), {"start_date": start_date}).all()
```

**4. Map results to models when possible**:
```python
# Raw query but still return proper models
from sqlmodel import col

query = text("""
    SELECT * FROM users 
    WHERE last_login > :cutoff
    ORDER BY RANDOM()
    LIMIT 10
""")
users = db.exec(query, {"cutoff": cutoff}).all()

# Convert to User models
return [User.model_validate(dict(row)) for row in users]
```

**5. Test raw SQL thoroughly**:
```python
def test_complex_aggregation_query():
    """Test raw SQL aggregation query."""
    # Test with known data
    result = get_daily_stats(start_date, db)
    
    # Verify structure
    assert len(result) > 0
    assert all(hasattr(row, 'date') for row in result)
    
    # Verify calculations
    first_day = result[0]
    manual_count = db.exec(
        select(func.count(Order.id))
        .where(func.date_trunc('day', Order.created_at) == first_day.date)
    ).first()
    assert first_day.total == manual_count
```

### Decision Checklist

Before writing raw SQL, ask:

- [ ] Can this be done with SQLModel select/where/join? → Use SQLModel
- [ ] Does this use PostgreSQL-specific features (JSONB, arrays, full-text)? → Raw SQL OK
- [ ] Is this a complex aggregation with multiple GROUP BY/window functions? → Raw SQL OK
- [ ] Is this a bulk operation affecting 1000+ rows? → Raw SQL OK
- [ ] Does the ORM version have performance issues (N+1, inefficient SQL)? → Raw SQL OK
- [ ] Is this a one-time migration or maintenance task? → Raw SQL OK
- [ ] Would parameterized queries be used (no string interpolation)? → Must be yes
- [ ] Is there a comment explaining why raw SQL is necessary? → Must be yes

### Anti-Patterns

**❌ Don't use raw SQL for simple queries**:
```python
# WRONG - this is a simple select
query = "SELECT * FROM users WHERE status = :status"
users = db.exec(text(query), {"status": "active"}).all()

# CORRECT - use SQLModel
users = db.exec(select(User).where(User.status == "active")).all()
```

**❌ Don't bypass type safety unnecessarily**:
```python
# WRONG - loses type safety
query = "INSERT INTO users (name, email) VALUES (:name, :email)"
db.exec(text(query), {"name": name, "email": email})

# CORRECT - use SQLModel for type validation
user = User(name=name, email=email)
db.add(user)
db.commit()
```

**❌ Don't use string formatting**:
```python
# WRONG - SQL injection vulnerability
query = f"SELECT * FROM users WHERE name = '{name}'"  # NEVER

# CORRECT - always parameterize
query = "SELECT * FROM users WHERE name = :name"
db.exec(text(query), {"name": name})
```

### Summary

**Default to SQLModel ORM** for:
- All CRUD operations
- Simple queries and filters
- Joins with defined relationships
- Anything that benefits from type safety

**Use raw SQL only when**:
- PostgreSQL-specific features are required
- Complex aggregations/window functions are needed
- Bulk operations on large datasets
- Performance is critical and ORM is inefficient
- Database maintenance tasks

**Always**:
- Use parameterized queries (never string interpolation)
- Document why raw SQL is necessary
- Test raw SQL queries thoroughly
- Map results back to models when possible

## Workflow Overview

Follow these phases in order:

1. **Requirements Gathering** - Understand the resource, fields, relationships, and constraints
2. **Explore Existing Patterns** - Review current codebase architecture
3. **Create Plan File** - Document design decisions in `.plan/` directory
4. **Documentation First** - Update API docs before implementation
5. **Implementation** - Follow strict ordering: model → DDL → routes → tests
6. **Verification** - Run comprehensive checklist before considering complete

## Phase 1: Requirements Gathering

Before writing any code, gather complete requirements. Ask about:

### Resource Identity
- **Resource name**: Singular and plural forms (e.g., "project" / "projects")
- **Primary use case**: What problem does this resource solve?
- **User story**: Who needs this and why?

### Fields and Schema
For each field, determine:
- **Name**: Snake_case field name
- **Type**: String, integer, boolean, float, date, datetime, UUID, enum
- **Required vs Optional**: Can it be null?
- **Constraints**: Max length, min/max values, regex patterns, foreign keys
- **Defaults**: Default values for creation
- **Computed fields**: Fields calculated from other data
- **Arrays**: Does the field hold multiple values?
- **Enums**: Fixed set of allowed values?
- **Config-driven options**: Should values come from config file?

### Ownership Model
- **Profile-scoped**: Owned by individual users (most resources)
- **Account-scoped**: Shared across account/organization
- **Public**: No ownership restrictions

### Delete Behavior
- **Soft delete**: Set `deleted_at` timestamp, keep data
- **Hard delete**: Physically remove from database
- **Cascade behavior**: What happens to related resources?

### Relationships
- **Foreign keys**: References to other tables
- **One-to-many**: Parent has multiple children
- **Many-to-many**: Requires junction table
- **Cascading**: Do deletes/updates cascade?

### Special Considerations
- **Validation rules**: Cross-field validation, business logic
- **Authorization**: Who can read/write/delete?
- **Pagination**: Expected result set size?
- **Filtering**: Which fields should be filterable?
- **Sorting**: Default sort order?
- **Search**: Full-text search needed?

## Phase 2: Explore Existing Patterns

**CRITICAL**: Before creating plan, review existing codebase to maintain consistency.

### Files to Read

**Schema files**:
- `sql/schema.sql` - Existing table definitions, naming conventions, constraint patterns
- `sql/drop_all_tables.sql` - Table drop order (dependency order)

**Models**:
- `app/models/*.py` - SQLModel patterns, base classes, common fields
- Look for: `Base`, `TimestampMixin`, `SoftDeleteMixin`, naming conventions

**Routes**:
- `app/api/v1/routes/*.py` - Endpoint patterns, auth decorators, response models
- Look for: Dependency injection patterns, pagination, filtering, error handling

**Tests**:
- `tests/test_*.py` - Test structure, fixtures, factories, assertion patterns
- Look for: Common test setup, auth helpers, data factories

**Documentation**:
- `doc/api.md` - API documentation format, examples, conventions

**Configuration**:
- `app/main.py` - Router registration pattern
- `config/*.json` - Config file structure if using config-driven fields

### Pattern Recognition

Note:
- Common field patterns (created_at, updated_at, deleted_at, created_by, owner_id)
- Auth/authorization patterns (current_user dependency, ownership checks)
- Naming conventions (table names, route prefixes, model class names)
- Error response formats
- Pagination implementation
- Test organization and naming

## Phase 3: Create Plan File

Create `.plan/<resource>-api.md` documenting all design decisions before coding.

This plan file serves as:
- Design document for review
- Implementation contract
- Test case specification
- Architecture decision record

Include these sections:
1. Product (user story, acceptance criteria, non-goals)
2. Development (files, architecture decisions, DDL, models, endpoints, examples)
3. Testing (test cases organized by type with Test Intent Validation)

## Phase 4: Documentation First

**BEFORE implementing**, update `doc/api.md` with complete API documentation for all endpoints.

Include for each endpoint:
- HTTP method and path
- Description
- Authentication requirements
- Request parameters/body with types and constraints
- Success response with example
- Error responses with status codes
- Validation rules

## Phase 5: Implementation

Follow this exact order:

1. **SQLModel classes** (`app/models/<resource>.py`)
2. **DDL** (`sql/schema.sql`)
3. **Drop statement** (`sql/drop_all_tables.sql`)
4. **Service layer** (`app/services/<resource>_service.py`) - if needed
5. **Config file** (`config/<resource>_options.json`) - if needed
6. **Routes** (`app/api/v1/routes/<resource>.py`)
7. **Register router** (`app/main.py`)
8. **Tests** (`tests/test_<resource>.py`)
9. **Run migration** (apply DDL)
10. **Run tests** (verify everything works)

## Phase 6: Code Patterns

### SQLModel Pattern

```python
class ResourceBase(SQLModel):
    """Shared fields"""
    name: str
    
class Resource(ResourceBase, table=True):
    """DB model - has ID, timestamps"""
    id: UUID
    owner_id: UUID
    created_at: datetime
    
class ResourceCreate(ResourceBase):
    """Only settable fields"""
    pass
    
class ResourceUpdate(SQLModel):
    """All fields optional"""
    name: Optional[str] = None
    
class ResourceResponse(ResourceBase):
    """API response - includes ID"""
    id: UUID
    created_at: datetime
```

### Route Pattern

```python
@router.post("", response_model=ResponseModel, status_code=201)
async def create_resource(
    data: CreateModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new resource."""
    resource = Service.create(data, current_user.profile_id, db)
    return resource
```

### DDL Pattern

```sql
CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_resources_owner_id ON resources(owner_id);
```

### Test Pattern

```python
def test_create_resource_success(auth_headers, resource_data):
    """Test successful resource creation."""
    response = client.post("/api/v1/resources", json=resource_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == resource_data["name"]
```

## Phase 7: Verification Checklist

Before considering complete, verify:

**Documentation**:
- [ ] `doc/api.md` updated with all endpoints
- [ ] Request/response examples included
- [ ] Error responses documented

**Database**:
- [ ] `sql/schema.sql` has table DDL with indexes
- [ ] `sql/drop_all_tables.sql` updated
- [ ] Migration applied successfully

**Models**:
- [ ] SQLModel classes follow pattern (Base, Table, Create, Update, Response)
- [ ] All fields properly typed

**Routes**:
- [ ] All CRUD endpoints implemented (POST, GET, GET by ID, PATCH, DELETE)
- [ ] Auth dependencies present
- [ ] Router registered in `app/main.py`

**Tests**:
- [ ] Happy path tests pass
- [ ] Error handling tests pass (422)
- [ ] Auth tests pass (401)
- [ ] Authorization tests pass (403)
- [ ] Not found tests pass (404)
- [ ] Edge case tests pass
- [ ] Coverage > 90%

**Test Intent Validation**:
- [ ] All tests pass product lens (user behavior)
- [ ] All tests pass developer lens (code coverage)
- [ ] All tests pass tester lens (independent, meaningful)

**Functional**:
- [ ] All endpoints work via API
- [ ] Ownership checks enforce security
- [ ] Soft delete works correctly (if applicable)
- [ ] Validation errors return proper codes

**Plan File**:
- [ ] `.plan/<resource>-api.md` completed
- [ ] Architecture decisions documented
- [ ] Test cases specified

## Summary

This systematic workflow ensures:
- Complete planning before coding
- Consistent patterns across APIs  
- Documentation stays synchronized
- Comprehensive test coverage
- Security by default (auth/ownership)
- Maintainable, scalable codebase

Follow each phase fully before moving to the next.
