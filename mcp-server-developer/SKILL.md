---
name: mcp-server-developer
description: MCP Server Developer for building Model Context Protocol servers that expose tools, resources, and prompts to AI models. Use when creating MCP servers, designing tool schemas, implementing resources, or integrating external systems with Claude and other LLM clients. Covers Python (FastMCP) and TypeScript SDKs, transport selection (stdio, streamable HTTP), security best practices, and testing strategies.
---

# MCP Server Developer

Build production-ready MCP (Model Context Protocol) servers that expose tools, resources, and prompts to AI models like Claude.

## Usage Notification

**REQUIRED**: When triggered, state: "🔌 Using MCP Server Developer skill - building MCP server with proper protocol compliance."

## Core Objective

Create MCP servers that:
- **Expose tools** for AI models to take actions
- **Provide resources** as context for LLM interactions
- **Define prompts** as reusable instruction templates
- **Follow security** best practices
- **Work reliably** across different transports

## MCP Overview

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources/tools. It uses JSON-RPC 2.0 as its messaging foundation.

### Architecture

```
┌─────────────────────────────────────────────┐
│           HOST (Claude, Cursor, etc.)       │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  Client 1 ────→ Your MCP Server      │   │
│  │  Client 2 ────→ Other MCP Server     │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  • Manages client lifecycle                 │
│  • Enforces security policies               │
│  • Coordinates LLM integration              │
└─────────────────────────────────────────────┘
```

### Core Primitives

| Primitive | Purpose | Direction |
|-----------|---------|-----------|
| **Tools** | Execute actions (API calls, computations) | Client → Server |
| **Resources** | Provide read-only context data | Client → Server |
| **Prompts** | Reusable instruction templates | Client → Server |

## When to Build an MCP Server

### Build an MCP Server When

| Scenario | Example |
|----------|---------|
| Exposing internal APIs to AI | Database queries, internal services |
| Providing domain-specific tools | CRM operations, ticket management |
| Giving AI access to private data | Documentation, knowledge bases |
| Automating workflows | CI/CD triggers, deployment actions |
| Integrating third-party services | GitHub, Slack, Jira, custom APIs |

### Don't Build an MCP Server When

| Scenario | Alternative |
|----------|-------------|
| Simple one-off scripts | Direct API integration |
| Public data access | Use existing MCP servers from registry |
| No AI interaction needed | Regular API/SDK |
| Sensitive operations without human oversight | Keep manual |

## Workflow Overview

Follow these phases:

1. **Requirements** - Define tools, resources, and prompts needed
2. **Design** - Plan schemas, naming, and architecture
3. **Implementation** - Build with Python or TypeScript SDK
4. **Testing** - Verify with MCP Inspector and unit tests
5. **Security Review** - Apply security checklist
6. **Deployment** - Choose transport and deploy

## Phase 1: Requirements Gathering

### Define Your Server's Purpose

Answer these questions:

- **What actions** should AI be able to take? → Tools
- **What data** should AI have access to? → Resources
- **What workflows** should be templated? → Prompts
- **Who is the audience?** → User-facing vs. assistant-only
- **What are the security boundaries?** → Auth, rate limits, sandboxing

### Tool Requirements

For each tool, determine:

| Aspect | Questions |
|--------|-----------|
| **Name** | Clear, verb-based (e.g., `create_issue`, `search_documents`) |
| **Inputs** | What parameters? Required vs optional? Types and constraints? |
| **Output** | Text, structured JSON, or both? |
| **Side effects** | Does it modify state? Is it idempotent? |
| **Error cases** | What can fail? How to communicate errors? |

### Resource Requirements

For each resource:

| Aspect | Questions |
|--------|-----------|
| **URI scheme** | Static (`config://settings`) or templated (`file:///{path}`)? |
| **Content type** | Text, JSON, binary? |
| **Freshness** | Static or dynamic? Subscription needed? |
| **Size** | Small enough for context? Chunking needed? |

## Phase 2: Design

### Tool Design Principles

