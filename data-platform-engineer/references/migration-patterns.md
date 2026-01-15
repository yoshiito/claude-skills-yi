# Migration Patterns

Safe database schema migration patterns.

## Migration Safety Principles

1. **Always reversible**: Every migration should have a rollback
2. **No locks on large tables**: Avoid blocking reads/writes
3. **Backwards compatible**: Old code should work during migration
4. **Incremental**: Break large changes into small steps
5. **Tested**: Test migrations on production-like data

---

## Safe Operations

### Adding a Column

```sql
-- ✅ SAFE: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(50);

-- ✅ SAFE: Add column with default (PostgreSQL 11+)
ALTER TABLE users ADD COLUMN verified BOOLEAN DEFAULT false;

-- ❌ UNSAFE: Add NOT NULL without default on existing table
ALTER TABLE users ADD COLUMN required_field VARCHAR(50) NOT NULL;

-- ✅ SAFE: Multi-step NOT NULL addition
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN required_field VARCHAR(50);
-- Step 2: Backfill (in batches)
UPDATE users SET required_field = 'default_value' 
WHERE required_field IS NULL AND id BETWEEN 1 AND 10000;
-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN required_field SET NOT NULL;
```

### Adding an Index

```sql
-- ❌ UNSAFE: Regular index creation locks table
CREATE INDEX idx_users_email ON users(email);

-- ✅ SAFE: Concurrent index creation (no lock)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Note: CONCURRENTLY cannot be in a transaction
-- If it fails, clean up with:
DROP INDEX CONCURRENTLY IF EXISTS idx_users_email;
```

### Removing a Column

```sql
-- Step 1: Stop writing to column (application change)
-- Step 2: Deploy application change
-- Step 3: Drop column
ALTER TABLE users DROP COLUMN old_column;

-- For large tables, drop in stages:
-- First, mark as unused
COMMENT ON COLUMN users.old_column IS 'DEPRECATED: To be removed';

-- Later, drop
ALTER TABLE users DROP COLUMN old_column;
```

### Renaming a Column

```sql
-- ❌ UNSAFE: Direct rename breaks application
ALTER TABLE users RENAME COLUMN name TO full_name;

-- ✅ SAFE: Multi-step rename
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Step 2: Backfill
UPDATE users SET full_name = name;

-- Step 3: Add trigger to sync during transition
CREATE OR REPLACE FUNCTION sync_name_columns()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        IF NEW.name IS NOT NULL AND NEW.full_name IS NULL THEN
            NEW.full_name = NEW.name;
        ELSIF NEW.full_name IS NOT NULL AND NEW.name IS NULL THEN
            NEW.name = NEW.full_name;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_names
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_name_columns();

-- Step 4: Update application to use new column
-- Step 5: Remove trigger
DROP TRIGGER sync_names ON users;
DROP FUNCTION sync_name_columns();

-- Step 6: Drop old column
ALTER TABLE users DROP COLUMN name;
```

### Changing Column Type

```sql
-- ❌ UNSAFE: Direct type change may fail or lock
ALTER TABLE users ALTER COLUMN age TYPE INTEGER;

-- ✅ SAFE: Multi-step type change
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN age_int INTEGER;

-- Step 2: Backfill with conversion
UPDATE users SET age_int = age::INTEGER;

-- Step 3: Swap columns (application change to use new)
-- Step 4: Drop old column
ALTER TABLE users DROP COLUMN age;

-- Step 5: Rename new column
ALTER TABLE users RENAME COLUMN age_int TO age;
```

---

## Large Table Migrations

### Batch Updates

```python
def batch_update(
    conn,
    table: str,
    update_sql: str,
    batch_size: int = 10000,
    sleep_between: float = 0.1
):
    """Update large table in batches to avoid locks."""
    total_updated = 0
    
    while True:
        # Update a batch
        result = conn.execute(f"""
            WITH batch AS (
                SELECT id FROM {table}
                WHERE {condition_for_unprocessed}
                LIMIT {batch_size}
                FOR UPDATE SKIP LOCKED
            )
            UPDATE {table}
            SET {update_sql}
            WHERE id IN (SELECT id FROM batch)
            RETURNING id
        """)
        
        batch_count = result.rowcount
        conn.commit()
        
        if batch_count == 0:
            break
        
        total_updated += batch_count
        print(f"Updated {total_updated} rows...")
        
        # Sleep to reduce load
        time.sleep(sleep_between)
    
    return total_updated
```

### Online Schema Change Pattern

For very large tables, use tools like:
- `pg_repack` (PostgreSQL)
- `gh-ost` (MySQL)
- `pt-online-schema-change` (Percona)

```bash
# Example: pg_repack to rebuild table without locks
pg_repack -t users -d mydb

# Example: Add column with gh-ost (MySQL)
gh-ost \
  --alter="ADD COLUMN phone VARCHAR(50)" \
  --database=mydb \
  --table=users \
  --execute
```

