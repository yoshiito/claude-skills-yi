# Composition Patterns

How skills compose into agents and how to design the composition.

---

## The Composition Model

An agent's effective knowledge = **always-embedded skills + currently-loaded reference files**.

```
agent-name (agent)
├── sf-skill-a (always embedded via skills:)
│   ├── SKILL.md                    <- always in context
│   └── references/topic.md        <- loaded on demand
└── sf-skill-b (always embedded via skills:)
    ├── SKILL.md                    <- always in context
    └── references/platform.md     <- loaded on demand
```

---

## Two Loading Mechanisms

| Mechanism | What loads | When | Context cost |
|---|---|---|---|
| **Always embedded** | Full SKILL.md content | Agent startup | Permanent |
| **On-demand references** | Reference file content | Agent reads via Read tool | Temporary |

### Always Embedded
For core knowledge the agent cannot function without. Goes in agent's `skills:` field.
**Cost**: Permanently in context for every task, even when not needed.

### On-Demand References
For specialized knowledge loaded only when the task requires it.
**Cost**: Temporary. Only in context for the current task.

---

## Subagent Discovery Constraint

Subagents can ONLY access:
1. Their own system prompt (agent body)
2. CLAUDE.md files (global and project)
3. Skills in their `skills:` field — full content injected at startup

Subagents CANNOT discover or invoke skills outside their `skills:` field. This shapes everything.

---

## Design Principles

### Fewer Skills, More References

Rather than many small skills (all permanently in context), prefer fewer skills with reference files.

**Bad**: 5 skills in `skills:` field, each 200 lines = 1000 lines permanently in context
**Good**: 2 skills in `skills:` (300 lines permanent) + reference files loaded on demand

### Reusability Determines Skill Boundaries

| Criterion | Result |
|-----------|--------|
| Knowledge serves ONE agent only | References within that agent's skill |
| Knowledge serves MULTIPLE agents | Separate skill |

Example:
- API doc patterns -> only document-writer uses it -> reference file in sf-document-writer
- Platform write operations -> document-writer AND market-researcher use it -> separate sf-doc-write-operations skill

### Entry Point = Embedded Knowledge

The entry point skill (with `context: fork` + `agent:`) is also the primary embedded skill. No separate "launcher" skill needed.

---

## Composition Design Workflow

When designing a new agent + skills:

1. **Define the agent's purpose** — what does it do?
2. **Apply the agent test** — should this be an agent or knowledge for existing agent?
3. **Identify knowledge needs** — what does the agent need to know?
4. **Split by reusability**:
   - Reusable across agents -> separate skill
   - Agent-specific -> references in the agent's primary skill
5. **Design reference routing** — when does the agent read which reference?
6. **Verify context budget** — too many skills permanently embedded?

---

## Composition Examples

### Single-Skill Agent

Agent with one primary skill (no reusable skills needed).

```
reviewer (agent)
└── sf-reviewer (always embedded)
    ├── SKILL.md
    └── references/...
```

### Multi-Skill Agent

Agent with agent-specific + reusable skills.

```
market-researcher (agent)
├── sf-market-researcher (agent-specific)
├── sf-research-methodology (reusable)
└── sf-doc-write-operations (reusable)
```

### Shared Skill Across Agents

Same skill embedded by multiple agents.

```
sf-research-methodology
├── Embedded by: market-researcher
├── Embedded by: product-owner
└── references/ loaded on demand by whichever agent needs them
```

### Full Example: Document Writer

```
document-writer (agent)
├── tools: Read, Write, Edit, Glob, Grep, Bash
├── sf-document-writer (always embedded — agent-specific)
│   ├── SKILL.md — inventory, workflow, quality, reference routing
│   └── references/
│       ├── api-doc-patterns.md         <- on demand
│       ├── user-doc-patterns.md        <- on demand
│       └── decision-log-patterns.md    <- on demand
└── sf-doc-write-operations (always embedded — reusable)
    ├── SKILL.md — publish workflow, platform routing
    └── references/
        ├── notion-write-operations.md   <- on demand
        ├── confluence-write-operations.md <- on demand
        └── mkdocs-write-operations.md   <- on demand
```

**Entry point**: `/sf-document-writer <request>` -> forks to document-writer agent
**Always in context**: sf-document-writer SKILL.md + sf-doc-write-operations SKILL.md
**On demand**: whichever reference files the task requires

---

## Declaration Pattern

The agent declares which knowledge it's currently using:

```
<document-writer>: [api-doc-patterns, notion] Updating the /users endpoint documentation...
```

This tells the user exactly which expertise is active.

---

## Checklist

Before finalizing composition:
- [ ] Each embedded skill is justified (agent needs it for EVERY task)
- [ ] Specialized knowledge is in reference files, not embedded
- [ ] Reusable skills are separate, agent-specific knowledge is in references
- [ ] Entry point skill has dual purpose (embedded + launcher)
- [ ] Context budget is reasonable (not too many embedded skills)
- [ ] Reference routing defined in each skill's SKILL.md
- [ ] Declaration pattern documented in agent body
