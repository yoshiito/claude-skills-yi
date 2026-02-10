# Playwright MCP Design Review Reference

Complete reference for Playwright MCP tools used by UX Designer to review live designs in browsers.

## Purpose for UX Designer

Playwright MCP enables UX Designer to:
- **Review live implementations** - See how designs render in actual browsers
- **Verify design fidelity** - Compare implemented UI against design specs
- **Check responsive behavior** - Test across different viewport sizes
- **Validate accessibility** - Inspect accessibility tree structure
- **Document issues** - Take screenshots for design feedback

---

## Available MCP Tools

### Navigation & Control

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_navigate` | Navigate to a URL |
| `mcp__playwright__browser_navigate_back` | Go back in browser history |
| `mcp__playwright__browser_close` | Close the current page |
| `mcp__playwright__browser_resize` | Resize the browser window |
| `mcp__playwright__browser_tabs` | List, create, close, or select browser tabs |

### Inspection & Capture

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_snapshot` | Capture accessibility snapshot (preferred over screenshot) |
| `mcp__playwright__browser_take_screenshot` | Take visual screenshot (PNG/JPEG) |
| `mcp__playwright__browser_console_messages` | Get console messages (debug info) |
| `mcp__playwright__browser_network_requests` | View network requests |

### Interaction

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_click` | Click on an element |
| `mcp__playwright__browser_hover` | Hover over an element |
| `mcp__playwright__browser_type` | Type text into an element |
| `mcp__playwright__browser_fill_form` | Fill multiple form fields |
| `mcp__playwright__browser_select_option` | Select dropdown option |
| `mcp__playwright__browser_press_key` | Press keyboard key |
| `mcp__playwright__browser_drag` | Drag and drop between elements |
| `mcp__playwright__browser_file_upload` | Upload files |

### Advanced

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_evaluate` | Execute JavaScript on page |
| `mcp__playwright__browser_run_code` | Run Playwright code snippet |
| `mcp__playwright__browser_wait_for` | Wait for text, disappearance, or time |
| `mcp__playwright__browser_handle_dialog` | Handle browser dialogs |
| `mcp__playwright__browser_install` | Install browser if missing |

---

## Key Concepts

### Accessibility Snapshots vs Screenshots

**Prefer snapshots over screenshots** for design review.

```
browser_snapshot captures the accessibility tree - a structured representation of the page.
This provides:
- Element hierarchy and relationships
- Text content and labels
- Interactive element refs for further actions
- Semantic structure (headings, landmarks, roles)
```

Screenshots are useful for:
- Visual documentation
- Sharing with stakeholders
- Capturing complex visual issues

### Element References

Snapshot output includes `ref` identifiers for elements:
```
[ref=button-submit] Button "Submit Order"
[ref=input-email] Textbox "Email address"
```

Use these refs for subsequent interactions:
```
browser_click(ref="button-submit", element="Submit Order button")
```

---

## UX Designer Workflows

### 1. Design Fidelity Review

**Goal**: Verify implemented UI matches design specifications.

```
Step 1: Navigate to the page
→ browser_navigate(url="https://app.example.com/login")

Step 2: Capture accessibility snapshot
→ browser_snapshot()
   Review: Element hierarchy, labels, structure

Step 3: Take screenshot for visual comparison
→ browser_take_screenshot(type="png")
   Compare: Against Penpot design export

Step 4: Check specific viewport
→ browser_resize(width=375, height=812)  # iPhone X
→ browser_take_screenshot(type="png")
```

### 2. Component State Review

**Goal**: Verify all component states are implemented correctly.

```
Step 1: Navigate and snapshot initial state
→ browser_navigate(url="...")
→ browser_snapshot()

Step 2: Hover to see hover state
→ browser_hover(ref="button-primary", element="Primary button")
→ browser_take_screenshot(type="png")

Step 3: Click to see active/pressed state
→ browser_click(ref="button-primary", element="Primary button")

Step 4: Tab through for focus states
→ browser_press_key(key="Tab")
→ browser_take_screenshot(type="png")
```

### 3. Responsive Design Review

**Goal**: Verify design works across breakpoints.

```
Common breakpoints to test:
- Mobile: 375x812 (iPhone X)
- Tablet: 768x1024 (iPad)
- Desktop: 1280x720
- Large: 1920x1080

For each:
→ browser_resize(width=X, height=Y)
→ browser_snapshot()
→ browser_take_screenshot(type="png", filename="mobile-375.png")
```

### 4. Interactive Flow Review

**Goal**: Verify user flows work as designed.

```
Step 1: Navigate to starting point
→ browser_navigate(url="...")

Step 2: Complete the flow
→ browser_type(ref="input-email", text="user@example.com")
→ browser_type(ref="input-password", text="password123")
→ browser_click(ref="button-login", element="Login button")

Step 3: Wait for navigation
→ browser_wait_for(text="Dashboard")

Step 4: Capture result
→ browser_snapshot()
→ browser_take_screenshot(type="png")
```

