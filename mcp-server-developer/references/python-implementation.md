# Python MCP Implementation Guide

Complete guide for building MCP servers with Python using FastMCP.

## Installation

```bash
# Official MCP SDK with CLI tools
pip install "mcp[cli]"

# Or with uv (recommended)
uv add "mcp[cli]"
```

## Basic Server Structure

### Minimal Server

```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP(
    name="my-server",
    version="1.0.0",
    description="My MCP server"
)

# Define a tool
@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### Running the Server

```bash
# Default (stdio transport)
python my_server.py

# With streamable HTTP
python my_server.py --transport streamable-http --port 8000

# Development mode with inspector
mcp dev my_server.py
```

## Tools

### Basic Tool

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

### Tool with Complex Types

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskInput(BaseModel):
    """Input for creating a task."""
    title: str = Field(..., description="Task title", max_length=200)
    description: Optional[str] = Field(None, description="Detailed description")
    priority: Priority = Field(Priority.MEDIUM, description="Task priority level")
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")

class Task(BaseModel):
    """A task in the system."""
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    tags: list[str]
    created_at: str
    status: str

@mcp.tool()
def create_task(task: TaskInput) -> Task:
    """Create a new task.

    Use this when the user wants to add a new task to their list.
    The task will be created with 'pending' status.
    """
    new_task = Task(
        id=generate_id(),
        title=task.title,
        description=task.description,
        priority=task.priority,
        tags=task.tags,
        created_at=datetime.now().isoformat(),
        status="pending"
    )
    save_task(new_task)
    return new_task
```

### Tool with Output Schema

```python
class WeatherData(BaseModel):
    """Weather information."""
    temperature: float = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Current conditions (sunny, cloudy, etc.)")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in km/h")

@mcp.tool(output_schema=WeatherData)
def get_weather(city: str) -> WeatherData:
    """Get current weather for a city."""
    data = weather_api.get_current(city)
    return WeatherData(
        temperature=data["temp_c"],
        conditions=data["condition"],
        humidity=data["humidity"],
        wind_speed=data["wind_kph"]
    )
```

### Async Tools

```python
import httpx

@mcp.tool()
async def fetch_user(user_id: str) -> dict:
    """Fetch user data from the API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
```

### Tool with Context

Access server context for logging, progress, and more.

```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

@mcp.tool()
async def process_files(
    folder: str,
    ctx: Context[ServerSession, None]
) -> dict:
    """Process all files in a folder."""
    files = list_files(folder)
    total = len(files)

    await ctx.info(f"Starting to process {total} files")

    processed = 0
    for i, file in enumerate(files):
        await ctx.report_progress(
            progress=i,
            total=total,
            message=f"Processing {file.name}"
        )
        process_file(file)
        processed += 1

    await ctx.info(f"Completed processing {processed} files")

    return {
        "processed": processed,
        "total": total,
        "folder": folder
    }
```

### Error Handling

```python
from mcp.server.fastmcp import ToolError

@mcp.tool()
def get_order(order_id: str) -> dict:
    """Get order details by ID."""
    # Validate input
    if not order_id:
        raise ToolError("Order ID is required")

    if not is_valid_order_id(order_id):
        raise ToolError(
            f"Invalid order ID format: '{order_id}'. "
            "Expected format: ORD-XXXXXX"
        )

    # Fetch order
    order = db.get_order(order_id)
    if not order:
        raise ToolError(
            f"Order '{order_id}' not found. "
            "Please verify the order ID or search for orders."
        )

    return order.to_dict()
```

## Resources

### Static Resource

```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Application configuration settings."""
    return json.dumps({
        "theme": "dark",
        "language": "en",
        "notifications": True
    })
```

### Dynamic Resource with URI Template

```python
@mcp.resource("file:///{path}")
def read_file(path: str) -> str:
    """Read a file from the project directory."""
    # Security: validate path
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(PROJECT_DIR):
        raise ValueError("Access denied: path outside project directory")

    return resolved.read_text()
```

### Resource with Metadata

```python
@mcp.resource(
    "db://users/{user_id}",
    name="User Profile",
    description="Get user profile by ID",
    mime_type="application/json"
)
def get_user_resource(user_id: str) -> str:
    """User profile data."""
    user = db.get_user(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    return json.dumps(user.to_dict())
```

### Binary Resource

```python
@mcp.resource("images://{image_id}")
def get_image(image_id: str) -> bytes:
    """Get image by ID."""
    image_path = IMAGES_DIR / f"{image_id}.png"
    if not image_path.exists():
        raise ValueError(f"Image {image_id} not found")
    return image_path.read_bytes()
```

## Prompts

### Basic Prompt

```python
@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"""Please review the following {language} code for:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security vulnerabilities

```{language}
{code}
```

Provide specific, actionable feedback."""
```

### Prompt with Multiple Messages

```python
from mcp.types import PromptMessage, TextContent

@mcp.prompt()
def debug_session(error_message: str, code: str) -> list[PromptMessage]:
    """Start a debugging session for an error."""
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"I'm encountering this error:\n\n```\n{error_message}\n```"
            )
        ),
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Here's my code:\n\n```python\n{code}\n```"
            )
        ),
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text="Please help me understand what's causing this error and how to fix it."
            )
        )
    ]
```

