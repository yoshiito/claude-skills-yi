# MCP Security Checklist

Comprehensive security requirements and best practices for MCP servers.

## Security Principles

1. **Least Privilege** - Only expose what's necessary
2. **Defense in Depth** - Multiple layers of protection
3. **Fail Secure** - Errors should deny, not allow
4. **Input Validation** - Never trust client data
5. **Output Sanitization** - Don't leak sensitive data

## Pre-Deployment Checklist

### Input Validation

- [ ] **All tool parameters are validated**
  ```python
  @mcp.tool()
  def get_user(user_id: str) -> dict:
      # Validate format before use
      if not is_valid_uuid(user_id):
          raise ToolError("Invalid user ID format")
      ...
  ```

- [ ] **String lengths are bounded**
  ```python
  class Input(BaseModel):
      name: str = Field(..., max_length=200)
      description: str = Field(None, max_length=5000)
  ```

- [ ] **Numeric ranges are enforced**
  ```python
  class Input(BaseModel):
      quantity: int = Field(..., ge=1, le=1000)
      price: float = Field(..., ge=0, le=1000000)
  ```

- [ ] **Enums used for fixed options**
  ```python
  class Status(str, Enum):
      PENDING = "pending"
      COMPLETED = "completed"

  # Not: status: str  # Too permissive
  ```

- [ ] **Arrays have size limits**
  ```python
  class Input(BaseModel):
      items: list[str] = Field(..., max_length=100)
  ```

### Path Traversal Prevention

- [ ] **File paths are validated against allowed directories**
  ```python
  ALLOWED_DIR = Path("/app/data").resolve()

  @mcp.tool()
  def read_file(path: str) -> str:
      resolved = Path(path).resolve()

      # Check path is within allowed directory
      if not resolved.is_relative_to(ALLOWED_DIR):
          raise ToolError("Access denied: path outside allowed directory")

      # Check path exists and is a file
      if not resolved.is_file():
          raise ToolError("File not found")

      return resolved.read_text()
  ```

- [ ] **No path components like `..` allowed**
  ```python
  def validate_path(path: str) -> Path:
      if ".." in path:
          raise ToolError("Invalid path: '..' not allowed")

      resolved = (ALLOWED_DIR / path).resolve()
      if not resolved.is_relative_to(ALLOWED_DIR):
          raise ToolError("Access denied")

      return resolved
  ```

- [ ] **Symlinks are handled safely**
  ```python
  resolved = Path(path).resolve()  # Follows symlinks
  # Then check if result is still in allowed directory
  ```

### SQL Injection Prevention

- [ ] **Parameterized queries used (never string interpolation)**
  ```python
  # ✓ Correct - parameterized
  query = "SELECT * FROM users WHERE id = :user_id"
  result = db.execute(text(query), {"user_id": user_id})

  # ✗ Wrong - SQL injection vulnerable
  query = f"SELECT * FROM users WHERE id = '{user_id}'"  # NEVER
  ```

- [ ] **ORM preferred over raw SQL when possible**
  ```python
  # ✓ Preferred - ORM handles escaping
  user = db.exec(select(User).where(User.id == user_id)).first()
  ```

- [ ] **Raw SQL inputs are type-checked before use**
  ```python
  def search(query: str, limit: int) -> list:
      # Validate limit is actually an int
      if not isinstance(limit, int) or limit < 1 or limit > 100:
          raise ToolError("Invalid limit")
      ...
  ```

### Command Injection Prevention

- [ ] **Shell commands use subprocess with list arguments**
  ```python
  # ✓ Correct - arguments are not shell-interpreted
  result = subprocess.run(["ls", "-la", directory], capture_output=True)

  # ✗ Wrong - shell injection possible
  result = subprocess.run(f"ls -la {directory}", shell=True)  # NEVER
  ```

- [ ] **User input never passed directly to shell**
  ```python
  # If shell is absolutely necessary, validate strictly
  ALLOWED_COMMANDS = {"status", "version", "help"}

  def run_command(command: str) -> str:
      if command not in ALLOWED_COMMANDS:
          raise ToolError(f"Unknown command: {command}")
      ...
  ```

