# Database Operations

Patterns for local/remote database management, multi-database coordination, and operational concerns.

## Local Development Setup

### Docker Compose Patterns

```yaml
# docker-compose.yml - Full local data stack
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: app_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d  # Init SQL
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5

  # PostgreSQL with pgvector extension
  postgres-vector:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: vectors_dev
    ports:
      - "5433:5432"
    volumes:
      - pgvector_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"  # REST API
      - "6334:6334"  # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      QDRANT__SERVICE__GRPC_PORT: 6334

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  pgvector_data:
  qdrant_data:
  redis_data:
```

### Init Scripts for Local Setup

```sql
-- init-scripts/01-extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Fuzzy text search

-- init-scripts/02-schemas.sql
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS analytics;
```

### Makefile for Database Operations

```makefile
# Database operations
.PHONY: db-up db-down db-reset db-shell db-migrate

db-up:
	docker-compose up -d postgres qdrant redis

db-down:
	docker-compose down

db-reset:
	docker-compose down -v
	docker-compose up -d postgres qdrant redis
	sleep 3
	$(MAKE) db-migrate

db-shell:
	docker-compose exec postgres psql -U dev -d app_dev

db-migrate:
	alembic upgrade head

db-seed:
	python scripts/seed_dev_data.py
```

---

## Environment Configuration

### Connection String Patterns

```python
# config/database.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class DatabaseSettings(BaseSettings):
    """Database configuration with environment-specific defaults."""

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "dev"
    postgres_password: str = "dev"
    postgres_db: str = "app_dev"
    postgres_pool_size: int = 5
    postgres_max_overflow: int = 10

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_grpc_port: int = 6334
    qdrant_api_key: str | None = None  # Required for Qdrant Cloud

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_prefix = ""  # No prefix, use exact var names
        env_file = ".env"

    @property
    def postgres_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def postgres_async_url(self) -> str:
        """Async PostgreSQL URL for SQLAlchemy async."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

@lru_cache
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
```

### Environment Files

```bash
# .env.example (commit this)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev
POSTGRES_DB=app_dev

QDRANT_HOST=localhost
QDRANT_PORT=6333

REDIS_URL=redis://localhost:6379/0

# .env.production (never commit)
POSTGRES_HOST=prod-db.example.com
POSTGRES_PORT=5432
POSTGRES_USER=app_user
POSTGRES_PASSWORD=<secret>
POSTGRES_DB=app_production

QDRANT_HOST=qdrant-cloud.example.com
QDRANT_PORT=6333
QDRANT_API_KEY=<secret>

REDIS_URL=redis://:password@redis.example.com:6379/0
```

### Multi-Environment Connection Factory

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from qdrant_client import QdrantClient
import redis

class DatabaseConnections:
    """Factory for database connections."""

    def __init__(self, settings: DatabaseSettings):
        self.settings = settings
        self._postgres_engine = None
        self._qdrant_client = None
        self._redis_client = None

    @property
    def postgres(self):
        """Lazy PostgreSQL engine."""
        if self._postgres_engine is None:
            self._postgres_engine = create_engine(
                self.settings.postgres_url,
                pool_size=self.settings.postgres_pool_size,
                max_overflow=self.settings.postgres_max_overflow,
                pool_pre_ping=True,  # Verify connections before use
            )
        return self._postgres_engine

    @property
    def qdrant(self) -> QdrantClient:
        """Lazy Qdrant client."""
        if self._qdrant_client is None:
            if self.settings.qdrant_api_key:
                # Qdrant Cloud
                self._qdrant_client = QdrantClient(
                    host=self.settings.qdrant_host,
                    port=self.settings.qdrant_port,
                    api_key=self.settings.qdrant_api_key,
                    https=True
                )
            else:
                # Local Qdrant
                self._qdrant_client = QdrantClient(
                    host=self.settings.qdrant_host,
                    port=self.settings.qdrant_port
                )
        return self._qdrant_client

    @property
    def redis(self):
        """Lazy Redis client."""
        if self._redis_client is None:
            self._redis_client = redis.from_url(
                self.settings.redis_url,
                decode_responses=True
            )
        return self._redis_client

    def health_check(self) -> dict:
        """Check connectivity to all databases."""
        status = {}

        # PostgreSQL
        try:
            with self.postgres.connect() as conn:
                conn.execute("SELECT 1")
            status['postgres'] = 'healthy'
        except Exception as e:
            status['postgres'] = f'unhealthy: {e}'

        # Qdrant
        try:
            self.qdrant.get_collections()
            status['qdrant'] = 'healthy'
        except Exception as e:
            status['qdrant'] = f'unhealthy: {e}'

        # Redis
        try:
            self.redis.ping()
            status['redis'] = 'healthy'
        except Exception as e:
            status['redis'] = f'unhealthy: {e}'

        return status
