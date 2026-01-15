# Accessibility Checklist

Comprehensive WCAG 2.1 AA compliance checklist for frontend testing.

## Automated Testing

### Component Level (jest-axe)

```typescript
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

describe('Component accessibility', () => {
  it('has no violations', async () => {
    const { container } = render(<Component />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('has no violations in all states', async () => {
    // Test default state
    const { container, rerender } = render(<Button />)
    expect(await axe(container)).toHaveNoViolations()

    // Test loading state
    rerender(<Button isLoading />)
    expect(await axe(container)).toHaveNoViolations()

    // Test disabled state
    rerender(<Button disabled />)
    expect(await axe(container)).toHaveNoViolations()
  })
})
```

### E2E Level (Playwright + axe)

```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Page accessibility', () => {
  test('homepage has no violations', async ({ page }) => {
    await page.goto('/')
    
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze()
    
    expect(results.violations).toEqual([])
  })

  test('critical pages pass a11y', async ({ page }) => {
    const pages = ['/', '/login', '/dashboard', '/settings']
    
    for (const url of pages) {
      await page.goto(url)
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze()
      
      expect(results.violations, `Violations on ${url}`).toEqual([])
    }
  })
})
```

---

## Manual Testing Checklist

### 1. Perceivable

#### 1.1 Text Alternatives

- [ ] **Images have alt text**: All `<img>` elements have meaningful `alt` attributes
- [ ] **Decorative images**: Decorative images have `alt=""` or `role="presentation"`
- [ ] **Complex images**: Charts/diagrams have detailed text descriptions
- [ ] **Icons**: Icon buttons have accessible names (aria-label or visually hidden text)
- [ ] **SVGs**: SVG icons have `role="img"` and `aria-label` or `<title>`

```typescript
// Test icon button accessibility
it('icon button has accessible name', () => {
  render(<IconButton icon="close" aria-label="Close dialog" />)
  expect(screen.getByRole('button', { name: 'Close dialog' })).toBeInTheDocument()
})
```

#### 1.2 Time-based Media

- [ ] **Videos have captions**: All videos have synchronized captions
- [ ] **Audio has transcript**: Audio content has text transcript
- [ ] **Auto-play disabled**: Media doesn't auto-play (or can be stopped)

#### 1.3 Adaptable

- [ ] **Semantic HTML**: Content uses proper heading hierarchy (h1 > h2 > h3)
- [ ] **Landmarks**: Page has proper landmark regions (header, main, nav, footer)
- [ ] **Lists**: Groups of items use `<ul>`, `<ol>`, or `<dl>`
- [ ] **Tables**: Data tables have proper headers (`<th>`, scope)
- [ ] **Reading order**: Content makes sense when CSS is disabled

```typescript
// Test landmark regions
it('page has proper landmarks', async ({ page }) => {
  await page.goto('/')
  
  await expect(page.getByRole('banner')).toBeVisible() // header
  await expect(page.getByRole('main')).toBeVisible()
  await expect(page.getByRole('navigation')).toBeVisible()
  await expect(page.getByRole('contentinfo')).toBeVisible() // footer
})

// Test heading hierarchy
it('has proper heading structure', async ({ page }) => {
  await page.goto('/')
  
  const h1s = await page.getByRole('heading', { level: 1 }).count()
  expect(h1s).toBe(1) // Only one h1 per page
})
```

#### 1.4 Distinguishable

- [ ] **Color contrast (text)**: 4.5:1 minimum for normal text
- [ ] **Color contrast (large text)**: 3:1 for text 18pt+ or 14pt bold
- [ ] **Color contrast (UI)**: 3:1 for UI components and graphics
- [ ] **Color not sole indicator**: Information not conveyed by color alone
- [ ] **Text resize**: Content readable at 200% zoom
- [ ] **Text spacing**: Works with increased line/letter spacing

```typescript
// Verify color is not sole indicator
it('error state not indicated by color alone', () => {
  render(<Input error="Invalid email" />)
  
  // Should have error icon or text, not just red border
  expect(screen.getByRole('img', { name: /error/i })).toBeInTheDocument()
  // or
  expect(screen.getByText('Invalid email')).toBeInTheDocument()
})
```

---

### 2. Operable

