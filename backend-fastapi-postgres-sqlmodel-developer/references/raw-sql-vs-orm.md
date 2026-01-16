# Raw SQL vs SQLModel ORM Decision Guide

**DEFAULT**: Use SQLModel ORM for standard CRUD operations. Only use raw SQL when you have a specific, justified reason.

## When to Use SQLModel ORM (Default - 95% of operations)

### Standard CRUD Operations
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

### Simple Queries with Filters
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

### Joins and Relationships
```python
statement = (
    select(Project, User)
    .join(User)
    .where(Project.status == "active")
)
results = db.exec(statement).all()
```

### Benefits of ORM
- Type safety with Pydantic validation
- Automatic SQL injection protection
- IDE autocomplete for fields
- Easier to test and mock
- Cleaner, more maintainable code
- Automatic handling of relationships

## When to Use Raw SQL

Use raw SQL only in these specific scenarios:

### 1. Complex Aggregations

When: Multiple GROUP BY, HAVING clauses, complex aggregations, window functions

```python
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

### 2. PostgreSQL-Specific Features

When: Using JSONB operations, full-text search, array operations, CTEs

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

### 3. Bulk Operations

When: Inserting/updating thousands of rows at once

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

### 4. Performance-Critical Queries

When: Query has performance issues with ORM due to N+1 queries or inefficient SQL generation

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

### 5. Database Maintenance Operations

When: Running migrations, maintenance tasks, or database administration

```python
query = "VACUUM ANALYZE resources"
query = "ANALYZE resources"
query = "CREATE INDEX CONCURRENTLY idx_name ON table(column)"
```

## Raw SQL Guidelines

When using raw SQL, follow these rules:

### 1. Always Use Parameterized Queries
```python
# CORRECT
query = "SELECT * FROM users WHERE id = :user_id"
result = db.exec(text(query), {"user_id": user_id})

# WRONG - SQL injection vulnerability
query = f"SELECT * FROM users WHERE id = {user_id}"  # NEVER
```

### 2. Document Why Raw SQL is Necessary
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

### 3. Keep SQL in Constants or Separate Files
```python
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

### 4. Map Results to Models When Possible
```python
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

### 5. Test Raw SQL Thoroughly
```python
def test_complex_aggregation_query():
    """Test raw SQL aggregation query."""
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

## Decision Checklist

Before writing raw SQL, ask:

- [ ] Can this be done with SQLModel select/where/join? → Use SQLModel
- [ ] Does this use PostgreSQL-specific features (JSONB, arrays, full-text)? → Raw SQL OK
- [ ] Is this a complex aggregation with multiple GROUP BY/window functions? → Raw SQL OK
- [ ] Is this a bulk operation affecting 1000+ rows? → Raw SQL OK
- [ ] Does the ORM version have performance issues (N+1, inefficient SQL)? → Raw SQL OK
- [ ] Is this a one-time migration or maintenance task? → Raw SQL OK
- [ ] Would parameterized queries be used (no string interpolation)? → Must be yes
- [ ] Is there a comment explaining why raw SQL is necessary? → Must be yes

## Anti-Patterns

### Don't Use Raw SQL for Simple Queries
```python
# WRONG
query = "SELECT * FROM users WHERE status = :status"
users = db.exec(text(query), {"status": "active"}).all()

# CORRECT
users = db.exec(select(User).where(User.status == "active")).all()
```

### Don't Bypass Type Safety Unnecessarily
```python
# WRONG
query = "INSERT INTO users (name, email) VALUES (:name, :email)"
db.exec(text(query), {"name": name, "email": email})

# CORRECT
user = User(name=name, email=email)
db.add(user)
db.commit()
```

### Never Use String Formatting
```python
# WRONG - SQL injection vulnerability
query = f"SELECT * FROM users WHERE name = '{name}'"  # NEVER

# CORRECT
query = "SELECT * FROM users WHERE name = :name"
db.exec(text(query), {"name": name})
```

## Summary

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
