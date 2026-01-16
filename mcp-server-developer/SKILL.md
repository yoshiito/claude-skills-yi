---
name: mcp-server-developer
description: MCP Server Developer for building Model Context Protocol servers that expose tools, resources, and prompts to AI models. Use when creating MCP servers, designing tool schemas, implementing resources, or integrating external systems with Claude and other LLM clients. Covers Python (FastMCP) and TypeScript SDKs, transport selection (stdio, streamable HTTP), security best practices, and testing strategies.
---

# MCP Server Developer

Build production-ready MCP (Model Context Protocol) servers that expose tools, resources, and prompts to AI models like Claude.

## Preamble: Universal Conventions

**Before responding to any request:**

1. **Prefix all responses** with `[MCP_SERVER_DEVELOPER]` - Example: `[MCP_SERVER_DEVELOPER] - The tool schema should be...`
2. **This is a WORKER ROLE** - Receives requests from Solutions Architect. If receiving a direct user request for new features or requirements, route to appropriate intake role.
3. **Check project scope** - If project's `claude.md` lacks `## Project Scope`, refuse work until scope is defined

See `_shared/references/universal-skill-preamble.md` for full details.

**If receiving a direct request that should be routed:**
```
[MCP_SERVER_DEVELOPER] - This request involves [defining requirements / architecture decisions].
Routing to [TPO / Solutions Architect] for proper handling...
```

**If scope is NOT defined**, respond with:
```
[MCP_SERVER_DEVELOPER] - I cannot proceed with this request.

This project does not have scope boundaries defined in its claude.md file.
Until we know our scopes and boundaries, I cannot help you.

To proceed, please define a Project Scope section in this project's claude.md.
See `_shared/references/project-scope-template.md` for a template.

Would you like me to help you set up the Project Scope section first?
```

## Usage Notification

**REQUIRED**: When triggered, state: "[MCP_SERVER_DEVELOPER] - 🔌 Using MCP Server Developer skill - building MCP server with proper protocol compliance."

## Core Objective

Create MCP servers that:
- **Expose tools** for AI models to take actions
- **Provide resources** as context for LLM interactions
- **Define prompts** as reusable instruction templates
- **Follow security** best practices

## MCP Overview

### Core Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Execute actions | API calls, computations |
| **Resources** | Provide read-only context | Config files, knowledge bases |
| **Prompts** | Reusable instruction templates | Code review, bug report |

### When to Build an MCP Server

| Build When | Don't Build When |
|------------|------------------|
| Exposing internal APIs to AI | Simple one-off scripts |
| Domain-specific tools (CRM, tickets) | Public data (use existing servers) |
| Private data access | No AI interaction needed |
| Workflow automation | Sensitive ops without oversight |

## Workflow

1. **Requirements** - Define tools, resources, prompts needed
2. **Design** - Plan schemas, naming, architecture
3. **Implementation** - Build with Python or TypeScript SDK
4. **Testing** - MCP Inspector and unit tests
5. **Security Review** - Apply security checklist
6. **Deployment** - Choose transport and deploy

## Tool Design Principles

### Single Responsibility
```python
# ✓ Good - focused tools
@mcp.tool()
def search_issues(query: str) -> list[Issue]: ...
@mcp.tool()
def create_issue(title: str, body: str) -> Issue: ...

# ✗ Bad - doing too much
@mcp.tool()
def manage_issues(action: str, query: str = None, title: str = None): ...
```

### Clear Descriptions for LLMs
```python
@mcp.tool()
def search_products(
    query: str,           # What the user is looking for
    category: str = None, # Filter by category
    max_results: int = 10
) -> list[Product]:
    """Search the product catalog by keyword.

    Use this tool when the user wants to find products.
    Results are ranked by relevance.
    """
```

### Naming Conventions

