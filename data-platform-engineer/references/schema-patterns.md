# Schema Patterns

Database schema design patterns for common scenarios.

## Naming Conventions

```sql
-- Tables: plural, snake_case
users, projects, project_members

-- Columns: snake_case
created_at, updated_at, user_id

-- Primary keys: id
id UUID PRIMARY KEY

-- Foreign keys: singular_table_id
user_id, project_id

-- Indexes: idx_table_column(s)
idx_users_email, idx_projects_owner_status

-- Constraints: table_column_type
users_email_unique, projects_status_check
```

---

## Core Entity Patterns

### User/Account Pattern

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified_at TIMESTAMPTZ,
    
    -- Profile
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    
    -- Authentication (if storing locally)
    password_hash VARCHAR(255),
    
    -- Status
    status VARCHAR(50) DEFAULT 'active' 
        CHECK (status IN ('pending', 'active', 'suspended', 'deleted')),
    
    -- Metadata
    settings JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ  -- Soft delete
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE status != 'deleted';
CREATE INDEX idx_users_created ON users(created_at DESC);
```

### Multi-tenant Pattern

```sql
-- Tenant/Organization
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Membership
CREATE TABLE organization_members (
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member' 
        CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (organization_id, user_id)
);

-- Tenant-scoped data
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    -- All queries should filter by organization_id
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_org ON projects(organization_id);

-- Row-Level Security for tenant isolation
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON projects
    USING (organization_id = current_setting('app.current_org_id')::uuid);
```

### Hierarchical Data Pattern

```sql
-- Self-referential for tree structures
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    depth INTEGER DEFAULT 0,
    path TEXT,  -- Materialized path: '/root/parent/child'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_path ON categories(path text_pattern_ops);

-- Query all descendants
SELECT * FROM categories WHERE path LIKE '/electronics/%';

-- Alternative: Closure table for complex queries
CREATE TABLE category_paths (
    ancestor_id UUID REFERENCES categories(id),
    descendant_id UUID REFERENCES categories(id),
    depth INTEGER NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);

-- Query all descendants
SELECT c.* FROM categories c
JOIN category_paths cp ON c.id = cp.descendant_id
WHERE cp.ancestor_id = :category_id;
```

---

## Relationship Patterns

### One-to-Many

```sql
-- Parent
CREATE TABLE authors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL
);

-- Child with foreign key
CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL
);

CREATE INDEX idx_books_author ON books(author_id);
```

### Many-to-Many

```sql
-- Junction table
CREATE TABLE book_tags (
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (book_id, tag_id)
);

-- With extra attributes
CREATE TABLE project_members (
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '[]',
    invited_by UUID REFERENCES users(id),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (project_id, user_id)
);
```

### Polymorphic Associations

```sql
-- Option 1: Separate foreign keys (preferred for small number of types)
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Polymorphic target
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    -- Only one should be set
    CHECK (
        (post_id IS NOT NULL)::int + 
        (task_id IS NOT NULL)::int = 1
    ),
    content TEXT NOT NULL,
    author_id UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Option 2: Type + ID columns (flexible but no FK constraint)
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    commentable_type VARCHAR(50) NOT NULL,
    commentable_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_comments_target ON comments(commentable_type, commentable_id);
```

---

## Audit and History Patterns

### Audit Log

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- What changed
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    
    -- Change details
    old_data JSONB,
    new_data JSONB,
    changed_fields TEXT[],
    
    -- Who changed it
    user_id UUID REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    
    -- When
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, user_id)
    VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP != 'INSERT' THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) END,
        current_setting('app.current_user_id', true)::uuid
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

### Soft Deletes

```sql
-- Add deleted_at column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Create view for active records
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

-- Or use partial index
CREATE INDEX idx_users_active ON users(email) WHERE deleted_at IS NULL;

-- Soft delete function
CREATE OR REPLACE FUNCTION soft_delete()
RETURNS TRIGGER AS $$
BEGIN
    NEW.deleted_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## Performance Patterns

### Denormalization for Read Performance

```sql
-- Normalized (write-optimized)
SELECT 
    p.name as project_name,
    COUNT(t.id) as task_count,
    u.name as owner_name
FROM projects p
JOIN users u ON p.owner_id = u.id
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, u.name;

-- Denormalized (read-optimized)
ALTER TABLE projects ADD COLUMN task_count INTEGER DEFAULT 0;
ALTER TABLE projects ADD COLUMN owner_name VARCHAR(255);

-- Update via trigger or background job
CREATE OR REPLACE FUNCTION update_project_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE projects 
    SET task_count = (SELECT COUNT(*) FROM tasks WHERE project_id = NEW.project_id)
    WHERE id = NEW.project_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Partitioning

```sql
-- Range partitioning for time-series
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    data JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2025_01 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE events_2025_02 PARTITION OF events
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automatic partition management (use pg_partman extension)
```

### Materialized Views

```sql
-- Create materialized view for complex aggregation
CREATE MATERIALIZED VIEW daily_stats AS
SELECT 
    DATE_TRUNC('day', created_at) as day,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM events
GROUP BY DATE_TRUNC('day', created_at);

-- Create index on materialized view
CREATE INDEX idx_daily_stats_day ON daily_stats(day DESC);

-- Refresh (blocks reads during refresh)
REFRESH MATERIALIZED VIEW daily_stats;

-- Concurrent refresh (doesn't block, requires unique index)
CREATE UNIQUE INDEX idx_daily_stats_unique ON daily_stats(day);
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_stats;
```

---

## JSON/JSONB Patterns

### Flexible Metadata

```sql
-- Store flexible attributes
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    -- Structured fields for common attributes
    price DECIMAL(10,2),
    category VARCHAR(100),
    -- JSONB for variable attributes
    attributes JSONB DEFAULT '{}'
);

-- Query JSONB
SELECT * FROM products 
WHERE attributes->>'color' = 'red';

SELECT * FROM products 
WHERE attributes @> '{"size": "large"}';

-- Index JSONB for performance
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);

-- Index specific paths
CREATE INDEX idx_products_color ON products((attributes->>'color'));
```

### Event Data

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    -- Common fields extracted for indexing
    user_id UUID,
    session_id UUID,
    -- Full event data
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- GIN index for arbitrary queries
CREATE INDEX idx_events_data ON events USING GIN(data);

-- B-tree indexes for common queries
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_user ON events(user_id);
```

---

## Migration Safety

### Safe Column Addition

```sql
-- Safe: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(50);

-- Safe: Add column with default (PostgreSQL 11+)
ALTER TABLE users ADD COLUMN verified BOOLEAN DEFAULT false;

-- Unsafe: Add NOT NULL without default
-- ALTER TABLE users ADD COLUMN required_field VARCHAR(50) NOT NULL;

-- Safe alternative: Add nullable, backfill, then add constraint
ALTER TABLE users ADD COLUMN required_field VARCHAR(50);
UPDATE users SET required_field = 'default' WHERE required_field IS NULL;
ALTER TABLE users ALTER COLUMN required_field SET NOT NULL;
```

### Safe Index Creation

```sql
-- Create index without locking table
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- Note: CONCURRENTLY can't be in a transaction
```

### Safe Column Rename

```sql
-- Don't rename directly - add new, migrate, drop old
-- 1. Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- 2. Copy data
UPDATE users SET full_name = name;

-- 3. Update application to use new column

-- 4. Drop old column (later)
ALTER TABLE users DROP COLUMN name;
```
