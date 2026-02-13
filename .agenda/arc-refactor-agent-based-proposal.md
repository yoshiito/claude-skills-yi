# Yoshi Framework — Agent-Based Architecture Proposal

**A Claude Code plugin for structurally-enforced engineering workflows.**

**Review with ✓ (agree), ✗ (disagree), or ? (discuss)**

---

## 1. Design Philosophy

The current framework enforces role boundaries via **instructions** — telling Claude "don't do X." This is inherently soft. Claude can ignore, misinterpret, or drift from instructions under context pressure.

This proposal replaces instructions with **structure**:

| Enforcement | How | Example |
|-------------|-----|---------|
| **Tool restriction** | Agent `tools:` field | Code reviewer has no Write/Edit — physically can't modify code |
| **MCP filtering** | Agent `mcpServers:` field | Only PC agent sees GitHub Projects — others can't touch tickets |
| **Slash commands** | `disable-model-invocation: true` | Modes and roles are invoked explicitly, never auto-triggered |
| **Blocking checks** | Agent reads config before work | Missing project settings → agent refuses to proceed |
| **Isolation** | Each agent is a subprocess | Agent context is bounded — no cross-contamination |

**What stays as instructions**: Orchestration logic in CLAUDE.md (mode behavior, confirmation rules, routing). These are decisions the main Claude instance must make — they can't be structural.

---

## 2. Plugin Structure

Everything ships as a single Claude Code plugin.

```
yoshi-framework/
├── .claude-plugin/
│   └── plugin.json                      # Manifest
├── agents/                              # Agent definitions (source of truth)
│   ├── project-coordinator.md
│   ├── product-owner.md
│   ├── solutions-architect.md
│   ├── support-engineer.md
│   ├── frontend-developer.md
│   ├── backend-developer.md
│   ├── code-reviewer.md
│   ├── frontend-tester.md
│   ├── backend-tester.md
│   ├── api-designer.md
│   ├── data-platform-engineer.md
│   ├── ai-integration-engineer.md
│   ├── mcp-server-developer.md
│   ├── tech-doc-writer.md
│   ├── ux-designer.md
│   └── svg-designer.md
├── skills/
│   │                                    # --- Role routing (fork to agent) ---
│   ├── po/SKILL.md                      # /yoshi-framework:po → product-owner
│   ├── sa/SKILL.md                      # /yoshi-framework:sa → solutions-architect
│   ├── se/SKILL.md                      # /yoshi-framework:se → support-engineer
│   ├── fe/SKILL.md                      # /yoshi-framework:fe → frontend-developer
│   ├── be/SKILL.md                      # /yoshi-framework:be → backend-developer
│   ├── cr/SKILL.md                      # /yoshi-framework:cr → code-reviewer
│   ├── pc/SKILL.md                      # /yoshi-framework:pc → project-coordinator
│   ├── test/SKILL.md                    # /yoshi-framework:test → tester
│   ├── docs/SKILL.md                    # /yoshi-framework:docs → tech-doc-writer
│   ├── ux/SKILL.md                      # /yoshi-framework:ux → ux-designer
│   ├── svg/SKILL.md                     # /yoshi-framework:svg → svg-designer
│   ├── api/SKILL.md                     # /yoshi-framework:api → api-designer
│   ├── data/SKILL.md                    # /yoshi-framework:data → data-platform-engineer
│   ├── ai/SKILL.md                      # /yoshi-framework:ai → ai-integration-engineer
│   ├── mcp/SKILL.md                     # /yoshi-framework:mcp → mcp-server-developer
│   │                                    # --- Mode transitions (inline) ---
│   ├── mode-collab/SKILL.md             # /yoshi-framework:mode-collab
│   ├── mode-execute/SKILL.md            # /yoshi-framework:mode-execute
│   ├── mode-explore/SKILL.md            # /yoshi-framework:mode-explore
│   ├── mode-exit/SKILL.md               # /yoshi-framework:mode-exit
│   │                                    # --- Generative templates (inline) ---
│   ├── template-bug/SKILL.md
│   ├── template-feature/SKILL.md
│   ├── template-mission/SKILL.md
│   ├── template-subtask/SKILL.md
│   │                                    # --- Embedded knowledge (not invokable) ---
│   ├── ticket-templates/SKILL.md
│   ├── definition-of-ready/SKILL.md
│   ├── definition-of-done/SKILL.md
│   ├── atomic-design/SKILL.md
│   ├── coding-standards/SKILL.md
│   └── testing-patterns/SKILL.md
├── hooks/
│   └── hooks.json
├── scripts/
│   └── install-agents.sh               # Symlink workaround for #13605
├── CLAUDE.md                            # Orchestration rules (auto-loaded)
├── README.md
└── LICENSE
```