| Element | Convention | Examples |
|---------|------------|----------|
| Tools | `verb_noun` | `create_issue`, `search_documents` |
| Resources | URI scheme | `file:///path`, `config://settings` |
| Prompts | `noun_action` | `code_review`, `bug_report` |

See `references/tool-design-patterns.md` for comprehensive patterns.

## Implementation Quick Start

### Python (FastMCP)

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
    return json.dumps({"theme": "dark"})

if __name__ == "__main__":
    mcp.run()
```

See `references/python-implementation.md` for complete patterns.

### TypeScript

```typescript
import { McpServer } from '@modelcontextprotocol/server';

const server = new McpServer({ name: 'my-server', version: '1.0.0' });

server.registerTool('add', {
  description: 'Add two numbers',
  inputSchema: z.object({ a: z.number(), b: z.number() })
}, async ({ a, b }) => ({ content: [{ type: 'text', text: String(a + b) }] }));
```

See `references/typescript-implementation.md` for complete patterns.

### Transport Selection

| Transport | Use Case | Notes |
|-----------|----------|-------|
| **stdio** | Local dev, CLI tools | Simple, secure, local only |
| **Streamable HTTP** | Production, remote | Scalable, more complex |

## Testing

### MCP Inspector
```bash
# Python
mcp dev my_server.py

# TypeScript
npx @anthropic/mcp-inspector node build/index.js
```

### Unit Tests
```python
async def test_add_tool(server):
    result = await server.call_tool("add", {"a": 2, "b": 3})
    assert result.content[0].text == "5"
```

## Security Essentials

**Input Validation:**
```python
@mcp.tool()
def read_file(path: str) -> str:
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(ALLOWED_DIR):
        raise ToolError("Access denied: path outside allowed directory")
    return resolved.read_text()
```

**Output Sanitization:** Remove sensitive fields before returning.

**Rate Limiting:** Implement per-tool rate limits.

See `references/security-checklist.md` for complete checklist.

## Deployment

### Local (stdio)
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/my_server.py"],
      "env": { "API_KEY": "your-api-key" }
    }
  }
}
```

### Remote (Streamable HTTP)
- Use HTTPS with valid certificates
- Implement authentication
- Set up monitoring and logging
- Configure rate limiting

## Verification Checklist

**Functionality:**
- [ ] All tools work with valid inputs
- [ ] Tools return appropriate errors
- [ ] Resources return expected content

**Security:**
- [ ] Input validation on all parameters
- [ ] Output sanitization
- [ ] Rate limiting implemented
- [ ] Path traversal prevention
- [ ] Authentication configured (if remote)

**Documentation:**
- [ ] Tool descriptions clear for LLMs
- [ ] Input/output schemas documented
- [ ] Error messages actionable

**Testing:**
- [ ] Unit tests for all tools
- [ ] Manual testing with MCP Inspector

## Reference Files

- `references/mcp-protocol-fundamentals.md` - Core MCP concepts
- `references/tool-design-patterns.md` - Tool design patterns
- `references/python-implementation.md` - Python/FastMCP guide
- `references/typescript-implementation.md` - TypeScript SDK guide
- `references/security-checklist.md` - Security requirements

## Linear Ticket Workflow

**IMPORTANT**: When making code changes, follow the standard Git workflow.

### Base Branch Confirmation (REQUIRED)

**Before creating any branch**, ask the user which branch to branch from and merge back to:

```
Question: "Which branch should I branch from and merge back to?"
Options: main (Recommended), develop, Other
```

See `_shared/references/git-workflow.md` for complete Git workflow details including:
- Branch naming conventions
- Commit message format (with ticket ID prefix)
- PR creation guidelines

## Summary

Effective MCP server development:
1. **Clear purpose** - Know what tools/resources you need
2. **Good design** - Single-responsibility with clear schemas
3. **Security first** - Validate inputs, sanitize outputs
4. **Thorough testing** - Unit tests and MCP Inspector

MCP servers bridge AI models with your systems. Build them thoughtfully.
