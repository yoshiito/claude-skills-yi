---
name: frontend-tester
description: Frontend test coverage analysis and quality assurance for React applications. Use when reviewing test coverage, generating component tests, creating E2E tests with Playwright, identifying edge cases, evaluating test quality, ensuring accessibility compliance (WCAG), or setting up visual regression testing. Complements the Atomic Design skill's Storybook stories with comprehensive testing strategies. Provides frameworks for component testing with React Testing Library, E2E testing with Playwright, accessibility testing, and visual regression.
---

# Frontend Tester

Ensure comprehensive test coverage for React applications through component tests, E2E tests, accessibility validation, and visual regression testing.

## Usage Notification

**REQUIRED**: When triggered, state: "🧪 Using Frontend Tester skill - ensuring comprehensive frontend test coverage."

## Core Philosophy

Frontend testing pyramid:
```
         /\
        /  \        E2E Tests (Playwright)
       /    \       Few, critical paths
      /------\
     /        \     Integration Tests
    /          \    Component interactions
   /------------\
  /              \  Unit/Component Tests
 /                \ Many, fast, isolated
/------------------\
```

## Test Types Overview

| Type | Tool | Purpose | Speed | Quantity |
|------|------|---------|-------|----------|
| Component | React Testing Library | Test components in isolation | Fast | Many |
| Integration | RTL + MSW | Test component interactions | Medium | Some |
| E2E | Playwright | Test full user journeys | Slow | Few |
| Visual | Playwright/Chromatic | Catch visual regressions | Slow | Key screens |
| Accessibility | axe-core + Playwright | WCAG compliance | Fast | All |

## Component Testing (React Testing Library)

### Philosophy

Test components the way users interact with them:
- Query by accessible roles, labels, text
- Avoid testing implementation details
- Focus on behavior, not internals

### Query Priority

```javascript
// 1. Accessible to everyone
getByRole('button', { name: 'Submit' })
getByLabelText('Email address')
getByPlaceholderText('Enter email')
getByText('Welcome back')

// 2. Semantic queries
getByAltText('Profile picture')
getByTitle('Close')

// 3. Test IDs (last resort)
getByTestId('custom-element')
```

### Component Test Structure

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ComponentName } from './ComponentName'

describe('ComponentName', () => {
  // Setup
  const defaultProps = {
    // Required props with sensible defaults
  }
  
  const renderComponent = (props = {}) => {
    return render(<ComponentName {...defaultProps} {...props} />)
  }

  describe('rendering', () => {
    it('renders with required props', () => {
      renderComponent()
      expect(screen.getByRole('...')).toBeInTheDocument()
    })
  })

  describe('interactions', () => {
    it('handles user action', async () => {
      const user = userEvent.setup()
      const onAction = jest.fn()
      renderComponent({ onAction })
      
      await user.click(screen.getByRole('button', { name: 'Action' }))
      
      expect(onAction).toHaveBeenCalledWith(expectedArgs)
    })
  })

  describe('states', () => {
    it('shows loading state', () => {
      renderComponent({ isLoading: true })
      expect(screen.getByRole('progressbar')).toBeInTheDocument()
    })
  })
})
```

See `references/component-test-patterns.md` for comprehensive patterns.

## E2E Testing (Playwright)

### When to Use E2E

- Critical user journeys (signup, checkout, core workflows)
- Cross-page interactions
- Authentication flows
- Third-party integrations
- Visual regression on full pages

### Playwright Test Structure

```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature: User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
  })

  test('successful login redirects to dashboard', async ({ page }) => {
    // Arrange
    await page.getByLabel('Email').fill('user@example.com')
    await page.getByLabel('Password').fill('password123')
    
    // Act
    await page.getByRole('button', { name: 'Sign in' }).click()
    
    // Assert
    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible()
  })

  test('invalid credentials shows error', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com')
    await page.getByLabel('Password').fill('wrongpassword')
    await page.getByRole('button', { name: 'Sign in' }).click()
    
    await expect(page.getByRole('alert')).toContainText('Invalid credentials')
    await expect(page).toHaveURL('/login')
  })
})
```

See `references/playwright-patterns.md` for comprehensive patterns.

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email)
    await this.page.getByLabel('Password').fill(password)
    await this.page.getByRole('button', { name: 'Sign in' }).click()
  }

  async getErrorMessage() {
    return this.page.getByRole('alert').textContent()
  }
}

// Usage in test
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@example.com', 'password')
  await expect(page).toHaveURL('/dashboard')
})
```

## Accessibility Testing

### WCAG 2.1 AA Requirements

| Category | Requirements |
|----------|--------------|
| **Perceivable** | Color contrast 4.5:1, alt text, captions |
| **Operable** | Keyboard accessible, no seizure triggers, enough time |
| **Understandable** | Readable, predictable, input assistance |
| **Robust** | Compatible with assistive tech |

### Automated A11y Testing

