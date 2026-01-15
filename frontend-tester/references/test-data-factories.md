# Test Data Factories

Patterns for generating consistent, realistic test data.

## Factory Pattern

### Basic Factory

```typescript
// factories/user.ts
interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user' | 'guest'
  createdAt: Date
}

type UserOverrides = Partial<User>

let userIdCounter = 1

export function createUser(overrides: UserOverrides = {}): User {
  const id = `user-${userIdCounter++}`
  
  return {
    id,
    email: `${id}@example.com`,
    name: `Test User ${userIdCounter}`,
    role: 'user',
    createdAt: new Date(),
    ...overrides,
  }
}

// Usage
const user = createUser()
const admin = createUser({ role: 'admin', name: 'Admin User' })
const users = [createUser(), createUser(), createUser()]
```

### Factory with Builder Pattern

```typescript
// factories/user.ts
class UserFactory {
  private user: Partial<User> = {}

  withId(id: string) {
    this.user.id = id
    return this
  }

  withEmail(email: string) {
    this.user.email = email
    return this
  }

  withName(name: string) {
    this.user.name = name
    return this
  }

  asAdmin() {
    this.user.role = 'admin'
    return this
  }

  asGuest() {
    this.user.role = 'guest'
    return this
  }

  build(): User {
    return createUser(this.user)
  }
}

export const userFactory = () => new UserFactory()

// Usage
const admin = userFactory().withName('Admin').asAdmin().build()
const guest = userFactory().asGuest().build()
```

---

## Complex Data Structures

### Related Entities

```typescript
// factories/index.ts
interface Project {
  id: string
  name: string
  ownerId: string
  status: 'active' | 'archived'
  tasks: Task[]
}

interface Task {
  id: string
  title: string
  projectId: string
  assigneeId: string | null
  status: 'todo' | 'in_progress' | 'done'
}

let projectIdCounter = 1
let taskIdCounter = 1

export function createTask(
  projectId: string,
  overrides: Partial<Task> = {}
): Task {
  const id = `task-${taskIdCounter++}`
  
  return {
    id,
    title: `Task ${taskIdCounter}`,
    projectId,
    assigneeId: null,
    status: 'todo',
    ...overrides,
  }
}

export function createProject(overrides: Partial<Project> = {}): Project {
  const id = `project-${projectIdCounter++}`
  const owner = createUser()
  
  return {
    id,
    name: `Project ${projectIdCounter}`,
    ownerId: owner.id,
    status: 'active',
    tasks: [],
    ...overrides,
  }
}

export function createProjectWithTasks(
  taskCount: number,
  overrides: Partial<Project> = {}
): Project {
  const project = createProject(overrides)
  project.tasks = Array.from({ length: taskCount }, () =>
    createTask(project.id)
  )
  return project
}

// Usage
const emptyProject = createProject()
const projectWith5Tasks = createProjectWithTasks(5)
const projectWithCustomTasks = createProject({
  tasks: [
    createTask('p1', { title: 'Design', status: 'done' }),
    createTask('p1', { title: 'Develop', status: 'in_progress' }),
    createTask('p1', { title: 'Test', status: 'todo' }),
  ],
})
```

---

## Faker Integration

### Using @faker-js/faker

```typescript
// factories/user.ts
import { faker } from '@faker-js/faker'

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    createdAt: faker.date.past(),
    avatar: faker.image.avatar(),
    ...overrides,
  }
}

export function createAddress(overrides: Partial<Address> = {}): Address {
  return {
    street: faker.location.streetAddress(),
    city: faker.location.city(),
    state: faker.location.state(),
    zipCode: faker.location.zipCode(),
    country: faker.location.country(),
    ...overrides,
  }
}

export function createProduct(overrides: Partial<Product> = {}): Product {
  return {
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: parseFloat(faker.commerce.price()),
    category: faker.commerce.department(),
    image: faker.image.url(),
    ...overrides,
  }
}
```

### Seeded Randomness

```typescript
import { faker } from '@faker-js/faker'

// Set seed for reproducible data
faker.seed(12345)

// Now all generated data will be consistent
const user1 = createUser() // Always same data with this seed
const user2 = createUser() // Consistent second user

// Reset for different data
faker.seed(67890)
const differentUser = createUser()
```

---

## API Response Mocks

### MSW Handlers with Factories

```typescript
// mocks/handlers.ts
import { rest } from 'msw'
import { createUser, createProject } from '../factories'

export const handlers = [
  // List users
  rest.get('/api/users', (req, res, ctx) => {
    const users = Array.from({ length: 10 }, () => createUser())
    return res(
      ctx.json({
        data: users,
        pagination: { page: 1, totalPages: 1, total: 10 },
      })
    )
  }),

  // Get single user
  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params
    const user = createUser({ id: id as string })
    return res(ctx.json(user))
  }),

  // Create user
  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json()
    const user = createUser(body)
    return res(ctx.status(201), ctx.json(user))
  }),

  // Error scenario
  rest.get('/api/users/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ error: 'Internal server error' })
    )
  }),
]
```

### Scenario-based Handlers

