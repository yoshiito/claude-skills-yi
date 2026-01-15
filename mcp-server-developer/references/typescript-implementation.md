# TypeScript MCP Implementation Guide

Complete guide for building MCP servers with TypeScript using the official SDK.

## Installation

```bash
# Server package
npm install @modelcontextprotocol/server zod

# Client package (if building a client)
npm install @modelcontextprotocol/client zod

# Development tools
npm install -D typescript @types/node tsx
```

**Note:** Zod (v3.25+) is a required peer dependency for schema validation.

## Project Setup

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./build",
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

### package.json

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/server": "^1.0.0",
    "zod": "^3.25.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

## Basic Server Structure

### Minimal Server

```typescript
import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';

const server = new McpServer({
  name: 'my-server',
  version: '1.0.0'
});

// Register a tool
server.registerTool(
  'greet',
  {
    description: 'Greet someone by name',
    inputSchema: z.object({
      name: z.string().describe('Name to greet')
    })
  },
  async ({ name }) => ({
    content: [{ type: 'text', text: `Hello, ${name}!` }]
  })
);

// Start server with stdio transport
server.listen();
```

### Running the Server

```bash
# Development
npx tsx src/index.ts

# Production
npm run build && npm start

# With MCP Inspector
npx @anthropic/mcp-inspector node build/index.js
```

## Tools

### Basic Tool

```typescript
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

### Tool with Complex Schema

```typescript
const PriorityEnum = z.enum(['low', 'medium', 'high']);

const TaskInputSchema = z.object({
  title: z.string()
    .max(200)
    .describe('Task title'),
  description: z.string()
    .max(2000)
    .optional()
    .describe('Detailed description'),
  priority: PriorityEnum
    .default('medium')
    .describe('Task priority level'),
  tags: z.array(z.string())
    .default([])
    .describe('Tags for categorization'),
  dueDate: z.string()
    .optional()
    .describe('Due date in ISO format')
});

const TaskOutputSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().nullable(),
  priority: PriorityEnum,
  status: z.enum(['pending', 'in_progress', 'completed']),
  tags: z.array(z.string()),
  createdAt: z.string(),
  dueDate: z.string().nullable()
});

server.registerTool(
  'create_task',
  {
    title: 'Create Task',
    description: `Create a new task in the system.

Use this when the user wants to add a new task to their list.
Tasks are created with 'pending' status by default.`,
    inputSchema: TaskInputSchema,
    outputSchema: TaskOutputSchema
  },
  async (input) => {
    const task = {
      id: crypto.randomUUID(),
      title: input.title,
      description: input.description ?? null,
      priority: input.priority,
      status: 'pending' as const,
      tags: input.tags,
      createdAt: new Date().toISOString(),
      dueDate: input.dueDate ?? null
    };

    // Save task to database
    await saveTask(task);

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }],
      structuredContent: task
    };
  }
);
```

### Tool with Structured Output

```typescript
const WeatherSchema = z.object({
  temperature: z.number().describe('Temperature in Celsius'),
  conditions: z.string().describe('Current weather conditions'),
  humidity: z.number().describe('Humidity percentage'),
  windSpeed: z.number().describe('Wind speed in km/h')
});

server.registerTool(
  'get_weather',
  {
    description: 'Get current weather for a city',
    inputSchema: z.object({
      city: z.string().describe('City name')
    }),
    outputSchema: WeatherSchema
  },
  async ({ city }) => {
    const weather = await fetchWeather(city);

    return {
      content: [{
        type: 'text',
        text: `Weather in ${city}: ${weather.temperature}°C, ${weather.conditions}`
      }],
      structuredContent: weather
    };
  }
);
```

### Error Handling

```typescript
import { ToolError } from '@modelcontextprotocol/server';

