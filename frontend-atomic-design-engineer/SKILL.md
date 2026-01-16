---
name: frontend-atomic-design-engineer
description: Militant enforcement of atomic design principles, component modularity, and Storybook documentation for frontend development. Use when building React components, creating component libraries, structuring frontend applications, refactoring component hierarchies, or ensuring comprehensive component documentation. Enforces strict 5-tier hierarchy (Atoms→Molecules→Organisms→Templates→Pages), single responsibility, composition patterns, mandatory Storybook stories with interaction tests, and systematic architecture with zero compromise.
---

# Atomic Design Enforcer

Enforce atomic design principles and modular architecture with zero compromise. Every component must justify its place in the atomic hierarchy and maintain single responsibility.

## Usage Notification

**REQUIRED**: When triggered, state: "⚛️ Using Frontend Developer skill - enforcing atomic design principles and strict modularity."

## Atomic Design Hierarchy

**MANDATORY**: All components must fit into exactly one of these five categories.

| Level | Definition | Max Lines | Data Fetching | Business Logic |
|-------|-----------|-----------|---------------|----------------|
| **Atoms** | Fundamental building blocks (buttons, inputs, icons) | 100 | Never | Never |
| **Molecules** | Simple combinations of 2-5 atoms | 150 | Never | Simple validation only |
| **Organisms** | Complex sections combining molecules/atoms | 300 | Allowed for domain | Allowed |
| **Templates** | Page layouts, content-agnostic | 250 | Never | Layout logic only |
| **Pages** | Specific instances with real data | No limit | Required | Required |

### Hierarchy Rules

**Atoms**: Receive primitive props only. No API calls, business logic, or complex state.

**Molecules**: Combine atoms into functional groups. May have simple interaction logic (validation, toggles).

**Organisms**: Self-contained interface sections. Can manage data fetching for their specific domain.

**Templates**: Define structure and placement. Accept content as props/children. Never hardcode specific content.

**Pages**: Route targets that compose templates with real data. Handle all state management and data orchestration.

See `references/component-examples.md` for detailed code examples at each level.

## Component Organization

**MANDATORY DIRECTORY STRUCTURE**:

```
src/
├── components/
│   ├── atoms/
│   │   └── Button/
│   │       ├── Button.jsx
│   │       ├── Button.module.css
│   │       ├── Button.stories.jsx
│   │       ├── Button.test.jsx
│   │       └── index.js
│   ├── molecules/
│   ├── organisms/
│   ├── templates/
│   └── pages/
├── hooks/
├── utils/
├── services/
└── stores/
```

**Each component directory must contain**: Component file, styles, tests, stories, and index.

## Storybook Requirements

**MANDATORY**: Every component must have complete Storybook stories before production.

### Minimum Story Counts

| Level | Min Stories | Required Coverage |
|-------|-------------|-------------------|
| Atoms | 5+ | Default + all variants + states |
| Molecules | 6+ | Default + variants + states + interactive |
| Organisms | 8+ | Default + empty + error + loading + edge cases + responsive |
| Templates | 4+ | Layout flexibility + responsive behavior |

### Story Structure Standards

```javascript
export default {
  title: 'AtomicLevel/ComponentName',  // Must match hierarchy
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: { /* prop controls */ },
};

export const Default = { args: { /* props */ } };
export const Variant = { args: { /* props */ } };
```

### Interaction Testing

**MANDATORY for interactive components**: Use play functions to test interactions:

```javascript
import { within, userEvent, expect } from '@storybook/test';

export const UserTypesAndSearches = {
  args: { placeholder: 'Search...' },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByPlaceholderText('Search...');
    await userEvent.type(input, 'test query');
    await expect(input).toHaveValue('test query');
  },
};
```

See `references/storybook-patterns.md` for complete examples and configuration.

## Modularity Rules

1. **Single Responsibility**: Each component does ONE thing. Split if multiple concerns.
2. **Composition Over Inheritance**: Build complexity through composition, never inheritance.
3. **No Deep Prop Drilling**: Use context for data crossing 3+ levels.
4. **Explicit Dependencies**: All dependencies through props or context. No globals.
5. **Separation of Logic/Presentation**: Business logic in hooks/services. Components present only.

## Component Checklist

**Atomic Classification**:
- [ ] Fits clearly into one atomic category
- [ ] No atoms with business logic or data fetching
- [ ] No molecules fetching data
- [ ] Templates remain content-agnostic
- [ ] Pages handle all data orchestration

**Modularity**:
- [ ] Single responsibility
- [ ] Composed from smaller components
- [ ] No prop drilling beyond 2 levels
- [ ] All dependencies explicit

