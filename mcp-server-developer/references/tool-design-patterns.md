# Tool Design Patterns

Best practices and patterns for designing effective MCP tools.

## Design Principles

### 1. Single Responsibility

Each tool should do one thing well.

```python
# ✓ Good - focused, single-purpose tools
@mcp.tool()
def search_issues(
    query: str,
    repo: str,
    state: str = "open"
) -> list[Issue]:
    """Search for issues in a repository."""
    ...

@mcp.tool()
def create_issue(
    repo: str,
    title: str,
    body: str
) -> Issue:
    """Create a new issue in a repository."""
    ...

@mcp.tool()
def close_issue(
    repo: str,
    issue_number: int,
    reason: str = None
) -> Issue:
    """Close an existing issue."""
    ...

# ✗ Bad - multi-purpose tool with action parameter
@mcp.tool()
def manage_issues(
    action: str,  # "search", "create", "close", "update"
    repo: str,
    query: str = None,
    title: str = None,
    body: str = None,
    issue_number: int = None
):
    """Manage issues - search, create, close, or update."""
    if action == "search":
        ...
    elif action == "create":
        ...
    # Complex, hard for LLM to use correctly
```

**Why:** LLMs understand focused tools better. Complex multi-action tools lead to incorrect usage.

### 2. Clear, Descriptive Names

Use `verb_noun` format that describes the action.

| Good Names | Bad Names |
|------------|-----------|
| `create_issue` | `issue` |
| `search_documents` | `docs` |
| `get_user_profile` | `user` |
| `send_notification` | `notify` |
| `calculate_shipping` | `shipping` |
| `validate_email` | `email_check` |

### 3. Comprehensive Descriptions

Write descriptions that help LLMs understand when and how to use the tool.

```python
@mcp.tool()
def search_products(
    query: str,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    in_stock: bool = True
) -> list[Product]:
    """Search the product catalog by keyword.

    Use this tool when the user wants to find products by name, description,
    or brand. Results are ranked by relevance.

    Examples of when to use:
    - "Find red running shoes"
    - "Show me laptops under $1000"
    - "Search for wireless headphones"

    The query can include:
    - Product names (e.g., "iPhone 15")
    - Descriptions (e.g., "waterproof bluetooth speaker")
    - Brand names (e.g., "Sony", "Nike")

    Returns up to 20 products sorted by relevance.
    """
    ...
```

### 4. Self-Documenting Parameters

Every parameter should have a clear description.

```python
from pydantic import BaseModel, Field

class CreateOrderInput(BaseModel):
    """Input for creating a new order."""

    customer_id: str = Field(
        ...,
        description="Unique customer identifier (UUID format)"
    )
    items: list[OrderItem] = Field(
        ...,
        description="List of items to order (at least one required)",
        min_length=1
    )
    shipping_address: Address = Field(
        ...,
        description="Delivery address for the order"
    )
    shipping_method: str = Field(
        default="standard",
        description="Shipping speed: 'standard' (5-7 days), 'express' (2-3 days), 'overnight'"
    )
    gift_wrap: bool = Field(
        default=False,
        description="Whether to gift wrap the order (+$5.00)"
    )
    notes: str | None = Field(
        default=None,
        description="Special instructions for the order (max 500 chars)",
        max_length=500
    )
```

## Schema Design Patterns

### Enums for Fixed Options

Use enums when parameters have a fixed set of valid values.

```python
from enum import Enum

class IssueState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

@mcp.tool()
def list_issues(
    repo: str,
    state: IssueState = IssueState.OPEN,
    sort: str = "created",
    order: SortOrder = SortOrder.DESC
) -> list[Issue]:
    """List issues in a repository."""
    ...
```

### Optional vs Required Parameters

Be intentional about what's required vs optional.

