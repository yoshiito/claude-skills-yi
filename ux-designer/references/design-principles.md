# Design Thinking Principles

Core design thinking that underpins all UX decisions. Apply these BEFORE reaching for Material Design specifications.

## The Design Thinking Mindset

**Design is problem-solving, not decoration.** Every visual choice must answer: "What user problem does this solve?"

### The 5 Questions (MANDATORY before designing)

1. **WHO** is the user? (Demographics, context, expertise level)
2. **WHAT** are they trying to accomplish? (Task, not feature)
3. **WHERE** will they use this? (Device, environment, attention level)
4. **WHEN** in their journey? (First use, power user, stressed, relaxed)
5. **WHY** does this matter to them? (Motivation, pain points)

**If you cannot answer these questions, you are not ready to design.**

---

## Visual Hierarchy Principles

### The 3-Second Rule

Users should understand the page purpose and primary action within 3 seconds. Test by asking:
- What is this page for?
- What should I do first?
- Where do I look next?

### Hierarchy Through Contrast

Create hierarchy using MULTIPLE contrast dimensions:

| Dimension | Low Emphasis | High Emphasis |
|-----------|--------------|---------------|
| **Size** | 14px body | 32px headline |
| **Weight** | Regular 400 | Bold 700 |
| **Color** | Muted gray | Primary brand |
| **Space** | Tight padding | Generous margins |
| **Position** | Bottom/edges | Top/center |

**Rule**: Use 2-3 dimensions together for clear hierarchy. Size alone is not enough.

### The F-Pattern and Z-Pattern

**F-Pattern** (content-heavy pages):
- Users scan horizontally across the top
- Move down and scan a shorter horizontal line
- Continue down the left side vertically

**Z-Pattern** (minimal pages):
- Top left → Top right → Bottom left → Bottom right
- Use for landing pages, forms, single-action screens

**Design implication**: Place primary actions and key content along these scan paths.

---

## Gestalt Principles (Non-Negotiable)

### 1. Proximity
Items close together are perceived as related. Group related elements, separate unrelated ones.

**Application**:
- Form fields and their labels: 4-8px gap
- Related field groups: 16-24px gap
- Unrelated sections: 32-48px gap

### 2. Similarity
Elements that look alike are perceived as related.

**Application**:
- All clickable elements share visual treatment
- All section headers share typography
- All status indicators use consistent iconography

### 3. Closure
The mind completes incomplete shapes.

**Application**:
- Card designs don't need full borders
- Progress indicators can be partial circles
- Icons can be simplified outlines

### 4. Continuity
Eyes follow lines and curves naturally.

**Application**:
- Align elements along invisible lines
- Use consistent grid alignment
- Create visual flow between sections

### 5. Figure-Ground
Users distinguish foreground from background.

**Application**:
- Modal overlays need sufficient contrast with page
- Active states must be distinguishable from inactive
- Focus states must pop from surrounding content

---

## Cognitive Load Reduction

### Miller's Law: 7 plus/minus 2

Users can hold 5-9 items in working memory. Chunk information accordingly.

**Application**:
- Navigation: 5-7 top-level items maximum
- Form sections: 5-7 fields before a visual break
- Option lists: Chunk into categories if > 7 items

### Hick's Law: Decision Time

Decision time increases logarithmically with choices. Fewer options = faster decisions.

**Application**:
- Primary action: 1 per view
- Secondary actions: 2-3 maximum
- If more actions needed, use progressive disclosure

### Recognition Over Recall

Users recognize patterns faster than they recall information.

**Application**:
- Show recent items, don't require search
- Use icons WITH labels (not icons alone)
- Provide examples in empty states

---

## Information Architecture

### Progressive Disclosure

Show only what's needed at each step. Reveal complexity gradually.

| Level | What to Show |
|-------|--------------|
| **Surface** | Primary actions, essential info |
| **One click** | Secondary options, details |
| **Intentional dig** | Advanced settings, edge cases |

### Content Hierarchy

1. **Page title**: What is this?
2. **Primary content**: The main thing
3. **Supporting content**: Context and details
4. **Actions**: What can I do?
5. **Navigation**: Where else can I go?

### Empty States as Onboarding

Empty states are teaching moments, not error states.

**Include**:
- Clear explanation of what this area will contain
- Visual representation of the future state
- Single clear action to populate the state

---

## User Flow Principles

### The Happy Path

Design the ideal path first. Make it:
- **Obvious**: No guessing required
- **Short**: Minimum steps to goal
- **Reversible**: Easy to undo/go back

### Error Prevention > Error Handling

| Prevention | Handling |
|------------|----------|
| Disable invalid options | Show error after attempt |
| Inline validation as user types | Form-level error summary |
| Confirmation for destructive actions | Undo after the fact |

### Feedback Loops

Every user action needs feedback:

| Action | Feedback | Timing |
|--------|----------|--------|
| Hover | Visual change | Immediate |
| Click | State change | < 100ms |
| Submit | Progress indicator | Immediate |
| Complete | Success confirmation | Upon completion |

---

## Design Decision Framework

For every design choice, document:

```
DECISION: [What element/pattern]
PROBLEM: [What user problem does this solve?]
ALTERNATIVES: [What else was considered?]
TRADE-OFFS: [What's sacrificed for this choice?]
VALIDATION: [How will we know this works?]
```

**If you cannot articulate the PROBLEM, reconsider the design.**

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Instead |
|--------------|--------------|---------|
| **Everything is bold** | Nothing stands out | Use bold sparingly for emphasis |
| **Rainbow colors** | No hierarchy, visual noise | 1 primary + 1 accent + neutrals |
| **Ambiguous icon-only buttons** | Unfamiliar icons cause guessing | Use established icons OR add labels for clarity |
| **Tiny touch targets** | Mobile usability fail | 48x48dp minimum |
| **Hidden navigation** | Users don't find features | Progressive disclosure, not hiding |
| **Centered everything** | Hard to scan, no anchor points | Left-align content, center sparingly |
| **Decorative animation** | Distracting, performance hit | Functional motion only |

---

## Validation Questions

Before finalizing any design:

1. Can a new user complete the primary task without help?
2. Is there ONE clear focal point per view?
3. Can users scan and find what they need in 3 seconds?
4. Does the visual hierarchy match the task hierarchy?
5. Are related items grouped and unrelated items separated?
6. Is there clear feedback for every interaction?
7. Can users recover from errors easily?
8. Does it work at mobile widths without horizontal scroll?