---

## Data Migration Patterns

### ETL Migration

```python
def migrate_data(source_conn, dest_conn, batch_size: int = 10000):
    """Migrate data from old schema to new."""
    last_id = 0
    
    while True:
        # Extract batch from source
        rows = source_conn.execute(f"""
            SELECT * FROM old_table
            WHERE id > {last_id}
            ORDER BY id
            LIMIT {batch_size}
        """).fetchall()
        
        if not rows:
            break
        
        # Transform
        transformed = [transform_row(row) for row in rows]
        
        # Load to destination
        dest_conn.executemany(
            "INSERT INTO new_table VALUES (...)",
            transformed
        )
        dest_conn.commit()
        
        last_id = rows[-1]['id']
        print(f"Migrated up to id {last_id}")
```

### Dual-Write Migration

```python
class DualWriteService:
    """Write to both old and new during migration."""
    
    def __init__(self, old_repo, new_repo, read_from='old'):
        self.old_repo = old_repo
        self.new_repo = new_repo
        self.read_from = read_from
    
    def create(self, data):
        # Write to both
        old_result = self.old_repo.create(data)
        try:
            new_result = self.new_repo.create(self.transform(data))
        except Exception as e:
            # Log but don't fail - old is source of truth
            log_error(f"New repo write failed: {e}")
        
        return old_result
    
    def read(self, id):
        # Read from configured source
        if self.read_from == 'old':
            return self.old_repo.read(id)
        else:
            return self.new_repo.read(id)
    
    def switch_to_new(self):
        """After validation, switch reads to new."""
        self.read_from = 'new'
```

---

## Migration Versioning

### Migration File Structure

```
migrations/
├── 001_create_users.sql
├── 001_create_users.down.sql
├── 002_add_email_index.sql
├── 002_add_email_index.down.sql
├── 003_add_phone_column.sql
└── 003_add_phone_column.down.sql
```

### Migration Runner

```python
class MigrationRunner:
    def __init__(self, conn, migrations_dir: str):
        self.conn = conn
        self.migrations_dir = migrations_dir
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        self.conn.commit()
    
    def get_applied_migrations(self) -> set[str]:
        result = self.conn.execute(
            "SELECT version FROM schema_migrations"
        )
        return {row[0] for row in result}
    
    def get_pending_migrations(self) -> list[str]:
        applied = self.get_applied_migrations()
        all_migrations = sorted([
            f.replace('.sql', '') 
            for f in os.listdir(self.migrations_dir)
            if f.endswith('.sql') and not f.endswith('.down.sql')
        ])
        return [m for m in all_migrations if m not in applied]
    
    def migrate(self):
        """Apply all pending migrations."""
        pending = self.get_pending_migrations()
        
        for migration in pending:
            print(f"Applying migration: {migration}")
            
            # Read and execute migration
            with open(f"{self.migrations_dir}/{migration}.sql") as f:
                sql = f.read()
            
            try:
                self.conn.execute(sql)
                self.conn.execute(
                    "INSERT INTO schema_migrations (version) VALUES (:v)",
                    {"v": migration}
                )
                self.conn.commit()
                print(f"  ✓ Applied {migration}")
            except Exception as e:
                self.conn.rollback()
                print(f"  ✗ Failed {migration}: {e}")
                raise
    
    def rollback(self, steps: int = 1):
        """Rollback last N migrations."""
        applied = sorted(self.get_applied_migrations(), reverse=True)
        
        for migration in applied[:steps]:
            print(f"Rolling back: {migration}")
            
            down_file = f"{self.migrations_dir}/{migration}.down.sql"
            if not os.path.exists(down_file):
                raise Exception(f"No rollback file for {migration}")
            
            with open(down_file) as f:
                sql = f.read()
            
            self.conn.execute(sql)
            self.conn.execute(
                "DELETE FROM schema_migrations WHERE version = :v",
                {"v": migration}
            )
            self.conn.commit()
            print(f"  ✓ Rolled back {migration}")
```

---

## Pre-Migration Checklist

- [ ] Migration tested on staging with production-like data
- [ ] Rollback script exists and tested
- [ ] Application compatible with both old and new schema
- [ ] Backup taken before migration
- [ ] Monitoring in place for errors
- [ ] Maintenance window scheduled (if needed)
- [ ] Team notified of migration
- [ ] Load reduced (if applicable)

## Post-Migration Checklist

- [ ] Application functioning correctly
- [ ] No increase in error rates
- [ ] Query performance acceptable
- [ ] Data integrity verified
- [ ] Rollback script retained (for a period)
- [ ] Documentation updated
- [ ] Cleanup of old columns/tables scheduled