### Plugin Manifest

```json
{
  "name": "yoshi-framework",
  "version": "1.0.0",
  "description": "Structurally-enforced engineering workflows for Claude Code",
  "author": { "name": "Yoshi" },
  "skills": "./skills/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### Symlink Workaround (Bug #13605)

Plugin subagents currently cannot access MCP servers. Until fixed, agents are symlinked to user scope where MCP works:

```bash
#!/bin/bash
# scripts/install-agents.sh
PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AGENT_DIR="$HOME/.claude/agents"
mkdir -p "$AGENT_DIR"
for agent in "$PLUGIN_DIR/agents/"*.md; do
  ln -sf "$agent" "$AGENT_DIR/$(basename "$agent")"
done
echo "Agents symlinked to ~/.claude/agents/"
```

**Cleanup**: When #13605 is resolved, delete symlinks. Agents work from plugin scope. No other changes.

---

## 3. Components

### 3A. Agents — Execution

Agents are subprocesses with restricted tool access. Each agent is a `.md` file with YAML frontmatter (tools, model, skills) and markdown body (system prompt).

**Every agent body includes:**

```markdown
[ROLE-NAME] You are the [Role Name].
EVERY response MUST start with [ROLE-NAME].

## BLOCKING: Settings Check
1. Read `.claude/config/project-settings.json`
2. If missing → STOP. Tell user to configure.
3. If this agent NOT in `roster.active` → STOP. Not authorized.
4. Proceed.
```

**Agent categories by tool access:**

| Category | Agents | Tools | MCP | Why |
|----------|--------|-------|-----|-----|
| **Gateway** | project-coordinator | Read, Write, Edit, Glob, Grep, Bash | github-projects | Only agent with ticket access |
| **Intake** | product-owner, solutions-architect, support-engineer | Read, Write, Edit, Glob, Grep | — | Define work, no execution tools needed |
| **Worker** | all developers, testers, doc-writer, designers | Read, Write, Edit, Glob, Grep, Bash | — | Build things |
| **Review** | code-reviewer | Read, Glob, Grep | — | Cannot modify code — read-only |

### 3B. Skills — Four Purposes

All skills are SKILL.md files under `skills/`. They differ in **purpose** and **frontmatter**, not mechanism.

#### Role Routing Skills

Thin wrappers that fork to an agent. User types `/yoshi-framework:po` → skill forks to `product-owner` agent.

```yaml
# skills/po/SKILL.md
---
name: po
description: "Invoke Product Owner"
context: fork
agent: product-owner
disable-model-invocation: true
---
$ARGUMENTS
```

All role routing skills follow this pattern. `context: fork` + `agent:` routes to the named agent. `disable-model-invocation: true` prevents auto-triggering.

| Skill | Routes To | Agent Category |
|-------|-----------|----------------|
| `/po` | product-owner | Intake |
| `/sa` | solutions-architect | Intake |
| `/se` | support-engineer | Intake |
| `/fe` | frontend-developer | Worker |
| `/be` | backend-developer | Worker |
| `/cr` | code-reviewer | Review |
| `/pc` | project-coordinator | Gateway |
| `/test` | frontend-tester or backend-tester | Worker |
| `/docs` | tech-doc-writer | Worker |
| `/ux` | ux-designer | Worker |
| `/svg` | svg-designer | Worker |
| `/api` | api-designer | Worker |
| `/data` | data-platform-engineer | Worker |
| `/ai` | ai-integration-engineer | Worker |
| `/mcp` | mcp-server-developer | Worker |

#### Mode Transition Skills

Change the session's operating mode. Run inline (no `context: fork`) — they inject transition logic into main Claude's context.

```yaml
# skills/mode-execute/SKILL.md
---
name: mode-execute
description: "Enter Plan Execution mode"
disable-model-invocation: true
---
## Mode Transition: Plan Execution (⚡)
1. Invoke project-coordinator agent to verify DoR
2. If DoR PASS → spawn Agent Team from plan's task list
3. Lead enters delegate mode (coordination only, no implementation)
4. If DoR FAIL → stay in 🤝 Collab, report gaps
```

| Skill | Effect | Prerequisite |
|-------|--------|-------------|
| `/mode-collab` | → 🤝 Collab | If leaving Explore → prompt to document |
| `/mode-execute` | → ⚡ Plan Execution | PC verifies DoR. Fail → stay in Collab |
| `/mode-explore` | → 🔍 Explore | None |
| `/mode-exit` | → 🤝 Collab | Same as /mode-collab |

#### Generative Template Skills

Generate pre-filled ticket content. Fork to project-coordinator agent with the template type as argument.

```yaml
# skills/template-bug/SKILL.md
---
name: template-bug
description: "Generate a bug ticket"
context: fork
agent: project-coordinator
disable-model-invocation: true
---
Generate a bug ticket using the ticket-templates knowledge. $ARGUMENTS
```

| Skill | Generates |
|-------|-----------|
| `/template-bug` | Bug ticket body |
| `/template-feature` | Feature ticket body |
| `/template-mission` | Mission (epic) ticket body |
| `/template-subtask` | Dev subtask ticket body |

#### Knowledge Skills (Embedded Only)

Domain knowledge embedded into agents via the `skills:` field in agent frontmatter. Never invoked by users or Claude directly.

```yaml
# skills/ticket-templates/SKILL.md
---
name: ticket-templates
user-invocable: false
disable-model-invocation: true
---
[Template content here]
```

Both flags set = only accessible when an agent preloads it via `skills:`.

| Skill | Embedded In |
|-------|-------------|
| ticket-templates | project-coordinator |
| definition-of-ready | project-coordinator |
| definition-of-done | project-coordinator |
| atomic-design | frontend-developer |
| coding-standards | all developers |
| testing-patterns | all testers |

---

## 4. Orchestration (CLAUDE.md)

The plugin's `CLAUDE.md` is auto-loaded and contains ONLY orchestration logic — decisions the main Claude instance makes between agent invocations.

### What goes in CLAUDE.md (~120-150 lines)

**Mode behavior** (what happens INSIDE each mode, not transitions):

| Mode | Behavior |
|------|----------|
| 🤝 **Collab** | Confirm before invoking agents. User drives. Serial agent invocation. |
| ⚡ **Plan Execution** | Agent Team spawned from plan. Lead delegates, teammates execute in parallel. |
| 🔍 **Explore** | No confirmation. Prompt to document at topic changes. Serial agent invocation. |

**Confirmation rules:**

| Context | Confirm? |
|---------|----------|
| Collab: invoking any agent | Yes — y/n |
| Collab: multiple agents | One prompt for all — y/n |
| Plan Execution: all invocations | No |
| Explore: all invocations | No |
| Mode transitions | Handled by mode skill |

**Routing rules:**
- User types `/role` → route to agent (via slash command skill)
- Ambiguous request → suggest appropriate intake role
- Out of scope → agent says so, suggests correct role

**Handoff relay:**
- Agent returns structured output (Completed / For next / Constraints)
- Main Claude passes handoff context to next agent
- In Plan Execution: follow routing table automatically

**Compaction recovery:**
- Read `.claude/config/project-settings.json` (mode, roster)
- Read current plan if in Plan Execution
- Declare: `"📚 RECOVERED — Mode: [X]. Resuming step [N]."`
- Agents are stateless — no agent recovery needed

### What does NOT go in CLAUDE.md

| Concern | Where It Lives Instead |
|---------|----------------------|
| Mode transition logic | Mode command skills |
| Role boundaries | Agent `tools:` field |
| Ticket access control | Agent `mcpServers:` field |
| Domain knowledge | Knowledge skills embedded in agents |
| Identity prefix | Agent body (system prompt) |
| Template formats | Generative template skills |

---

## 5. Configuration

### Project Settings: `.claude/config/project-settings.json`

Every project using the framework must have this file. Every agent checks for it before working.

```json
{
  "framework": {
    "version": "2.0"
  },
  "team": {
    "slug": "my-team",
    "ticketSystem": "github",
    "mainBranch": "main"
  },
  "domain": {
    "directory": "./src",
    "projectType": "fullstack"
  },
  "roster": {
    "active": [
      "product-owner",
      "solutions-architect",
      "frontend-developer",
      "code-reviewer",
      "project-coordinator"
    ]
  },
  "techStack": {
    "languages": ["typescript"],
    "frameworks": ["react", "fastapi"],
    "databases": ["postgresql"]
  }
}
```

**Blocking behavior:** Missing file or agent not in roster → agent refuses to work. This is structural — every agent's body contains the check.

---

## 6. Execution Models

Two models depending on mode:

### Collab & Explore: Serial Agent Invocation

Main Claude invokes one agent at a time via `context: fork`. Agents return structured handoff output. Main Claude relays context to the next agent.

**Agent output format** (in every agent body):
```
## Handoff
**Completed:** [what was done]
**For next:** [what's needed]
**Constraints:** [decisions/limits to respect]
```

**Flow:**
```
1. User or mode triggers agent A (via slash command)
2. Agent A does work, returns handoff output
3. Main Claude reads handoff, determines next agent
4. Main Claude invokes agent B with: "[Agent A handoff context]. Now do [task]."
5. Repeat until done
```

### Plan Execution: Agent Teams (Experimental)

Plan Execution leverages Claude Code's **Agent Teams** feature — multiple Claude Code instances coordinating via a shared task list with dependency management.

**How it works:**
```
1. User invokes /mode-execute
2. PC agent verifies DoR on the plan
3. DoR passes → lead spawns an Agent Team
4. Plan's tasks become the shared task list (with dependencies)
5. Lead enters delegate mode (coordination only, no implementation)
6. Teammates claim and execute tasks as dependencies clear
7. TaskCompleted hooks enforce quality gates
8. Lead synthesizes results when all tasks complete
```

**Plan format** (task list with dependencies):

```markdown
| Task | Agent | Description | Depends On |
|------|-------|-------------|-----------|
| 1 | product-owner | Define requirements | — |
| 2 | solutions-architect | Design architecture | 1 |
| 3 | frontend-developer | Implement UI | 2 |
| 4 | frontend-tester | Write tests | 3 |
| 5 | code-reviewer | Review code | 3 |
```

Tasks 4 and 5 can execute in **parallel** once task 3 completes — Agent Teams handles this natively via the dependency DAG.

**Key Agent Teams capabilities:**
- **Shared task list** with dependency DAG — tasks block on unresolved dependencies
- **Delegate mode** — lead restricted to coordination tools only (no coding)
- **`TaskCompleted` hook** — quality gate before a task can be marked done
- **`TeammateIdle` hook** — can send feedback to keep a teammate working
- **Self-claiming** — teammates pick up next unblocked task automatically
- **File locking** — prevents race conditions on task claiming
- **Stored locally** — `~/.claude/tasks/{team-name}/`

**Limitation**: Agent Teams is experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`). For stable fallback, Plan Execution can degrade to serial agent invocation (same as Collab mode but autonomous).

