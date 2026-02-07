# Penpot Programmatic Design Patterns

Code patterns for generating designs in Penpot via MCP tools.

## Quick Reference

| Task | Method |
|------|--------|
| Create rectangle | `penpot.createRectangle()` |
| Create board (frame) | `penpot.createBoard()` |
| Create text | `penpot.createText("content")` |
| Create ellipse | `penpot.createEllipse()` |
| Create path | `penpot.createPath()` |
| Create from SVG | `penpot.createShapeFromSvg(svgString)` |
| Group shapes | `penpot.group(shapes)` |
| Find shapes | `penpotUtils.findShapes(predicate)` |
| Get page structure | `penpotUtils.shapeStructure(penpot.root, 3)` |

---

## Essential Patterns

### 1. Explore Before Creating

**Always understand the current design before adding to it:**

```javascript
// Get overview of current page
const structure = penpotUtils.shapeStructure(penpot.root, 3);
return structure;
```

```javascript
// Find existing components
const buttons = penpotUtils.findShapes(
  shape => shape.name?.toLowerCase().includes('button'),
  penpot.root
);
return buttons.map(b => ({ name: b.name, id: b.id }));
```

### 2. Create a Board (Frame)

```javascript
const board = penpot.createBoard();
board.name = "Card Component";
board.x = 100;
board.y = 100;
board.resize(320, 200);

// Style it
board.fills = [{ fillColor: '#FFFFFF' }];
board.borderRadius = 8;

// Add shadow (Material elevation level 1)
board.shadows = [{
  style: 'drop-shadow',
  offsetX: 0,
  offsetY: 1,
  blur: 3,
  spread: 0,
  color: { color: '#000000', opacity: 0.12 }
}];

return { id: board.id, name: board.name };
```

### 3. Add Text with Typography

```javascript
const text = penpot.createText("Headline Text");
text.name = "Title";
text.fontSize = "24";
text.fontWeight = "600";
text.fontFamily = "Inter";  // or "Roboto" for Material
text.lineHeight = "1.2";
text.fills = [{ fillColor: '#1A1A1A' }];

// Position relative to parent
if (parentBoard) {
  parentBoard.appendChild(text);
  penpotUtils.setParentXY(text, 16, 16);
}

return { id: text.id };
```

### 4. Apply Flex Layout

```javascript
const board = penpot.createBoard();
board.name = "Flex Container";
board.resize(320, 400);

// Add flex layout
const flex = board.addFlexLayout();
flex.dir = 'column';           // 'row' | 'column' | 'row-reverse' | 'column-reverse'
flex.rowGap = 12;              // Gap between rows
flex.columnGap = 12;           // Gap between columns
flex.alignItems = 'start';     // 'start' | 'center' | 'end' | 'stretch'
flex.justifyContent = 'start'; // 'start' | 'center' | 'end' | 'space-between' | 'space-around'

// Padding
flex.horizontalPadding = 16;
flex.verticalPadding = 16;
// Or individually: flex.topPadding, flex.rightPadding, flex.bottomPadding, flex.leftPadding

return { id: board.id, layout: 'flex' };
```

### 5. Create Button Component

```javascript
// Primary button
const button = penpot.createBoard();
button.name = "Button - Primary";
button.resize(120, 48);
button.borderRadius = 8;
button.fills = [{ fillColor: '#6200EE' }];  // Material primary

// Button label
const label = penpot.createText("Button");
label.fontSize = "14";
label.fontWeight = "500";
label.fills = [{ fillColor: '#FFFFFF' }];
label.align = 'center';

// Add flex for centering
button.appendChild(label);
const flex = button.addFlexLayout();
flex.alignItems = 'center';
flex.justifyContent = 'center';

return { id: button.id };
```

### 6. Create Card Component

