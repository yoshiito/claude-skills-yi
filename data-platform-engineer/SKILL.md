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

| Data Type | Pattern | Examples |
|-----------|---------|----------|
| Structured, relational | RDBMS | PostgreSQL, MySQL |
| Document/flexible | Document DB | MongoDB, PostgreSQL JSONB |
| Key-value, caching | KV Store | Redis, DynamoDB |
| Vector embeddings | Vector DB | Qdrant, Pinecone, pgvector |
| Time-series | TSDB | TimescaleDB, InfluxDB |
| Search/full-text | Search engine | Elasticsearch, Meilisearch |

### Decision Framework

```
Structured with relationships? → Relational (PostgreSQL)
  └── Need vector search? → pgvector extension
Highly variable schema? → Document DB or JSONB
Time-series data? → TSDB
AI/semantic search? → Vector DB
```

## Schema Design

### Best Practices

```sql
-- UUIDs for distributed systems
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Soft deletes for audit trail
deleted_at TIMESTAMPTZ

-- JSONB for flexible metadata
metadata JSONB DEFAULT '{}'

-- Proper foreign keys with indexes
CREATE INDEX idx_projects_owner ON projects(owner_id);
```

### Indexing Strategy

| Index Type | Use Case |
|------------|----------|
| B-tree (default) | Equality, range, sorting |
| Partial | Subset of rows |
| Composite | Multiple columns |
| GIN | JSONB, arrays, full-text |

See `references/schema-patterns.md` for comprehensive patterns.

## Vector Search / RAG

### Architecture

```
Documents → Chunker → Embedder → Vector DB (Qdrant/pgvector)
                                     │
                         Metadata Store (PostgreSQL)
```

### pgvector Quick Reference

```sql
CREATE EXTENSION vector;

CREATE TABLE documents (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(384),  -- Match model dimension
    metadata JSONB
);

-- HNSW index (recommended)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Search query
SELECT id, content, 1 - (embedding <=> $1) as similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 10;
```

See `references/vector-search-patterns.md` for RAG optimization.

## ETL/ELT Pipeline Patterns

| Pattern | Use Case |
|---------|----------|
| **ETL** | Complex transforms, data cleansing |
| **ELT** | Large data, SQL transforms, data lakes |
| **Incremental** | Load only new/changed records |
| **CDC** | Real-time change streaming |

### Data Quality Checks

Essential checks:
- Null validation
- Format validation (email, dates)
- Referential integrity
- Reasonable ranges

See `references/pipeline-patterns.md` for implementation patterns.

## Query Optimization

### Checklist

1. Use `EXPLAIN ANALYZE` to understand query plans
2. Add indexes for frequently filtered/joined columns
3. Avoid `SELECT *` - fetch only needed columns
4. Use cursor-based pagination (not OFFSET)
5. Denormalize for read-heavy workloads
6. Cache frequently accessed data

### Connection Pooling

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

## Data Modeling Patterns

| Pattern | Use Case |
|---------|----------|
| **Event Sourcing** | Audit trail, temporal queries |
| **SCD Type 2** | Track historical changes |
| **CQRS** | Separate read/write optimizations |
| **Materialized Views** | Pre-computed aggregations |

## Backup Strategy

| Type | Frequency | Retention |
|------|-----------|-----------|
| Full backup | Daily | 30 days |
| Incremental | Hourly | 7 days |
| Transaction log | Continuous | 24 hours |
| Pre-change snapshot | Before changes | Until verified |

## Quality Checklist

- [ ] Schema properly normalized (or intentionally denormalized)
- [ ] Indexes on frequently queried columns
- [ ] Foreign keys with appropriate ON DELETE
- [ ] Connection pooling configured
- [ ] Backup strategy implemented and tested
- [ ] Monitoring for slow queries
- [ ] Data quality checks in pipelines
- [ ] Recovery procedure tested

## Related Skills

### Upstream (Provide Requirements)

| Skill | Provides |
|-------|----------|
| **Solutions Architect** | Data flow requirements |
| **AI Integration Engineer** | RAG/embedding needs |

### Downstream (Consume Data Design)

| Skill | Coordination |
|-------|-------------|
| **Backend Developer** | Schema implementation |
| **AI Integration Engineer** | Vector storage setup |

## Reference Files

- `references/schema-patterns.md` - Database schema patterns
- `references/vector-search-patterns.md` - RAG and vector optimization
- `references/pipeline-patterns.md` - ETL/ELT patterns
- `references/migration-patterns.md` - Safe schema migrations

## Summary

Effective data platform engineering:
- Choose storage based on access patterns
- Index strategically, not excessively
- Design pipelines for failure (idempotent, resumable)
- Plan for scale before you need it
- Test backups regularly

Data is the foundation. Build it solid.