server.registerTool(
  'get_order',
  {
    description: 'Get order details by ID',
    inputSchema: z.object({
      orderId: z.string().describe('Order ID in format ORD-XXXXXX')
    })
  },
  async ({ orderId }) => {
    // Validate format
    if (!orderId.match(/^ORD-[A-Z0-9]{6}$/)) {
      throw new ToolError(
        `Invalid order ID format: '${orderId}'. ` +
        "Expected format: ORD-XXXXXX (e.g., ORD-ABC123)"
      );
    }

    const order = await db.getOrder(orderId);
    if (!order) {
      throw new ToolError(
        `Order '${orderId}' not found. ` +
        "Please verify the order ID or search for orders by customer."
      );
    }

    return {
      content: [{ type: 'text', text: JSON.stringify(order) }]
    };
  }
);
```

### Tool with Multiple Content Types

```typescript
server.registerTool(
  'generate_chart',
  {
    description: 'Generate a chart from data',
    inputSchema: z.object({
      type: z.enum(['bar', 'line', 'pie']),
      data: z.array(z.object({
        label: z.string(),
        value: z.number()
      }))
    })
  },
  async ({ type, data }) => {
    const chartBuffer = await generateChart(type, data);
    const base64 = chartBuffer.toString('base64');

    return {
      content: [
        {
          type: 'text',
          text: `Generated ${type} chart with ${data.length} data points`
        },
        {
          type: 'image',
          data: base64,
          mimeType: 'image/png'
        }
      ]
    };
  }
);
```

## Resources

### Static Resource

```typescript
server.registerResource(
  'settings',
  'config://settings',
  {
    title: 'Application Settings',
    description: 'Current configuration settings',
    mimeType: 'application/json'
  },
  async () => ({
    contents: [{
      uri: 'config://settings',
      text: JSON.stringify({
        theme: 'dark',
        language: 'en',
        notifications: true
      }, null, 2)
    }]
  })
);
```

### Dynamic Resource with Template

```typescript
server.registerResourceTemplate(
  'user-profile',
  'users://{userId}',
  {
    title: 'User Profile',
    description: 'Get user profile by ID',
    mimeType: 'application/json'
  },
  async (uri, { userId }) => {
    const user = await db.getUser(userId);
    if (!user) {
      throw new Error(`User ${userId} not found`);
    }

    return {
      contents: [{
        uri: uri.href,
        text: JSON.stringify(user)
      }]
    };
  }
);
```

### Resource with Subscription Support

```typescript
import { EventEmitter } from 'events';

const fileWatcher = new EventEmitter();

server.registerResource(
  'config',
  'file:///config.json',
  {
    title: 'Configuration File',
    description: 'Application configuration',
    mimeType: 'application/json'
  },
  async () => ({
    contents: [{
      uri: 'file:///config.json',
      text: await fs.readFile('config.json', 'utf-8')
    }]
  })
);

// Notify clients when file changes
fileWatcher.on('change', () => {
  server.notifyResourceUpdated('file:///config.json');
});
```

## Prompts

### Basic Prompt

```typescript
server.registerPrompt(
  'code_review',
  {
    title: 'Code Review',
    description: 'Review code for quality and best practices',
    argsSchema: z.object({
      code: z.string().describe('Code to review'),
      language: z.string().optional().describe('Programming language')
    })
  },
  ({ code, language }) => ({
    messages: [{
      role: 'user',
      content: {
        type: 'text',
        text: `Please review this ${language ?? ''} code for quality and best practices:

\`\`\`${language ?? ''}
${code}
\`\`\`

Provide specific, actionable feedback on:
- Code quality
- Potential bugs
- Performance
- Security`
      }
    }]
  })
);
```

### Prompt with Multiple Messages

```typescript
server.registerPrompt(
  'debug_session',
  {
    title: 'Debug Session',
    description: 'Start a debugging session for an error',
    argsSchema: z.object({
      errorMessage: z.string().describe('The error message'),
      code: z.string().describe('Related code'),
      stackTrace: z.string().optional().describe('Stack trace if available')
    })
  },
  ({ errorMessage, code, stackTrace }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `I'm encountering this error:\n\n\`\`\`\n${errorMessage}\n\`\`\``
        }
      },
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Here's my code:\n\n\`\`\`\n${code}\n\`\`\``
        }
      },
      ...(stackTrace ? [{
        role: 'user' as const,
        content: {
          type: 'text' as const,
          text: `Stack trace:\n\n\`\`\`\n${stackTrace}\n\`\`\``
        }
      }] : []),
      {
        role: 'user',
        content: {
          type: 'text',
          text: 'Please help me understand what\'s causing this error and how to fix it.'
        }
      }
    ]
  })
);
```

## Transport Configuration

### stdio (Default)

```typescript
// Default stdio transport
server.listen();
```

### Streamable HTTP

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/server';

// Create Express app with MCP endpoint
const app = createMcpExpressApp(server);

// Add custom middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

app.listen(8000, () => {
  console.log('MCP server running on http://localhost:8000');
});
```