### Output Sanitization

- [ ] **Sensitive fields removed from responses**
  ```python
  @mcp.tool()
  def get_user(user_id: str) -> dict:
      user = db.get_user(user_id)

      return {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          # Excluded: password_hash, api_keys, ssn, etc.
      }
  ```

- [ ] **Error messages don't leak internal details**
  ```python
  try:
      result = db.query(...)
  except DatabaseError as e:
      # ✗ Wrong - exposes internal details
      raise ToolError(f"Database error: {e}")

      # ✓ Correct - generic message, log details internally
      logger.error(f"Database error: {e}")
      raise ToolError("Unable to retrieve data. Please try again.")
  ```

- [ ] **Stack traces not exposed to clients**
  ```python
  @mcp.tool()
  def risky_operation() -> dict:
      try:
          return perform_operation()
      except Exception as e:
          logger.exception("Operation failed")
          raise ToolError("Operation failed. Contact support if this persists.")
  ```

### Rate Limiting

- [ ] **Tools are rate limited**
  ```python
  from functools import wraps
  from time import time

  def rate_limit(calls: int, period: int):
      """Limit to `calls` per `period` seconds."""
      timestamps = []

      def decorator(func):
          @wraps(func)
          async def wrapper(*args, **kwargs):
              now = time()
              timestamps[:] = [t for t in timestamps if now - t < period]
              if len(timestamps) >= calls:
                  raise ToolError(
                      f"Rate limit exceeded. Maximum {calls} calls per {period} seconds."
                  )
              timestamps.append(now)
              return await func(*args, **kwargs)
          return wrapper
      return decorator

  @mcp.tool()
  @rate_limit(calls=100, period=60)
  def api_call() -> dict:
      ...
  ```

- [ ] **Expensive operations have stricter limits**
  ```python
  @mcp.tool()
  @rate_limit(calls=10, period=60)
  def generate_report() -> dict:
      """Generate report - limited to 10/minute due to resource intensity."""
      ...
  ```

- [ ] **Rate limits apply per-session or per-user**
  ```python
  # Track by session ID for per-session limits
  rate_limiters: dict[str, RateLimiter] = {}

  @mcp.tool()
  async def limited_tool(ctx: Context) -> dict:
      session_id = ctx.session.id
      limiter = rate_limiters.setdefault(session_id, RateLimiter())

      if not limiter.allow():
          raise ToolError("Rate limit exceeded")
      ...
  ```

### Authentication (Remote Servers)

- [ ] **Authentication required for all endpoints**
  ```python
  async def verify_token(authorization: str = Header(...)):
      if not authorization.startswith("Bearer "):
          raise HTTPException(401, "Invalid authorization header")

      token = authorization[7:]
      if not verify_jwt(token):
          raise HTTPException(401, "Invalid or expired token")
  ```

- [ ] **API keys are not logged or exposed**
  ```python
  # ✓ Correct - mask sensitive values in logs
  logger.info(f"Request from API key: {api_key[:8]}...")

  # ✗ Wrong - full key in logs
  logger.info(f"Request with key: {api_key}")
  ```

- [ ] **Tokens have appropriate expiration**
  ```python
  def create_token(user_id: str) -> str:
      return jwt.encode({
          "sub": user_id,
          "exp": datetime.utcnow() + timedelta(hours=1)  # Short expiry
      }, SECRET_KEY)
  ```

- [ ] **Session IDs are cryptographically secure**
  ```python
  import secrets

  def generate_session_id() -> str:
      return secrets.token_urlsafe(32)  # 256 bits of entropy
  ```

### Authorization

- [ ] **Users can only access their own data**
  ```python
  @mcp.tool()
  async def get_my_tasks(ctx: Context) -> list[Task]:
      user_id = ctx.session.user_id

      # Only return tasks owned by this user
      return db.query(Task).filter(Task.owner_id == user_id).all()
  ```