```

---

## Qdrant Operations

### Collection Management

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance,
    OptimizersConfigDiff, HnswConfigDiff,
    QuantizationConfig, ScalarQuantization, ScalarType
)

def create_collection(
    client: QdrantClient,
    name: str,
    vector_size: int,
    distance: Distance = Distance.COSINE,
    on_disk: bool = False,
    quantization: bool = False
):
    """Create collection with production-ready settings."""

    vectors_config = VectorParams(
        size=vector_size,
        distance=distance,
        on_disk=on_disk  # Store vectors on disk for large collections
    )

    # Optional: Scalar quantization for memory efficiency (slight accuracy loss)
    quantization_config = None
    if quantization:
        quantization_config = QuantizationConfig(
            scalar=ScalarQuantization(
                type=ScalarType.INT8,
                quantile=0.99,
                always_ram=True  # Keep quantized vectors in RAM
            )
        )

    client.create_collection(
        collection_name=name,
        vectors_config=vectors_config,
        hnsw_config=HnswConfigDiff(
            m=16,
            ef_construct=100,
            full_scan_threshold=10000
        ),
        optimizers_config=OptimizersConfigDiff(
            indexing_threshold=20000,
            memmap_threshold=50000  # Use mmap for large segments
        ),
        quantization_config=quantization_config
    )

def create_payload_indexes(client: QdrantClient, collection: str):
    """Create indexes for common filter patterns."""

    # Keyword index for exact match
    client.create_payload_index(
        collection_name=collection,
        field_name="source",
        field_schema="keyword"
    )

    # Datetime index for range queries
    client.create_payload_index(
        collection_name=collection,
        field_name="created_at",
        field_schema="datetime"
    )

    # Integer index
    client.create_payload_index(
        collection_name=collection,
        field_name="version",
        field_schema="integer"
    )
```

### Backup and Restore

```python
def create_snapshot(client: QdrantClient, collection: str) -> str:
    """Create collection snapshot."""
    result = client.create_snapshot(collection_name=collection)
    return result.name

def list_snapshots(client: QdrantClient, collection: str) -> list:
    """List available snapshots."""
    return client.list_snapshots(collection_name=collection)

def restore_snapshot(
    client: QdrantClient,
    collection: str,
    snapshot_name: str,
    snapshot_url: str = None
):
    """Restore collection from snapshot."""
    if snapshot_url:
        # Restore from remote URL
        client.recover_snapshot(
            collection_name=collection,
            location=snapshot_url
        )
    else:
        # Restore from local snapshot
        client.recover_snapshot(
            collection_name=collection,
            location=f"file:///qdrant/snapshots/{collection}/{snapshot_name}"
        )
```

### Collection Statistics and Monitoring

```python
def get_collection_stats(client: QdrantClient, collection: str) -> dict:
    """Get collection statistics for monitoring."""
    info = client.get_collection(collection_name=collection)

    return {
        'vectors_count': info.vectors_count,
        'points_count': info.points_count,
        'segments_count': len(info.segments) if info.segments else 0,
        'status': info.status.value,
        'optimizer_status': info.optimizer_status.value,
        'indexed_vectors_count': info.indexed_vectors_count,
        'config': {
            'vector_size': info.config.params.vectors.size,
            'distance': info.config.params.vectors.distance.value,
            'on_disk': info.config.params.vectors.on_disk
        }
    }

def wait_for_indexing(client: QdrantClient, collection: str, timeout: int = 300):
    """Wait for collection indexing to complete."""
    import time

    start = time.time()
    while time.time() - start < timeout:
        info = client.get_collection(collection_name=collection)
        if info.status.value == "green":
            return True
        time.sleep(5)

    raise TimeoutError(f"Collection {collection} indexing did not complete in {timeout}s")
```

---

## Multi-Database Coordination

### Polyglot Persistence Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  PostgreSQL   │    │    Qdrant     │    │    Redis      │
│  (Source of   │───▶│   (Vector     │    │   (Cache,     │
│   Truth)      │    │   Search)     │    │   Sessions)   │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Data Consistency Patterns