---

## 7. Enforcement Summary

| What | How | Strength |
|------|-----|----------|
| Code reviewer can't edit code | `tools: Read, Glob, Grep` (no Write/Edit) | **Hard** |
| Only PC touches tickets | `mcpServers: [github-projects]` on PC only | **Hard** (agent), Soft (main Claude) |
| Agents blocked without config | Blocking check in every agent body | **Structural** |
| Agents not in roster can't run | Roster check in every agent body | **Structural** |
| Roles invoked explicitly | `disable-model-invocation: true` on all commands | **Structural** |
| Modes invoked explicitly | `disable-model-invocation: true` on mode commands | **Structural** |
| Knowledge not directly invocable | `user-invocable: false` + `disable-model-invocation: true` | **Structural** |
| Identity prefix on every response | Agent body is system prompt | **Structural** |
| PO scope authority | PO agent has scope-related knowledge; others don't | Soft (instruction) |
| Main Claude routes through PC | CLAUDE.md instruction | Soft (instruction) |

### Soft enforcement reality

Two things remain instruction-based:

1. **Main Claude ticket routing** — Main Claude itself has access to all MCP servers globally. CLAUDE.md says "route ticket ops through PC agent" but main Claude could technically call them directly. Full fix awaits GitHub issue #6915 (agent-exclusive MCP access).