```javascript
// Card container
const card = penpot.createBoard();
card.name = "Card";
card.resize(320, 240);
card.borderRadius = 12;
card.fills = [{ fillColor: '#FFFFFF' }];
card.shadows = [{
  style: 'drop-shadow',
  offsetX: 0,
  offsetY: 2,
  blur: 8,
  color: { color: '#000000', opacity: 0.08 }
}];

// Add flex layout
const flex = card.addFlexLayout();
flex.dir = 'column';
flex.rowGap = 8;
flex.horizontalPadding = 16;
flex.verticalPadding = 16;

// Title
const title = penpot.createText("Card Title");
title.fontSize = "20";
title.fontWeight = "600";
title.fills = [{ fillColor: '#1A1A1A' }];
card.appendChild(title);

// Description
const desc = penpot.createText("Card description text goes here. Keep it concise.");
desc.fontSize = "14";
desc.fills = [{ fillColor: '#666666' }];
desc.growType = 'auto-height';
card.appendChild(desc);

return { id: card.id };
```

---

## Material Design Tokens

### Elevation Shadows

```javascript
const ELEVATION = {
  level0: [],  // No shadow
  level1: [{ style: 'drop-shadow', offsetY: 1, blur: 3, color: { color: '#000000', opacity: 0.12 } }],
  level2: [{ style: 'drop-shadow', offsetY: 3, blur: 6, color: { color: '#000000', opacity: 0.16 } }],
  level3: [{ style: 'drop-shadow', offsetY: 8, blur: 16, color: { color: '#000000', opacity: 0.20 } }],
  level4: [{ style: 'drop-shadow', offsetY: 12, blur: 24, color: { color: '#000000', opacity: 0.24 } }]
};

// Usage
card.shadows = ELEVATION.level2;
```

### Typography Scale

```javascript
const TYPOGRAPHY = {
  displayLarge:  { fontSize: '57', fontWeight: '400', lineHeight: '1.12' },
  displayMedium: { fontSize: '45', fontWeight: '400', lineHeight: '1.16' },
  displaySmall:  { fontSize: '36', fontWeight: '400', lineHeight: '1.22' },
  headlineLarge: { fontSize: '32', fontWeight: '400', lineHeight: '1.25' },
  headlineMedium:{ fontSize: '28', fontWeight: '400', lineHeight: '1.29' },
  headlineSmall: { fontSize: '24', fontWeight: '400', lineHeight: '1.33' },
  titleLarge:    { fontSize: '22', fontWeight: '500', lineHeight: '1.27' },
  titleMedium:   { fontSize: '16', fontWeight: '500', lineHeight: '1.5' },
  titleSmall:    { fontSize: '14', fontWeight: '500', lineHeight: '1.43' },
  bodyLarge:     { fontSize: '16', fontWeight: '400', lineHeight: '1.5' },
  bodyMedium:    { fontSize: '14', fontWeight: '400', lineHeight: '1.43' },
  bodySmall:     { fontSize: '12', fontWeight: '400', lineHeight: '1.33' },
  labelLarge:    { fontSize: '14', fontWeight: '500', lineHeight: '1.43' },
  labelMedium:   { fontSize: '12', fontWeight: '500', lineHeight: '1.33' },
  labelSmall:    { fontSize: '11', fontWeight: '500', lineHeight: '1.45' }
};

// Usage
const text = penpot.createText("Headline");
Object.assign(text, TYPOGRAPHY.headlineMedium);
```

### Spacing Scale (8dp grid)

```javascript
const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48
};
```

### Color Palette

```javascript
const COLORS = {
  // Primary
  primary: '#6200EE',
  primaryVariant: '#3700B3',
  onPrimary: '#FFFFFF',

  // Secondary
  secondary: '#03DAC6',
  secondaryVariant: '#018786',
  onSecondary: '#000000',

  // Surface
  background: '#FFFFFF',
  surface: '#FFFFFF',
  surfaceVariant: '#F5F5F5',

  // Text
  onBackground: '#1A1A1A',
  onSurface: '#1A1A1A',
  onSurfaceVariant: '#666666',

  // Semantic
  error: '#B00020',
  onError: '#FFFFFF',
  success: '#4CAF50',
  warning: '#FF9800'
};
```

