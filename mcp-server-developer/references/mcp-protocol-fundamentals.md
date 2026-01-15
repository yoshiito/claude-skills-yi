# MCP Protocol Fundamentals

Core concepts and protocol details for the Model Context Protocol.

## Protocol Overview

MCP uses **JSON-RPC 2.0** as its messaging foundation. All messages follow this structure:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": { ... }
}
```

**Current Specification Version:** 2025-11-25

## Architecture

### Component Roles

```
┌─────────────────────────────────────────────────────────────┐
│                    HOST PROCESS                              │
│  (Claude Desktop, Cursor, VS Code, ChatGPT, etc.)           │
│                                                              │
│  Responsibilities:                                           │
│  • Creates and manages client instances                      │
│  • Enforces security policies and consent                    │
│  • Handles user authorization decisions                      │
│  • Coordinates AI/LLM integration and sampling               │
│  • Aggregates context from multiple servers                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    MCP CLIENTS                          │  │
│  │                                                         │  │
│  │  Client 1 ─────────────→ Server A (Your Server)        │  │
│  │  Client 2 ─────────────→ Server B (Database)           │  │
│  │  Client 3 ─────────────→ Server C (GitHub)             │  │
│  │                                                         │  │
│  │  Each client:                                           │  │
│  │  • Maintains 1:1 stateful session with its server       │  │
│  │  • Handles protocol negotiation                         │  │
│  │  • Routes messages bidirectionally                      │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ (Isolated connections)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP SERVERS                               │
│                                                              │
│  Server A: Exposes your custom tools, resources, prompts     │
│  Server B: Provides database query capabilities              │
│  Server C: GitHub integration (issues, PRs, repos)           │
│                                                              │
│  Each server:                                                │
│  • Operates independently                                    │
│  • Cannot access other servers' data                         │
│  • Exposes focused functionality                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Servers should be easy to build** - Host handles complex orchestration
2. **Servers are composable** - Each provides focused functionality
3. **Isolation** - Servers cannot see other servers' context
4. **Progressive features** - Start minimal, add capabilities as needed

## Protocol Lifecycle

### Phase 1: Initialization

```
Client                                    Server
   │                                         │
   │──── initialize ────────────────────────►│
   │     {protocolVersion, capabilities,     │
   │      clientInfo}                        │
   │                                         │
   │◄─── initialize response ────────────────│
   │     {protocolVersion, capabilities,     │
   │      serverInfo, instructions}          │
   │                                         │
   │──── notifications/initialized ─────────►│
   │                                         │
   │         [Normal Operation Begins]       │
```

**Initialize Request (Client → Server):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": { "listChanged": true },
      "sampling": {}
    },
    "clientInfo": {
      "name": "Claude Desktop",
      "version": "1.0.0"
    }
  }
}
```

**Initialize Response (Server → Client):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true, "listChanged": true },
      "prompts": { "listChanged": true },
      "logging": {}
    },
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    },
    "instructions": "This server provides access to the product catalog."
  }
}
```

### Capability Negotiation

**Client Capabilities:**

| Capability | Description |
|------------|-------------|
| `roots` | Can provide filesystem roots to servers |
| `roots.listChanged` | Supports notifications when roots change |
| `sampling` | Supports LLM sampling requests from servers |
| `experimental` | Non-standard experimental features |

**Server Capabilities:**

| Capability | Sub-capability | Description |
|------------|----------------|-------------|
| `tools` | | Server offers callable tools |
| `tools.listChanged` | | Server notifies when tool list changes |
| `resources` | | Server provides readable resources |
| `resources.subscribe` | | Supports resource subscriptions |
| `resources.listChanged` | | Notifies when resource list changes |
| `prompts` | | Server offers prompt templates |
| `prompts.listChanged` | | Notifies when prompt list changes |
| `logging` | | Server emits structured log messages |
| `completions` | | Supports argument autocompletion |

### Phase 2: Normal Operation