#### 2.1 Keyboard Accessible

- [ ] **All functions keyboard accessible**: Every action available via keyboard
- [ ] **No keyboard traps**: Users can navigate away from all components
- [ ] **Focus visible**: Clear focus indicator on all interactive elements
- [ ] **Focus order logical**: Tab order follows visual/reading order
- [ ] **Skip links**: "Skip to main content" link available

```typescript
// Test keyboard navigation
it('all actions accessible via keyboard', async () => {
  const user = userEvent.setup()
  render(<Menu />)
  
  // Tab to menu
  await user.tab()
  expect(screen.getByRole('button', { name: 'Menu' })).toHaveFocus()
  
  // Open with Enter
  await user.keyboard('{Enter}')
  expect(screen.getByRole('menu')).toBeVisible()
  
  // Navigate menu items with arrows
  await user.keyboard('{ArrowDown}')
  expect(screen.getByRole('menuitem', { name: 'Option 1' })).toHaveFocus()
})

// Test no keyboard trap
it('can escape from modal', async () => {
  const user = userEvent.setup()
  render(<Modal open />)
  
  await user.keyboard('{Escape}')
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
})

// Test skip link
it('has skip to main content link', async ({ page }) => {
  await page.goto('/')
  
  await page.keyboard.press('Tab')
  const skipLink = page.getByRole('link', { name: /skip to main/i })
  await expect(skipLink).toBeFocused()
  
  await page.keyboard.press('Enter')
  await expect(page.getByRole('main')).toBeFocused()
})
```

#### 2.2 Enough Time

- [ ] **Adjustable timeouts**: Session timeouts can be extended
- [ ] **Pause/stop**: Moving content can be paused
- [ ] **No time limits**: No arbitrary time limits on interactions

#### 2.3 Seizures and Physical Reactions

- [ ] **No flashing**: No content flashes more than 3 times/second
- [ ] **Motion safe**: Animations respect `prefers-reduced-motion`

```typescript
// Test reduced motion
it('respects prefers-reduced-motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/')
  
  // Animations should be disabled or minimal
  const animatedElement = page.getByTestId('animated')
  const styles = await animatedElement.evaluate(el => 
    getComputedStyle(el).animationDuration
  )
  expect(styles).toBe('0s')
})
```

#### 2.4 Navigable

- [ ] **Page titles**: Descriptive, unique `<title>` for each page
- [ ] **Focus order**: Focus moves in logical sequence
- [ ] **Link purpose**: Link text is descriptive (not "click here")
- [ ] **Multiple ways**: Multiple ways to find pages (nav, search, sitemap)
- [ ] **Headings descriptive**: Headings describe content

```typescript
// Test descriptive links
it('links have descriptive text', async ({ page }) => {
  await page.goto('/')
  
  // Bad: "Click here", "Read more", "Learn more" without context
  const badLinks = await page.getByRole('link', { name: /^(click here|read more|learn more)$/i }).count()
  expect(badLinks).toBe(0)
})

// Test unique page titles
it('page has descriptive title', async ({ page }) => {
  await page.goto('/settings')
  await expect(page).toHaveTitle(/Settings/)
  
  await page.goto('/profile')
  await expect(page).toHaveTitle(/Profile/)
})
```

#### 2.5 Input Modalities

- [ ] **Touch targets**: 44x44px minimum for touch targets
- [ ] **Pointer gestures**: Complex gestures have simple alternatives
- [ ] **Motion actuation**: Motion-triggered actions have alternatives

---

### 3. Understandable

#### 3.1 Readable

- [ ] **Language declared**: `<html lang="en">` attribute set
- [ ] **Language changes**: Language changes marked with `lang` attribute

```typescript
// Test language declaration
it('has language attribute', async ({ page }) => {
  await page.goto('/')
  const lang = await page.getAttribute('html', 'lang')
  expect(lang).toBe('en')
})
```

#### 3.2 Predictable

- [ ] **Consistent navigation**: Navigation is consistent across pages
- [ ] **Consistent identification**: Components named consistently
- [ ] **No unexpected changes**: Focus/context doesn't change unexpectedly

