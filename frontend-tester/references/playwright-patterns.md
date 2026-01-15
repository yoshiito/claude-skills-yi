# Playwright E2E Patterns

Comprehensive patterns for end-to-end testing with Playwright.

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'results.xml' }],
  ],
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

## Test Structure

### Basic Test

```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/starting-page')
  })

  test('should do something', async ({ page }) => {
    // Arrange - setup state if needed
    
    // Act - perform actions
    await page.getByRole('button', { name: 'Click me' }).click()
    
    // Assert - verify outcome
    await expect(page.getByText('Success')).toBeVisible()
  })
})
```

### Test with Authentication

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test'

const authFile = 'playwright/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('test@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Sign in' }).click()
  
  await expect(page).toHaveURL('/dashboard')
  
  await page.context().storageState({ path: authFile })
})

// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'chromium',
    dependencies: ['setup'],
    use: {
      storageState: 'playwright/.auth/user.json',
    },
  },
]
```

---

## Locator Patterns

### Preferred Locators (Priority Order)

```typescript
// 1. Role-based (most robust)
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('checkbox', { name: 'Accept terms' })
page.getByRole('link', { name: 'Learn more' })
page.getByRole('heading', { name: 'Dashboard', level: 1 })
page.getByRole('navigation')
page.getByRole('main')
page.getByRole('dialog')
page.getByRole('alert')
page.getByRole('tab', { name: 'Settings' })
page.getByRole('tabpanel')

// 2. Label-based (forms)
page.getByLabel('Email address')
page.getByPlaceholder('Search...')

// 3. Text-based
page.getByText('Welcome back')
page.getByText(/error/i) // regex

// 4. Alt text (images)
page.getByAltText('User avatar')

// 5. Title
page.getByTitle('Close')

// 6. Test ID (last resort)
page.getByTestId('custom-element')
```

### Locator Filtering

```typescript
// Filter by text
page.getByRole('listitem').filter({ hasText: 'Product A' })

// Filter by child element
page.getByRole('listitem').filter({
  has: page.getByRole('button', { name: 'Delete' })
})

// Filter by NOT having
page.getByRole('listitem').filter({
  hasNot: page.getByRole('status', { name: 'Sold out' })
})

// Chain locators
page
  .getByRole('list', { name: 'Products' })
  .getByRole('listitem')
  .first()

// Nth element
page.getByRole('listitem').nth(2) // 0-indexed
page.getByRole('listitem').first()
page.getByRole('listitem').last()
```

---

## Actions

### Click Actions

```typescript
// Basic click
await page.getByRole('button').click()

// Double click
await page.getByRole('button').dblclick()

// Right click
await page.getByRole('button').click({ button: 'right' })

// Shift+click
await page.getByRole('button').click({ modifiers: ['Shift'] })

// Click at position
await page.getByRole('button').click({ position: { x: 10, y: 10 } })

// Force click (skip actionability checks)
await page.getByRole('button').click({ force: true })
```

### Input Actions

```typescript
// Type text
await page.getByLabel('Email').fill('user@example.com')

// Clear and type
await page.getByLabel('Email').clear()
await page.getByLabel('Email').fill('new@example.com')

// Type character by character (triggers events per key)
await page.getByLabel('Search').pressSequentially('hello', { delay: 100 })

// Press keys
await page.keyboard.press('Enter')
await page.keyboard.press('Control+a')
await page.getByLabel('Email').press('Tab')
```

### Select Actions

```typescript
// Select by value
await page.getByLabel('Country').selectOption('us')

// Select by label
await page.getByLabel('Country').selectOption({ label: 'United States' })

// Select multiple
await page.getByLabel('Colors').selectOption(['red', 'blue'])
```

### Checkbox/Radio

```typescript
// Check
await page.getByRole('checkbox', { name: 'Accept' }).check()

// Uncheck
await page.getByRole('checkbox', { name: 'Accept' }).uncheck()

// Set specific state
await page.getByRole('checkbox').setChecked(true)
await page.getByRole('checkbox').setChecked(false)
```

### File Upload

```typescript
// Single file
await page.getByLabel('Upload').setInputFiles('path/to/file.pdf')

// Multiple files
await page.getByLabel('Upload').setInputFiles([
  'path/to/file1.pdf',
  'path/to/file2.pdf',
])

// Clear files
await page.getByLabel('Upload').setInputFiles([])
```

### Drag and Drop

```typescript
await page.getByTestId('drag-item').dragTo(page.getByTestId('drop-zone'))
```

---

## Assertions

### Element Assertions

```typescript
// Visibility
await expect(page.getByRole('alert')).toBeVisible()
await expect(page.getByRole('dialog')).toBeHidden()

// Enabled/Disabled
await expect(page.getByRole('button')).toBeEnabled()
await expect(page.getByRole('button')).toBeDisabled()

// Checked
await expect(page.getByRole('checkbox')).toBeChecked()
await expect(page.getByRole('checkbox')).not.toBeChecked()

// Focus
await expect(page.getByLabel('Email')).toBeFocused()

// Text content
await expect(page.getByRole('alert')).toHaveText('Error occurred')
await expect(page.getByRole('alert')).toContainText('Error')
await expect(page.getByRole('heading')).toHaveText(/welcome/i)

// Input value
await expect(page.getByLabel('Email')).toHaveValue('user@example.com')
await expect(page.getByLabel('Email')).toBeEmpty()

