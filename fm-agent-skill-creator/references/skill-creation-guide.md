# Skill Creation Guide

How to create a Claude Code skill following framework conventions.

---

## What Is a Skill?

A skill is WHAT Claude knows or can do. It has:
- **Knowledge or capability**: patterns, formats, standards, procedures
- **No identity**: the agent carries the identity
- **No tool restrictions**: inherits the agent's tools
- **File location**: `skills/<name>/SKILL.md` with optional `references/`

Skills are composable — multiple per agent, same skill across agents.

---

## Skill Categories

| Category | What it teaches | Example |
|---|---|---|
| **Knowledge** | How to THINK — patterns, formats, quality standards | API doc patterns, coding standards |
| **Operations** | How to USE a tool — commands, APIs, platform quirks | Notion write operations, GitHub CLI |
| **Command** | A procedure that changes framework state | Mode transitions, agent routing |

Knowledge makes the agent smarter. Operations makes it competent with tools. Commands are plumbing.

---

## Skill File Structure

```
skills/<name>/
├── SKILL.md                  <- core skill definition
└── references/               <- optional, on-demand knowledge
    ├── topic-a.md
    └── topic-b.md
```

### Frontmatter

Controls invocation behavior:

```yaml
---
name: skill-name
description: "What this skill teaches"
disable-model-invocation: true
context: fork
agent: agent-name
---
```

| Field | What it controls |
|---|---|
| `name` | Skill identifier |
| `description` | Shown in skill selection |
| `disable-model-invocation` | When `true`, slash-command only |
| `user-invocable` | When `false`, Claude-only |
| `allowed-tools` | Tools available when skill is active |
| `model` | Model override |
| `context` | Set to `fork` for subagent launch |
| `agent` | Which agent to launch (requires `context: fork`) |
| `hooks` | Lifecycle hooks |
| `argument-hint` | Hint text for skill arguments |

See official docs: https://code.claude.com/docs/en/skills

### Invocation Control Matrix

| Flags | Effect | Use case |
|---|---|---|
| Neither set | Users AND Claude can invoke | General-purpose |
| `disable-model-invocation: true` | Slash-command only | Role routing, mode transitions |
| `user-invocable: false` | Claude-only | Programmatic skills |
| Both set | Embedded-only (via agent `skills:` field) | Knowledge and operations |

---

## Entry Point Pattern (Dual-Purpose Skill)

One skill serves as BOTH embedded knowledge AND agent launcher:

```yaml
---
name: sf-document-writer
description: "Document writing knowledge and document-writer agent entry point"
context: fork
agent: document-writer
disable-model-invocation: true
---
```

- User types `/sf-document-writer <request>` -> forks to document-writer agent
- Agent has `sf-document-writer` in its `skills:` field -> full content always embedded
- Same file, two uses

---

## Embedded-Only Pattern

For skills ONLY loaded via an agent's `skills:` field:

```yaml
---
name: sf-doc-write-operations
description: "Documentation platform write operations"
user-invocable: false
disable-model-invocation: true
---
```

Cannot be invoked by user or Claude — only accessible as embedded content.

---

## Reference Files

### When to Use References

- SKILL.md should stay under 300 lines
- Specialized knowledge loaded on demand
- Platform-specific details are conditional

### Reference Routing Pattern

The SKILL.md tells the agent WHEN to read which reference:

```markdown
## Reference Routing

| Task | Reference |
|------|-----------|
| Writing API docs | Read `references/api-doc-patterns.md` |
| Writing user docs | Read `references/user-doc-patterns.md` |
| Platform = Notion | Read `references/notion-write-operations.md` |
```

### Split Into Separate Skill vs References

| Criterion | Result |
|-----------|--------|
| Reusable across multiple agents | Separate skill |
| Only serves one agent | References within that agent's skill |

---

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Runtime framework skills | `sf-` prefix | `sf-document-writer` |
| Management framework skills | `fm-` prefix | `fm-agent-skill-creator` |
| Library skills | No prefix | `skill-creator` |
| Reference files | Topic/platform name | `api-doc-patterns.md` |

The `sf-` prefix namespaces runtime framework skills. The `fm-` prefix namespaces management/meta skills used to build and maintain the framework itself.

---

## YAML Generation System (Legacy)

Some skills use YAML-based generation:

```
{skill-name}/
├── skill.yaml        <- source of truth
├── SKILL.md          <- GENERATED (don't edit directly)
└── references/
```

**Rule**: If `skill.yaml` exists, edit it and regenerate. Never edit SKILL.md directly.

Key files:
- `skill-creator/references/skill-template.md.j2` — Jinja2 template
- `skill-creator/references/generate-skill.py` — generator script
- `skill-creator/references/skill-schema.md` — YAML schema docs

For new skills in the agent architecture, direct SKILL.md editing is preferred unless following legacy patterns.

---

## Checklist

Before finalizing a skill:
- [ ] Frontmatter has name, description, correct invocation flags
- [ ] Category identified (knowledge, operations, command)
- [ ] Entry point skills: `context: fork` + `agent:` + `disable-model-invocation: true`
- [ ] Embedded-only skills: both `user-invocable: false` AND `disable-model-invocation: true`
- [ ] Reference routing defined (if has reference files)
- [ ] Under 300 lines (target), 500 (hard limit)
- [ ] Reference files under 200 lines (target), 400 (hard limit)