```python
@mcp.tool()
def search_users(
    # Required - the core functionality needs this
    query: str,

    # Optional with sensible defaults
    limit: int = 10,
    offset: int = 0,

    # Optional filters - narrow results if provided
    department: str = None,
    role: str = None,
    active_only: bool = True
) -> list[User]:
    """Search for users by name or email."""
    ...
```

**Rules of thumb:**
- **Required:** Parameters essential for the tool to function
- **Optional with defaults:** Common parameters with sensible defaults
- **Optional nullable:** Filters that narrow results when provided

### Structured Output

When tools return complex data, use structured output schemas.

```python
from pydantic import BaseModel

class OrderSummary(BaseModel):
    """Summary of an order."""
    order_id: str
    status: str
    total: float
    item_count: int
    created_at: str
    estimated_delivery: str | None

class OrderDetails(BaseModel):
    """Complete order details."""
    order_id: str
    status: str
    customer: CustomerInfo
    items: list[OrderItem]
    subtotal: float
    tax: float
    shipping: float
    total: float
    shipping_address: Address
    billing_address: Address
    created_at: str
    updated_at: str
    tracking_number: str | None

@mcp.tool(output_schema=OrderDetails)
def get_order(order_id: str) -> OrderDetails:
    """Get complete details for an order."""
    ...
```

## Error Handling Patterns

### Descriptive Error Messages

Errors should tell the LLM what went wrong and how to fix it.

```python
from mcp.server.fastmcp import ToolError

@mcp.tool()
def get_user(user_id: str) -> User:
    """Get user by ID."""
    # Validate format
    if not is_valid_uuid(user_id):
        raise ToolError(
            f"Invalid user_id format: '{user_id}'. "
            "Expected UUID format (e.g., '123e4567-e89b-12d3-a456-426614174000')"
        )

    user = db.get_user(user_id)
    if not user:
        raise ToolError(
            f"User not found: '{user_id}'. "
            "Please verify the user ID or search for users by name."
        )

    if not user.is_active:
        raise ToolError(
            f"User '{user_id}' is deactivated. "
            "Use get_inactive_user() to retrieve deactivated user info."
        )

    return user
```

### Graceful Degradation

When partial results are available, return them with context.

```python
@mcp.tool()
def get_dashboard_data() -> DashboardData:
    """Get dashboard metrics and data."""
    result = DashboardData()
    errors = []

    # Try each data source independently
    try:
        result.sales = get_sales_metrics()
    except Exception as e:
        errors.append(f"Sales data unavailable: {e}")
        result.sales = None

    try:
        result.inventory = get_inventory_status()
    except Exception as e:
        errors.append(f"Inventory data unavailable: {e}")
        result.inventory = None

    try:
        result.orders = get_recent_orders()
    except Exception as e:
        errors.append(f"Order data unavailable: {e}")
        result.orders = None

    if errors:
        result.warnings = errors

    return result
```

### Retry Hints

Tell the LLM when retrying might help.

```python
@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email."""
    try:
        result = email_service.send(to, subject, body)
        return {"success": True, "message_id": result.id}
    except RateLimitError:
        raise ToolError(
            "Email rate limit exceeded. Please wait 60 seconds and try again."
        )
    except InvalidRecipientError:
        raise ToolError(
            f"Invalid email address: '{to}'. Please verify the address."
        )
    except ServiceUnavailableError:
        raise ToolError(
            "Email service temporarily unavailable. "
            "This is usually resolved within a few minutes. Please retry."
        )
```

## Common Tool Patterns

### CRUD Operations

Standard pattern for resource management.

```python
# Create
@mcp.tool()
def create_project(name: str, description: str = None) -> Project:
    """Create a new project."""
    ...

# Read (single)
@mcp.tool()
def get_project(project_id: str) -> Project:
    """Get a project by ID."""
    ...

# Read (list with filtering)
@mcp.tool()
def list_projects(
    owner: str = None,
    status: str = None,
    limit: int = 20,
    offset: int = 0
) -> list[Project]:
    """List projects with optional filters."""
    ...

# Update
@mcp.tool()
def update_project(
    project_id: str,
    name: str = None,
    description: str = None,
    status: str = None
) -> Project:
    """Update a project's properties."""
    ...

# Delete
@mcp.tool()
def delete_project(project_id: str) -> dict:
    """Delete a project."""
    ...
```