2. **PO scope authority** — "Only PO defines scope" is behavioral, not structural. Other agents could suggest scope changes. This is enforced via agent body instructions.

**Mitigation for #1**: Add hooks that block `gh issue`/`gh project` commands from non-PC contexts. This adds a hard enforcement layer at the shell level.

---

## 8. What This Eliminates

| Current Artifact | Status | Replaced By |
|-----------------|--------|-------------|
| Preamble content in SKILL.md files | Eliminated | Agent body (system prompt) |
| Mode transition logic in CLAUDE.md | Eliminated | Mode command skills |
| Boundary enforcement instructions | Mostly eliminated | Agent `tools:` field |
| PC gateway instructions | Mostly eliminated | `mcpServers:` field + hooks |
| Complex compaction recovery | Simplified | Agents are stateless, only mode/plan needs recovery |
| `_shared/references/session-modes.md` | Eliminated | Mode command skills |
| `_shared/references/utility-skills.md` | Eliminated | Agent config replaces this |
| `_shared/references/confirmation-format.md` | Eliminated | CLAUDE.md confirmation rules (5 lines) |
| Free-text mode keywords (EXECUTE, EXPLORE) | Eliminated | Slash commands (`/mode-execute`, `/mode-explore`) |

---

## 9. Open Questions