After initialization, clients and servers exchange messages based on negotiated capabilities.

### Phase 3: Shutdown

**stdio transport:**
1. Close input stream
2. Wait for server to exit
3. Send SIGTERM if needed
4. Force SIGKILL after timeout

**HTTP transport:**
1. Close HTTP connection(s)
2. Server cleans up session state

## Core Primitives

### Tools

Tools let servers expose executable functions to clients.

**Tool Definition:**

```json
{
  "name": "create_issue",
  "title": "Create GitHub Issue",
  "description": "Create a new issue in a GitHub repository",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": {
        "type": "string",
        "description": "Repository in format 'owner/repo'"
      },
      "title": {
        "type": "string",
        "description": "Issue title"
      },
      "body": {
        "type": "string",
        "description": "Issue body in markdown"
      }
    },
    "required": ["repo", "title"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "id": { "type": "integer" },
      "number": { "type": "integer" },
      "url": { "type": "string" }
    }
  },
  "annotations": {
    "audience": ["user", "assistant"],
    "priority": 0.8
  }
}
```

**List Tools (Client → Server):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Call Tool (Client → Server):**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "create_issue",
    "arguments": {
      "repo": "acme/widgets",
      "title": "Bug in checkout flow",
      "body": "The checkout fails when..."
    }
  }
}
```

**Tool Result (Server → Client):**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"id\": 123, \"number\": 456, \"url\": \"https://github.com/acme/widgets/issues/456\"}"
      }
    ],
    "structuredContent": {
      "id": 123,
      "number": 456,
      "url": "https://github.com/acme/widgets/issues/456"
    },
    "isError": false
  }
}
```

**Content Types:**

| Type | Description |
|------|-------------|
| `text` | Plain text content |
| `image` | Base64-encoded image with mimeType |
| `audio` | Base64-encoded audio with mimeType |
| `resource_link` | URI reference to a resource |
| `resource` | Embedded resource content |

### Resources

Resources expose read-only data for LLM context.

**Resource Definition:**

```json
{
  "uri": "file:///project/README.md",
  "name": "README.md",
  "title": "Project README",
  "description": "Main documentation for the project",
  "mimeType": "text/markdown",
  "size": 2048,
  "annotations": {
    "audience": ["user", "assistant"],
    "priority": 0.9
  }
}
```

**URI Templates (RFC 6570):**

```json
{
  "uriTemplate": "db://users/{user_id}",
  "name": "User Profile",
  "description": "Access user profile by ID"
}
```

**List Resources:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list"
}
```

**Read Resource:**

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///project/README.md"
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "contents": [
      {
        "uri": "file:///project/README.md",
        "mimeType": "text/markdown",
        "text": "# My Project\n\nThis project does..."
      }
    ]
  }
}
```

**Resource Subscriptions:**

```json
// Subscribe
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/subscribe",
  "params": { "uri": "file:///project/config.json" }
}

// Update notification (Server → Client)
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": { "uri": "file:///project/config.json" }
}

// List changed notification (Server → Client)
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/list_changed"
}
```

### Prompts

Prompts are reusable instruction templates.

**Prompt Definition:**

```json
{
  "name": "code_review",
  "title": "Request Code Review",
  "description": "Asks the LLM to analyze code quality",
  "arguments": [
    {
      "name": "code",
      "description": "The code to review",
      "required": true
    },
    {
      "name": "language",
      "description": "Programming language",
      "required": false
    }
  ]
}
```