### With Authentication

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/server';
import type { Request, Response, NextFunction } from 'express';

function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey || apiKey !== process.env.API_KEY) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }

  next();
}

const app = createMcpExpressApp(server);
app.use('/mcp', authMiddleware);

app.listen(8000);
```

### DNS Rebinding Protection

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/server';

// Auto-protected when binding to localhost
const app = createMcpExpressApp(server);

// For broader binding, specify allowed hosts
const app = createMcpExpressApp(server, {
  host: '0.0.0.0',
  allowedHosts: ['localhost', '127.0.0.1', 'myserver.example.com']
});
```

## State Management

### Server with State

```typescript
interface AppState {
  tasks: Map<string, Task>;
  users: Map<string, User>;
}

const state: AppState = {
  tasks: new Map(),
  users: new Map()
};

server.registerTool(
  'create_task',
  {
    description: 'Create a new task',
    inputSchema: TaskInputSchema
  },
  async (input) => {
    const task: Task = {
      id: crypto.randomUUID(),
      ...input,
      status: 'pending',
      createdAt: new Date().toISOString()
    };

    state.tasks.set(task.id, task);

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }]
    };
  }
);
```

### Dependency Injection Pattern

```typescript
interface Dependencies {
  db: Database;
  cache: Cache;
  logger: Logger;
}

function createServer(deps: Dependencies) {
  const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
  });

  server.registerTool(
    'get_user',
    {
      description: 'Get user by ID',
      inputSchema: z.object({ userId: z.string() })
    },
    async ({ userId }) => {
      deps.logger.info(`Fetching user ${userId}`);

      // Check cache first
      let user = await deps.cache.get(`user:${userId}`);
      if (!user) {
        user = await deps.db.getUser(userId);
        await deps.cache.set(`user:${userId}`, user);
      }

      return {
        content: [{ type: 'text', text: JSON.stringify(user) }]
      };
    }
  );

  return server;
}

// Usage
const server = createServer({
  db: new Database(process.env.DATABASE_URL),
  cache: new Redis(process.env.REDIS_URL),
  logger: new Logger()
});
```

## Testing

### Unit Testing Tools

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { createServer } from './server';