### 5. Accessibility Audit

**Goal**: Verify semantic structure and accessibility.

```
Step 1: Capture full page snapshot
→ browser_snapshot()

Review in snapshot:
- Heading hierarchy (h1 → h2 → h3)
- Landmark regions (main, nav, footer)
- Button and link labels
- Form input associations
- ARIA labels and roles

Step 2: Check keyboard navigation
→ browser_press_key(key="Tab")  # Repeat
→ browser_snapshot()  # Check focus indicator visibility
```

---

## Tool Reference Details

### browser_navigate

Navigate to a URL.

```json
{
  "url": "https://example.com/page"
}
```

### browser_snapshot

Capture accessibility snapshot (better than screenshot for understanding structure).

```json
{
  "filename": "optional-save-path.md"  // Optional: save to file
}
```

### browser_take_screenshot

Take a visual screenshot.

```json
{
  "type": "png",                    // or "jpeg"
  "fullPage": false,                // true for full scrollable page
  "filename": "screenshot.png",     // optional save path
  "ref": "element-ref",             // optional: screenshot specific element
  "element": "Description"          // required if ref provided
}
```

### browser_resize

Resize browser window for responsive testing.

```json
{
  "width": 375,
  "height": 812
}
```

### browser_click

Click on an element.

```json
{
  "ref": "button-submit",           // from snapshot
  "element": "Submit button",       // human-readable description
  "button": "left",                 // left, right, middle
  "doubleClick": false,
  "modifiers": ["Shift"]            // Alt, Control, Meta, Shift
}
```

### browser_hover

Hover over an element (for hover states).

```json
{
  "ref": "card-item",
  "element": "Card item"
}
```

### browser_type

Type text into an editable element.

```json
{
  "ref": "input-search",
  "text": "search query",
  "element": "Search input",
  "slowly": false,                  // true for one char at a time
  "submit": false                   // true to press Enter after
}
```

### browser_fill_form

Fill multiple form fields at once.

```json
{
  "fields": [
    { "ref": "input-name", "name": "Name field", "type": "textbox", "value": "John" },
    { "ref": "checkbox-terms", "name": "Terms checkbox", "type": "checkbox", "value": "true" },
    { "ref": "select-country", "name": "Country dropdown", "type": "combobox", "value": "USA" }
  ]
}
```

### browser_press_key

Press a keyboard key.

```json
{
  "key": "Tab"                      // ArrowLeft, Enter, Escape, etc.
}
```

### browser_wait_for

Wait for conditions.

```json
{
  "text": "Loading complete",       // Wait for text to appear
  "textGone": "Loading...",         // Wait for text to disappear
  "time": 2                         // Wait N seconds
}
```

### browser_tabs

Manage browser tabs.

```json
{
  "action": "list"                  // list, new, close, select
  "index": 1                        // for close/select
}
```

### browser_evaluate

Execute JavaScript on page.

```json
{
  "function": "() => document.title",
  "ref": "element-ref",             // optional: evaluate on element
  "element": "Description"
}
```

---

## Common Viewport Sizes

| Device | Width | Height |
|--------|-------|--------|
| iPhone SE | 375 | 667 |
| iPhone X/11/12 | 375 | 812 |
| iPhone 12 Pro Max | 428 | 926 |
| iPad | 768 | 1024 |
| iPad Pro | 1024 | 1366 |
| Laptop | 1280 | 720 |
| Desktop | 1920 | 1080 |
| Large Desktop | 2560 | 1440 |

---

## Design Review Checklist

Use this checklist when reviewing implementations:

### Visual Fidelity
- [ ] Colors match design specs
- [ ] Typography (font, size, weight, line-height) correct
- [ ] Spacing (margins, padding) follows design
- [ ] Border radius matches design
- [ ] Shadows/elevation correct

### Component States
- [ ] Default state renders correctly
- [ ] Hover state works
- [ ] Focus state visible and accessible
- [ ] Active/pressed state works
- [ ] Disabled state styled correctly

### Responsive Design
- [ ] Mobile layout works (375px)
- [ ] Tablet layout works (768px)
- [ ] Desktop layout works (1280px)
- [ ] Large screen layout works (1920px)
- [ ] No horizontal scrolling at any breakpoint

### Accessibility
- [ ] Heading hierarchy correct
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Form labels associated correctly
- [ ] Images have alt text
- [ ] Color contrast sufficient

### Interactions
- [ ] Buttons trigger correct actions
- [ ] Navigation works as expected
- [ ] Forms submit correctly
- [ ] Error states display properly
- [ ] Loading states implemented

---

## Sources

- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP Documentation](https://executeautomation.github.io/mcp-playwright/)
- [Cloudflare Playwright MCP](https://developers.cloudflare.com/browser-rendering/playwright/playwright-mcp/)