```
[ ] Plugin namespacing: `/yoshi-framework:po` is verbose. Can we alias to `/po`?
    - Depends on whether user has other plugins with conflicting names
    - Could deploy skills to user scope (`~/.claude/skills/`) instead

[ ] Plan file format: Where do plans live? What's the standard format?
    - Current: `.agenda/` directory in project
    - Needs: defined schema for task list so Agent Teams can parse it
    - Tasks need: agent assignment, description, dependencies

[ ] Agent Teams integration: How does /mode-execute translate a plan into a team?
    - Plan's task table → shared task list with dependencies
    - Each task's "Agent" column → teammate agent type to spawn
    - Lead enters delegate mode automatically
    - TaskCompleted hook: who verifies? PC agent? Code reviewer?
    - How to map our agents to teammate types?
    - Experimental flag required: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS

[ ] Agent Teams + our agents: Can teammates use our custom agent definitions?
    - Teammates are independent Claude Code sessions
    - They load CLAUDE.md and skills, but do they load agents from ~/.claude/agents/?
    - If not, teammates may not have our tool restrictions — critical gap

[ ] Test strategy: How do we validate the framework works?
    - Agent isolation: invoke each agent, verify it can't exceed its tools
    - Mode transitions: verify each mode command produces correct state
    - Handoff relay: verify context passes correctly between agents
    - Blocking check: verify agents refuse without project settings

[ ] Hook enforcement: What specific hooks block non-PC ticket access?
    - Pre-tool hook on Bash that checks for `gh issue`/`gh project` patterns
    - Only allows if current context is project-coordinator agent

[ ] Knowledge skill loading: Does `skills:` embedding work across plugin boundaries?
    - i.e., can an agent in `~/.claude/agents/` embed a skill from plugin `skills/`?
    - If not, knowledge may need to live in `~/.claude/skills/` too

[ ] Scope authority: Is PO scope authority enforceable structurally?
    - Could restrict scope-related file writes to PO agent only
    - But "scope" is conceptual, not a specific file
```

---

## 10. Implementation Plan

### Phase 1: Core Infrastructure
- [ ] Create plugin directory structure
- [ ] Write plugin manifest
- [ ] Create project-settings.json schema
- [ ] Write `install-agents.sh` symlink script

### Phase 2: Agents (3-4 priority agents first)
- [ ] project-coordinator (gateway — most complex)
- [ ] product-owner (intake — defines work)
- [ ] frontend-developer (worker — builds things)
- [ ] code-reviewer (review — validates read-only enforcement)

### Phase 3: Slash Commands
- [ ] Role routing skills (thin, mechanical)
- [ ] Mode command skills (transition logic)
- [ ] Generative template skills

### Phase 4: Knowledge Skills
- [ ] Extract domain knowledge from current SKILL.md files
- [ ] Create embedded knowledge skills with both flags set
- [ ] Wire into agent `skills:` fields

### Phase 5: CLAUDE.md
- [ ] Write orchestration rules (~120-150 lines)
- [ ] Remove everything that moved to agents/skills

### Phase 6: Hooks
- [ ] Ticket access blocking hooks
- [ ] `TaskCompleted` hook for quality gates in Agent Teams
- [ ] `TeammateIdle` hook for keeping teammates productive
- [ ] Any pre/post tool hooks needed

### Phase 7: Agent Teams Integration
- [ ] Prototype `/mode-execute` → Agent Team spawning
- [ ] Define plan format that maps to shared task list
- [ ] Test teammate agent type assignment
- [ ] Validate tool restrictions carry over to teammates
- [ ] Build serial fallback for when Agent Teams is disabled

### Phase 8: Testing
- [ ] Agent isolation tests
- [ ] Mode transition tests
- [ ] Serial handoff tests (Collab/Explore)
- [ ] Agent Team execution tests (Plan Execution)
- [ ] Blocking check tests
- [ ] End-to-end workflow test