- [ ] **Admin operations require elevated permissions**
  ```python
  @mcp.tool()
  async def delete_user(user_id: str, ctx: Context) -> dict:
      if not ctx.session.is_admin:
          raise ToolError("Admin permission required")
      ...
  ```

- [ ] **Resource access is scoped appropriately**
  ```python
  @mcp.tool()
  async def read_document(doc_id: str, ctx: Context) -> dict:
      doc = db.get_document(doc_id)

      # Check user has access to this document
      if not user_can_access(ctx.session.user_id, doc):
          raise ToolError("Access denied")

      return doc
  ```

### Transport Security

- [ ] **HTTPS used in production**
  ```python
  # Production deployment
  if __name__ == "__main__":
      mcp.run(
          transport="streamable-http",
          host="0.0.0.0",
          port=443,
          ssl_certfile="/etc/ssl/cert.pem",
          ssl_keyfile="/etc/ssl/key.pem"
      )
  ```

- [ ] **Local servers bind to localhost only**
  ```python
  # Development - localhost only
  mcp.run(
      transport="streamable-http",
      host="127.0.0.1",  # Not 0.0.0.0
      port=8000
  )
  ```

- [ ] **DNS rebinding protection enabled**
  ```typescript
  // TypeScript
  const app = createMcpExpressApp(server, {
    allowedHosts: ['localhost', '127.0.0.1', 'api.example.com']
  });
  ```

- [ ] **Origin header validated for HTTP transport**
  ```python
  ALLOWED_ORIGINS = {"https://claude.ai", "https://cursor.so"}

  async def validate_origin(request: Request):
      origin = request.headers.get("Origin")
      if origin and origin not in ALLOWED_ORIGINS:
          raise HTTPException(403, "Invalid origin")
  ```

### Secrets Management

- [ ] **Secrets loaded from environment, not hardcoded**
  ```python
  # ✓ Correct
  API_KEY = os.environ["API_KEY"]
  DATABASE_URL = os.environ["DATABASE_URL"]

  # ✗ Wrong
  API_KEY = "sk-1234567890"  # NEVER hardcode
  ```

- [ ] **Secrets not in version control**
  ```gitignore
  # .gitignore
  .env
  .env.local
  *.pem
  credentials.json
  ```

- [ ] **Different secrets for each environment**
  ```bash
  # dev.env
  API_KEY=dev-key-xxx

  # prod.env
  API_KEY=prod-key-yyy  # Different!
  ```

### Logging and Monitoring

- [ ] **Security events are logged**
  ```python
  logger.warning(f"Rate limit exceeded for session {session_id}")
  logger.warning(f"Invalid API key attempt from {ip_address}")
  logger.error(f"Authorization denied for user {user_id} on resource {resource_id}")
  ```

- [ ] **Sensitive data not logged**
  ```python
  # ✓ Correct
  logger.info(f"User {user_id} authenticated")

  # ✗ Wrong
  logger.info(f"User {user_id} authenticated with password {password}")
  ```

- [ ] **Logs are retained appropriately**
  ```python
  # Configure log rotation
  logging.handlers.RotatingFileHandler(
      "server.log",
      maxBytes=10_000_000,  # 10MB
      backupCount=5
  )
  ```

### Error Handling

- [ ] **Errors don't expose internal state**
  ```python
  except DatabaseError as e:
      # Log full error internally
      logger.error(f"Database error: {e}", exc_info=True)

      # Return generic message to client
      raise ToolError("Database operation failed")
  ```

- [ ] **Failures are fail-secure**
  ```python
  def check_permission(user_id: str, resource_id: str) -> bool:
      try:
          return permission_service.check(user_id, resource_id)
      except Exception:
          # On error, deny access (fail secure)
          logger.error("Permission check failed", exc_info=True)
          return False  # Not True!
  ```

## Security Anti-Patterns

### Don't Do This

**Trusting client input:**
```python
# ✗ Bad - trusts client-provided user ID
@mcp.tool()
def get_user_data(user_id: str) -> dict:
    return db.get_all_user_data(user_id)  # Anyone can access anyone's data

# ✓ Good - use authenticated user's ID
@mcp.tool()
async def get_my_data(ctx: Context) -> dict:
    return db.get_all_user_data(ctx.session.user_id)
```