**1. Single Responsibility**
```python
# ✓ Good - focused tools
@mcp.tool()
def search_issues(query: str, status: str = None) -> list[Issue]: ...

@mcp.tool()
def create_issue(title: str, body: str) -> Issue: ...

# ✗ Bad - doing too much
@mcp.tool()
def manage_issues(action: str, query: str = None, title: str = None): ...
```

**2. Clear Descriptions for LLMs**
```python
@mcp.tool()
def search_products(
    query: str,           # What the user is looking for
    category: str = None, # Filter by category (electronics, clothing, etc.)
    max_results: int = 10 # Maximum number of results to return
) -> list[Product]:
    """Search the product catalog by keyword.

    Use this tool when the user wants to find products. The query can be
    a product name, description keyword, or brand. Results are ranked by
    relevance.
    """
```

**3. Descriptive Error Messages**
```python
@mcp.tool()
def get_order(order_id: str) -> Order:
    """Retrieve order details by ID."""
    order = db.get_order(order_id)
    if not order:
        raise ToolError(f"Order '{order_id}' not found. Please verify the order ID.")
    return order
```

### Schema Design

**Input Schema Best Practices:**

```python
from pydantic import BaseModel, Field

class CreateIssueInput(BaseModel):
    """Input for creating a GitHub issue."""

    title: str = Field(
        ...,
        description="Issue title (max 256 chars)",
        max_length=256
    )
    body: str = Field(
        ...,
        description="Issue description in markdown format"
    )
    labels: list[str] = Field(
        default=[],
        description="Labels to apply (e.g., 'bug', 'enhancement')"
    )
    assignees: list[str] = Field(
        default=[],
        description="GitHub usernames to assign"
    )
```

**Output Schema Best Practices:**

```python
class CreateIssueOutput(BaseModel):
    """Output from creating a GitHub issue."""

    id: int = Field(description="Unique issue ID")
    number: int = Field(description="Issue number in the repository")
    url: str = Field(description="Web URL to view the issue")
    state: str = Field(description="Current state: 'open' or 'closed'")
```

### Naming Conventions

| Element | Convention | Examples |
|---------|------------|----------|
| Tools | `verb_noun` | `create_issue`, `search_documents`, `get_user` |
| Resources | URI scheme | `file:///path`, `db://table/id`, `config://settings` |
| Prompts | `noun_action` | `code_review`, `bug_report`, `meeting_summary` |

## Phase 3: Implementation

### Python with FastMCP

See `references/python-implementation.md` for complete patterns.

**Basic Server:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="my-server", version="1.0.0")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.resource("config://settings")
def get_settings() -> str:
    """Current application settings."""
    return json.dumps({"theme": "dark", "language": "en"})

@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"Please review this {language} code for quality and best practices:\n\n```{language}\n{code}\n```"

if __name__ == "__main__":
    mcp.run()
```

### TypeScript with Official SDK

See `references/typescript-implementation.md` for complete patterns.

**Basic Server:**

```typescript
import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';

const server = new McpServer({
  name: 'my-server',
  version: '1.0.0'
});

server.registerTool(
  'add',
  {
    description: 'Add two numbers together',
    inputSchema: z.object({
      a: z.number().describe('First number'),
      b: z.number().describe('Second number')
    })
  },
  async ({ a, b }) => ({
    content: [{ type: 'text', text: String(a + b) }]
  })
);
```

### Transport Selection

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Local dev, CLI tools | Simple, secure | Local only |
| **Streamable HTTP** | Production, remote | Scalable, resumable | More complex |

**Decision Guide:**

```
Is the server running locally with the client?
├── YES → Use stdio (simpler, more secure)
└── NO → Use Streamable HTTP
         └── Need session state? → Stateful mode
         └── Stateless API? → Stateless mode
```

## Phase 4: Testing

### Manual Testing with MCP Inspector

```bash
# Python
mcp dev my_server.py

# TypeScript
npx @anthropic/mcp-inspector node build/index.js
```

### Unit Testing Tools

```python
import pytest
from my_server import mcp

@pytest.fixture
def server():
    return mcp

async def test_add_tool(server):
    """Test the add tool returns correct sum."""
    result = await server.call_tool("add", {"a": 2, "b": 3})
    assert result.content[0].text == "5"

