# Pipeline Patterns

Data pipeline patterns for ETL/ELT and data processing.

## Pipeline Architecture Patterns

### Batch Processing

```
┌─────────┐     ┌───────────┐     ┌─────────┐
│ Source  │────►│ Transform │────►│  Load   │
└─────────┘     └───────────┘     └─────────┘
     │                                  │
     └──────── Scheduled (cron) ────────┘
```

**Use when:**
- Data freshness of hours/daily is acceptable
- Processing large volumes
- Cost optimization matters

### Stream Processing

```
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌─────────┐
│ Source  │────►│  Queue  │────►│ Processor │────►│  Sink   │
└─────────┘     └─────────┘     └───────────┘     └─────────┘
                     │                │
                     └── Continuous ──┘
```

**Use when:**
- Real-time or near-real-time needed
- Event-driven processing
- Continuous data flow

### Lambda Architecture (Batch + Stream)

```
                    ┌─────────────────┐
              ┌────►│  Batch Layer   │────┐
              │     │ (comprehensive) │    │
┌─────────┐   │     └─────────────────┘    │    ┌─────────┐
│ Source  │───┤                            ├───►│  Serve  │
└─────────┘   │     ┌─────────────────┐    │    └─────────┘
              └────►│  Speed Layer   │────┘
                    │  (real-time)   │
                    └─────────────────┘
```

---

## ETL Patterns

### Extract Patterns

```python
# Pattern 1: Full extraction
def extract_full(source_conn):
    """Extract all records from source."""
    query = "SELECT * FROM source_table"
    return source_conn.execute(query).fetchall()

# Pattern 2: Incremental extraction (timestamp-based)
def extract_incremental(source_conn, last_run: datetime):
    """Extract only new/changed records."""
    query = """
        SELECT * FROM source_table 
        WHERE updated_at > :last_run
    """
    return source_conn.execute(query, {"last_run": last_run}).fetchall()

# Pattern 3: CDC (Change Data Capture)
def extract_cdc(source_conn, last_lsn: str):
    """Extract from change log."""
    query = """
        SELECT operation, data, lsn
        FROM change_log
        WHERE lsn > :last_lsn
        ORDER BY lsn
    """
    return source_conn.execute(query, {"last_lsn": last_lsn}).fetchall()

# Pattern 4: Chunked extraction (for large tables)
def extract_chunked(source_conn, chunk_size: int = 10000):
    """Extract in chunks to manage memory."""
    offset = 0
    while True:
        query = f"""
            SELECT * FROM source_table
            ORDER BY id
            LIMIT {chunk_size} OFFSET {offset}
        """
        chunk = source_conn.execute(query).fetchall()
        if not chunk:
            break
        yield chunk
        offset += chunk_size
```

### Transform Patterns

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class TransformResult:
    data: list[dict]
    errors: list[dict]
    stats: dict

# Pattern 1: Row-by-row transformation
def transform_rows(records: list[dict]) -> TransformResult:
    """Transform each record individually."""
    results = []
    errors = []
    
    for record in records:
        try:
            transformed = {
                'id': record['id'],
                'full_name': f"{record['first_name']} {record['last_name']}",
                'email_domain': record['email'].split('@')[1],
                'created_date': record['created_at'].date(),
            }
            results.append(transformed)
        except Exception as e:
            errors.append({
                'record': record,
                'error': str(e)
            })
    
    return TransformResult(
        data=results,
        errors=errors,
        stats={'processed': len(records), 'errors': len(errors)}
    )

# Pattern 2: Batch transformation with pandas
import pandas as pd

def transform_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Transform using pandas for efficiency."""
    return df.assign(
        full_name=df['first_name'] + ' ' + df['last_name'],
        email_domain=df['email'].str.split('@').str[1],
        created_date=pd.to_datetime(df['created_at']).dt.date
    ).drop(columns=['first_name', 'last_name'])

# Pattern 3: Lookup enrichment
def transform_with_lookup(
    records: list[dict],
    lookup_data: dict[str, dict]
) -> list[dict]:
    """Enrich records with lookup data."""
    results = []
    
    for record in records:
        enriched = record.copy()
        lookup_key = record.get('category_id')
        
        if lookup_key and lookup_key in lookup_data:
            enriched['category_name'] = lookup_data[lookup_key]['name']
            enriched['category_type'] = lookup_data[lookup_key]['type']
        
        results.append(enriched)
    
    return results

# Pattern 4: Aggregation
def transform_aggregate(records: list[dict]) -> list[dict]:
    """Aggregate records by dimension."""
    df = pd.DataFrame(records)
    
    aggregated = df.groupby(['date', 'category']).agg({
        'amount': 'sum',
        'count': 'count',
        'user_id': 'nunique'
    }).reset_index()
    
    aggregated.columns = ['date', 'category', 'total_amount', 'event_count', 'unique_users']
    
    return aggregated.to_dict('records')
```

### Load Patterns

```python
# Pattern 1: Insert (append only)
def load_insert(dest_conn, records: list[dict], table: str):
    """Simple insert of new records."""
    if not records:
        return
    
    columns = records[0].keys()
    placeholders = ', '.join([f':{col}' for col in columns])
    
    query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders})
    """
    
    dest_conn.execute(query, records)
    dest_conn.commit()