**Exposing internal errors:**
```python
# ✗ Bad
except Exception as e:
    raise ToolError(str(e))  # May contain sensitive info

# ✓ Good
except Exception as e:
    logger.exception("Operation failed")
    raise ToolError("Operation failed")
```

**SQL with string formatting:**
```python
# ✗ Bad - SQL injection
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✓ Good - parameterized
query = "SELECT * FROM users WHERE name = :name"
db.execute(text(query), {"name": name})
```

**Shell with user input:**
```python
# ✗ Bad - command injection
subprocess.run(f"grep {pattern} {file}", shell=True)

# ✓ Good - use list arguments
subprocess.run(["grep", pattern, file])
```

**Hardcoded secrets:**
```python
# ✗ Bad
API_KEY = "sk-prod-12345"

# ✓ Good
API_KEY = os.environ["API_KEY"]
```

## Specific Attack Mitigations

### Confused Deputy Prevention

When your server acts on behalf of users, ensure it validates the user has permission:

```python
@mcp.tool()
async def delete_resource(resource_id: str, ctx: Context) -> dict:
    resource = db.get_resource(resource_id)

    # Verify current user owns this resource
    if resource.owner_id != ctx.session.user_id:
        raise ToolError("Access denied")

    db.delete(resource)
    return {"deleted": True}
```

### Tool Poisoning Defense

If loading tool definitions from external sources, validate them:

```python
def load_external_tool(definition: dict) -> None:
    # Only allow tools from trusted sources
    if definition.get("source") not in TRUSTED_SOURCES:
        raise SecurityError("Untrusted tool source")

    # Validate tool schema
    validate_tool_schema(definition)

    # Sanitize description (could contain injection attempts)
    definition["description"] = sanitize_text(definition["description"])
```

### Supply Chain Security

```python
# Pin dependencies to specific versions
# requirements.txt
mcp==1.0.0
pydantic==2.5.0
fastapi==0.109.0

# Verify package integrity
# pip install --require-hashes -r requirements.txt
```

## Security Testing

### Test Cases to Include

```python
def test_path_traversal_blocked():
    """Ensure path traversal attacks are blocked."""
    with pytest.raises(ToolError) as exc:
        await server.call_tool("read_file", {"path": "../../../etc/passwd"})
    assert "Access denied" in str(exc.value)

def test_sql_injection_blocked():
    """Ensure SQL injection is prevented."""
    result = await server.call_tool("search_users", {
        "query": "'; DROP TABLE users; --"
    })
    # Should return empty results, not execute DROP
    assert "error" not in result

def test_rate_limiting():
    """Ensure rate limiting works."""
    for _ in range(100):
        await server.call_tool("api_call", {})

    with pytest.raises(ToolError) as exc:
        await server.call_tool("api_call", {})
    assert "Rate limit" in str(exc.value)

def test_auth_required():
    """Ensure authentication is required."""
    response = client.post("/mcp/tools/call", json={...})
    assert response.status_code == 401

def test_authorization_enforced():
    """Ensure users can't access others' data."""
    # Login as user A
    token_a = login("user_a")

    # Try to access user B's data
    with pytest.raises(ToolError) as exc:
        await server.call_tool("get_user_data", {
            "user_id": "user_b_id"
        })
    assert "Access denied" in str(exc.value)
```

## Summary

Before deploying an MCP server:

1. **Validate all inputs** - Type check, bound lengths, use enums
2. **Sanitize all outputs** - Remove sensitive fields, generic errors
3. **Prevent injection attacks** - Parameterized queries, no shell=True
4. **Implement rate limiting** - Protect against abuse
5. **Authenticate remote access** - Tokens, API keys
6. **Authorize resource access** - Users see only their data
7. **Secure transport** - HTTPS, localhost binding
8. **Manage secrets properly** - Environment variables, not code
9. **Log security events** - Without logging sensitive data
10. **Test security controls** - Automated security tests