### Search with Pagination

Pattern for searchable collections.

```python
class SearchResult(BaseModel):
    """Paginated search result."""
    items: list[Document]
    total: int
    limit: int
    offset: int
    has_more: bool

@mcp.tool()
def search_documents(
    query: str,
    folder: str = None,
    file_type: str = None,
    created_after: str = None,
    created_before: str = None,
    limit: int = 20,
    offset: int = 0
) -> SearchResult:
    """Search documents by content or metadata.

    Supports pagination - use offset to get more results.
    Maximum 100 results per request.
    """
    limit = min(limit, 100)  # Cap at 100

    results = search_engine.search(
        query=query,
        filters={
            "folder": folder,
            "file_type": file_type,
            "created_after": created_after,
            "created_before": created_before
        },
        limit=limit + 1,  # Fetch one extra to check has_more
        offset=offset
    )

    has_more = len(results) > limit
    items = results[:limit]

    return SearchResult(
        items=items,
        total=search_engine.count(query),
        limit=limit,
        offset=offset,
        has_more=has_more
    )
```

### Batch Operations

For efficiency when operating on multiple items.

```python
class BatchResult(BaseModel):
    """Result of a batch operation."""
    successful: list[str]
    failed: list[dict]  # {"id": "...", "error": "..."}
    total: int
    success_count: int
    failure_count: int

@mcp.tool()
def batch_update_status(
    item_ids: list[str],
    new_status: str
) -> BatchResult:
    """Update status for multiple items at once.

    More efficient than calling update_item multiple times.
    Maximum 100 items per batch.
    """
    if len(item_ids) > 100:
        raise ToolError("Maximum 100 items per batch. Split into multiple calls.")

    successful = []
    failed = []

    for item_id in item_ids:
        try:
            update_item_status(item_id, new_status)
            successful.append(item_id)
        except Exception as e:
            failed.append({"id": item_id, "error": str(e)})

    return BatchResult(
        successful=successful,
        failed=failed,
        total=len(item_ids),
        success_count=len(successful),
        failure_count=len(failed)
    )
```

### Confirmation for Destructive Actions

Pattern for operations that need user confirmation.

```python
@mcp.tool()
def delete_all_completed_tasks(
    project_id: str,
    confirm: bool = False
) -> dict:
    """Delete all completed tasks in a project.

    WARNING: This action cannot be undone.

    Set confirm=True to proceed with deletion.
    Without confirmation, returns a preview of what would be deleted.
    """
    completed_tasks = get_completed_tasks(project_id)

    if not confirm:
        return {
            "action": "preview",
            "message": f"Would delete {len(completed_tasks)} completed tasks",
            "tasks": [{"id": t.id, "title": t.title} for t in completed_tasks[:10]],
            "total_count": len(completed_tasks),
            "instruction": "Set confirm=True to proceed with deletion"
        }

    # Actually delete
    deleted_count = 0
    for task in completed_tasks:
        delete_task(task.id)
        deleted_count += 1

    return {
        "action": "deleted",
        "deleted_count": deleted_count,
        "message": f"Successfully deleted {deleted_count} completed tasks"
    }
```

### Long-Running Operations

Pattern for operations that take time.

