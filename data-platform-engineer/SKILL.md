---
name: data-platform-engineer
description: Data Platform Engineer for designing data pipelines, storage strategies, and retrieval systems. Use when designing database schemas, building ETL/ELT pipelines, implementing vector search for RAG, optimizing query performance, managing data quality, or architecting data infrastructure. Pattern-focused and stack-agnostic with emphasis on RAG/vector search strategies. Covers relational, document, vector, and time-series data patterns.
---

# Data Platform Engineer

Design data infrastructure, pipelines, and retrieval systems with emphasis on patterns over specific tools.

## Usage Notification

**REQUIRED**: When triggered, state: "📊 Using Data Platform Engineer skill - designing data infrastructure and retrieval patterns."

## Core Objective

Build reliable data infrastructure that:
- Stores data efficiently and durably
- Enables fast, flexible retrieval
- Maintains data quality
- Scales with growth
- Supports AI/ML workloads (RAG, embeddings)

## Data Architecture Patterns

### Storage Selection

| Data Type | Pattern | Example Technologies |
|-----------|---------|---------------------|
| Structured, relational | RDBMS | PostgreSQL, MySQL |
| Document/flexible schema | Document DB | MongoDB, PostgreSQL JSONB |
| Key-value, caching | KV Store | Redis, DynamoDB |
| Vector embeddings | Vector DB | Qdrant, Pinecone, pgvector |
| Time-series | TSDB | TimescaleDB, InfluxDB |
| Search/full-text | Search engine | Elasticsearch, Meilisearch |
| Files/blobs | Object storage | S3, MinIO |
| Graph relationships | Graph DB | Neo4j, PostgreSQL + recursive CTEs |

### Decision Framework

```
Is the data structured with relationships?
├── YES → Relational (PostgreSQL)
│         └── Need vector search too? → pgvector extension
└── NO → Is schema highly variable?
         ├── YES → Document DB or JSONB columns
         └── NO → Is it time-series?
                  ├── YES → TSDB
                  └── NO → Is it for AI/semantic search?
                           ├── YES → Vector DB
                           └── NO → Evaluate specific needs
```

## Schema Design Patterns

### Relational Schema Best Practices

```sql
-- Use UUIDs for distributed systems
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Soft deletes for audit trail
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- JSONB for flexible metadata
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}';

-- Proper foreign keys with indexes
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_projects_owner ON projects(owner_id);

-- Many-to-many with junction table
CREATE TABLE project_members (
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (project_id, user_id)
);
```

### Indexing Strategy

```sql
-- B-tree (default): equality, range, sorting
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_created ON projects(created_at DESC);

-- Partial index: subset of rows
CREATE INDEX idx_active_projects ON projects(owner_id) 
WHERE status = 'active';

-- Composite index: multiple columns
CREATE INDEX idx_members_lookup ON project_members(user_id, project_id);

-- GIN index: JSONB, arrays, full-text
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- Full-text search
ALTER TABLE projects ADD COLUMN search_vector tsvector;
CREATE INDEX idx_projects_search ON projects USING GIN(search_vector);
```

See `references/schema-patterns.md` for comprehensive patterns.

## Vector Search / RAG Data Patterns

### Vector Storage Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Source Documents                                            │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────┐     ┌─────────┐     ┌─────────────────┐        │
│  │ Chunker │────►│ Embedder│────►│ Vector DB       │        │
│  └─────────┘     └─────────┘     │ (Qdrant/pgvector)│        │
│                                   └─────────────────┘        │
│                                           │                  │
│  Metadata Store ◄─────────────────────────┘                 │
│  (PostgreSQL)                                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Vector DB Schema (Qdrant)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

# Create collection with payload indexing
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,  # Embedding dimension
        distance=Distance.COSINE
    )
)

# Add payload indexes for filtering
client.create_payload_index(
    collection_name="documents",
    field_name="source",
    field_schema="keyword"
)
client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema="datetime"
)
```

### pgvector Schema

```sql
-- Enable extension
CREATE EXTENSION vector;

