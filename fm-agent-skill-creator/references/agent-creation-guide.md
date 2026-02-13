# Agent Creation Guide

How to create a Claude Code agent following framework conventions.

---

## What Is an Agent?

An agent is WHO Claude becomes. It has:
- **Identity**: name, prefix, declaration in every response
- **Tool restrictions**: frontmatter defines available tools (HARD restriction)
- **Boundaries**: write domain, role scope, blocking checks
- **File location**: `agents/<name>.md`

One agent per subprocess. Not composable.

---

## Agent File Structure

A `.md` file with two parts: frontmatter and body.

### Frontmatter

Controls structural enforcement — things Claude CANNOT override:

```yaml
---
name: agent-name
description: "What this agent does"
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
skills:
  - sf-agent-registry
  - sf-agent-specific-skill
---
```

**MANDATORY**: Every agent MUST include `sf-agent-registry` in its `skills:` field. This provides the routing table for cross-agent handoffs.

| Field | What it controls | Required? |
|---|---|---|
| `name` | Agent identifier | Yes |
| `description` | Shown in agent selection | Yes |
| `tools` | Tool whitelist — HARD restriction | Yes (or `disallowedTools`) |
| `disallowedTools` | Tool blacklist — alternative to `tools` | Alternative |
| `skills` | Skills always loaded at startup — full content injected | No |
| `model` | Which Claude model (sonnet, opus) | No |
| `permissionMode` | Permission prompting behavior | No |
| `maxTurns` | Turn limit before stopping | No |
| `mcpServers` | Available MCP servers | No |
| `hooks` | Lifecycle hooks | No |
| `memory` | Agent memory configuration | No |

**MCP access** comes from the project's `.mcp.json`, not the agent definition. Keeps agents portable.

See official docs: https://code.claude.com/docs/en/sub-agents

### Body (System Prompt)

Six required sections:

#### 1. Identity and Declaration

Who the agent is and how it identifies itself.

```markdown
You are the document-writer agent. You author and maintain all documentation.

**Declaration rule**: Every response starts with `<document-writer>: [loaded-references] ...`
```

#### 2. Blocking Check

Read project config, refuse if not configured or agent isn't active.

```markdown
Before any work:
1. Read the project's CLAUDE.md
2. Find the Agent Framework Configuration YAML block
3. Verify this agent is listed as active
4. If not configured or not active -> refuse with instructions
```

#### 3. Role Boundaries

What this agent DOES and does NOT do. Do NOT hardcode agent names — the sf-agent-registry handles routing.

```markdown
**This agent DOES:**
- Write and maintain documentation files
- Manage documentation inventory

**This agent does NOT do:**
- Write source code
- Define requirements
```

#### 4. Write Domain

Which directories and systems this agent may modify.

```markdown
**MAY write to:**
- docs/
- documentation platform (configured MCP)

**MUST NOT write to:**
- src/, tests/
- Any non-documentation directory
```

#### 5. Handoff Format

Provided by sf-agent-registry (embedded in every agent). No need to define in agent body — the registry provides the standardized handoff format and routing table.

The agent body SHOULD include a reminder to use the registry:

```markdown
**Handoff**: Use sf-agent-registry for routing. Describe WHAT needs to happen, suggest WHO from the catalog.
```

#### 6. Intake Pattern (Intake Agents Only)

Defines how the agent greets the user and sets up context. Behavior varies by invocation context.

**Applies to**: Intake agents (product-owner, solutions-architect, support-engineer, etc.)
**Does NOT apply to**: Worker agents (receive tickets, not raw requests) or utility agents (receive structured commands).

| Context | Intake Type | Behavior |
|---|---|---|
| **Vanilla** | Orient | Present structured options menu specific to this agent's domain |
| **Collab** | Orient | Same as vanilla (with mode prefix) |
| **Plan Execution** | Confirm | Confirm which ticket/work item is being picked up, then proceed |
| **Exploration** | Confirm | Confirm agent is loaded and ready to co-work |

**Orient menu** (Vanilla/Collab) — agent-specific, defined per agent:

```markdown
<agent-name>: What would you like to work on?
1. [Domain-specific option A]
2. [Domain-specific option B]
3. [Domain-specific option C]
```

**Confirm** (Plan Execution) — standardized across all agents:

```markdown
⚡ <agent-name>: Picking up #123 — "Ticket title"
Starting Phase 1...
```

**Confirm** (Exploration) — standardized across all agents:

```markdown
🔍 <agent-name>: Ready. What are we exploring?
```

**Key rules**:
- Orient menus MUST be specific to the agent's domain (not generic)
- Plan Execution MUST reference the actual ticket being worked
- Worker agents do NOT define intake — their intake is ticket validation in the workflow

---

## Tool Selection Guidance

| If the agent needs to... | Include these tools |
|---|---|
| Read code/docs | Read, Glob, Grep |
| Write/edit files | Write, Edit |
| Run commands (build, deploy, test) | Bash |
| Review only (no modifications) | Read, Glob, Grep ONLY |

**Key principle**: A code reviewer MUST NOT have Write or Edit. Different tool access = different agent.

---

## Common Agent Patterns

### Developer Agent
- Tools: Read, Write, Edit, Glob, Grep, Bash
- Skills: coding standards, framework-specific patterns
- Write domain: src/, tests/ (specific directories)

### Reviewer Agent
- Tools: Read, Glob, Grep (NO Write, Edit)
- Skills: review patterns, quality standards
- Write domain: None (read-only)

### Writer Agent
- Tools: Read, Write, Edit, Glob, Grep, Bash
- Skills: writing knowledge, platform operations
- Write domain: docs/, documentation platforms

---

## Checklist

Before finalizing an agent:
- [ ] Frontmatter has name, description, tools
- [ ] `sf-agent-registry` is in the `skills:` field
- [ ] Body has all 6 sections (identity, blocking, boundaries, write domain, handoff, intake)
- [ ] Role boundaries do NOT hardcode other agent names (registry handles routing)
- [ ] Tools match actual needs (not more, not less)
- [ ] Write domain explicitly defined
- [ ] Intake pattern defined for intake agents (orient menu + confirm behaviors)
- [ ] No hardcoded MCP servers
- [ ] Under 200 lines (target), 400 (hard limit)
- [ ] Skills in `skills:` field are ones the agent ALWAYS needs
