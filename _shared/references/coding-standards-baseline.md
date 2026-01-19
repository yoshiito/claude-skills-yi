# Baseline Coding Standards

Universal coding standards that apply to ALL projects. These are non-negotiable minimums.

Projects may extend or override specific rules in their `claude.md` → `## Coding Standards` section.

---

## Security Standards (CRITICAL)

These standards prevent common vulnerabilities. Violations are always **Critical** severity.

### No Hardcoded Secrets

```
❌ BAD:
api_key = "sk-1234567890abcdef"
password = "admin123"
connection_string = "postgres://user:pass@localhost/db"

✅ GOOD:
api_key = os.environ.get("API_KEY")
password = config.get_secret("db_password")
connection_string = settings.DATABASE_URL
```

**Rule**: Never commit secrets, API keys, passwords, or credentials to code.

### Input Validation

```
❌ BAD:
def get_user(user_id):
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")

✅ GOOD:
def get_user(user_id: int):
    if not isinstance(user_id, int) or user_id < 0:
        raise ValueError("Invalid user ID")
    return db.query("SELECT * FROM users WHERE id = ?", [user_id])
```

**Rule**: Validate and sanitize all external input (user input, API params, file uploads).

### SQL Injection Prevention

```
❌ BAD:
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

✅ GOOD:
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))
```

**Rule**: Always use parameterized queries. Never concatenate user input into SQL.

### XSS Prevention

```
❌ BAD (JavaScript/Frontend):
element.innerHTML = userInput;

✅ GOOD:
element.textContent = userInput;
// Or use a sanitization library if HTML is needed
```

**Rule**: Encode/escape output. Never render untrusted HTML directly.

### Authentication & Authorization

**Rule**: Every endpoint that accesses protected resources must verify:
1. User is authenticated (valid session/token)
2. User is authorized (has permission for this action)

### Sensitive Data Logging

```
❌ BAD:
logger.info(f"User login: {email}, password: {password}")
logger.debug(f"API response: {response_with_pii}")

✅ GOOD:
logger.info(f"User login attempt: {email}")
logger.debug(f"API response status: {response.status_code}")
```

**Rule**: Never log passwords, tokens, PII, or full response bodies containing sensitive data.

---

## Error Handling Standards

### Catch and Handle Appropriately

```
❌ BAD:
try:
    process_data()
except:
    pass  # Silent failure

❌ BAD:
try:
    process_data()
except Exception as e:
    print(e)  # Logging to stdout, not handled

✅ GOOD:
try:
    process_data()
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    return {"error": "Invalid input"}, 400
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise ServiceUnavailable("Please try again later")
```

**Rule**: Catch specific exceptions. Log appropriately. Handle or re-raise.

### No Information Leakage

```
❌ BAD:
except Exception as e:
    return {"error": str(e)}  # May expose internal details

✅ GOOD:
except Exception as e:
    logger.error(f"Internal error: {e}", exc_info=True)
    return {"error": "An internal error occurred"}, 500
```

**Rule**: Don't expose stack traces, internal paths, or system details to end users.

### No Silent Failures

```
❌ BAD:
def send_email(user):
    try:
        email_service.send(user.email)
    except:
        pass  # Email silently fails

✅ GOOD:
def send_email(user):
    try:
        email_service.send(user.email)
    except EmailError as e:
        logger.error(f"Failed to send email to {user.id}: {e}")
        # Decide: retry, queue, or alert
        raise
```

**Rule**: All failures must be logged and either handled or surfaced.

---

## Code Quality Standards

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | Descriptive, camelCase or snake_case (be consistent) | `userEmail`, `user_email` |
| Functions | Verb + noun, describes action | `getUserById()`, `validate_input()` |
| Classes | PascalCase, noun | `UserService`, `OrderRepository` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT` |
| Booleans | Reads as question | `isValid`, `hasPermission`, `canEdit` |

**Rule**: Names should be self-documenting. Avoid abbreviations unless universally understood.

### Single Responsibility

```
❌ BAD:
def process_order(order):
    # Validates order
    # Saves to database
    # Sends email
    # Updates inventory
    # Logs analytics
    # ... 200 lines

✅ GOOD:
def process_order(order):
    validated = validate_order(order)
    saved = order_repository.save(validated)
    notification_service.send_confirmation(saved)
    inventory_service.update(saved.items)
    analytics.track_order(saved)