```python
@mcp.tool()
async def generate_report(
    report_type: str,
    start_date: str,
    end_date: str,
    ctx: Context
) -> dict:
    """Generate a detailed report.

    This may take several minutes for large date ranges.
    Progress updates will be provided.
    """
    await ctx.info(f"Starting {report_type} report generation...")

    # Phase 1: Data collection
    await ctx.report_progress(progress=0, total=100, message="Collecting data...")
    data = await collect_report_data(start_date, end_date)

    await ctx.report_progress(progress=30, total=100, message="Processing data...")
    processed = process_data(data)

    await ctx.report_progress(progress=60, total=100, message="Generating report...")
    report = generate_report_document(processed)

    await ctx.report_progress(progress=90, total=100, message="Saving report...")
    report_url = save_report(report)

    await ctx.report_progress(progress=100, total=100, message="Complete!")

    return {
        "status": "complete",
        "report_url": report_url,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }
```

## Anti-Patterns to Avoid

### 1. God Tools

```python
# ✗ Bad - does everything
@mcp.tool()
def database(
    operation: str,  # "query", "insert", "update", "delete", "create_table", ...
    table: str,
    data: dict = None,
    where: dict = None,
    sql: str = None
):
    """Perform any database operation."""
    ...
```

**Problem:** Too complex, error-prone, security risk

### 2. Vague Descriptions

```python
# ✗ Bad - unhelpful description
@mcp.tool()
def process(data: dict) -> dict:
    """Process the data."""
    ...

# ✓ Good - clear description
@mcp.tool()
def validate_order(order: OrderInput) -> ValidationResult:
    """Validate an order before submission.

    Checks:
    - All required fields are present
    - Item quantities are positive
    - Shipping address is deliverable
    - Payment method is valid

    Returns validation result with any errors found.
    """
    ...
```

### 3. Exposing Internal Implementation

```python
# ✗ Bad - exposes internal IDs and structure
@mcp.tool()
def get_user(
    _internal_shard_id: int,
    _partition_key: str,
    user_id: str
) -> dict:
    """Get user from the distributed database."""
    ...

# ✓ Good - clean interface
@mcp.tool()
def get_user(user_id: str) -> User:
    """Get user by their unique ID."""
    # Internal sharding logic hidden
    ...
```

### 4. Inconsistent Return Types

```python
# ✗ Bad - inconsistent returns
@mcp.tool()
def find_user(query: str):
    users = search(query)
    if len(users) == 0:
        return "No users found"  # String
    elif len(users) == 1:
        return users[0]  # User object
    else:
        return users  # List

# ✓ Good - consistent return type
@mcp.tool()
def find_users(query: str) -> list[User]:
    """Find users matching the query. Returns empty list if none found."""
    return search(query)
```

### 5. Silent Failures

```python
# ✗ Bad - silently returns None
@mcp.tool()
def get_config(key: str) -> str | None:
    return config.get(key)  # None if not found, no explanation

# ✓ Good - explicit error handling
@mcp.tool()
def get_config(key: str) -> str:
    """Get configuration value by key."""
    value = config.get(key)
    if value is None:
        raise ToolError(
            f"Configuration key '{key}' not found. "
            f"Available keys: {', '.join(config.keys())}"
        )
    return value
```

## Tool Organization

### Namespacing for Large Servers

When a server has many tools, use prefixes for organization.

```python
# GitHub server with namespaced tools
@mcp.tool()
def github_issues_list(...): ...

@mcp.tool()
def github_issues_create(...): ...

@mcp.tool()
def github_issues_close(...): ...

@mcp.tool()
def github_pr_list(...): ...

@mcp.tool()
def github_pr_create(...): ...

@mcp.tool()
def github_pr_merge(...): ...

@mcp.tool()
def github_repos_list(...): ...

@mcp.tool()
def github_repos_create(...): ...
```

### Tool Discovery

Help LLMs discover related tools.

```python
@mcp.tool()
def search_orders(query: str) -> list[OrderSummary]:
    """Search orders by customer name, email, or order ID.

    Returns summary information. For complete order details,
    use get_order() with the order_id.

    Related tools:
    - get_order: Get complete details for a specific order
    - list_orders: List recent orders with filters
    - cancel_order: Cancel a pending order
    """
    ...
```
