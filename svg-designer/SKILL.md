---
name: svg-designer
description: SVG Designer for creating logos, icons, illustrations, and animations. Use when generating brand logos, icon sets, UI illustrations, loading animations, or any vector graphics. Produces clean, optimized SVG code with proper structure, accessibility, and scalability. Covers design rationale, technical best practices, and export guidance for various contexts (favicon, social media, app icons).
---

# SVG Designer

Create professional vector graphics including logos, icons, illustrations, and animations with clean, optimized SVG code.

## Usage Notification

**REQUIRED**: When triggered, state: "🎨 Using SVG Designer skill - creating vector graphics with design rationale."

## Core Principles

1. **Design before code**: Explain rationale before producing SVG
2. **Clean structure**: Grouped elements, meaningful IDs, comments
3. **Accessibility**: Title, desc, aria-labels where appropriate
4. **Optimization**: No redundant paths, efficient coordinates
5. **Scalability**: Proper viewBox, no fixed dimensions

## Workflow

### Phase 1: Context Gathering

Before designing, understand:

**For Logos:**
- Brand name and tagline (if any)
- Industry/domain
- Core values (3-5 keywords)
- Target audience
- Existing brand colors (or preferences)
- Style preference (geometric, organic, typographic, abstract)

**For Icons:**
- Purpose/meaning
- Context (UI, marketing, documentation)
- Style to match (outline, filled, duotone)
- Size constraints

**For Illustrations:**
- Subject matter
- Mood/tone
- Color palette
- Complexity level

### Phase 2: Design Rationale

Before producing code, explain:

```
## Design Rationale

**Concept**: [Core idea driving the design]

**Visual Elements**:
- [Element 1]: Represents [meaning]
- [Element 2]: Represents [meaning]

**Color Choices**:
- [Color 1]: Chosen because [reason]
- [Color 2]: Chosen because [reason]

**Typography** (if applicable):
- Font style: [Description]
- Weight: [Choice and why]

**Why This Works**:
[1-2 sentences connecting design to brand values]
```

### Phase 3: SVG Production

Produce clean, well-structured SVG code.

## SVG Structure Standards

### Basic Template

```svg
<svg 
  xmlns="http://www.w3.org/2000/svg" 
  viewBox="0 0 [width] [height]"
  role="img"
  aria-labelledby="title desc"
>
  <!-- Accessibility -->
  <title id="title">[Short title]</title>
  <desc id="desc">[Longer description]</desc>
  
  <!-- Definitions (gradients, filters, clips) -->
  <defs>
    <!-- Reusable elements here -->
  </defs>
  
  <!-- Main content grouped logically -->
  <g id="[element-name]">
    <!-- Paths and shapes -->
  </g>
</svg>
```

### Grouping Convention

```svg
<!-- Logo structure -->
<g id="logo">
  <g id="icon">
    <!-- Icon paths -->
  </g>
  <g id="wordmark">
    <!-- Text/typography paths -->
  </g>
</g>

<!-- Icon structure -->
<g id="icon-name">
  <g id="background" opacity="0">
    <!-- Hit area if needed -->
  </g>
  <g id="foreground">
    <!-- Visible elements -->
  </g>
</g>
```

### ViewBox Guidelines

| Use Case | ViewBox | Rationale |
|----------|---------|-----------|
| Square icon | `0 0 24 24` | Standard icon grid |
| Wide logo | `0 0 200 60` | Horizontal lockup |
| Tall logo | `0 0 60 200` | Vertical lockup |
| Square logo | `0 0 100 100` | Flexible square |

## Design Patterns by Type

### Logo Styles

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| **Geometric** | Clean shapes, mathematical precision | Tech, finance, modern brands |
| **Organic** | Flowing curves, natural forms | Health, nature, lifestyle |
| **Typographic** | Letterforms as primary element | Personal brands, luxury |
| **Abstract** | Non-literal symbolic forms | Innovation, creative industries |
| **Combination** | Icon + wordmark | Versatile brand identity |

### Icon Styles

| Style | Stroke | Fill | Best For |
|-------|--------|------|----------|
| **Outline** | 1.5-2px | None | UI, minimalist |
| **Filled** | None | Solid | App icons, emphasis |
| **Duotone** | None | Two colors | Modern UI, illustration |
| **Glyph** | None | Single color | System icons |

See `references/design-patterns.md` for visual examples.

## Color Guidelines

### Contrast Requirements

- Logo on light background: Ensure readability
- Logo on dark background: Provide alternate version
- Monochrome version: Always include single-color variant

### Gradient Definitions