```typescript
// Test no unexpected focus changes
it('does not change focus unexpectedly', async () => {
  const user = userEvent.setup()
  render(<Form />)
  
  // Typing in field should not move focus
  await user.type(screen.getByLabelText('Name'), 'John')
  expect(screen.getByLabelText('Name')).toHaveFocus()
})
```

#### 3.3 Input Assistance

- [ ] **Error identification**: Errors clearly identified
- [ ] **Labels/instructions**: Inputs have clear labels
- [ ] **Error suggestions**: Helpful error messages
- [ ] **Error prevention**: Confirm before destructive actions

```typescript
// Test error identification
it('announces errors to screen readers', () => {
  render(<Input error="Email is required" />)
  
  const input = screen.getByRole('textbox')
  expect(input).toHaveAccessibleDescription('Email is required')
  expect(input).toHaveAttribute('aria-invalid', 'true')
})

// Test form labels
it('all inputs have labels', () => {
  render(<Form />)
  
  const inputs = screen.getAllByRole('textbox')
  inputs.forEach(input => {
    expect(input).toHaveAccessibleName()
  })
})

// Test destructive action confirmation
it('confirms before delete', async () => {
  const user = userEvent.setup()
  render(<DeleteButton />)
  
  await user.click(screen.getByRole('button', { name: 'Delete' }))
  
  // Confirmation dialog should appear
  expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  expect(screen.getByText(/are you sure/i)).toBeInTheDocument()
})
```

---

### 4. Robust

#### 4.1 Compatible

- [ ] **Valid HTML**: No duplicate IDs, proper nesting
- [ ] **Name, role, value**: Custom components have proper ARIA

```typescript
// Test custom component accessibility
it('custom dropdown has proper ARIA', () => {
  render(<CustomDropdown options={['A', 'B', 'C']} />)
  
  const trigger = screen.getByRole('combobox')
  expect(trigger).toHaveAttribute('aria-expanded', 'false')
  expect(trigger).toHaveAttribute('aria-haspopup', 'listbox')
  
  fireEvent.click(trigger)
  
  expect(trigger).toHaveAttribute('aria-expanded', 'true')
  expect(screen.getByRole('listbox')).toBeInTheDocument()
})

// Test no duplicate IDs
it('has no duplicate IDs', async ({ page }) => {
  await page.goto('/')
  
  const ids = await page.evaluate(() => {
    const elements = document.querySelectorAll('[id]')
    return Array.from(elements).map(el => el.id)
  })
  
  const duplicates = ids.filter((id, i) => ids.indexOf(id) !== i)
  expect(duplicates).toEqual([])
})
```

---

## Common ARIA Patterns

### Dialog/Modal

```html
<div 
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure you want to proceed?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

### Tab Panel

```html
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content 1</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Content 2</div>
```

### Alert

```html
<div role="alert" aria-live="polite">
  Your changes have been saved.
</div>
```

### Loading State

```html
<div aria-busy="true" aria-live="polite">
  <span role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
    Loading...
  </span>
</div>
```

---

## Screen Reader Testing

### Manual Testing Steps

1. **VoiceOver (Mac)**
   - Enable: Cmd + F5
   - Navigate: VO + arrows
   - Interact: VO + Space
   - Rotor: VO + U

2. **NVDA (Windows)**
   - Navigate: Tab, arrows
   - Read: NVDA + Down
   - Elements list: NVDA + F7

3. **Testing Flow**
   - [ ] Can navigate with headings (H key)
   - [ ] Can navigate with landmarks (D key)
   - [ ] Can navigate forms (F key)
   - [ ] Can navigate links (K key)
   - [ ] All content is announced
   - [ ] Dynamic content updates announced

---

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Missing alt text | Add `alt="description"` or `alt=""` for decorative |
| Low contrast | Increase color contrast to 4.5:1 |
| Missing form labels | Add `<label>` or `aria-label` |
| No focus indicator | Add `:focus` styles |
| Keyboard trap | Ensure Escape closes modals |
| Missing landmarks | Add `<header>`, `<main>`, `<nav>`, `<footer>` |
| Bad heading order | Follow h1 > h2 > h3 hierarchy |
| Missing page title | Add unique `<title>` per page |
| Auto-playing media | Remove autoplay or add controls |
| Motion sensitivity | Respect `prefers-reduced-motion` |