# Pattern 2: Upsert (insert or update)
def load_upsert(dest_conn, records: list[dict], table: str, key_columns: list[str]):
    """Insert new records, update existing."""
    if not records:
        return
    
    columns = list(records[0].keys())
    
    # PostgreSQL upsert
    query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({', '.join([f':{col}' for col in columns])})
        ON CONFLICT ({', '.join(key_columns)})
        DO UPDATE SET {', '.join([f'{col} = EXCLUDED.{col}' for col in columns if col not in key_columns])}
    """
    
    dest_conn.execute(query, records)
    dest_conn.commit()

# Pattern 3: Truncate and load (full refresh)
def load_truncate_insert(dest_conn, records: list[dict], table: str):
    """Full refresh - truncate then insert."""
    dest_conn.execute(f"TRUNCATE TABLE {table}")
    load_insert(dest_conn, records, table)

# Pattern 4: Swap table (zero downtime refresh)
def load_swap_table(dest_conn, records: list[dict], table: str):
    """Load to staging, then swap atomically."""
    staging_table = f"{table}_staging"
    
    # Load to staging
    dest_conn.execute(f"TRUNCATE TABLE {staging_table}")
    load_insert(dest_conn, records, staging_table)
    
    # Atomic swap
    dest_conn.execute(f"""
        BEGIN;
        ALTER TABLE {table} RENAME TO {table}_old;
        ALTER TABLE {staging_table} RENAME TO {table};
        ALTER TABLE {table}_old RENAME TO {staging_table};
        COMMIT;
    """)
```

---

## Data Quality Patterns

### Validation Framework

```python
from dataclasses import dataclass
from typing import Callable
from enum import Enum

class Severity(Enum):
    ERROR = "error"      # Blocks pipeline
    WARNING = "warning"  # Logs but continues
    INFO = "info"        # Informational only

@dataclass
class ValidationRule:
    name: str
    check: Callable[[pd.DataFrame], bool]
    severity: Severity
    description: str

class DataValidator:
    def __init__(self, rules: list[ValidationRule]):
        self.rules = rules
    
    def validate(self, df: pd.DataFrame) -> dict:
        results = {
            'passed': True,
            'checks': [],
            'errors': [],
            'warnings': []
        }
        
        for rule in self.rules:
            try:
                passed = rule.check(df)
                results['checks'].append({
                    'name': rule.name,
                    'passed': passed,
                    'severity': rule.severity.value
                })
                
                if not passed:
                    message = f"{rule.name}: {rule.description}"
                    if rule.severity == Severity.ERROR:
                        results['errors'].append(message)
                        results['passed'] = False
                    elif rule.severity == Severity.WARNING:
                        results['warnings'].append(message)
                        
            except Exception as e:
                results['errors'].append(f"{rule.name}: Check failed - {e}")
                results['passed'] = False
        
        return results

# Example rules
validation_rules = [
    ValidationRule(
        name="no_null_ids",
        check=lambda df: df['id'].notna().all(),
        severity=Severity.ERROR,
        description="ID column contains null values"
    ),
    ValidationRule(
        name="valid_emails",
        check=lambda df: df['email'].str.contains('@').all(),
        severity=Severity.ERROR,
        description="Invalid email format detected"
    ),
    ValidationRule(
        name="reasonable_amounts",
        check=lambda df: (df['amount'] >= 0).all() & (df['amount'] < 1000000).all(),
        severity=Severity.WARNING,
        description="Amount outside reasonable range"
    ),
    ValidationRule(
        name="no_future_dates",
        check=lambda df: (pd.to_datetime(df['created_at']) <= pd.Timestamp.now()).all(),
        severity=Severity.WARNING,
        description="Future dates detected"
    ),
]
```

### Data Profiling

```python
def profile_dataframe(df: pd.DataFrame) -> dict:
    """Generate data profile for monitoring."""
    profile = {
        'row_count': len(df),
        'columns': {},
        'generated_at': datetime.now().isoformat()
    }
    
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'null_count': int(df[col].isna().sum()),
            'null_pct': float(df[col].isna().mean()),
            'unique_count': int(df[col].nunique())
        }
        
        if df[col].dtype in ['int64', 'float64']:
            col_profile.update({
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median())
            })
        elif df[col].dtype == 'object':
            col_profile['avg_length'] = float(df[col].str.len().mean())
        
        profile['columns'][col] = col_profile
    
    return profile
```

---

## Error Handling Patterns

### Dead Letter Queue

```python
class PipelineWithDLQ:
    def __init__(self, dlq_table: str):
        self.dlq_table = dlq_table
    
    def process_with_dlq(self, records: list[dict]) -> dict:
        """Process records, send failures to DLQ."""
        success = []
        failed = []
        
        for record in records:
            try:
                transformed = self.transform(record)
                success.append(transformed)
            except Exception as e:
                failed.append({
                    'original_record': record,
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'failed_at': datetime.now().isoformat()
                })
        
        # Write failures to DLQ
        if failed:
            self.write_to_dlq(failed)
        
        return {
            'processed': len(success),
            'failed': len(failed),
            'success_rate': len(success) / len(records) if records else 0
        }
    
    def write_to_dlq(self, records: list[dict]):
        """Write failed records to dead letter queue."""
        # Insert into DLQ table for later investigation
        pass
    
    def replay_dlq(self, batch_size: int = 100):
        """Attempt to reprocess DLQ records."""
        # Fetch from DLQ, attempt reprocessing
        pass
```

### Retry with Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            
            raise last_exception
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def fetch_from_api(url: str) -> dict:
    """Fetch data from API with retries."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