```typescript
// mocks/scenarios.ts
import { rest } from 'msw'
import { createUser, createProject } from '../factories'

export const emptyStateHandlers = [
  rest.get('/api/projects', (req, res, ctx) => {
    return res(ctx.json({ data: [], pagination: { total: 0 } }))
  }),
]

export const loadedStateHandlers = [
  rest.get('/api/projects', (req, res, ctx) => {
    const projects = Array.from({ length: 20 }, () => 
      createProjectWithTasks(5)
    )
    return res(ctx.json({ data: projects, pagination: { total: 20 } }))
  }),
]

export const errorStateHandlers = [
  rest.get('/api/projects', (req, res, ctx) => {
    return res(ctx.status(500), ctx.json({ error: 'Server error' }))
  }),
]

// Usage in tests
import { server } from './server'
import { emptyStateHandlers, errorStateHandlers } from './scenarios'

it('shows empty state', async () => {
  server.use(...emptyStateHandlers)
  render(<ProjectList />)
  expect(await screen.findByText('No projects')).toBeInTheDocument()
})

it('shows error state', async () => {
  server.use(...errorStateHandlers)
  render(<ProjectList />)
  expect(await screen.findByText('Failed to load')).toBeInTheDocument()
})
```

---

## Edge Case Data

### Boundary Values

```typescript
export const edgeCaseUsers = {
  // Empty/minimal
  minimal: createUser({
    name: '',
    email: 'a@b.co',
  }),

  // Maximum lengths
  maxLength: createUser({
    name: 'A'.repeat(255),
    email: `${'a'.repeat(64)}@${'b'.repeat(189)}.com`,
  }),

  // Unicode
  unicode: createUser({
    name: '日本語ユーザー 🎉',
    email: 'unicode@例え.jp',
  }),

  // Special characters
  specialChars: createUser({
    name: "O'Brien-Smith, Jr.",
    email: "test+alias@example.com",
  }),

  // XSS attempt (should be escaped)
  xssAttempt: createUser({
    name: '<script>alert("xss")</script>',
    email: 'xss@example.com',
  }),

  // SQL injection attempt (should be escaped)
  sqlInjection: createUser({
    name: "Robert'); DROP TABLE users;--",
    email: 'sql@example.com',
  }),
}

// Usage
it('handles unicode names', () => {
  render(<UserCard user={edgeCaseUsers.unicode} />)
  expect(screen.getByText('日本語ユーザー 🎉')).toBeInTheDocument()
})

it('escapes XSS attempts', () => {
  render(<UserCard user={edgeCaseUsers.xssAttempt} />)
  expect(screen.queryByRole('script')).not.toBeInTheDocument()
})
```

### State Combinations

```typescript
export const projectStates = {
  // Status variations
  active: createProject({ status: 'active' }),
  archived: createProject({ status: 'archived' }),

  // Task variations
  noTasks: createProject({ tasks: [] }),
  onlyCompleteTasks: createProjectWithTasks(5).then(p => ({
    ...p,
    tasks: p.tasks.map(t => ({ ...t, status: 'done' })),
  })),
  allOverdue: createProjectWithTasks(5).then(p => ({
    ...p,
    tasks: p.tasks.map(t => ({
      ...t,
      dueDate: new Date('2020-01-01'),
    })),
  })),

  // Size variations
  small: createProjectWithTasks(1),
  medium: createProjectWithTasks(10),
  large: createProjectWithTasks(100),
  huge: createProjectWithTasks(1000),
}
```

---

## Fixtures for Playwright

### Test Data Setup

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test'
import { createUser, createProject } from '../factories'

type TestFixtures = {
  testUser: User
  testProject: Project
}

export const test = base.extend<TestFixtures>({
  testUser: async ({ page }, use) => {
    const user = createUser()
    // Could also seed database here
    await use(user)
    // Cleanup after test
  },

  testProject: async ({ testUser }, use) => {
    const project = createProject({ ownerId: testUser.id })
    await use(project)
  },
})

// Usage
test('displays project', async ({ page, testUser, testProject }) => {
  // testUser and testProject available
  await page.goto(`/projects/${testProject.id}`)
  await expect(page.getByText(testProject.name)).toBeVisible()
})
```

### Database Seeding

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test'
import { prisma } from '../lib/prisma' // or your DB client

export const test = base.extend({
  seededUser: async ({ page }, use) => {
    // Create in database
    const user = await prisma.user.create({
      data: {
        email: `test-${Date.now()}@example.com`,
        name: 'Test User',
      },
    })

    await use(user)

    // Cleanup
    await prisma.user.delete({ where: { id: user.id } })
  },
})
```

---

## Organization

### Recommended Structure

```
src/
├── test/
│   ├── factories/
│   │   ├── index.ts        # Re-export all
│   │   ├── user.ts
│   │   ├── project.ts
│   │   └── task.ts
│   ├── mocks/
│   │   ├── handlers.ts     # MSW handlers
│   │   ├── scenarios.ts    # Scenario-specific handlers
│   │   └── server.ts       # MSW server setup
│   ├── fixtures/
│   │   ├── users.ts        # Predefined user fixtures
│   │   ├── projects.ts     # Predefined project fixtures
│   │   └── edge-cases.ts   # Edge case data
│   └── utils/
│       ├── render.tsx      # Custom render with providers
│       └── test-utils.ts   # Shared test utilities
```

### Central Export

```typescript
// test/factories/index.ts
export * from './user'
export * from './project'
export * from './task'

// test/index.ts
export * from './factories'
export * from './fixtures'
export { server } from './mocks/server'
export { render, screen, waitFor } from './utils/render'
```