```svg
<defs>
  <!-- Linear gradient -->
  <linearGradient id="gradient-1" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#6366F1" />
    <stop offset="100%" stop-color="#8B5CF6" />
  </linearGradient>
  
  <!-- Radial gradient -->
  <radialGradient id="gradient-2" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#FFF" />
    <stop offset="100%" stop-color="#E5E7EB" />
  </radialGradient>
</defs>

<!-- Usage -->
<circle fill="url(#gradient-1)" />
```

### Common Palettes

```
Trustworthy/Corporate:
- Primary: #1E40AF (Blue)
- Secondary: #1F2937 (Slate)

Innovative/Tech:
- Primary: #6366F1 (Indigo)
- Secondary: #8B5CF6 (Violet)

Natural/Organic:
- Primary: #059669 (Emerald)
- Secondary: #065F46 (Dark Green)

Energetic/Bold:
- Primary: #DC2626 (Red)
- Secondary: #F97316 (Orange)

Luxury/Premium:
- Primary: #1F2937 (Near Black)
- Secondary: #D4AF37 (Gold)
```

## Animation Patterns

### CSS Animation in SVG

```svg
<svg viewBox="0 0 100 100">
  <style>
    .spin { 
      animation: rotate 2s linear infinite;
      transform-origin: center;
    }
    @keyframes rotate {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
  </style>
  
  <circle class="spin" cx="50" cy="50" r="40" />
</svg>
```

### SMIL Animation (Native SVG)

```svg
<svg viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40">
    <animate
      attributeName="r"
      values="40;45;40"
      dur="1s"
      repeatCount="indefinite"
    />
  </circle>
</svg>
```

See `references/animation-patterns.md` for loading spinners, transitions, and micro-interactions.

## Accessibility

### Required Elements

```svg
<!-- For meaningful images -->
<svg role="img" aria-labelledby="title desc">
  <title id="title">Company Logo</title>
  <desc id="desc">Blue geometric shape representing innovation</desc>
  ...
</svg>

<!-- For decorative images -->
<svg aria-hidden="true" focusable="false">
  ...
</svg>

<!-- For interactive icons -->
<button aria-label="Close menu">
  <svg aria-hidden="true" focusable="false">
    ...
  </svg>
</button>
```

### Color Accessibility

- Don't rely on color alone for meaning
- Ensure sufficient contrast (4.5:1 for text, 3:1 for graphics)
- Test with color blindness simulators

## Export Guidelines

### Size Recommendations

| Context | Dimensions | Format |
|---------|------------|--------|
| Favicon | 16x16, 32x32, 48x48 | .ico or .png |
| Apple Touch | 180x180 | .png |
| Android | 192x192, 512x512 | .png |
| Open Graph | 1200x630 | .png |
| Twitter Card | 1200x600 | .png |
| App Store | 1024x1024 | .png |

### Multi-Format Delivery

When delivering a logo, provide:

1. **Primary SVG**: Full-color, scalable
2. **Monochrome SVG**: Single color (black)
3. **Reversed SVG**: For dark backgrounds
4. **Favicon ICO**: Multi-size favicon
5. **PNG exports**: Key sizes as needed

## Optimization

### Before Delivery

- Remove unnecessary attributes (default values)
- Simplify paths where possible
- Remove hidden elements
- Combine redundant groups
- Use `<use>` for repeated elements

### SVGO Settings

```json
{
  "plugins": [
    "removeDoctype",
    "removeComments",
    "removeMetadata",
    "removeEditorsNSData",
    "cleanupAttrs",
    "mergeStyles",
    "minifyStyles",
    "removeUselessDefs",
    "cleanupNumericValues",
    "convertColors",
    "removeUnknownsAndDefaults",
    "removeUselessStrokeAndFill",
    "cleanupEnableBackground",
    "convertPathData",
    "convertTransform",
    "removeEmptyAttrs",
    "removeEmptyContainers",
    "mergePaths",
    "removeUnusedNS",
    "sortAttrs"
  ]
}
```

## Reference Files

- `references/design-patterns.md` - Logo and icon style examples
- `references/animation-patterns.md` - Loading spinners, transitions
- `references/icon-library.md` - Common UI icon templates

## Quality Checklist

Before delivering SVG:

- [ ] Design rationale documented
- [ ] viewBox properly set (no fixed width/height)
- [ ] Elements logically grouped with IDs
- [ ] Accessibility elements included (title, desc)
- [ ] Colors defined efficiently (variables or defs)
- [ ] No redundant paths or attributes
- [ ] Tested at multiple sizes
- [ ] Monochrome variant works
- [ ] File is well-commented for editing

## Summary

Good SVG design:
- Starts with understanding the brand/purpose
- Explains the "why" before the "what"
- Produces clean, accessible, scalable code
- Delivers multiple variants for different contexts

Design with intention, code with precision.