```typescript
// Component level with jest-axe
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

it('has no accessibility violations', async () => {
  const { container } = render(<Component />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

```typescript
// E2E level with Playwright
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('page has no a11y violations', async ({ page }) => {
  await page.goto('/dashboard')
  
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()
  
  expect(results.violations).toEqual([])
})
```

### Manual A11y Checklist

- [ ] **Keyboard navigation**: All interactive elements reachable with Tab
- [ ] **Focus visible**: Clear focus indicators on all elements
- [ ] **Screen reader**: Content announced in logical order
- [ ] **Color contrast**: 4.5:1 for text, 3:1 for UI components
- [ ] **Form labels**: All inputs have associated labels
- [ ] **Error messages**: Errors announced to screen readers
- [ ] **Headings**: Logical heading hierarchy (h1 → h2 → h3)
- [ ] **Alt text**: All images have meaningful alt text
- [ ] **Motion**: Respect prefers-reduced-motion

See `references/accessibility-checklist.md` for complete checklist.

## Visual Regression Testing

### Setup with Playwright

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },
})
```

### Visual Test Patterns

```typescript
test('component visual regression', async ({ page }) => {
  await page.goto('/components/button')
  
  // Full page screenshot
  await expect(page).toHaveScreenshot('button-page.png')
  
  // Component screenshot
  const button = page.getByRole('button', { name: 'Primary' })
  await expect(button).toHaveScreenshot('primary-button.png')
})

test('responsive visual regression', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 })
  await page.goto('/dashboard')
  await expect(page).toHaveScreenshot('dashboard-mobile.png')
  
  await page.setViewportSize({ width: 1280, height: 720 })
  await expect(page).toHaveScreenshot('dashboard-desktop.png')
})
```

### What to Visually Test

- [ ] Key landing pages
- [ ] Critical user flows (before/after states)
- [ ] Component variants (from Storybook)
- [ ] Responsive breakpoints
- [ ] Dark/light themes
- [ ] Error states and empty states

## Integration with Storybook

### Testing Storybook Stories

```typescript
// Import stories as tests
import { composeStories } from '@storybook/react'
import * as ButtonStories from './Button.stories'

const { Primary, Secondary, Disabled } = composeStories(ButtonStories)

describe('Button stories', () => {
  it('Primary renders correctly', () => {
    render(<Primary />)
    expect(screen.getByRole('button')).toHaveClass('btn-primary')
  })
})
```

### Storybook Play Functions to Tests

```typescript
// Button.stories.tsx
export const WithInteraction: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const button = canvas.getByRole('button')
    
    await userEvent.click(button)
    await expect(button).toHaveAttribute('aria-pressed', 'true')
  },
}
```

## Test Coverage Strategy

### Coverage by Atomic Level

| Level | Component Tests | Integration | E2E | Visual |
|-------|-----------------|-------------|-----|--------|
| Atoms | Props, states, a11y | - | - | Storybook |
| Molecules | Props, interactions | Simple flows | - | Storybook |
| Organisms | Props, state, API | User flows | - | Storybook + pages |
| Templates | Layout rendering | - | - | Key breakpoints |
| Pages | - | Full flows | Critical paths | Key pages |

### What to Test at Each Level

**Component Tests (atoms, molecules)**:
- All prop variations
- User interactions (click, type, hover)
- State changes (loading, error, empty)
- Accessibility (roles, labels, keyboard)

**Integration Tests (organisms)**:
- API mocking with MSW
- State management integration
- Component composition
- Form submissions

**E2E Tests (pages)**:
- Authentication flows
- Critical user journeys
- Checkout/payment (if applicable)
- Cross-page navigation
- Error recovery

## Mocking Strategies

### API Mocking with MSW

```typescript
// mocks/handlers.ts
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(
      ctx.json({
        id: req.params.id,
        name: 'Test User',
        email: 'test@example.com',
      })
    )
  }),
  
  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json()
    return res(
      ctx.status(201),
      ctx.json({ id: 'new-id', ...body })
    )
  }),
]

// In tests
import { server } from './mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

it('handles API error', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )
  
  render(<UserProfile id="123" />)
  await expect(screen.findByText('Error loading user')).resolves.toBeInTheDocument()
})
```

## Test Quality Checklist

Before tests are complete:

**Coverage**:
- [ ] Happy path tested
- [ ] All user interactions tested
- [ ] Error states tested
- [ ] Loading states tested
- [ ] Empty states tested
- [ ] Edge cases (long text, special chars)
- [ ] Responsive behavior tested

**Quality**:
- [ ] Tests use accessible queries (roles, labels)
- [ ] No implementation details tested
- [ ] Tests are independent
- [ ] Tests are deterministic (no flaky tests)
- [ ] Async properly handled (waitFor, findBy)

**Accessibility**:
- [ ] All components pass axe checks
- [ ] Keyboard navigation tested
- [ ] Screen reader flow verified
- [ ] Color contrast validated

**Performance**:
- [ ] Tests run in < 30 seconds (component)
- [ ] E2E tests run in < 5 minutes
- [ ] No unnecessary waiting

## Reference Files

- `references/component-test-patterns.md` - RTL patterns and examples
- `references/playwright-patterns.md` - E2E test patterns
- `references/accessibility-checklist.md` - Complete WCAG checklist
- `references/test-data-factories.md` - Test data generation patterns

## Summary

Comprehensive frontend testing:
- **Component tests**: Fast, isolated, behavior-focused with RTL
- **Integration tests**: API mocking with MSW, component interactions
- **E2E tests**: Critical paths with Playwright
- **Accessibility**: axe-core automation + manual checklist
- **Visual regression**: Screenshot comparison for key screens

Test like a user, not like an implementation.