describe('Task Tools', () => {
  let server: McpServer;

  beforeEach(() => {
    server = createServer({ tasks: new Map() });
  });

  it('should create a task', async () => {
    const result = await server.callTool('create_task', {
      title: 'Test Task',
      priority: 'high'
    });

    expect(result.isError).toBe(false);
    const task = JSON.parse(result.content[0].text);
    expect(task.title).toBe('Test Task');
    expect(task.priority).toBe('high');
    expect(task.status).toBe('pending');
  });

  it('should validate required fields', async () => {
    await expect(
      server.callTool('create_task', { priority: 'high' })
    ).rejects.toThrow();
  });

  it('should return error for invalid task ID', async () => {
    const result = await server.callTool('get_task', {
      taskId: 'nonexistent'
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain('not found');
  });
});
```

### Testing with Mocks

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Weather Tool', () => {
  it('should fetch weather data', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      temperature: 22.5,
      conditions: 'Sunny',
      humidity: 65
    });

    const server = createServer({ weatherApi: { fetch: mockFetch } });

    const result = await server.callTool('get_weather', {
      city: 'Tokyo'
    });

    expect(mockFetch).toHaveBeenCalledWith('Tokyo');
    const data = JSON.parse(result.content[0].text);
    expect(data.temperature).toBe(22.5);
  });

  it('should handle API errors', async () => {
    const mockFetch = vi.fn().mockRejectedValue(new Error('API unavailable'));

    const server = createServer({ weatherApi: { fetch: mockFetch } });

    const result = await server.callTool('get_weather', {
      city: 'Tokyo'
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain('unavailable');
  });
});
```

### Integration Testing

```typescript
import { spawn } from 'child_process';

async function sendRequest(
  proc: ChildProcess,
  method: string,
  params: unknown,
  id: number = 1
): Promise<unknown> {
  return new Promise((resolve) => {
    const request = JSON.stringify({
      jsonrpc: '2.0',
      id,
      method,
      params
    });

    proc.stdout!.once('data', (data) => {
      resolve(JSON.parse(data.toString()));
    });

    proc.stdin!.write(request + '\n');
  });
}

describe('Integration Tests', () => {
  let serverProcess: ChildProcess;

  beforeAll(() => {
    serverProcess = spawn('node', ['build/index.js'], {
      stdio: ['pipe', 'pipe', 'inherit']
    });
  });

  afterAll(() => {
    serverProcess.kill();
  });

  it('should initialize correctly', async () => {
    const response = await sendRequest(serverProcess, 'initialize', {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: { name: 'test', version: '1.0' }
    });

    expect(response.result.serverInfo.name).toBe('my-server');
  });
});
```

## Complete Example Server

```typescript
/**
 * Example MCP server for a task management system.
 */
import { McpServer, ToolError } from '@modelcontextprotocol/server';
import { z } from 'zod';

// Schemas
const PriorityEnum = z.enum(['low', 'medium', 'high']);
const StatusEnum = z.enum(['pending', 'in_progress', 'completed']);

const TaskSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().nullable(),
  priority: PriorityEnum,
  status: StatusEnum,
  tags: z.array(z.string()),
  createdAt: z.string(),
  updatedAt: z.string()
});

type Task = z.infer<typeof TaskSchema>;

// State
const tasks = new Map<string, Task>();

// Server
const server = new McpServer({
  name: 'task-manager',
  version: '1.0.0'
});

// Tools
server.registerTool(
  'create_task',
  {
    title: 'Create Task',
    description: `Create a new task in the system.

Use this when the user wants to add a new task to their list.
Tasks are created with 'pending' status by default.`,
    inputSchema: z.object({
      title: z.string().max(200).describe('Task title'),
      description: z.string().max(2000).optional().describe('Detailed description'),
      priority: PriorityEnum.default('medium').describe('Task priority'),
      tags: z.array(z.string()).default([]).describe('Tags for categorization')
    }),
    outputSchema: TaskSchema
  },
  async (input) => {
    const now = new Date().toISOString();
    const task: Task = {
      id: crypto.randomUUID(),
      title: input.title,
      description: input.description ?? null,
      priority: input.priority,
      status: 'pending',
      tags: input.tags,
      createdAt: now,
      updatedAt: now
    };

    tasks.set(task.id, task);

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }],
      structuredContent: task
    };
  }
);

server.registerTool(
  'get_task',
  {
    description: 'Get a task by ID',
    inputSchema: z.object({
      taskId: z.string().describe('Task ID')
    }),
    outputSchema: TaskSchema
  },
  async ({ taskId }) => {
    const task = tasks.get(taskId);
    if (!task) {
      throw new ToolError(`Task '${taskId}' not found`);
    }

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }],
      structuredContent: task
    };
  }
);

server.registerTool(
  'list_tasks',
  {
    description: 'List all tasks with optional filters',
    inputSchema: z.object({
      status: StatusEnum.optional().describe('Filter by status'),
      priority: PriorityEnum.optional().describe('Filter by priority'),
      tag: z.string().optional().describe('Filter by tag')
    }),
    outputSchema: z.array(TaskSchema)
  },
  async ({ status, priority, tag }) => {
    let result = Array.from(tasks.values());

    if (status) {
      result = result.filter(t => t.status === status);
    }
    if (priority) {
      result = result.filter(t => t.priority === priority);
    }
    if (tag) {
      result = result.filter(t => t.tags.includes(tag));
    }

    result.sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );

    return {
      content: [{ type: 'text', text: JSON.stringify(result) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  'update_task',
  {
    description: 'Update an existing task',
    inputSchema: z.object({
      taskId: z.string().describe('Task ID'),
      title: z.string().max(200).optional(),
      description: z.string().max(2000).optional(),
      priority: PriorityEnum.optional(),
      status: StatusEnum.optional(),
      tags: z.array(z.string()).optional()
    }),
    outputSchema: TaskSchema
  },
  async ({ taskId, ...updates }) => {
    const task = tasks.get(taskId);
    if (!task) {
      throw new ToolError(`Task '${taskId}' not found`);
    }

    // Apply updates
    if (updates.title !== undefined) task.title = updates.title;
    if (updates.description !== undefined) task.description = updates.description;
    if (updates.priority !== undefined) task.priority = updates.priority;
    if (updates.status !== undefined) task.status = updates.status;
    if (updates.tags !== undefined) task.tags = updates.tags;
    task.updatedAt = new Date().toISOString();

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }],
      structuredContent: task
    };
  }
);

server.registerTool(
  'delete_task',
  {
    description: 'Delete a task by ID',
    inputSchema: z.object({
      taskId: z.string().describe('Task ID')
    })
  },
  async ({ taskId }) => {
    if (!tasks.has(taskId)) {
      throw new ToolError(`Task '${taskId}' not found`);
    }

    tasks.delete(taskId);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ deleted: true, taskId })
      }]
    };
  }
);

server.registerTool(
  'complete_task',
  {
    description: "Mark a task as completed (shortcut for updating status to 'completed')",
    inputSchema: z.object({
      taskId: z.string().describe('Task ID')
    }),
    outputSchema: TaskSchema
  },
  async ({ taskId }) => {
    const task = tasks.get(taskId);
    if (!task) {
      throw new ToolError(`Task '${taskId}' not found`);
    }

    task.status = 'completed';
    task.updatedAt = new Date().toISOString();

    return {
      content: [{ type: 'text', text: JSON.stringify(task) }],
      structuredContent: task
    };
  }
);

// Resources
server.registerResource(
  'summary',
  'tasks://summary',
  {
    title: 'Tasks Summary',
    description: 'Summary of all tasks by status and priority',
    mimeType: 'application/json'
  },
  async () => {
    const allTasks = Array.from(tasks.values());

    const summary = {
      total: allTasks.length,
      byStatus: {
        pending: allTasks.filter(t => t.status === 'pending').length,
        in_progress: allTasks.filter(t => t.status === 'in_progress').length,
        completed: allTasks.filter(t => t.status === 'completed').length
      },
      byPriority: {
        high: allTasks.filter(t => t.priority === 'high').length,
        medium: allTasks.filter(t => t.priority === 'medium').length,
        low: allTasks.filter(t => t.priority === 'low').length
      }
    };

    return {
      contents: [{
        uri: 'tasks://summary',
        text: JSON.stringify(summary, null, 2)
      }]
    };
  }
);

// Prompts
server.registerPrompt(
  'daily_planning',
  {
    title: 'Daily Planning',
    description: 'Generate a daily planning prompt'
  },
  () => ({
    messages: [{
      role: 'user',
      content: {
        type: 'text',
        text: `Help me plan my day by:
1. Reviewing my current tasks
2. Identifying high-priority items
3. Suggesting a reasonable order to tackle them
4. Estimating time needed for each task

Please start by listing my current tasks.`
      }
    }]
  })
);

server.registerPrompt(
  'task_breakdown',
  {
    title: 'Task Breakdown',
    description: 'Break down a task into subtasks',
    argsSchema: z.object({
      taskTitle: z.string().describe('Title of the task to break down')
    })
  },
  ({ taskTitle }) => ({
    messages: [{
      role: 'user',
      content: {
        type: 'text',
        text: `I need to break down this task into smaller, actionable steps:

Task: ${taskTitle}

Please help me:
1. Identify the main components of this task
2. Create specific, actionable subtasks
3. Estimate effort for each subtask
4. Suggest an order to complete them`
      }
    }]
  })
);

// Start server
server.listen();
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "node",
      "args": ["/path/to/build/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```
