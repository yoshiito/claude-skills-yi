# [Project Name]

[One-line project description]

## First Action

**Before responding, invoke a skill.** Every interaction must go through a skill—no freeform responses.

## Intake Roles

These skills accept direct user requests:

- `/technical-product-owner` — features, requirements, "I want...", "we need..."
- `/solutions-architect` — architecture, design, "how should we...", integrations
- `/technical-program-manager` — status, delivery, scheduling, blockers
- `/support-engineer` — errors, bugs, incidents, "this broke..."

## Worker Roles

These skills require an existing ticket with Technical Spec + Gherkin before invocation:

- `/backend-fastapi-postgres-sqlmodel-developer`
- `/frontend-atomic-design-engineer`
- `/backend-fastapi-pytest-tester`
- `/frontend-tester`
- `/api-designer`
- `/data-platform-engineer`
- `/ai-integration-engineer`
- `/mcp-server-developer`
- `/tech-doc-writer-manager`
- `/material-ux-designer`
- `/svg-designer`

If a worker skill receives a direct request for new work, it routes to the appropriate intake role.

## Project Scope

### Team Context

- **Team Slug**: `[slug]` — used in branch names (`feature/{slug}/...`), ticket assignments
- **Ticket System**: `linear` | `github` | `none`
- **Main Branch**: `main`

### Domain Ownership

Skills check ownership before creating tickets or making decisions. Work outside owned domain must be flagged to domain owner, not actioned.

- [e.g., Backend APIs]: [Owner role + person, e.g., Solutions Architect @alice]
- [e.g., Frontend UI]: [Owner role + person]
- [e.g., Data Pipeline]: [Owner role + person]

### Active Roles

Only these skills are active on this project. Skills not listed cannot be invoked.

- [e.g., TPO]: [Scope, e.g., Customer-facing features]
- [e.g., Solutions Architect]: [Scope, e.g., Full-stack architecture]
- [e.g., Backend Developer]: [Scope, e.g., API implementation]

### Cross-Domain Protocol

When work involves a domain you don't own:

1. Document the gap or dependency
2. Tag the domain owner
3. Do NOT create tickets or implementations for that domain

## Naming

- **Plan names**: Feature description only. No dates, quarters, sprints, or years. Confirm with user before using.
- **Branch names**: `{type}/{team-slug}/{TICKET-ID}-{description}`

## Ticket Requirements

All tickets must include:

- **Technical Spec**: MUST/MUST NOT/SHOULD constraints (guardrails for AI agents)
- **Gherkin Scenarios**: Given/When/Then (validation for testers)

TPgM blocks ticket creation if these are missing.

## Skill Behavior

1. Prefix all responses with `[ROLE_NAME]`
2. Check Project Scope before acting—refuse if undefined
3. Verify domain ownership before creating tickets or making decisions
4. Ask user to confirm base branch before creating feature branches