-- Documents table with vector column
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(384),  -- Match your model dimension
    metadata JSONB DEFAULT '{}',
    source VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- IVFFlat index for approximate search (faster, less accurate)
CREATE INDEX idx_documents_embedding ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- HNSW index (slower to build, faster queries, more accurate)
CREATE INDEX idx_documents_embedding_hnsw ON documents 
USING hnsw (embedding vector_cosine_ops);

-- Search query
SELECT id, content, 1 - (embedding <=> $1) as similarity
FROM documents
WHERE source = 'knowledge_base'
ORDER BY embedding <=> $1
LIMIT 10;
```

See `references/vector-search-patterns.md` for RAG optimization.

## ETL/ELT Pipeline Patterns

### Pipeline Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     ETL vs ELT                            │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ETL (Extract-Transform-Load):                           │
│  Source → Transform (external) → Load to destination     │
│  Good for: Complex transforms, data cleansing            │
│                                                           │
│  ELT (Extract-Load-Transform):                           │
│  Source → Load to destination → Transform (in DB)        │
│  Good for: Large data, SQL transforms, data lakes        │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Pipeline Patterns

```python
# Pattern 1: Simple ETL with Python
def etl_pipeline():
    # Extract
    raw_data = extract_from_source()
    
    # Transform
    cleaned = clean_data(raw_data)
    enriched = enrich_data(cleaned)
    validated = validate_data(enriched)
    
    # Load
    load_to_destination(validated)

# Pattern 2: Incremental loading
def incremental_load():
    # Get last processed timestamp
    last_run = get_last_run_timestamp()
    
    # Extract only new/changed records
    new_records = extract_where(updated_at > last_run)
    
    # Upsert to destination
    upsert_to_destination(new_records)
    
    # Update checkpoint
    save_checkpoint(datetime.now())

# Pattern 3: Change Data Capture (CDC)
def cdc_pipeline():
    # Listen to database changes
    for change in listen_to_changes():
        if change.operation == 'INSERT':
            handle_insert(change.data)
        elif change.operation == 'UPDATE':
            handle_update(change.data)
        elif change.operation == 'DELETE':
            handle_delete(change.data)
```

### Data Quality Checks

```python
from dataclasses import dataclass

@dataclass
class QualityCheck:
    name: str
    check_fn: callable
    severity: str  # 'error' | 'warning'

def run_quality_checks(data, checks: list[QualityCheck]):
    results = []
    
    for check in checks:
        passed = check.check_fn(data)
        results.append({
            "check": check.name,
            "passed": passed,
            "severity": check.severity
        })
    
    errors = [r for r in results if not r["passed"] and r["severity"] == "error"]
    if errors:
        raise DataQualityError(errors)
    
    return results

# Example checks
quality_checks = [
    QualityCheck(
        name="no_nulls_in_email",
        check_fn=lambda df: df['email'].notna().all(),
        severity="error"
    ),
    QualityCheck(
        name="valid_email_format",
        check_fn=lambda df: df['email'].str.contains('@').all(),
        severity="error"
    ),
    QualityCheck(
        name="reasonable_dates",
        check_fn=lambda df: (df['created_at'] < datetime.now()).all(),
        severity="warning"
    ),
]
```

See `references/pipeline-patterns.md` for more patterns.

## Query Optimization

### Optimization Checklist

1. **Use EXPLAIN ANALYZE** to understand query plans
2. **Add indexes** for frequently filtered/joined columns
3. **Avoid SELECT *** - fetch only needed columns
4. **Use pagination** for large result sets
5. **Denormalize** for read-heavy workloads
6. **Cache** frequently accessed data

### Common Query Patterns

```sql
-- Pagination with cursor (efficient for large datasets)
SELECT * FROM projects
WHERE created_at < :cursor_timestamp
ORDER BY created_at DESC
LIMIT 20;

-- Avoid OFFSET for large pages
-- BAD: SELECT * FROM projects LIMIT 20 OFFSET 10000;

-- Aggregation with indexes
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
WHERE user_id = :user_id
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- Efficient full-text search
SELECT id, title, 
    ts_rank(search_vector, query) as rank