async def test_add_tool_validates_input(server):
    """Test the add tool rejects invalid input."""
    with pytest.raises(ValidationError):
        await server.call_tool("add", {"a": "not a number", "b": 3})
```

### Integration Testing

```python
async def test_create_issue_integration():
    """Test creating an issue against real GitHub API."""
    # Use test repository
    result = await server.call_tool("create_issue", {
        "title": "Test Issue",
        "body": "This is a test",
        "repo": "test-org/test-repo"
    })

    assert result.content[0].text
    data = json.loads(result.content[0].text)
    assert "id" in data
    assert data["state"] == "open"

    # Cleanup
    await server.call_tool("close_issue", {"issue_id": data["id"]})
```

## Phase 5: Security Review

See `references/security-checklist.md` for complete checklist.

### Critical Security Requirements

**Input Validation:**
```python
@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from the allowed directory."""
    # Validate path is within allowed directory
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(ALLOWED_DIR):
        raise ToolError("Access denied: path outside allowed directory")

    return resolved.read_text()
```

**Rate Limiting:**
```python
from functools import wraps
from time import time

def rate_limit(calls: int, period: int):
    """Limit tool calls to `calls` per `period` seconds."""
    timestamps = []

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time()
            timestamps[:] = [t for t in timestamps if now - t < period]
            if len(timestamps) >= calls:
                raise ToolError(f"Rate limit exceeded: {calls} calls per {period}s")
            timestamps.append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@rate_limit(calls=10, period=60)
def expensive_operation() -> str:
    """A rate-limited operation."""
    ...
```

**Output Sanitization:**
```python
@mcp.tool()
def search_users(query: str) -> list[dict]:
    """Search users by name."""
    users = db.search_users(query)

    # Remove sensitive fields before returning
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            # Exclude: password_hash, api_keys, etc.
        }
        for u in users
    ]
```

## Phase 6: Deployment

### Local Deployment (stdio)

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/my_server.py"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Remote Deployment (Streamable HTTP)

**Docker Configuration:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "server.py", "--transport", "streamable-http", "--port", "8000"]
```

**Production Considerations:**

- Use HTTPS with valid certificates
- Implement authentication (OAuth, API keys)
- Set up monitoring and logging
- Configure rate limiting at infrastructure level
- Use health checks for orchestration

## Verification Checklist

Before deploying, verify:

**Functionality:**
- [ ] All tools work correctly with valid inputs
- [ ] Tools return appropriate errors for invalid inputs
- [ ] Resources return expected content
- [ ] Prompts generate valid message structures

**Security:**
- [ ] Input validation on all tool parameters
- [ ] Output sanitization (no sensitive data leakage)
- [ ] Rate limiting implemented
- [ ] Path traversal prevention (if file access)
- [ ] SQL injection prevention (if database access)
- [ ] Authentication configured (if remote)

**Documentation:**
- [ ] Tool descriptions are clear for LLMs
- [ ] Input/output schemas are fully documented
- [ ] Error messages are actionable

**Testing:**
- [ ] Unit tests for all tools
- [ ] Integration tests for external dependencies
- [ ] Manual testing with MCP Inspector

**Deployment:**
- [ ] Transport selected appropriately
- [ ] Environment variables configured
- [ ] Logging enabled
- [ ] Health checks working

## Reference Files

- `references/mcp-protocol-fundamentals.md` - Core MCP concepts and protocol details
- `references/tool-design-patterns.md` - Patterns for effective tool design
- `references/python-implementation.md` - Python/FastMCP implementation guide
- `references/typescript-implementation.md` - TypeScript SDK implementation guide
- `references/security-checklist.md` - Security requirements and checklist

## Summary

Effective MCP server development requires:

1. **Clear purpose** - Know what tools/resources/prompts you need
2. **Good design** - Single-responsibility tools with clear schemas
3. **Proper implementation** - Use SDKs correctly, handle errors
4. **Thorough testing** - Unit, integration, and manual testing
5. **Security first** - Validate inputs, sanitize outputs, rate limit
6. **Appropriate deployment** - Choose transport based on use case

MCP servers bridge AI models with your systems. Build them thoughtfully.
