# [Project Name]

[One-line project description]

uses: yoshi-skills-framework

---

## Skills Path

- **Skills Path**: `[skills-path]`

All file references use `{Skills Path}/` prefix. Set this to your Claude Code skills library directory.

**Example**: `/Users/me/.claude/skills`

## Placeholder Detection — BLOCKING

**Placeholder patterns**: `[Project Name]`, `[slug]`, `[e.g., ...]`, `[Add your rules here]`, `[skills-path]`

If ANY placeholders exist, PM blocks all work activities. PM can respond and help configure, but cannot route, invoke ASC, or start work. User cannot override this block.

## Session Start

**If placeholders exist** → PM responds but blocks work until configured.

**If configured** → `[PM] - How can I help you today?`

## Project Scope

### Team Context

- **Team Slug**: `[slug]`
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

- **Plan names**: Feature description only. No dates, quarters, sprints, or years.

## Coding Standards

**Baseline**: See `{Skills Path}/_shared/references/coding-standards-baseline.md`

### Project-Specific Rules

- [Add your rules here]
