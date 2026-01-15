# Log Analysis Patterns

This guide covers techniques for reading and analyzing application logs, plus recommendations for structured logging setup.

## Log Analysis Fundamentals

### Finding Relevant Logs

1. **Identify log location** (from project config)
2. **Filter by time window** around the incident
3. **Search for identifiers**: request ID, user ID, error code
4. **Follow the correlation chain** across services

### Using Claude Code Tools

```
# Find log files
Glob("**/logs/*.log")
Glob("/var/log/app/**/*.log")

# Search for specific error
Grep(pattern="ERROR.*authentication", path="/var/log/app/")

# Read recent log entries
Read("/var/log/app/api.log", offset=-100)  # Last 100 lines
```

## Log Levels and Their Meaning

| Level | When to Use | Investigation Priority |
|-------|-------------|----------------------|
| `CRITICAL` | System failure, data loss | Immediate |
| `ERROR` | Operation failed, needs attention | High |
| `WARNING` | Unexpected but handled | Medium |
| `INFO` | Normal operations | Reference |
| `DEBUG` | Detailed diagnostic | Deep dive only |

### Reading Strategy by Level

1. **Start with ERROR/CRITICAL** - These are the problems
2. **Check WARNING before ERROR** - Often shows degradation leading to failure
3. **Use INFO for context** - What was the system doing?
4. **DEBUG only if needed** - For deep technical investigation

## Common Log Patterns to Recognize

### HTTP Request Logs

```
2025-01-15T10:30:45Z INFO [api] method=POST path=/api/users status=201 duration=45ms
2025-01-15T10:30:46Z ERROR [api] method=GET path=/api/users/123 status=500 duration=1203ms error="database connection timeout"
```

**Key fields**: method, path, status code, duration, error

**What to look for**:
- Status 5xx = Server errors (your problem)
- Status 4xx = Client errors (usually their problem, but patterns indicate issues)
- Long duration = Performance problems
- Repeated paths = Potential hotspots

### Database Query Logs

```
2025-01-15T10:30:45Z DEBUG [db] query="SELECT * FROM users WHERE id = ?" params=[123] duration=5ms
2025-01-15T10:30:46Z WARNING [db] query="SELECT * FROM orders WHERE user_id = ?" params=[123] duration=2500ms slow_query=true
```

**What to look for**:
- `slow_query` flags
- Duration > threshold (varies by query type)
- N+1 patterns (same query repeated with different params)
- Lock wait / deadlock messages

### Authentication/Authorization Logs

```
2025-01-15T10:30:45Z INFO [auth] event=login_success user_id=123 ip=192.168.1.1
2025-01-15T10:30:46Z WARNING [auth] event=login_failed email=user@example.com reason=invalid_password attempts=3
2025-01-15T10:30:47Z ERROR [auth] event=token_validation_failed reason=expired token_age=3601s
```

**What to look for**:
- Failed login patterns (brute force?)
- Token expiration issues
- Permission denied for legitimate users

### Background Job Logs

```
2025-01-15T10:30:45Z INFO [worker] job=send_email job_id=abc123 status=started
2025-01-15T10:30:50Z INFO [worker] job=send_email job_id=abc123 status=completed duration=5s
2025-01-15T10:30:55Z ERROR [worker] job=process_payment job_id=def456 status=failed error="payment gateway timeout" retry=1/3
```

**What to look for**:
- Jobs stuck in `started` without completion
- High retry counts
- Repeated failures for same job type

## Correlation and Tracing

### Using Request IDs

Modern applications use request/correlation IDs to trace requests across services:

```
# All logs for a specific request
Grep(pattern="request_id=req_abc123", path="/var/log/app/")
```

This reveals the full journey:
```
10:30:45 [gateway] request_id=req_abc123 Received request
10:30:45 [api] request_id=req_abc123 Processing /api/orders
10:30:46 [db] request_id=req_abc123 SELECT * FROM orders...
10:30:46 [cache] request_id=req_abc123 Cache miss for order_123
10:30:47 [api] request_id=req_abc123 Returning 200
```

### Distributed Tracing

For microservices, look for trace IDs:
```
trace_id=trace_xyz span_id=span_001
```

These connect logs across service boundaries.

## Structured Logging Recommendations

### Why Structured Logs?

| Unstructured | Structured |
|--------------|------------|
| `Error processing user 123: connection timeout` | `{"level":"error","user_id":123,"error":"connection_timeout"}` |
| Hard to parse programmatically | Easy to filter and aggregate |
| Inconsistent format | Consistent schema |

### Recommended Log Schema

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "ERROR",
  "logger": "api.users",
  "message": "Failed to fetch user",
  "request_id": "req_abc123",
  "trace_id": "trace_xyz",
  "user_id": "user_456",
  "error": {
    "type": "DatabaseError",
    "message": "Connection timeout",
    "code": "DB_TIMEOUT"
  },
  "context": {
    "endpoint": "/api/users/456",
    "method": "GET",
    "duration_ms": 5000
  }
}
```

### Key Fields to Always Include

| Field | Purpose |
|-------|---------|
| `timestamp` | When (ISO 8601 format) |
| `level` | Severity |
| `logger` | Which component |
| `message` | Human-readable description |
| `request_id` | Correlation across logs |
| `error` | Error details (when applicable) |

### Python Logging Setup Example

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Usage
logger.info("user_created", user_id=123, email="user@example.com")
logger.error("payment_failed",
    user_id=123,
    error_code="INSUFFICIENT_FUNDS",
    amount=99.99
)
```

## Log Analysis Checklist

When investigating an issue:

- [ ] Identify the time window of the incident
- [ ] Find the first error occurrence
- [ ] Trace back 5-10 minutes for precursor warnings
- [ ] Check for correlated errors in other services
- [ ] Look for patterns (same error repeated, escalating frequency)
- [ ] Identify affected users/requests
- [ ] Note any recent deployments in that time window
- [ ] Check resource metrics (if available) - memory, CPU, connections

## Common Pitfalls

### Log Volume
- **Problem**: Too many logs to read
- **Solution**: Use Grep with specific patterns, filter by level

### Missing Context
- **Problem**: Logs don't have enough info to debug
- **Solution**: Add request IDs, user IDs, relevant business context

### Time Zone Confusion
- **Problem**: Logs in different time zones
- **Solution**: Always use UTC, convert user-reported times

### Stale Logs
- **Problem**: Looking at old logs after rotation
- **Solution**: Check log rotation schedule, look in archived logs

## Quick Reference: Search Patterns

```bash
# Errors in time range
grep "2025-01-15T10:3" /var/log/app/api.log | grep ERROR

# Specific user
grep "user_id.*123" /var/log/app/*.log

# Slow operations
grep "duration.*[0-9]\{4,\}ms" /var/log/app/api.log  # 4+ digit ms = 1s+

# Failed requests
grep "status.*5[0-9][0-9]" /var/log/app/api.log

# Connection issues
grep -i "connection\|timeout\|refused" /var/log/app/*.log
```