**Storybook**:
- [ ] Stories file exists
- [ ] Meets minimum story count
- [ ] All variants/states covered
- [ ] Interactive components have play tests
- [ ] Uses mock data, no API calls

## Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| God Components | Do everything | Break down into hierarchy |
| Anemic Atoms | Too simple to be useful | Provide meaningful abstraction |
| Molecule Bloat | >150 lines or >5 atoms | Promote to organism |
| Template Specificity | Assumes specific content | Keep abstract |
| Page Components | Trying to make pages reusable | Extract to organisms/templates |

## Enforcement

Code reviews must reject:
- Misclassified components
- Atoms with business logic
- Molecules fetching data
- Templates with specific content
- Missing or incomplete Storybook stories
- Stories without interaction tests for interactive components

## Related Skills

### Upstream Skills (Provide Input)

| Skill | Provides |
|-------|----------|
| **TPO** | MRD with user flows, interaction requirements |
| **Solutions Architect** | API contracts, response formats |
| **UX Designer** | Designs, user flows, interaction specs |

### Downstream/Parallel Skills

| Skill | Coordination Point |
|-------|-------------------|
| **Frontend Tester** | Test scenarios, accessibility |
| **Backend Developer** | API contract alignment |
| **Tech Doc Writer** | Component documentation |
| **TPgM** | Progress tracking, blockers |

### Consultation Triggers

- **UX Designer**: Interaction patterns, empty/error states, responsive behavior
- **Frontend Tester**: Test scenarios, accessibility, E2E coverage
- **Backend Developer**: API contracts, data formats

### Handoff Checklist

```
□ UX Designer's designs implemented
□ Storybook stories complete
□ Frontend Tester has test strategy
□ Accessibility validated
□ TPgM updated on progress
```

## Linear Ticket Workflow

**CRITICAL**: When assigned a Linear sub-issue, follow this workflow to ensure traceability.

### Worker Workflow

```
1. Accept work → Move ticket to "In Progress"
2. Create branch → {type}/{team}/LIN-XXX-description (team from claude.md)
3. Do work → Commit with [LIN-XXX] prefix
4. Track progress → Add comment on ticket
5. Complete work → Create PR, move to "In Review"
6. PR merged → Move to "Done"
```

**Branch Pattern**: `{type}/{team}/{LIN-XXX}-{description}`
- `type`: `feature`, `fix`, `refactor`, `docs`, `test`
- `team`: From project's `claude.md` Team Context (e.g., `portal`)
- Example: `feature/portal/LIN-101-password-reset-form`

### Starting Work

When you begin work on an assigned sub-issue:

```python
# Update ticket status
mcp.update_issue(id="LIN-XXX", state="In Progress")

# Add start comment
mcp.create_comment(
    issueId="LIN-XXX",
    body="""🚀 **Started work**
- Branch: `feature/portal/LIN-XXX-password-reset-form`
- Approach: Creating ResetPasswordForm molecule with validation
"""
)
```

### Commit Message Format

```
[LIN-XXX] Brief description of change

- Detail 1
- Detail 2

Ticket: https://linear.app/team/issue/LIN-XXX
```

### Completion Comment Template

When PR is ready for review:

```python
mcp.update_issue(id="LIN-XXX", state="In Review")

mcp.create_comment(
    issueId="LIN-XXX",
    body="""🔍 **Ready for review**
- PR: [link to PR]

## Implementation Summary
- Components: ResetPasswordForm (molecule), PasswordInput (atom)
- Storybook stories: 8 stories with interaction tests
- Accessibility: axe checks passing

## Test Coverage
- Component tests: 15 tests passing
- E2E tests: 3 critical path tests
- Visual regression: baseline captured

## Files Changed
- `src/components/molecules/ResetPasswordForm/`
- `src/components/atoms/PasswordInput/`
- `src/pages/ResetPasswordPage.jsx`
"""
)
```

### After PR Merge

```python
mcp.update_issue(id="LIN-XXX", state="Done")

mcp.create_comment(
    issueId="LIN-XXX",
    body="""✅ **Completed**
- PR merged: [link]
- Storybook deployed
"""
)
```

See `_shared/references/linear-ticket-traceability.md` for full workflow details.

## Reference Files

- `references/component-examples.md` - Detailed code examples for each atomic level
- `references/storybook-patterns.md` - Complete Storybook configuration and story examples

## Summary

Build maintainable, scalable, and testable frontend applications through disciplined architecture and comprehensive component documentation.

**Remember**: Consult UX Designer for design decisions and Frontend Tester for test strategy before implementation.