FROM articles,
    to_tsquery('english', 'postgres & performance') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;
```

### Connection Pooling

```python
# Use connection pooling for production
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,           # Maintained connections
    max_overflow=10,       # Extra connections if needed
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections after 30min
)
```

## Data Modeling Patterns

### Event Sourcing

Store all changes as events:

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_events_aggregate ON events(aggregate_type, aggregate_id, created_at);

-- Rebuild state by replaying events
SELECT event_type, event_data
FROM events
WHERE aggregate_type = 'order' AND aggregate_id = :order_id
ORDER BY created_at;
```

### Slowly Changing Dimensions (SCD Type 2)

Track historical changes:

```sql
CREATE TABLE products_history (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL,
    name VARCHAR(255),
    price DECIMAL(10,2),
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ,  -- NULL = current
    is_current BOOLEAN DEFAULT true
);

-- Get current state
SELECT * FROM products_history WHERE is_current = true;

-- Get state at point in time
SELECT * FROM products_history
WHERE product_id = :id
  AND valid_from <= :timestamp
  AND (valid_to IS NULL OR valid_to > :timestamp);
```

### CQRS (Command Query Responsibility Segregation)

Separate read and write models:

```
Write Model (Normalized):
- users, projects, tasks (normalized)
- Optimized for writes, consistency

Read Model (Denormalized):
- project_dashboard (materialized view)
- user_activity_feed (pre-aggregated)
- Optimized for specific query patterns
```

```sql
-- Materialized view for read model
CREATE MATERIALIZED VIEW project_dashboard AS
SELECT 
    p.id,
    p.name,
    u.name as owner_name,
    COUNT(DISTINCT pm.user_id) as member_count,
    COUNT(t.id) as task_count,
    COUNT(t.id) FILTER (WHERE t.status = 'done') as completed_tasks
FROM projects p
JOIN users u ON p.owner_id = u.id
LEFT JOIN project_members pm ON p.id = pm.project_id
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name, u.name;

-- Refresh periodically or on trigger
REFRESH MATERIALIZED VIEW project_dashboard;
```

## Backup and Recovery

### Backup Strategy

| Type | Frequency | Retention | Use Case |
|------|-----------|-----------|----------|
| Full backup | Daily | 30 days | Complete restore |
| Incremental | Hourly | 7 days | Point-in-time |
| Transaction log | Continuous | 24 hours | Minimal data loss |
| Snapshots | Before changes | Until verified | Safe deployments |

### PostgreSQL Backup Commands

```bash
# Logical backup (SQL dump)
pg_dump -h localhost -U user -d dbname > backup.sql

# Compressed backup
pg_dump -h localhost -U user -d dbname | gzip > backup.sql.gz

# Parallel backup for large DBs
pg_dump -h localhost -U user -d dbname -j 4 -Fd -f backup_dir/

# Restore
psql -h localhost -U user -d dbname < backup.sql

# Point-in-time recovery (requires WAL archiving)
pg_basebackup -D /backup/base -Fp -Xs -P
```

## Reference Files

- `references/schema-patterns.md` - Database schema patterns
- `references/vector-search-patterns.md` - RAG and vector optimization
- `references/pipeline-patterns.md` - ETL/ELT patterns
- `references/migration-patterns.md` - Safe schema migrations

## Quality Checklist

Before deploying data infrastructure:

- [ ] Schema properly normalized (or intentionally denormalized)
- [ ] Indexes on frequently queried columns
- [ ] Foreign keys with appropriate ON DELETE behavior
- [ ] Connection pooling configured
- [ ] Backup strategy implemented and tested
- [ ] Monitoring for slow queries
- [ ] Data quality checks in pipelines
- [ ] Retention policies defined
- [ ] PII handling documented
- [ ] Recovery procedure tested

## Summary

Effective data platform engineering:
- Choose storage based on access patterns, not familiarity
- Index strategically, not excessively
- Design pipelines for failure (idempotent, resumable)
- Plan for scale before you need it
- Test backups regularly (untested backups aren't backups)

Data is the foundation. Build it solid.
