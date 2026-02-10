# Penpot MCP Tools Reference

Complete reference for Penpot MCP tools used by UX Designer for programmatic design generation.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__penpot__high_level_overview` | Get basic instructions on Penpot API usage |
| `mcp__penpot__penpot_api_info` | Retrieve API documentation for types and members |
| `mcp__penpot__execute_code` | Execute JavaScript code in Penpot plugin context |
| `mcp__penpot__export_shape` | Export a shape to PNG/SVG for visual verification |
| `mcp__penpot__import_image` | Import an image file into Penpot as a Rectangle fill |

---

## Core Concepts

### The `penpot` Object (Type: `Penpot`)

Primary API object for all Penpot interactions.

```javascript
// Current selection (shapes selected in UI)
penpot.selection  // Shape[]

// Current page root
penpot.root  // Shape (root of active page)

// Generate CSS for elements
penpot.generateStyle(shapes, { type: "css", withChildren: true })

// Generate HTML/SVG markup
penpot.generateMarkup(shapes)

// Create shapes
penpot.createRectangle()
penpot.createBoard()
penpot.createText("content")
penpot.createEllipse()
penpot.createPath()
penpot.createShapeFromSvg(svgString)
penpot.group(shapes)
```

### The `penpotUtils` Object

Essential utilities - **always use these instead of writing your own**.

```javascript
// Page operations
penpotUtils.getPages()                    // { id, name }[]
penpotUtils.getPageById(id)               // Page | null
penpotUtils.getPageByName(name)           // Page | null

// Shape structure
penpotUtils.shapeStructure(shape, maxDepth)  // { id, name, type, children?, layout? }

// Find shapes
penpotUtils.findShapeById(id)             // Shape | null
penpotUtils.findShape(predicate, root?)   // Shape | null (global if no root)
penpotUtils.findShapes(predicate, root?)  // Shape[]

// Containment
penpotUtils.isContainedIn(child, parent)  // boolean

// Positioning (CRITICAL - parentX/parentY are READ-ONLY)
penpotUtils.setParentXY(shape, parentX, parentY)

// Analysis
penpotUtils.analyzeDescendants(root, evaluator, maxDepth?)
```

### The `storage` Object

Persist data across tool calls. Store intermediate results and utility functions.

```javascript
// Store a value
storage.myData = { shapes: foundShapes };

// Reference later
return storage.myData.shapes.map(s => s.name);
```

---

## Shape Types and Properties

### Shape Type Union

All shape types: `Board`, `Group`, `Rectangle`, `Path`, `Text`, `Ellipse`, `Image`, `Boolean`, `SvgRaw`

### Common Properties (ShapeBase)

| Property | Type | Writable | Notes |
|----------|------|----------|-------|
| `x`, `y` | number | Yes | Top-left corner in absolute coordinates |
| `parentX`, `parentY` | number | **READ-ONLY** | Use `penpotUtils.setParentXY()` |
| `width`, `height` | number | **READ-ONLY** | Use `resize(w, h)` method |
| `bounds` | Bounds | **READ-ONLY** | Use x/y + resize() |
| `name` | string | Yes | Shape name |
| `fills` | Fill[] | Yes | Fill styling |
| `strokes` | Stroke[] | Yes | Stroke styling |
| `shadows` | Shadow[] | Yes | Drop shadows |
| `rotation` | number | Yes | Rotation angle |
| `opacity` | number | Yes | 0-1 |
| `blocked`, `hidden`, `visible` | boolean | Yes | Visibility flags |
| `parent` | Shape | Read | Parent shape |
| `children` | Shape[] | Read | Child shapes |
| `type` | string | Read | Shape type identifier |

### Shape Methods

```javascript
// Sizing
shape.resize(width, height)

// Rotation
shape.rotate(angle, center?)

// Z-Order
shape.bringToFront()
shape.sendToBack()
shape.bringForward()
shape.sendBackward()
shape.setParentIndex(index)  // 0-based

// Hierarchy
parent.appendChild(shape)     // Move to new parent
parent.insertChild(index, shape)

// Deletion (ONLY for permanent removal)
shape.remove()
```

---

## Styling

### Fills

```javascript
// Solid color
shape.fills = [{ fillColor: '#FFFFFF' }];

// With opacity
shape.fills = [{ fillColor: '#000000', fillOpacity: 0.5 }];

// Gradient (via fillColorGradient)
shape.fills = [{
  fillColorGradient: {
    type: 'linear',
    startX: 0, startY: 0,
    endX: 1, endY: 1,
    stops: [
      { offset: 0, color: '#FF0000' },
      { offset: 1, color: '#0000FF' }
    ]
  }
}];
```

### Strokes

```javascript
shape.strokes = [{
  strokeColor: '#000000',
  strokeWidth: 2,
  strokeStyle: 'solid',        // solid, dashed, dotted, mixed
  strokeAlignment: 'center'    // center, inner, outer
}];
```

### Shadows

```javascript
shape.shadows = [{
  style: 'drop-shadow',
  offsetX: 0,
  offsetY: 4,
  blur: 8,
  spread: 0,
  color: { color: '#000000', opacity: 0.12 }
}];
```

---

## Layout Systems

### Flex Layout

```javascript
const board = penpot.createBoard();
const flex = board.addFlexLayout();

// Direction
flex.dir = 'column';  // row, column, row-reverse, column-reverse

// Gaps
flex.rowGap = 16;
flex.columnGap = 16;

// Alignment
flex.alignItems = 'center';     // start, center, end, stretch
flex.justifyContent = 'start';  // start, center, end, space-between, space-around

