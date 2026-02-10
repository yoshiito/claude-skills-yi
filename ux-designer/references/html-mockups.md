# HTML Mockup Guidelines

Create self-contained HTML mockups as an alternative to Penpot when visual fidelity or interactivity is needed quickly.

---

## When to Use HTML Mockups

| Use HTML Mockups | Use Penpot |
|------------------|------------|
| Need pixel-perfect control | Early exploration/ideation |
| Complex interactions to demonstrate | Multiple layout variations |
| Penpot is struggling or slow | Asset library building |
| Developer handoff clarity | Stakeholder review |
| Responsive behavior demonstration | When user specifically requests Penpot |

**Default**: Ask user which format they prefer if unclear.

---

## Output Location

**All HTML mockups go in: `./.ux-design/`**

```
./.ux-design/
├── [project-name]/
│   ├── index.html          # Main mockup or index of mockups
│   ├── page-name.html      # Individual page mockups
│   └── assets/             # Only if external assets needed
│       ├── images/
│       └── fonts/
```

---

## Self-Contained Requirements (MANDATORY)

**Every HTML file MUST be portable — openable directly in any browser without a server.**

### CSS: Inline or `<style>` tag
```html
<style>
  /* All styles in the document */
  .card { ... }
</style>
```

### JavaScript: Inline `<script>` tag
```html
<script>
  // All scripts in the document
</script>
```

### Icons: Inline SVG or CSS
```html
<!-- Inline SVG (preferred) -->
<svg viewBox="0 0 24 24" width="24" height="24">
  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>

<!-- Or CSS-based icons -->
<span class="icon icon-home"></span>
```

### Images: Data URIs or placeholder boxes
```html
<!-- Placeholder (preferred for mockups) -->
<div class="image-placeholder" style="width:200px;height:150px;background:#e0e0e0;">
  <span>Product Image</span>
</div>

<!-- Or data URI for small images -->
<img src="data:image/svg+xml,..." alt="Logo">
```

### Fonts: System fonts or Google Fonts CDN
```html
<!-- System fonts (most portable) -->
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

<!-- Or Google Fonts (requires internet) -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## HTML Mockup Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Name] - UX Mockup</title>
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* Variables */
    :root {
      --color-primary: #6200EE;
      --color-on-primary: #FFFFFF;
      --color-surface: #FFFFFF;
      --color-on-surface: #1A1A1A;
      --color-outline: #E0E0E0;
      --spacing-xs: 4px;
      --spacing-sm: 8px;
      --spacing-md: 16px;
      --spacing-lg: 24px;
      --spacing-xl: 32px;
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 16px;
      --shadow-1: 0 1px 3px rgba(0,0,0,0.12);
      --shadow-2: 0 3px 6px rgba(0,0,0,0.16);
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.5;
      color: var(--color-on-surface);
      background: #F5F5F5;
    }

    /* Component styles below */
  </style>
</head>
<body>
  <!-- Mockup content -->

  <script>
    // Interaction scripts if needed
  </script>
</body>
</html>
```

---

## Responsive Mockups

**Include responsive breakpoints in single file:**

```html
<style>
  /* Mobile first */
  .container { padding: var(--spacing-md); }

  /* Tablet */
  @media (min-width: 768px) {
    .container { padding: var(--spacing-lg); max-width: 720px; margin: 0 auto; }
  }

  /* Desktop */
  @media (min-width: 1024px) {
    .container { max-width: 960px; }
  }

  /* Large desktop */
  @media (min-width: 1280px) {
    .container { max-width: 1200px; }
  }
</style>
```

---

## Interactive States

**Demonstrate hover, focus, active states:**

```html
<style>
  .button {
    background: var(--color-primary);
    color: var(--color-on-primary);
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .button:hover {
    filter: brightness(1.1);
  }

  .button:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }

  .button:active {
    transform: scale(0.98);
  }

  .button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
```

---

## Common Components

### Card
```html
<div style="background:white;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <h3 style="font-size:18px;font-weight:600;margin-bottom:8px;">Card Title</h3>
  <p style="color:#666;font-size:14px;">Card description text.</p>
</div>
```

### Button
```html
<button style="background:#6200EE;color:white;border:none;padding:12px 24px;border-radius:8px;font-weight:500;cursor:pointer;">
  Button Label
</button>
```

### Input Field
```html
<div style="display:flex;flex-direction:column;gap:4px;">
  <label style="font-size:12px;color:#666;">Label</label>
  <input type="text" placeholder="Placeholder" style="padding:12px;border:1px solid #E0E0E0;border-radius:4px;font-size:16px;">
</div>
```

### Navigation
```html
<nav style="display:flex;align-items:center;justify-content:space-between;padding:16px;background:white;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
  <span style="font-weight:600;font-size:20px;">App Name</span>
  <div style="display:flex;gap:16px;">
    <a href="#" style="color:#1A1A1A;text-decoration:none;">Link</a>
    <a href="#" style="color:#1A1A1A;text-decoration:none;">Link</a>
  </div>
</nav>
```

---

## Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Project folder | kebab-case | `tennis-journal/` |
| Page mockups | kebab-case | `session-entry.html` |
| Component demos | `component-[name].html` | `component-card.html` |
| State variations | `[page]-[state].html` | `login-error.html` |

---

## Handoff Notes

**Include design notes as HTML comments:**

```html
<!--
  DESIGN NOTES:
  - Primary action should be visually dominant
  - Error states use #B00020 with 12px icon
  - Touch targets minimum 48x48px
  - See references/design-guardrails.md for icon usage
-->
```

---

## Quality Checklist

- [ ] File opens directly in browser (no server needed)
- [ ] All CSS is inline or in `<style>` tags
- [ ] All JS is inline or in `<script>` tags
- [ ] No external image dependencies (use placeholders or data URIs)
- [ ] Responsive breakpoints included if web design
- [ ] Interactive states demonstrated (hover, focus, active)
- [ ] Accessibility: proper heading hierarchy, alt text, focus visible
- [ ] File saved to `./.ux-design/[project]/`