**Get Prompt:**

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')",
      "language": "python"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "description": "Code review for Python code",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code for quality and best practices:\n\n```python\ndef hello():\n    print('world')\n```"
        }
      }
    ]
  }
}
```

**Embedded Resources in Prompts:**

```json
{
  "role": "user",
  "content": {
    "type": "resource",
    "resource": {
      "uri": "file:///docs/style-guide.md",
      "mimeType": "text/markdown",
      "text": "# Style Guide\n\n..."
    }
  }
}
```

## Transport Mechanisms

### stdio (Standard Input/Output)

**Best for:** Local development, CLI tools, desktop apps

**How it works:**
- Client spawns server as subprocess
- Server reads from `stdin`, writes to `stdout`
- Messages delimited by newlines
- `stderr` available for logging

```
Client Process
    │
    ├── stdin ──────► Server Process (JSON-RPC messages)
    │
    └◄── stdout ───── Server Process (JSON-RPC responses)

    (stderr for logging)
```

**Requirements:**
- Server MUST NOT write non-MCP content to `stdout`
- Messages MUST NOT contain embedded newlines
- Server MAY write UTF-8 logs to `stderr`

### Streamable HTTP

**Best for:** Production, remote deployment, web apps

**Features:**
- Single HTTP endpoint for POST (send) and GET (receive SSE)
- Session management with `Mcp-Session-Id` header
- Supports resumability and message redelivery
- Both stateless and stateful modes

**Endpoint:**

```
https://example.com/mcp
├── POST  → Send JSON-RPC messages
└── GET   → Receive SSE stream for server notifications
```

**Session Management:**

```http
# Initial request
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream

# Server response includes session ID
HTTP/1.1 200 OK
Mcp-Session-Id: abc123-secure-uuid

# Subsequent requests include session ID
POST /mcp HTTP/1.1
Mcp-Session-Id: abc123-secure-uuid
```

**Security Requirements:**
- Validate `Origin` header (DNS rebinding protection)
- Use `localhost` binding for local servers
- Implement authentication for remote access
- Use HTTPS in production

## Utility Features

### Ping (Health Check)

```json
// Request
{ "jsonrpc": "2.0", "id": 1, "method": "ping" }

// Response
{ "jsonrpc": "2.0", "id": 1, "result": {} }
```

### Logging

Servers can emit structured logs:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "level": "info",
    "logger": "database",
    "data": {
      "message": "Connected to database",
      "host": "localhost",
      "port": 5432
    }
  }
}
```

**Log Levels:** `debug`, `info`, `notice`, `warning`, `error`, `critical`, `alert`, `emergency`

### Progress Reporting

For long-running operations:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "op-123",
    "progress": 50,
    "total": 100,
    "message": "Processing files..."
  }
}
```

### Cancellation

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": 5,
    "reason": "User cancelled operation"
  }
}
```

## Error Handling

**Standard JSON-RPC Error Codes:**

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid request | Not valid JSON-RPC |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Server internal error |

**MCP-Specific Errors:**

| Code | Name | Description |
|------|------|-------------|
| -32001 | Resource not found | Requested resource doesn't exist |
| -32002 | Tool execution failed | Tool returned error |

**Error Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "field": "repo",
      "reason": "Repository not found"
    }
  }
}
```

## Annotations

Both tools and resources support annotations for additional metadata:

```json
{
  "annotations": {
    "audience": ["user", "assistant"],
    "priority": 0.9,
    "custom_field": "value"
  }
}
```

**Standard Annotations:**

| Field | Type | Description |
|-------|------|-------------|
| `audience` | `string[]` | Who should see this (`user`, `assistant`) |
| `priority` | `number` | Importance hint (0.0 - 1.0) |

## Best Practices

### Protocol Compliance

1. **Always negotiate capabilities** - Don't assume features
2. **Handle unknown methods gracefully** - Return method not found
3. **Validate all inputs** - Never trust client data
4. **Use proper error codes** - Help clients handle errors

### Performance

1. **Batch operations when possible** - Reduce round trips
2. **Use subscriptions for dynamic data** - Avoid polling
3. **Implement pagination** - For large resource lists
4. **Set appropriate timeouts** - Prevent hanging connections

### Compatibility

1. **Support version negotiation** - Handle older clients
2. **Ignore unknown fields** - Forward compatibility
3. **Document breaking changes** - Semantic versioning