```

**Rule**: Functions do one thing. Classes have one reason to change.

### No Dead Code

```
❌ BAD:
def calculate_total(items):
    # Old implementation
    # total = sum(i.price for i in items)
    # return total * 1.1  # 10% tax

    # New implementation
    return sum(i.price * i.quantity for i in items)
```

**Rule**: Delete commented-out code. Use version control for history.

### Magic Numbers and Strings

```
❌ BAD:
if retries > 3:
    sleep(5)
if status == "A":
    ...

✅ GOOD:
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
STATUS_ACTIVE = "A"

if retries > MAX_RETRIES:
    sleep(RETRY_DELAY_SECONDS)
if status == STATUS_ACTIVE:
    ...
```

**Rule**: Extract magic values to named constants. Makes code self-documenting.

### Comments

```
❌ BAD:
# Increment counter
counter += 1

# Get user
user = get_user(id)

✅ GOOD:
# Workaround for legacy API that returns 1-indexed results
index = api_index - 1

# Rate limit: max 100 requests per minute per user (see RFC-2023-04)
if request_count > RATE_LIMIT:
    raise RateLimitExceeded()
```

**Rule**: Comment WHY, not WHAT. Code should explain what it does; comments explain why.

---

## Architecture Standards

### Layer Separation

```
❌ BAD:
# Controller directly queries database
@app.get("/users/{id}")
def get_user(id):
    return db.query("SELECT * FROM users WHERE id = ?", [id])

✅ GOOD:
# Controller → Service → Repository
@app.get("/users/{id}")
def get_user(id, user_service: UserService):
    return user_service.get_by_id(id)
```

**Rule**: Maintain clear boundaries between layers (controller/service/repository).

### Dependency Direction

```
❌ BAD:
# Domain depends on infrastructure
class User:
    def save(self):
        PostgresDB.insert(self)  # Domain knows about specific DB

✅ GOOD:
# Infrastructure depends on domain
class UserRepository:
    def save(self, user: User):
        self.db.insert(user)  # Repository handles persistence
```

**Rule**: Dependencies point inward. Domain doesn't know about infrastructure.

### No Circular Dependencies

**Rule**: Module A depends on B, B depends on C, C must NOT depend on A.

---

## Testing Standards

### Tests Exist for New Code

**Rule**: New functionality must have tests. No exceptions for "it's simple."

### Test Coverage

| Type | Minimum Coverage |
|------|------------------|
| Critical paths (auth, payments) | 90%+ |
| Business logic | 80%+ |
| Utilities | 70%+ |
| Glue code | Not required |

### Test Naming

```
❌ BAD:
def test_user():
def test_1():
def test_feature():

✅ GOOD:
def test_create_user_with_valid_email_succeeds():
def test_create_user_with_duplicate_email_returns_409():
def test_get_user_by_id_when_not_found_returns_404():
```

**Rule**: Test name should describe: what is being tested, under what conditions, expected result.

### No Flaky Tests

**Rule**: Tests must be deterministic. No:
- Sleep/timeouts as synchronization
- Dependency on external services without mocking
- Order-dependent tests
- Tests that fail intermittently

---

## Performance Standards

### N+1 Query Prevention

```
❌ BAD:
users = User.all()
for user in users:
    print(user.orders.count())  # Query per user

✅ GOOD:
users = User.all().prefetch_related('orders')
for user in users:
    print(len(user.orders))  # Prefetched
```

**Rule**: Use eager loading/joins for related data. Monitor query counts.

### Resource Cleanup

```
❌ BAD:
file = open("data.txt")
data = file.read()
# File never closed

✅ GOOD:
with open("data.txt") as file:
    data = file.read()
# Automatically closed
```

**Rule**: Use context managers or try/finally for resources (files, connections, locks).

### Async Context Awareness

```
❌ BAD (in async context):
async def fetch_data():
    time.sleep(5)  # Blocks event loop

✅ GOOD:
async def fetch_data():
    await asyncio.sleep(5)  # Non-blocking
```

**Rule**: No blocking calls in async contexts. Use async equivalents.

---

## How to Override Baseline Standards

Projects can override specific baseline standards in their `claude.md`:

```markdown
## Coding Standards

### Overrides from Baseline

| Baseline Rule | Project Override | Rationale |
|---------------|------------------|-----------|
| Test coverage 80% | 70% acceptable | Legacy codebase migration |
| camelCase variables | snake_case only | Python project convention |

### [Rest of project-specific standards]
```

**Important**: Overrides should be explicit and justified. Security standards should rarely be overridden.