// Padding
flex.horizontalPadding = 16;
flex.verticalPadding = 16;
// Or: topPadding, rightPadding, bottomPadding, leftPadding
```

### Grid Layout

```javascript
const board = penpot.createBoard();
const grid = board.addGridLayout();

grid.rows = [{ type: 'flex', value: 1 }];
grid.columns = [{ type: 'flex', value: 1 }, { type: 'fixed', value: 200 }];
grid.rowGap = 8;
grid.columnGap = 8;
```

**Critical**: When a board has flex/grid layout, child positions are controlled by the layout. Modify gaps/padding, not child x/y.

---

## Text Properties

```javascript
const text = penpot.createText("Content");
text.name = "Label";
text.fontSize = "16";
text.fontWeight = "500";      // 100-900
text.fontFamily = "Inter";
text.lineHeight = "1.5";
text.align = "center";        // left, center, right, justify
text.verticalAlign = "top";   // top, center, bottom
text.fills = [{ fillColor: '#1A1A1A' }];
text.growType = 'auto-height'; // For wrapping text
```

---

## Component Libraries

### Accessing Libraries

```javascript
penpot.library.local          // Current file's library
penpot.library.connected      // Connected external libraries
penpot.library.availableLibraries()  // Promise<LibrarySummary[]>
penpot.library.connectLibrary(libraryId)  // Promise<Library>
```

### Using Library Components

```javascript
// Find component
const button = library.components.find(c => c.name.includes('Button'));

// Create instance
const instance = button.instance();  // Returns Shape

// Get main component
const main = button.mainInstance();
```

### Creating Library Assets

```javascript
// Color
const color = penpot.library.local.createColor();
color.name = 'Brand Primary';
color.color = '#0066FF';

// Typography
const typo = penpot.library.local.createTypography();
typo.name = 'Body Large';

// Component from shapes
const component = penpot.library.local.createComponent([shape1, shape2]);
component.name = 'My Button';
```

---

## UX Designer Workflows

### 1. Explore Before Creating

**Always understand the current design first.**

```javascript
// Get page structure
const structure = penpotUtils.shapeStructure(penpot.root, 3);
return structure;

// Find existing components
const buttons = penpotUtils.findShapes(
  shape => shape.name?.toLowerCase().includes('button'),
  penpot.root
);
return buttons.map(b => ({ name: b.name, id: b.id, type: b.type }));
```

### 2. Visual Verification

**Always export to verify your work.**

```javascript
// After creating/modifying shapes
// Use mcp__penpot__export_shape to see the result
```

### 3. Working with Selection

```javascript
// Get user's current selection
const selected = penpot.selection;
if (selected.length === 0) {
  return 'Please select a shape to work with';
}

// Analyze selection
return penpotUtils.shapeStructure(selected[0], 2);
```

### 4. Generating CSS from Design

```javascript
// Extract CSS for implementation handoff
const css = penpot.generateStyle(penpot.selection, {
  type: 'css',
  withChildren: true
});
return css;
```

---

## Common Gotchas

| Issue | Solution |
|-------|----------|
| `parentX`/`parentY` won't change | Use `penpotUtils.setParentXY(shape, x, y)` |
| `width`/`height` won't change | Use `shape.resize(w, h)` |
| Child position not updating | Check if parent has flex/grid layout |
| Shapes not visible | Check z-order with children array order |
| Text baseline issues | Small 1-2px deviations are normal |

---

## API Types Reference

Full list of types in Penpot API:

`Penpot`, `ActiveUser`, `Blur`, `Board`, `VariantContainer`, `Boolean`, `CloseOverlay`, `Color`, `ColorShapeInfo`, `ColorShapeInfoEntry`, `Comment`, `CommentThread`, `CommonLayout`, `Context`, `ContextGeometryUtils`, `ContextTypesUtils`, `ContextUtils`, `Dissolve`, `Ellipse`, `EventsMap`, `Export`, `File`, `FileVersion`, `Fill`, `FlexLayout`, `Flow`, `Font`, `FontVariant`, `FontsContext`, `GridLayout`, `Group`, `GuideColumn`, `GuideColumnParams`, `GuideRow`, `GuideSquare`, `GuideSquareParams`, `HistoryContext`, `Image`, `Interaction`, `LayoutCellProperties`, `LayoutChildProperties`, `Library`, `LibraryColor`, `LibraryComponent`, `LibraryVariantComponent`, `LibraryElement`, `LibrarySummary`, `LibraryTypography`, `LocalStorage`, `NavigateTo`, `OpenOverlay`, `OpenUrl`, `OverlayAction`, `Page`, `Path`, `PathCommand`, `PluginData`, `PreviousScreen`, `Push`, `Rectangle`, `RulerGuide`, `Shadow`, `ShapeBase`, `Slide`, `Stroke`, `SvgRaw`, `Text`, `TextRange`, `ToggleOverlay`, `Track`, `User`, `Variants`, `Viewport`, `Action`, `Animation`, `BooleanType`, `Bounds`, `Gradient`, `Guide`, `ImageData`, `LibraryContext`, `Point`, `RulerGuideOrientation`, `Shape`, `StrokeCap`, `Theme`, `TrackType`, `Trigger`

Use `mcp__penpot__penpot_api_info` to get detailed documentation for any type.

---

## Sources

- [Penpot Plugin API Documentation](https://help.penpot.app/plugins/api/)
- [Penpot Plugins API Reference](https://penpot-plugins-api-doc.pages.dev/)
- [Penpot Plugin Examples](https://github.com/penpot/penpot-plugins)