// Attribute
await expect(page.getByRole('link')).toHaveAttribute('href', '/about')

// Class
await expect(page.getByRole('button')).toHaveClass(/primary/)

// CSS
await expect(page.getByRole('button')).toHaveCSS('background-color', 'rgb(0, 0, 255)')

// Count
await expect(page.getByRole('listitem')).toHaveCount(5)
```

### Page Assertions

```typescript
// URL
await expect(page).toHaveURL('/dashboard')
await expect(page).toHaveURL(/\/users\/\d+/)

// Title
await expect(page).toHaveTitle('Dashboard | App')
await expect(page).toHaveTitle(/Dashboard/)
```

### Soft Assertions

```typescript
// Continue test even if assertion fails
await expect.soft(page.getByRole('heading')).toHaveText('Title')
await expect.soft(page.getByRole('button')).toBeVisible()
// Test continues, failures reported at end
```

### Custom Timeout

```typescript
await expect(page.getByRole('alert')).toBeVisible({ timeout: 10000 })
```

---

## Page Object Model

### Page Object

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorAlert: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorAlert = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorAlert).toContainText(message)
  }
}

// pages/DashboardPage.ts
export class DashboardPage {
  readonly page: Page
  readonly heading: Locator
  readonly userMenu: Locator

  constructor(page: Page) {
    this.page = page
    this.heading = page.getByRole('heading', { name: 'Dashboard' })
    this.userMenu = page.getByRole('button', { name: 'User menu' })
  }

  async expectLoaded() {
    await expect(this.heading).toBeVisible()
  }

  async logout() {
    await this.userMenu.click()
    await this.page.getByRole('menuitem', { name: 'Logout' }).click()
  }
}
```

### Using Page Objects

```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

test('successful login flow', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const dashboardPage = new DashboardPage(page)

  await loginPage.goto()
  await loginPage.login('user@example.com', 'password123')
  
  await expect(page).toHaveURL('/dashboard')
  await dashboardPage.expectLoaded()
})
```

---

## API Mocking

```typescript
// Mock API response
await page.route('**/api/users', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'Mock User' }
    ]),
  })
})

// Mock error response
await page.route('**/api/users', async route => {
  await route.fulfill({
    status: 500,
    body: JSON.stringify({ error: 'Server error' }),
  })
})

// Modify response
await page.route('**/api/users', async route => {
  const response = await route.fetch()
  const json = await response.json()
  json.push({ id: 999, name: 'Injected User' })
  await route.fulfill({ response, json })
})

// Abort request
await page.route('**/*.png', route => route.abort())

// Delay response
await page.route('**/api/slow', async route => {
  await new Promise(r => setTimeout(r, 3000))
  await route.continue()
})
```

---

## Visual Testing

```typescript
// Full page screenshot
await expect(page).toHaveScreenshot('homepage.png')

// Element screenshot
await expect(page.getByRole('dialog')).toHaveScreenshot('modal.png')

// With options
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixels: 100,
  threshold: 0.2,
  animations: 'disabled',
  mask: [page.getByTestId('dynamic-content')],
})

// Multiple viewports
test('responsive screenshots', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 })
  await expect(page).toHaveScreenshot('mobile.png')
  
  await page.setViewportSize({ width: 768, height: 1024 })
  await expect(page).toHaveScreenshot('tablet.png')
  
  await page.setViewportSize({ width: 1440, height: 900 })
  await expect(page).toHaveScreenshot('desktop.png')
})
```

---

## Common Scenarios

### Wait for Navigation

```typescript
// Wait for URL change
await page.getByRole('link', { name: 'About' }).click()
await page.waitForURL('/about')

// Wait for navigation after form submit
await Promise.all([
  page.waitForNavigation(),
  page.getByRole('button', { name: 'Submit' }).click(),
])
```

### Handle Dialogs

```typescript
// Alert
page.on('dialog', dialog => dialog.accept())
await page.getByRole('button', { name: 'Delete' }).click()

// Confirm with dismiss
page.on('dialog', dialog => dialog.dismiss())

// Prompt with value
page.on('dialog', dialog => dialog.accept('my input'))
```

### Handle New Tabs

```typescript
const [newPage] = await Promise.all([
  page.waitForEvent('popup'),
  page.getByRole('link', { name: 'Open in new tab' }).click(),
])

await expect(newPage).toHaveURL('/new-page')
await newPage.close()
```

### Download Files

```typescript
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.getByRole('button', { name: 'Download' }).click(),
])

const path = await download.path()
const filename = download.suggestedFilename()
await download.saveAs('downloads/' + filename)
```

### Iframes

```typescript
const frame = page.frameLocator('#iframe-id')
await frame.getByRole('button', { name: 'Submit' }).click()
```

---

## Debugging

```typescript
// Pause execution
await page.pause()

// Slow down actions
test.use({ launchOptions: { slowMo: 500 } })

// Trace viewer
await context.tracing.start({ screenshots: true, snapshots: true })
// ... run test
await context.tracing.stop({ path: 'trace.zip' })

// Console logs
page.on('console', msg => console.log(msg.text()))

// Network requests
page.on('request', req => console.log(req.url()))
page.on('response', res => console.log(res.status(), res.url()))
```

### Run Options

```bash
# Run specific test
npx playwright test login.spec.ts

# Run in headed mode
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# Run specific project
npx playwright test --project=chromium

# Update snapshots
npx playwright test --update-snapshots

# Show report
npx playwright show-report
```
