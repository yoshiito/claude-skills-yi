---
name: material-ux-designer
description: Pragmatic Material Design UX guidance with flexible application. Use when designing user interfaces, interaction patterns, user flows, visual hierarchies, or making UX decisions for web and mobile applications. Provides Material Design principles (elevation, typography, motion, color systems) as a foundation while encouraging context-appropriate adaptations. Not a rigid framework but a solid starting point for accessible, usable interfaces.
---

# Material Design UX

Guide UX design decisions using Material Design principles as a foundation, not a rigid framework. Material Design offers proven patterns and accessibility standards. Apply these principles thoughtfully based on project context, brand identity, and user needs.

## Usage Notification

**REQUIRED**: When this skill is triggered, immediately state: "🎨 Using Frontend UX Designer skill - applying Material Design principles with pragmatic flexibility."

This notification must appear at the start of the response before any design guidance.

## Core Material Design Principles

Apply these foundational concepts while allowing room for creative interpretation:

### 1. Material as Metaphor
Use visual cues from physical materials (elevation, shadows, surfaces) to create intuitive hierarchy and depth. Surfaces behave logically: they cast shadows, overlap, and exist in a coordinate space. Adapt surface treatment to match brand aesthetic (subtle elevations for minimalist designs, pronounced shadows for bold interfaces).

### 2. Bold, Graphic, Intentional
Create clear visual hierarchies through deliberate use of typography, color, and spacing. Material Design favors strong typographic hierarchies and vibrant color palettes, but adapt scale and intensity to your context. A financial dashboard may use restrained typography while a creative portfolio embraces expressive type.

### 3. Motion Provides Meaning
Use animation to guide attention, show relationships, and provide feedback. Follow Material's easing curves and duration guidelines as starting points, but adjust timing and choreography to match your interface's personality and performance constraints.

## Layout and Structure

**Grid System**: Material's 8dp grid provides consistent spacing and alignment. Use as a foundation but deviate when design intent requires it. Responsive breakpoints (600, 960, 1280, 1920) are suggestions, not mandates.

**Elevation System**: Material defines 24 elevation levels (0-24dp). In practice, use 3-5 distinct elevations per interface:
- Level 0: Base surface (background)
- Level 1: Cards, panels (1-2dp)
- Level 2: Raised content (4-6dp)
- Level 3: Dialogs, modals (8-16dp)
- Level 4: Floating actions, tooltips (12-24dp)

Adapt shadow intensity based on overall visual weight. Light themes often need stronger shadows; dark themes work with subtle glows or borders.

## Typography

Material's type scale provides a solid starting point:
- **Display**: 57px / 45px / 36px (hero content)
- **Headline**: 32px / 28px / 24px (section headers)
- **Title**: 22px / 16px / 14px (subsections)
- **Body**: 16px / 14px (content)
- **Label**: 14px / 12px / 11px (UI elements)

**Practical application**: Start with these scales, then adjust line heights, letter spacing, and weights to match your brand. Material recommends Roboto but encourages font families that align with brand identity. Prioritize readability and hierarchy over strict adherence.

**Line height**: Material suggests 1.5 for body text. Increase for dense content (financial data, code), decrease for display type, adjust for specific fonts.

## Color Systems

Material's color approach: primary, secondary, tertiary colors with tonal variants (50-900). Use this structure for systematic color application, but customize the palette entirely.

**Practical guidance**:
- Define 1 primary color (brand identity, main actions)
- Define 1 secondary color (complementary actions, accents)
- Create light/dark variants for each (-100, base, +100 darkness)
- Use neutral grays (6-8 shades) for text, borders, backgrounds
- Define semantic colors (error, warning, success, info) that work with your palette

Material's color tool accessibility standards are non-negotiable: maintain 4.5:1 contrast for body text, 3:1 for large text and UI elements.

## Component Patterns

Material Design components (buttons, cards, dialogs, etc.) are references, not requirements. Understand their interaction patterns and accessibility considerations, then adapt visual treatment to your design system.

**Buttons**: Material defines text, outlined, contained, and FAB variants. The underlying principles (clear affordance, consistent padding, accessible touch targets) matter more than visual treatment. Minimum 48px touch target remains critical for mobile.

**Cards**: Material's card elevation and corner radius (typically 4dp) create consistent containers. Adapt corner radius (0dp for sharp/technical, 16dp+ for friendly/approachable) and elevation treatment to match aesthetic goals.

**Dialogs and Sheets**: Material's modal patterns (elevation, scrim opacity, positioning) ensure usability. Maintain the spatial logic (modals above all content, proper focus management) while styling to match your interface.

## Interaction and Motion

Material motion principles provide choreography guidance:
- **Duration**: 200-400ms for simple transitions, adjust based on distance traveled and complexity
- **Easing**: Material uses custom curves. Standard alternatives: ease-out for entrances, ease-in for exits, ease-in-out for complex motion
- **Shared element transitions**: Maintain spatial continuity by animating elements between states

Balance motion with performance and brand personality. Minimal interfaces may use faster, linear transitions. Playful interfaces can embrace bouncy, expressive motion.

## Accessibility

These Material Design accessibility standards are mandatory:
- **Color contrast**: 4.5:1 minimum for body text, 3:1 for large text/UI
- **Touch targets**: 48x48dp minimum for interactive elements
- **Focus indicators**: Clear, high-contrast focus states for keyboard navigation
- **Semantic HTML**: Proper heading hierarchy, ARIA labels, form associations
- **Motion**: Respect prefers-reduced-motion, provide static alternatives

## Responsive Design

Material breakpoints are starting points, not requirements:
- **Mobile**: < 600px (optimize for thumb reach, stack content)
- **Tablet**: 600-959px (consider landscape/portrait modes)
- **Desktop**: 960-1279px (multi-column layouts)
- **Large**: 1280-1919px (maximize screen real estate)
- **X-Large**: ≥ 1920px (maintain comfortable reading widths, avoid overstretch)

Adapt breakpoints to your content and layouts. E-commerce may need more granular breaks. Content-focused sites benefit from fluid typography and flexible containers.

## Design Tokens and Systems

Material's token system (spacing, sizing, typography, color) provides structure. Implement similar systematic thinking:
- Define spacing scale (4, 8, 12, 16, 24, 32, 48, 64px common)
- Create consistent sizing for icons (16, 20, 24, 32px)
- Establish border radius scale (0, 2, 4, 8, 16, 24, full)
- Document elevation/shadow system
- Maintain typography scale with clear use cases

## When to Diverge

**Strong adherence** to Material Design principles works for:
- Android applications (user expectations)
- Enterprise tools (established patterns reduce cognitive load)
- Rapid prototyping (leverage pre-built component libraries)

**Adapt freely** when:
- Brand identity demands distinct visual language
- User context differs from Material's assumptions (e.g., specialized tools, creative applications)
- Platform conventions conflict (iOS, desktop applications)
- Performance constraints require lighter approaches
- Marketing/promotional experiences need more creative freedom

## Workflow

1. **Understand context**: Project goals, user needs, technical constraints, brand requirements
2. **Apply principles**: Use Material Design's structural logic (hierarchy, spacing, elevation) as foundation
3. **Adapt visual treatment**: Customize color, typography, corner radii, shadows to match brand and context
4. **Validate patterns**: Ensure interaction patterns meet usability and accessibility standards
5. **Document decisions**: Create tokens and guidelines for consistent implementation

Material Design provides a solid foundation. Your design should feel appropriate for the product, not like a generic Material template.