```python
class DocumentService:
    """
    Service coordinating PostgreSQL (metadata) and Qdrant (vectors).
    PostgreSQL is the source of truth.
    """

    def __init__(self, db: DatabaseConnections, embedder):
        self.db = db
        self.embedder = embedder

    def create_document(self, content: str, metadata: dict) -> str:
        """Create document with coordinated writes."""
        doc_id = str(uuid.uuid4())

        # 1. Write to PostgreSQL first (source of truth)
        with self.db.postgres.begin() as conn:
            conn.execute(
                """
                INSERT INTO documents (id, content, metadata, created_at)
                VALUES (:id, :content, :metadata, NOW())
                """,
                {"id": doc_id, "content": content, "metadata": metadata}
            )

        # 2. Generate embedding and write to Qdrant
        try:
            embedding = self.embedder.encode(content)
            self.db.qdrant.upsert(
                collection_name="documents",
                points=[{
                    "id": doc_id,
                    "vector": embedding.tolist(),
                    "payload": {"content": content, **metadata}
                }]
            )
        except Exception as e:
            # Log error but don't fail - Qdrant can be rebuilt from PostgreSQL
            logger.error(f"Failed to index document {doc_id} in Qdrant: {e}")
            # Queue for retry
            self._queue_for_reindex(doc_id)

        # 3. Invalidate cache
        self.db.redis.delete(f"doc:{doc_id}")

        return doc_id

    def delete_document(self, doc_id: str):
        """Delete from all stores."""
        # 1. Delete from PostgreSQL
        with self.db.postgres.begin() as conn:
            conn.execute(
                "DELETE FROM documents WHERE id = :id",
                {"id": doc_id}
            )

        # 2. Delete from Qdrant
        try:
            self.db.qdrant.delete(
                collection_name="documents",
                points_selector=[doc_id]
            )
        except Exception as e:
            logger.error(f"Failed to delete {doc_id} from Qdrant: {e}")

        # 3. Invalidate cache
        self.db.redis.delete(f"doc:{doc_id}")

    def rebuild_vector_index(self, batch_size: int = 100):
        """Rebuild Qdrant index from PostgreSQL (disaster recovery)."""
        offset = 0

        while True:
            with self.db.postgres.connect() as conn:
                rows = conn.execute(
                    """
                    SELECT id, content, metadata
                    FROM documents
                    ORDER BY id
                    LIMIT :limit OFFSET :offset
                    """,
                    {"limit": batch_size, "offset": offset}
                ).fetchall()

            if not rows:
                break

            points = []
            for row in rows:
                embedding = self.embedder.encode(row.content)
                points.append({
                    "id": row.id,
                    "vector": embedding.tolist(),
                    "payload": {"content": row.content, **row.metadata}
                })

            self.db.qdrant.upsert(
                collection_name="documents",
                points=points
            )

            offset += batch_size
            logger.info(f"Indexed {offset} documents")
```

### Transaction Patterns

```python
from contextlib import contextmanager

@contextmanager
def multi_db_transaction(postgres_conn, qdrant_client, redis_client):
    """
    Pseudo-transaction across multiple databases.
    PostgreSQL is authoritative; others are eventually consistent.
    """
    qdrant_operations = []
    redis_operations = []

    class Operations:
        def queue_qdrant(self, op):
            qdrant_operations.append(op)

        def queue_redis(self, op):
            redis_operations.append(op)

    ops = Operations()

    try:
        with postgres_conn.begin() as txn:
            yield ops

            # If PostgreSQL commits, apply other operations
            for op in qdrant_operations:
                try:
                    op()
                except Exception as e:
                    logger.error(f"Qdrant operation failed: {e}")
                    # Queue for retry, don't rollback PostgreSQL

            for op in redis_operations:
                try:
                    op()
                except Exception as e:
                    logger.error(f"Redis operation failed: {e}")

    except Exception:
        # PostgreSQL rolled back, don't apply other operations
        raise
```

---

## Production Checklist

### Local Development
- [ ] Docker Compose with all required databases
- [ ] Init scripts for extensions and schemas
- [ ] Seed data scripts for development
- [ ] Makefile or scripts for common operations

### Environment Configuration
- [ ] Environment-specific settings (dev/staging/prod)
- [ ] Secrets management (never commit credentials)
- [ ] Connection pooling configured appropriately
- [ ] Health check endpoints for all databases

### Multi-Database
- [ ] Clear source of truth defined (usually PostgreSQL)
- [ ] Rebuild procedures documented and tested
- [ ] Failure handling for secondary stores
- [ ] Cache invalidation strategy

### Qdrant Operations
- [ ] Collection created with appropriate settings
- [ ] Payload indexes for filter patterns
- [ ] Snapshot/backup schedule configured
- [ ] Monitoring for collection status