### Prompt with Embedded Resource

```python
from mcp.types import PromptMessage, EmbeddedResource, TextResourceContents

@mcp.prompt()
def analyze_with_docs(query: str) -> list[PromptMessage]:
    """Analyze something using documentation context."""
    docs = load_documentation()

    return [
        PromptMessage(
            role="user",
            content=EmbeddedResource(
                type="resource",
                resource=TextResourceContents(
                    uri="docs://api-reference",
                    mimeType="text/markdown",
                    text=docs
                )
            )
        ),
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Based on the documentation above, please help with: {query}"
            )
        )
    ]
```

## Lifespan Management

### Database Connection

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass

@dataclass
class AppContext:
    db: Database
    cache: Cache

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Manage application lifecycle."""
    # Startup
    db = await Database.connect(DATABASE_URL)
    cache = await Cache.connect(REDIS_URL)

    yield AppContext(db=db, cache=cache)

    # Shutdown
    await cache.close()
    await db.close()

mcp = FastMCP("my-server", lifespan=app_lifespan)

@mcp.tool()
async def get_user(user_id: str, ctx: Context) -> dict:
    """Get user from database."""
    # Access lifespan context
    app = ctx.app_context
    return await app.db.get_user(user_id)
```

### HTTP Client Pool

```python
import httpx

@asynccontextmanager
async def http_lifespan(server: FastMCP):
    """Manage HTTP client lifecycle."""
    client = httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_connections=100)
    )
    yield {"http_client": client}
    await client.aclose()

mcp = FastMCP("api-server", lifespan=http_lifespan)

@mcp.tool()
async def fetch_data(url: str, ctx: Context) -> dict:
    """Fetch data from URL."""
    client = ctx.app_context["http_client"]
    response = await client.get(url)
    return response.json()
```

## Transport Configuration

### stdio (Default)

```python
if __name__ == "__main__":
    mcp.run()  # Defaults to stdio
```

### Streamable HTTP

```python
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )
```

### With Authentication

```python
from fastapi import Depends, HTTPException, Header

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from header."""
    if x_api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8000,
        dependencies=[Depends(verify_api_key)]
    )
```

## Testing

### Unit Testing Tools

```python
import pytest
from my_server import mcp

@pytest.mark.asyncio
async def test_add_tool():
    """Test the add tool."""
    result = await mcp.call_tool("add", {"a": 2, "b": 3})
    assert result.content[0].text == "5"

@pytest.mark.asyncio
async def test_create_task():
    """Test task creation."""
    result = await mcp.call_tool("create_task", {
        "task": {
            "title": "Test Task",
            "priority": "high"
        }
    })
    data = json.loads(result.content[0].text)
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_invalid_input():
    """Test error handling for invalid input."""
    with pytest.raises(ToolError) as exc_info:
        await mcp.call_tool("get_order", {"order_id": "invalid"})

    assert "Invalid order ID format" in str(exc_info.value)
```

### Testing with Mocked Dependencies

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_fetch_user_success():
    """Test fetching user from API."""
    mock_response = {
        "id": "123",
        "name": "John Doe",
        "email": "john@example.com"
    }

    with patch("my_server.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=Mock(json=lambda: mock_response)
        )

        result = await mcp.call_tool("fetch_user", {"user_id": "123"})
        data = json.loads(result.content[0].text)

        assert data["name"] == "John Doe"

@pytest.mark.asyncio
async def test_fetch_user_not_found():
    """Test handling of user not found."""
    with patch("my_server.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            side_effect=httpx.HTTPStatusError(
                "Not Found",
                request=Mock(),
                response=Mock(status_code=404)
            )
        )

        with pytest.raises(ToolError) as exc_info:
            await mcp.call_tool("fetch_user", {"user_id": "nonexistent"})

        assert "not found" in str(exc_info.value).lower()
```

### Integration Testing

```python
import subprocess
import json

@pytest.fixture
def server_process():
    """Start server as subprocess for integration testing."""
    proc = subprocess.Popen(
        ["python", "my_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    yield proc
    proc.terminate()
    proc.wait()

def send_request(proc, method: str, params: dict = None, id: int = 1):
    """Send JSON-RPC request to server."""
    request = {
        "jsonrpc": "2.0",
        "id": id,
        "method": method,
        "params": params or {}
    }
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    response = proc.stdout.readline()
    return json.loads(response)

def test_integration_initialize(server_process):
    """Test server initialization."""
    response = send_request(server_process, "initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    })

    assert "error" not in response
    assert response["result"]["serverInfo"]["name"] == "my-server"

def test_integration_tool_call(server_process):
    """Test calling a tool."""
    # Initialize first
    send_request(server_process, "initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    })

    # Call tool
    response = send_request(server_process, "tools/call", {
        "name": "add",
        "arguments": {"a": 5, "b": 3}
    }, id=2)

    assert "error" not in response
    assert response["result"]["content"][0]["text"] == "8"
```