---

## Common UI Patterns

### Input Field

```javascript
const inputContainer = penpot.createBoard();
inputContainer.name = "Input Field";
inputContainer.resize(280, 56);
inputContainer.borderRadius = 4;
inputContainer.fills = [{ fillColor: '#F5F5F5' }];
inputContainer.strokes = [{
  strokeColor: '#E0E0E0',
  strokeWidth: 1,
  strokeStyle: 'solid',
  strokeAlignment: 'inner'
}];

const flex = inputContainer.addFlexLayout();
flex.dir = 'column';
flex.justifyContent = 'center';
flex.horizontalPadding = 16;

const label = penpot.createText("Label");
label.fontSize = "12";
label.fills = [{ fillColor: '#666666' }];
inputContainer.appendChild(label);

const value = penpot.createText("Input value");
value.fontSize = "16";
value.fills = [{ fillColor: '#1A1A1A' }];
inputContainer.appendChild(value);

return { id: inputContainer.id };
```

### Navigation Bar

```javascript
const navbar = penpot.createBoard();
navbar.name = "Navigation Bar";
navbar.resize(360, 56);
navbar.fills = [{ fillColor: '#6200EE' }];
navbar.shadows = ELEVATION.level2;

const flex = navbar.addFlexLayout();
flex.dir = 'row';
flex.alignItems = 'center';
flex.horizontalPadding = 16;
flex.columnGap = 16;

// Title
const title = penpot.createText("App Title");
title.fontSize = "20";
title.fontWeight = "500";
title.fills = [{ fillColor: '#FFFFFF' }];
navbar.appendChild(title);

return { id: navbar.id };
```

### List Item

```javascript
const listItem = penpot.createBoard();
listItem.name = "List Item";
listItem.resize(360, 72);
listItem.fills = [{ fillColor: '#FFFFFF' }];

const flex = listItem.addFlexLayout();
flex.dir = 'row';
flex.alignItems = 'center';
flex.horizontalPadding = 16;
flex.columnGap = 16;

// Avatar placeholder
const avatar = penpot.createEllipse();
avatar.resize(40, 40);
avatar.fills = [{ fillColor: '#E0E0E0' }];
listItem.appendChild(avatar);

// Text container
const textContainer = penpot.createBoard();
textContainer.resize(260, 48);
textContainer.fills = [];
const textFlex = textContainer.addFlexLayout();
textFlex.dir = 'column';
textFlex.justifyContent = 'center';
textFlex.rowGap = 4;

const primary = penpot.createText("Primary text");
primary.fontSize = "16";
primary.fills = [{ fillColor: '#1A1A1A' }];
textContainer.appendChild(primary);

const secondary = penpot.createText("Secondary text");
secondary.fontSize = "14";
secondary.fills = [{ fillColor: '#666666' }];
textContainer.appendChild(secondary);

listItem.appendChild(textContainer);

return { id: listItem.id };
```

---

## Tips and Gotchas

| Topic | Key Points |
|-------|------------|
| **Positioning** | `x`/`y` writable; `parentX`/`parentY` READ-ONLY → use `penpotUtils.setParentXY()`; `width`/`height` READ-ONLY → use `resize()` |
| **Z-Order** | Children render in array order (first=bottom); use `bringToFront()`, `sendToBack()`, or `setParentIndex(i)` |
| **Layouts** | Flex/grid controls child positions; modify gaps/padding, not child x/y; check with `if (board.flex)` |
| **Text** | `growType: 'auto-height'` for wrapping; `align`: left/center/right/justify; `verticalAlign`: top/center/bottom |
| **Colors** | Hex strings `'#FFFFFF'`; opacity via `{ fillColor: '#000', fillOpacity: 0.5 }`; gradients via `fillColorGradient` |
| **Debug** | Use `return` for results; store in `storage` object; export with `mcp__penpot__export_shape` to verify |