---

## Orchestration Patterns

### Simple DAG

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    name: str
    func: Callable
    dependencies: list[str] = field(default_factory=list)

class SimplePipeline:
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task: Task):
        self.tasks[task.name] = task
    
    def run(self):
        """Execute tasks in dependency order."""
        completed = set()
        
        while len(completed) < len(self.tasks):
            for name, task in self.tasks.items():
                if name in completed:
                    continue
                
                # Check if dependencies are met
                if all(dep in completed for dep in task.dependencies):
                    print(f"Running task: {name}")
                    task.func()
                    completed.add(name)
        
        print("Pipeline complete!")

# Usage
pipeline = SimplePipeline()
pipeline.add_task(Task("extract", extract_data))
pipeline.add_task(Task("transform", transform_data, dependencies=["extract"]))
pipeline.add_task(Task("load", load_data, dependencies=["transform"]))
pipeline.run()
```

### Checkpoint/Resume

```python
class CheckpointedPipeline:
    def __init__(self, checkpoint_file: str):
        self.checkpoint_file = checkpoint_file
    
    def save_checkpoint(self, stage: str, data: Any):
        """Save checkpoint for resume capability."""
        checkpoint = {
            'stage': stage,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)
    
    def load_checkpoint(self) -> dict | None:
        """Load last checkpoint if exists."""
        try:
            with open(self.checkpoint_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def run(self):
        """Run pipeline with checkpoint support."""
        checkpoint = self.load_checkpoint()
        start_stage = checkpoint['stage'] if checkpoint else 'extract'
        
        stages = ['extract', 'transform', 'validate', 'load']
        start_idx = stages.index(start_stage)
        
        for stage in stages[start_idx:]:
            print(f"Running stage: {stage}")
            result = getattr(self, f'run_{stage}')()
            self.save_checkpoint(stage, result)
        
        # Cleanup checkpoint on success
        os.remove(self.checkpoint_file)
```

---

## Monitoring

### Pipeline Metrics

```python
@dataclass
class PipelineMetrics:
    pipeline_name: str
    run_id: str
    start_time: datetime
    end_time: datetime = None
    status: str = "running"
    records_processed: int = 0
    records_failed: int = 0
    stages: list = field(default_factory=list)

def track_pipeline():
    """Decorator to track pipeline execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics = PipelineMetrics(
                pipeline_name=func.__name__,
                run_id=str(uuid.uuid4()),
                start_time=datetime.now()
            )
            
            try:
                result = func(*args, **kwargs)
                metrics.status = "success"
                return result
            except Exception as e:
                metrics.status = "failed"
                metrics.error = str(e)
                raise
            finally:
                metrics.end_time = datetime.now()
                metrics.duration_seconds = (
                    metrics.end_time - metrics.start_time
                ).total_seconds()
                log_metrics(metrics)
        
        return wrapper
    return decorator
```