## Complete Example Server

```python
"""
Example MCP server for a task management system.
"""
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import json
import uuid

from mcp.server.fastmcp import FastMCP, Context, ToolError
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field


# Models
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: Priority
    status: Status
    tags: list[str] = []
    created_at: str
    updated_at: str

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Priority = Priority.MEDIUM
    tags: list[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    tags: Optional[list[str]] = None


# In-memory storage (replace with real database)
@dataclass
class AppState:
    tasks: dict[str, Task]

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Initialize application state."""
    yield AppState(tasks={})


# Create server
mcp = FastMCP(
    name="task-manager",
    version="1.0.0",
    description="Task management MCP server",
    lifespan=app_lifespan
)


# Tools
@mcp.tool()
async def create_task(
    task: TaskCreate,
    ctx: Context[ServerSession, AppState]
) -> Task:
    """Create a new task.

    Use this when the user wants to add a new task to their list.
    Tasks are created with 'pending' status by default.
    """
    now = datetime.now().isoformat()
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=Status.PENDING,
        tags=task.tags,
        created_at=now,
        updated_at=now
    )
    ctx.app_context.tasks[new_task.id] = new_task
    await ctx.info(f"Created task: {new_task.title}")
    return new_task

@mcp.tool()
async def get_task(
    task_id: str,
    ctx: Context[ServerSession, AppState]
) -> Task:
    """Get a task by ID."""
    task = ctx.app_context.tasks.get(task_id)
    if not task:
        raise ToolError(f"Task '{task_id}' not found")
    return task

@mcp.tool()
async def list_tasks(
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    tag: Optional[str] = None,
    ctx: Context[ServerSession, AppState] = None
) -> list[Task]:
    """List all tasks with optional filters.

    Filter by status, priority, or tag. Returns all tasks if no filters provided.
    """
    tasks = list(ctx.app_context.tasks.values())

    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if tag:
        tasks = [t for t in tasks if tag in t.tags]

    return sorted(tasks, key=lambda t: t.created_at, reverse=True)

@mcp.tool()
async def update_task(
    task_id: str,
    updates: TaskUpdate,
    ctx: Context[ServerSession, AppState]
) -> Task:
    """Update an existing task."""
    task = ctx.app_context.tasks.get(task_id)
    if not task:
        raise ToolError(f"Task '{task_id}' not found")

    # Apply updates
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now().isoformat()
    await ctx.info(f"Updated task: {task.title}")
    return task

@mcp.tool()
async def delete_task(
    task_id: str,
    ctx: Context[ServerSession, AppState]
) -> dict:
    """Delete a task by ID."""
    if task_id not in ctx.app_context.tasks:
        raise ToolError(f"Task '{task_id}' not found")

    task = ctx.app_context.tasks.pop(task_id)
    await ctx.info(f"Deleted task: {task.title}")
    return {"deleted": True, "task_id": task_id}

@mcp.tool()
async def complete_task(
    task_id: str,
    ctx: Context[ServerSession, AppState]
) -> Task:
    """Mark a task as completed.

    Shortcut for updating task status to 'completed'.
    """
    task = ctx.app_context.tasks.get(task_id)
    if not task:
        raise ToolError(f"Task '{task_id}' not found")

    task.status = Status.COMPLETED
    task.updated_at = datetime.now().isoformat()
    await ctx.info(f"Completed task: {task.title}")
    return task


# Resources
@mcp.resource("tasks://summary")
async def get_tasks_summary(ctx: Context[ServerSession, AppState]) -> str:
    """Summary of all tasks by status."""
    tasks = ctx.app_context.tasks.values()

    summary = {
        "total": len(tasks),
        "by_status": {
            "pending": len([t for t in tasks if t.status == Status.PENDING]),
            "in_progress": len([t for t in tasks if t.status == Status.IN_PROGRESS]),
            "completed": len([t for t in tasks if t.status == Status.COMPLETED])
        },
        "by_priority": {
            "high": len([t for t in tasks if t.priority == Priority.HIGH]),
            "medium": len([t for t in tasks if t.priority == Priority.MEDIUM]),
            "low": len([t for t in tasks if t.priority == Priority.LOW])
        }
    }
    return json.dumps(summary, indent=2)


# Prompts
@mcp.prompt()
def daily_planning() -> str:
    """Generate a daily planning prompt."""
    return """Help me plan my day by:
1. Reviewing my current tasks
2. Identifying high-priority items
3. Suggesting a reasonable order to tackle them
4. Estimating time needed for each task

Please start by listing my current tasks."""

@mcp.prompt()
def task_breakdown(task_title: str) -> str:
    """Help break down a task into subtasks."""
    return f"""I need to break down this task into smaller, actionable steps:

Task: {task_title}

Please help me:
1. Identify the main components of this task
2. Create specific, actionable subtasks
3. Estimate effort for each subtask
4. Suggest an order to complete them"""


if __name__ == "__main__":
    mcp.run()
```

## Claude Desktop Configuration

To use your server with Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python",
      "args": ["/path/to/task_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```
