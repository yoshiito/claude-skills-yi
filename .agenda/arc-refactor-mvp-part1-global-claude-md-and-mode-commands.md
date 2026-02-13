# MVP Part 1: Framework Foundation — Specification

**Scope**: Global CLAUDE.md + Project CLAUDE.md template + Mode command skills + State management + PreCompact hook
**Plugin name**: `yoshi-agent-framework`
**Target repo**: `/Users/yoshitakaito/Documents/GitHub/yi-agent-framework/`

---

## Glossary

These terms are used throughout this document. Read this section first.

| Term | Meaning |
|------|---------|
| **Agent** | A Claude Code agent file (`.md`) that gives Claude a specific role (e.g., backend-developer, product-owner). Each agent has its own identity, tools, and boundaries. |
| **Skill** | A reusable piece of knowledge or a command that can be loaded into an agent. Skills don't have their own identity — they add capabilities to agents. |
| **Global CLAUDE.md** | A file at `~/.claude/CLAUDE.md` that Claude reads on every session. It contains rules that apply to ALL projects. Think of it as the "application code" — the framework's behavior rules. |
| **Project CLAUDE.md** | A file at `<project>/CLAUDE.md` that Claude reads when working on a specific project. It contains project-specific configuration. Think of it as "environment variables" — values the framework reads to know how to behave on this project. |
| **Mode** | The current operating state of the framework. There are 3 modes (Collab, Execute, Explore) that change how agents interact with the user. |
| **Plugin** | A Claude Code plugin is a package that bundles agents, skills, and hooks into a single installable unit. |
| **Hook** | A shell command that Claude Code runs automatically when certain events happen (e.g., before context compaction). Defined in `hooks.json`. |
| **Compaction** | When a Claude Code conversation gets too long, Claude automatically summarizes the earlier parts to free up memory. This is called compaction. After compaction, anything that was only in the conversation (not in files) is lost. |
| **Task dependency** | When task B cannot start until task A is finished. Task B "depends on" task A. Task B is "blocked" until task A is complete. A task with no unfinished dependencies is "unblocked" and ready to work on. |
| **Agent Teams** | A Claude Code feature (not yet widely available) where multiple agents work in parallel. One agent acts as coordinator (assigns tasks), and other agents claim and execute tasks independently. |
| **Frontmatter** | YAML metadata at the top of a SKILL.md file (between `---` markers). Controls behavior like which tools the skill can use and whether Claude can auto-invoke it. |
| **Product Owner (PO)** | The agent responsible for defining what to build and why. Makes all scope decisions. |
| **Solutions Architect (SA)** | The agent responsible for system design and architecture decisions. |
| **Support Engineer (SE)** | The agent responsible for error triage and incident investigation. |
| **Project Coordinator (PC)** | The agent responsible for ticket management and quality gates. |
| **Definition of Ready (DoR)** | A checklist that must pass before work can begin on a ticket. Verified by the Project Coordinator. |

---

## What This Plugin Does

This plugin gives Claude Code a structured way to work on engineering projects using specialized agents (roles). Instead of Claude doing everything as one generalist, the framework assigns specific roles to specific agents, each with their own boundaries, tools, and knowledge.

The framework enforces rules through a 6-layer architecture. Each layer adds constraints:

| Layer | What it does | Where the files live |
|-------|-------------|---------------------|
| **Hook** | Runs shell commands on events (e.g., save state before compaction) | `hooks/` |
| **Agent frontmatter** | Restricts which tools an agent can use | `agents/*.md` (future MVP) |
| **Agent body** | Defines who the agent IS — its identity, role, and blocking checks | `agents/*.md` (future MVP) |
| **Skill** | Adds knowledge or transition commands to agents | `skills/*/SKILL.md` |
| **Project CLAUDE.md** | Project-specific config: which agents are active, who owns what | `<project>/CLAUDE.md` |
| **Global CLAUDE.md** | Framework-wide rules that ALL agents must follow on ALL projects | `~/.claude/CLAUDE.md` |

**This spec covers**: Global CLAUDE.md, Project CLAUDE.md template, Mode command skills, and the PreCompact hook.

**NOT in scope**: Agent definitions, domain knowledge skills, or role routing.

---

## Deliverable 1: Global CLAUDE.md

**File**: `boilerplate-claude-md/global-claude-md.md`
**Deploys to**: `~/.claude/CLAUDE.md`
**Target size**: ~200-230 lines
**Tone**: Every rule must use "MUST", not "should" or "consider". This file is enforcement, not suggestions.

The global CLAUDE.md contains the rules that all agents follow. It does NOT contain agent identities, project config, or transition procedures — those live elsewhere (see "What is NOT in Global CLAUDE.md" at the end of this deliverable).

### Section: Activation

The framework is OFF by default. It only activates when a project has been fully configured. Configuration lives in two places:

**Project CLAUDE.md** — human-readable rules and instructions:
- Project-Specific Rules (additional rules agents must follow on this project — can be empty, but section must exist)

**`.claude/config/` files** — structured data the framework reads programmatically:
- Active Agents — which agents are authorized on this project
- Team Context — team name, ticket system, main branch
- Domain Ownership — which agent owns which directories

ALL of the above are **blocking conditions**. If any is missing, the framework does not activate and Claude responds normally.

**What is NOT a blocking condition** — these are loaded separately:
- **Tech Stack and Conventions** — auto-detected by LSP when agents open relevant files, or declared explicitly in project config when auto-detection isn't possible (e.g., `atomic-design` for React projects that use that pattern)
- **Knowledge skills** — loaded via three mechanisms (always embedded, LSP auto-loaded, or explicitly declared in project config). See the Skill Survival Map for which skills use which loading mode.

If a user invokes a framework command on an unconfigured project, respond:

    This project is not configured for the framework. Run /mode-project-initialization to set up project configuration.

The `/mode-project-initialization` skill (Deliverable 3) walks the user through creating this configuration.

### Section: Mental Model

**Purpose**: Default Claude behavior is not usable for structured work requiring expertise — it cuts corners, ignores boundaries, and produces unpredictable results. This framework exists so that **the right expertise handles the right work**. Each agent carries specific knowledge and rigor for its domain. When agents respect their boundaries, work gets done correctly by the agent best equipped to do it.

This section must override Claude's natural instinct to finish work as fast as possible: **being helpful means being predictable**, not being fast.

Must establish 4 principles:

1. **Compliance IS helpfulness** — the framework's value is that each agent brings the right expertise to the right work. Following your boundaries ensures that.
2. **Refuse work outside your boundaries** — if the work belongs to a different agent, tell the user (or the agent that assigned the work) to invoke the appropriate agent instead. Do not do it yourself.
3. **Resist the efficiency trap** — "I can do this faster myself" ignores the expertise embedded in the correct agent's role. Work done without that rigor almost always needs to be redone, costing the user time and money.
4. **Ask when uncertain** — if rules seem to conflict, ask the user


Must include a **pre-action checklist** that agents run before doing any work:
- Have I checked what my agent is allowed to do?
- Is this action in my authorized list?
- Is this action NOT in my prohibitions?
- Am I listed as an active agent on this project? (check project CLAUDE.md)
- Am I allowed to write to this directory? (check Domain Ownership table in project CLAUDE.md)
- If I'm unsure about any of the above, have I asked the user?

### Section: Session Modes Overview

**Purpose**: Define the 3 modes and how they differ.

The framework operates in one of 3 modes at all times. The current mode is saved to a file (`.claude/state/mode.json`) so it persists across conversations. Users switch modes using slash commands: `/mode-collab`, `/mode-execute`, `/mode-explore`, `/mode-exit`.

Must include a comparison table. The real differences between modes:

| What differs | 🤝 Collab (default) | ⚡ Execute | 🔍 Explore |
|---|---|---|---|
| **Who picks the next agent?** | User tells Claude which agent to use | The plan determines which agent runs next | User tells Claude which agent to use |
| **Does the user confirm before an agent runs?** | Yes — strict y/n prompt | No — agents start immediately | No — agents start immediately |
| **What guides the work?** | Conversation with user | A pre-defined plan, followed exactly as written | Free experimentation |
| **When does documentation happen?** | As work progresses | As work progresses | User is prompted to document at topic changes and before exiting |
| **What happens after an agent finishes?** | Wait for user's next instruction | Automatically pick up the next available task from the plan | Wait for user's next instruction |

Must state: **before every response**, Claude must check what mode is active and follow that mode's rules.

### Section: Collab Mode 🤝 (Default)

**Purpose**: Interactive collaboration. User controls which agents run and when.

Required rules:
1. Before running any agent, Claude MUST ask the user for confirmation
2. Single agent confirmation format: `🤝 Invoking <AGENT>. (y/n)`
3. Multiple agents at once — ONE prompt for ALL: `🤝 Invoking <AGENT1+AGENT2>. (y/n)`
4. `y` means proceed. `n` means cancel.
5. Within a single user request, agents CAN chain — when agent A finishes, it can pass its output to agent B without going back to the user. But once the chain completes, wait for the user before doing anything else.
6. One step at a time — don't run ahead. Complete the current task, return results, then wait.

When an agent receives a request that's outside its role:

    <AGENT> This is outside my boundaries. Try invoking [suggested agent] for this.

### Section: Execute Mode ⚡

**Purpose**: Run through a pre-defined plan autonomously. The plan is the single source of truth — agents follow it exactly.

**How to enter**: User types `/mode-execute`. The Project Coordinator (PC) agent checks the Definition of Ready (DoR). If all checks pass, enter Execute mode. If any check fails, stay in Collab mode and report which checks failed.

**When entering Execute mode, announce** (MANDATORY):

    ⚡ Execute mode active.
    Plan: [name or reference to the plan].
    Status: [N of M tasks complete]. Next: [name of the next task to work on].

Required rules:
1. **Follow the plan exactly** — do what the plan AS-IS. Do not deviate, improvise, reinterpret, summarize, or skip steps. If it's not in the plan, don't do it.
2. **Task dependencies matter** — tasks in a plan can depend on other tasks. A dependent task can only start when the task it depends on is **fully complete** — meaning ALL phases of that task are done (development, code review, testing, merge), not just one agent's part. For example: if ticket Y depends on ticket X, a developer finishing their code on ticket X does NOT unblock ticket Y. Ticket X must pass code review, pass testing, and be merged before ticket Y can start. Starting ticket Y before ticket X is fully complete risks all work on Y being wasted if X fails review or testing. When multiple tasks are fully unblocked, they can run at the same time using Agent Teams (see glossary). If Agent Teams is not available, run unblocked tasks one at a time in the order they appear in the plan.
3. **No confirmation needed** — the agent assigned to a task in the plan starts working immediately without asking the user.
4. **Announce each task before starting**: `⚡ Executing task [N]: [what the task is]. Agent: [which agent is doing it]. Skills: [loaded skills].`
5. **After finishing a task**, the agent reports what it did using the handoff format (see Handoff Relay section), then moves to the next unblocked task.
6. **No scope changes during execution** — if the plan needs to change, the agent exits to Collab mode and explains why. The user resolves the issue in Collab mode, then the user re-enters Execute mode by typing `/mode-execute` when the plan is ready again. The agent does NOT re-enter Execute mode on its own.
7. **Only the user can exit Execute mode.** Agents cannot decide to stop on their own.
8. **Explain every pause** — Execute mode's goal is autonomous execution. If an agent stops for any reason, it must say WHY it stopped and what it needs from the user to continue. Silent pauses are not acceptable.

**If a task cannot be completed as written** — do NOT make something up. Stop and say:

    ⚡ Task [N] blocked: [explain why].
    The plan requires adjustment. Exiting to Collab for resolution.

**Agent Teams design note** (this is a future capability, document as a stub for now): Execute mode is designed to work with Claude Code's Agent Teams feature. In that setup, one agent acts as coordinator (it assigns tasks but does no implementation itself), and other agents claim tasks from a shared list as dependencies clear. When Agent Teams is not available, the system falls back to running agents one at a time.

### Section: Explore Mode 🔍

**Purpose**: Try things out quickly. Experiment freely, document later.

**How to enter**: User types `/mode-explore`. No prerequisites — enter immediately.

Required rules:
1. User tells Claude which agents to use (same as Collab)
2. Agents start working immediately — no confirmation prompt (so the user can iterate fast)
3. Keep going until the user exits

**Documentation prompting** (MANDATORY — this fires repeatedly, not just at exit):

When the user shifts to a different topic during exploration (e.g., moves from experimenting with authentication to experimenting with database schemas), Claude prompts:

    🔍 Document [topic they were just working on] findings? (y/n)

- `y` → run the tech-doc-writer agent to capture what was learned, then continue exploring the new topic
- `n` → continue without documenting

**Exit documentation check** (MANDATORY — fires when leaving Explore mode for ANY reason):

Before switching to another mode, Claude prompts one final time:

    🔍 Document current topic findings? (y/n)

- `y` → document first, then switch modes
- `n` → switch modes without documenting

### Section: Mode Transitions

- Users cannot go directly from Execute to Explore or vice versa. They must return to Collab first.
- Only the user can exit a mode — agents cannot change the mode on their own.
- `/mode-exit` does the same thing as `/mode-collab` — it's just an easier-to-remember alias.

### Section: Confirmation Format

Every agent interaction is prefixed with the current mode emoji (🤝, ⚡, or 🔍). Confirmations are no exception.

Confirmation only happens in Collab mode, so the prefix is always 🤝:

    🤝 Invoking <AGENT>. (y/n)

When invoking multiple agents at once — ONE prompt, not one per agent:

    🤝 Invoking <AGENT1+AGENT2>. (y/n)

How to handle responses:

| What the user types | What to do |
|---------------------|-----------|
| `y` or `Y` | Proceed |
| `n` or `N` | Cancel |
| Anything else | Show the same prompt again. Don't explain — just re-prompt. |

Execute and Explore modes skip confirmation entirely — agents start immediately.

### Section: Agent Declaration

**Purpose**: Every agent must identify itself in every message so the user always knows which agent is speaking.

The rule (framework-level): All agents MUST start every response with their identity.

The format (agent-level): Each agent's own definition file specifies what the declaration looks like. The standard format is:

    <agent-name>: [skill-1, skill-2] <response content>

Example: `<frontend-developer>: [atomic-design, coding-standards] Building the sidebar component...`

This spec only requires that agents declare themselves. The exact format is defined per-agent (in a future MVP), not here.

### Section: Handoff Relay

**Purpose**: When an agent finishes its work, it must leave a structured summary so the next agent knows what happened.

Required format:

    ## Handoff
    **Completed:** [what was done]
    **For next:** [what the next agent needs to do]
    **Constraints:** [decisions made, limits to respect, or dependencies to be aware of]

How handoffs flow between agents:
- In **Collab** and **Explore** modes, agents run one at a time. The Claude Code session reads the handoff output and passes it as context when starting the next agent.
- In **Execute** mode (with Agent Teams), handoffs are coordinated through a shared task list that all agents can read.

### Section: Relay Transparency

**Purpose**: When the main Claude session relays a sub-agent's output to the user, it may summarize or rephrase. That's acceptable — but the summary MUST preserve three things so the user can verify the right expertise did the right work:

1. **WHO** — which agent performed the work (full declaration: agent name + loaded skills)
2. **WHAT** — what was done (the substance of the output)
3. **HOW** — which skills/expertise were applied

Summarization is fine. Stripping the agent identity is not. The user needs to see that the backend-developer with coding-standards loaded wrote the API endpoint — not just "the endpoint was created."

Example of acceptable relay:

    <backend-developer>: [fastapi-patterns, coding-standards] implemented the /users endpoint
    with input validation and error handling per the technical spec.

Example of unacceptable relay:

    I've created the /users endpoint for you.

**Known limitation**: This is instruction-based enforcement. There is no Claude Code setting to force verbatim relay of sub-agent output ([#9512](https://github.com/anthropics/claude-code/issues/9512) — closed, not planned). Agent Teams partially solves this because users can view teammate output directly. For now, this rule is the best available approach.

### Section: Agent Boundary Enforcement

Required rules:
1. **Respect your boundaries** — only do things your agent is authorized to do
2. **Refuse work outside your boundaries** — say "this is outside my boundaries" and suggest which agent the user should invoke instead
3. **No boundary creep** — do exactly what was asked, nothing more
4. **Check domain ownership before writing** — before writing to any file or directory, check `.claude/config/domain-ownership.json` to confirm your agent owns that domain

When an agent receives work outside its boundaries:

    <AGENT> This request is outside my boundaries.
    For [what the user asked for], try invoking [suggested agent].

### Section: Scope Decision Authority

**Purpose**: Only the Product Owner (PO) agent decides what is in scope and what is not. All other agents defer to the PO for scope decisions.

Must include:

| Decision | Who decides |
|----------|-----------|
| What's MVP vs. future work | Product Owner only |
| What features to cut | Product Owner only |
| What to simplify | Product Owner only |
| Priority and sequencing | Product Owner only |

Other agents must respond: "Scope decisions require the Product Owner (/po)."

Agents MUST NOT:
- Suggest simplifications like "for MVP, let's just..." without PO approval
- Decide what's "essential" vs. "nice to have"
- Cut features on their own
- Redefine acceptance criteria to reduce scope

When an agent thinks scope should change:

    <AGENT> This may benefit from scope adjustment.
    Observation: [what the agent noticed]
    Suggestion: [the agent's idea]
    This is a scope decision — please invoke the Product Owner (/po) for approval.

**NEVER implement a reduced scope without explicit Product Owner approval.**

### Section: Quality Standards (DoR, DoD, Ticket Structure)

The framework enforces quality standards on tickets. The details of these standards — what a ticket must contain, what "ready" means, what "done" means — are defined in the Project Coordinator (PC) agent's skills (a future MVP deliverable). The Global CLAUDE.md only needs to establish that these standards exist and must be followed.

Required rules:
1. **Tickets must meet quality standards before work begins** — the PC agent verifies a Definition of Ready (DoR) checklist. If any check fails, work cannot start. This is what gates entry to Execute mode.
2. **Tickets must meet quality standards before marking complete** — the PC agent verifies a Definition of Done (DoD) checklist. If any check fails, work is not done.
3. **Ticket creators must make tickets self-contained** — every ticket includes ALL information the executor needs. The executor should not need to read external documents or conversation history.
4. **Ticket executors must follow tickets as written** — do what the ticket says. Don't add work that isn't listed. If something is unclear, ask the ticket creator — don't guess.

The specific checklists and templates are NOT defined here. They belong to the PC agent's skills.

### Section: Universal Agent Rules

These rules apply to every agent, in every response, in every mode. No exceptions.

1. **Identify yourself** — start every response with your agent declaration (see Agent Declaration section)
2. **Show the current mode** — prefix every response with the mode emoji (🤝, ⚡, or 🔍) before your agent declaration
3. **Check that the project is configured** — before doing any real work, verify that all blocking config exists: `.claude/config/active-agents.json`, `.claude/config/team-context.json`, `.claude/config/domain-ownership.json`, and a Project-Specific Rules section in the project's CLAUDE.md. If any is missing, refuse to work and tell the user to run `/mode-project-initialization`.
4. **Check domain ownership before writing** — before creating or modifying files, check `.claude/config/domain-ownership.json`. Only write to directories your agent owns.
5. **Check you're on the active list** — only respond as an agent if you're listed in the project's Active Agents section. If you're not listed, say so and stop.
6. **Respect task dependencies** — don't start work on a task that depends on an unfinished task.
7. **Store documentation in the ticket system** — when a ticket system is configured (GitHub or Linear), store documentation there. Only use local files when the ticket system is set to "none."
8. **Work on the current branch** — the user creates and manages branches. Agents only commit to whatever branch is currently checked out.

### Section: Compaction Recovery

Claude Code automatically summarizes old conversation history to free up memory (this is called "compaction"). After compaction, anything that was only in the conversation is lost. This section tells agents how to recover.

Steps after compaction:
1. Read the state file at `.claude/state/mode.json` to find out what mode was active
2. Re-read any skills listed in the state file's `loaded_skills` field
3. If Execute mode was active, re-read the plan and figure out which tasks are done and which is next
4. Announce recovery: `📚 RECOVERED — Mode: [🤝/⚡/🔍]. Resuming.`

The PreCompact hook (Deliverable 4) ensures the state file is up to date before compaction happens.

### What is NOT in Global CLAUDE.md

These things are intentionally excluded. They belong elsewhere.

| Thing | Where it belongs | Reason |
|-------|-----------------|--------|
| Agent declaration FORMAT (e.g., `<name>: [skills]`) | Each agent's own definition file | The format is part of the agent's identity, not a framework rule |
| Agent blocking checks (tool restrictions) | Agent frontmatter (future) | Enforced structurally by Claude Code, not by instructions |
| Domain knowledge (e.g., React patterns, pytest patterns) | Knowledge skills loaded into agents | Reusable and composable — doesn't belong in a global file |
| Project config (which agents are active, domain ownership) | `.claude/config/` JSON files + Project CLAUDE.md | Different per project |
| Mode transition steps (what happens when you type /mode-execute) | Mode command skills | These run once during transition. Global CLAUDE.md contains the ongoing rules for each mode. |
| Ticket templates and formats | Project Coordinator skills | That's PC's domain |
| Labels like "intake role" or "worker role" | Not needed anywhere | Agents know their own boundaries from their definition. We don't need to categorize them. |

---

## Deliverable 2: Project Configuration Templates

Project configuration lives in two places, each with a different purpose:

| Where | What goes here | Why |
|-------|---------------|-----|
| **Project CLAUDE.md** (`<project>/CLAUDE.md`) | Human-readable rules and instructions | Claude reads this as natural language instructions — auto-loaded, always in context |
| **`.claude/config/` files** | Structured data (JSON) the framework reads programmatically | Agents and skills parse these to make decisions |

Both are **blocking conditions** for framework activation (see Activation section in Deliverable 1). The `/mode-project-initialization` skill (Deliverable 3) walks the user through creating all of these.

### Part A: Project CLAUDE.md Template

**File**: `boilerplate-claude-md/project-claude-md.md`
**Deploys to**: `<project>/CLAUDE.md`
**Target size**: ~30-50 lines

Must include a note at the top: "Framework rules live in `~/.claude/CLAUDE.md`. This file is project-specific rules and instructions only. Structured configuration lives in `.claude/config/`."

#### Project-Specific Rules

A section where the team writes any additional rules agents must follow on THIS project that aren't covered by the global CLAUDE.md. This section CAN be empty, but it MUST exist (its presence signals the project has been initialized).

Examples of what goes here:
- "All API responses must use camelCase keys"
- "Never import from the legacy/ directory — it's being deprecated"
- "Database migrations must be reviewed by the SA before merging"

The template provides an empty section with example comments showing the kinds of rules teams typically add.

**Why Project CLAUDE.md instead of a config file**: Project CLAUDE.md is auto-loaded by Claude into every session for free. Project-specific rules are natural language instructions that agents should always follow — putting them in CLAUDE.md means they're always in context without any agent needing to explicitly read a file.

### Part B: Structured Config Files

**Directory**: `<project>/.claude/config/`

These are JSON files the framework reads programmatically. The `/mode-project-initialization` skill generates them.

#### `active-agents.json`

A list of every agent authorized to work on this project.
- Each entry has: agent name, slash command (e.g., `product-owner` → `/po`)
- The global CLAUDE.md's rule 5 ("check you're on the active list") reads THIS file. If an agent isn't listed here, it must refuse to work.
- The `/mode-project-initialization` skill presents ALL available agents and the user selects which ones to activate.

#### `team-context.json`

| Key | What to fill in |
|-----|----------------|
| Team | The team's name or slug |
| Ticket System | `github`, `linear`, or `none` — determines where documentation is stored |
| Main Branch | The primary branch name (usually `main`) |

#### `domain-ownership.json`

A mapping of: Domain name → Directory path → Which agent owns it.
- The global CLAUDE.md's rule 4 ("check domain ownership before writing") reads THIS file.
- Example entries: Frontend → `./src/components` → frontend-developer, Backend → `./src/api` → backend-developer, etc.

### What is NOT in project configuration (loaded separately)

These are loaded via other mechanisms, not as blocking project config:

| What | How it loads | Example |
|------|-------------|---------|
| **Tech Stack knowledge** | LSP auto-detection — agents detect languages/frameworks from files open in the editor | Opening `.py` files loads `fastapi-patterns` |
| **Convention skills** | Explicitly declared in `active-agents.json` per-agent, or LSP auto-loaded | `atomic-design` declared for frontend-developer |
| **Domain knowledge** | Always embedded in the agent, or LSP auto-loaded | `coding-standards` is always embedded in all dev agents |

---

## Deliverable 3: Mode Command Skills

There are 5 command skills. One handles project setup (`/mode-project-initialization`). The other four handle mode transitions (`/mode-collab`, `/mode-execute`, `/mode-explore`, `/mode-exit`).

The mode transition commands do NOT contain the rules for how to behave inside a mode — those rules live in the global CLAUDE.md. Think of it this way: the command is the **door** (you walk through it once), and the global CLAUDE.md is the **room** (you're in it the whole time).

All 5 skills share these frontmatter settings:
- `disable-model-invocation: true` — Claude cannot auto-run these. The user must explicitly type the slash command.
- `allowed-tools` — each skill lists only the tools it needs

### `/mode-project-initialization` — One-Time Project Setup

**File**: `skills/mode-project-initialization/SKILL.md`
**Allowed tools**: `Read`, `Write`, `Glob`
**Purpose**: This command sets up a project to use the framework. It is run ONCE per project, not on every session. It creates all the configuration files that the framework requires as blocking conditions (see Activation section in Deliverable 1). After this command completes, the project is ready to use modes and agents.

What this command does, step by step:
1. Check if configuration already exists. Read `.claude/config/active-agents.json` — if it exists, tell the user: `Project already initialized. Configuration found at .claude/config/. To reinitialize, delete .claude/config/ and run this command again.`
2. **Collect Team Context** — ask the user for: team name, ticket system (`github`, `linear`, or `none`), and main branch name. Write to `.claude/config/team-context.json`.
3. **Collect Active Agents** — present the full list of available agents with descriptions. The user selects which ones to activate for this project. Write to `.claude/config/active-agents.json`.
4. **Collect Domain Ownership** — scan the project directory structure (using `Glob`) to understand what directories exist. Ask the user to map directories to agents. Write to `.claude/config/domain-ownership.json`.
5. **Create Project CLAUDE.md** — if `CLAUDE.md` doesn't exist in the project root, create it from the template (Deliverable 2, Part A) with an empty Project-Specific Rules section. If it already exists, check for a Project-Specific Rules section — if missing, append it.
6. **Create state directory** — create `.claude/state/` with a default `mode.json` (mode: `"collab"`, empty loaded_skills).
7. **Announce completion**:

        Project initialized.
        - Active agents: [list]
        - Ticket system: [github/linear/none]
        - Domain ownership: [summary]
        - Mode: Collab (default)

        You can now use /mode-collab, /mode-execute, and /mode-explore.

### `/mode-collab` — Return to Collab Mode

**File**: `skills/mode-collab/SKILL.md`
**Allowed tools**: `Read`, `Write`

What this command does, step by step:
1. **Check project initialization** — verify all blocking config exists: `.claude/config/` files (`active-agents.json`, `team-context.json`, `domain-ownership.json`) and a Project-Specific Rules section in the project's CLAUDE.md. If ANY is missing: **STOP** and say `This project is not configured for the framework. Run /mode-project-initialization to set up project configuration.`
2. Read the state file (`.claude/state/mode.json`) to check what mode is currently active
3. If currently in Explore mode: before switching, ask `🔍 Document current topic findings? (y/n)`. On `y`, run the tech-doc-writer agent to capture findings, then continue. On `n`, continue. On anything else, ask again.
4. If NOT in Explore mode: skip the documentation prompt
5. Update the state file: set `mode` to `"collab"`, set `transitioned_at` to the current timestamp, clear `loaded_skills` to an empty list
6. Announce: `🤝 Collab mode active. Confirmation required for agent invocation.`

### `/mode-execute` — Enter Execute Mode

**File**: `skills/mode-execute/SKILL.md`
**Allowed tools**: `Read`, `Write`, `Task`

What this command does, step by step:
1. **Check project initialization** — verify all blocking config exists: `.claude/config/` files (`active-agents.json`, `team-context.json`, `domain-ownership.json`) and a Project-Specific Rules section in the project's CLAUDE.md. If ANY is missing: **STOP** and say `This project is not configured for the framework. Run /mode-project-initialization to set up project configuration.`
2. Read the state file to check the current mode
3. If currently in Explore mode: **STOP**. Cannot go directly from Explore to Execute. Tell the user: `Cannot transition directly from Explore to Execute. Use /mode-collab first.`
4. Run the Definition of Ready (DoR) check. **MVP stub**: since the Project Coordinator agent doesn't exist yet, log "DoR check skipped — PC agent not yet built" and continue. When the PC agent is built later, this step should invoke the PC to run its DoR checklist. If any check fails, stay in Collab mode and report what's missing.
5. Update the state file: set `mode` to `"execute"`
6. Find the plan. Look for it in the conversation context, ticket system, or plan files. The plan must have a list of tasks with dependencies between them. If no plan is found: **STOP** and say `⚡ Cannot enter Execute mode. No plan found. Define a plan in Collab mode first.`
7. Announce entry (mandatory format from the Execute Mode section of global CLAUDE.md), then start executing the first task that has no unfinished dependencies

### `/mode-explore` — Enter Explore Mode

**File**: `skills/mode-explore/SKILL.md`
**Allowed tools**: `Read`, `Write`

What this command does, step by step:
1. **Check project initialization** — verify all blocking config exists: `.claude/config/` files (`active-agents.json`, `team-context.json`, `domain-ownership.json`) and a Project-Specific Rules section in the project's CLAUDE.md. If ANY is missing: **STOP** and say `This project is not configured for the framework. Run /mode-project-initialization to set up project configuration.`
2. Read the state file to check the current mode
3. If currently in Execute mode: **STOP**. Cannot go directly from Execute to Explore. Tell the user: `Cannot transition directly from Execute to Explore. Use /mode-collab first.`
4. Update the state file: set `mode` to `"explore"`
5. Announce: `🔍 Explore mode active. No confirmation required. Documentation will be prompted at topic changes and before exiting.`

### `/mode-exit` — Exit Current Mode

**File**: `skills/mode-exit/SKILL.md`
**Allowed tools**: `Read`, `Write`

This is just an alias for `/mode-collab`. It runs the exact same steps (including the initialization check). It exists because `/mode-exit` is easier to remember than `/mode-collab` when you just want to "stop" the current mode.

---

## Deliverable 4: State Management + PreCompact Hook

### State File

**Path**: `.claude/state/mode.json` (inside the user's project directory)

This file tracks what mode is active. Mode commands write to it; agents and recovery logic read from it.

| Field | Type | What writes it |
|-------|------|---------------|
| `mode` | `"collab"`, `"execute"`, or `"explore"` | Mode command skills |
| `transitioned_at` | ISO 8601 timestamp (e.g., `"2026-02-11T10:00:00Z"`) | Mode command skills |
| `loaded_skills` | Array of skill name strings (e.g., `["coding-standards", "atomic-design"]`) | Agents, when they load knowledge skills |

If the file doesn't exist, the framework treats the current mode as `collab` with no loaded skills.

### hooks.json

**File**: `hooks/hooks.json`

This file tells Claude Code which hooks to run and when. It must define one hook:
- **Event**: `PreCompact` — fires right before Claude compacts (summarizes) the conversation
- **Command**: `node hooks/pre-compact-backup.mjs`
- **Matcher**: empty (fires on all compaction events, not filtered)

### pre-compact-backup.mjs

**File**: `hooks/pre-compact-backup.mjs`

This script runs right before compaction to make sure the state file is saved to disk. Without this, the current mode would be lost when compaction erases conversation history.

What the script must do:
- If `.claude/state/mode.json` exists: read it, add a `last_backup` timestamp, write it back
- If the file doesn't exist: create it with default values (`mode: "collab"`, empty skills, current timestamp)
- Log a confirmation message to stderr (e.g., `[PreCompact] State backed up`)
- If anything goes wrong: log the error to stderr but don't crash

### Why Both an Instruction AND a Hook? (Design Rationale)

Compaction is destructive — it erases conversation context. We need the mode state to survive.

| What we tried | What actually happens |
|--------------|----------------------|
| Rely on global CLAUDE.md instructions surviving | Known bug ([#19471](https://github.com/anthropics/claude-code/issues/19471)) — CLAUDE.md instructions are sometimes ignored after compaction |
| Rely on conversation memory | Lost — that's the whole point of compaction |

So we use both approaches:
1. **Instruction in global CLAUDE.md** (free, best-effort) — tells Claude to read the state file after compaction. Works most of the time.
2. **PreCompact hook** (guaranteed, structural) — saves state to disk before compaction happens. Even if Claude forgets the instruction, the state file exists on disk.

---

## Deliverable 5: Plugin Manifest

**File**: `.claude-plugin/plugin.json`

This file tells Claude Code what the plugin contains and where to find things.

Required fields:
- `name`: `yoshi-agent-framework`
- `version`: `0.1.0`
- `description`: Structurally-enforced engineering workflows for Claude Code
- `author.name`: Yoshitaka Ito
- `license`: MIT
- `skills`: `./skills/` — tells Claude Code where to find skill definitions
- `hooks`: `./hooks/hooks.json` — tells Claude Code where to find hook definitions

Note: `agents` and `mcpServers` fields will be added in future MVPs when agents and MCP servers are built.

---

## Expected Repo Structure

```
yi-agent-framework/
├── .claude-plugin/
│   └── plugin.json
├── boilerplate-claude-md/
│   ├── global-claude-md.md
│   └── project-claude-md.md
├── skills/
│   ├── mode-project-initialization/
│   │   └── SKILL.md
│   ├── mode-collab/
│   │   └── SKILL.md
│   ├── mode-execute/
│   │   └── SKILL.md
│   ├── mode-explore/
│   │   └── SKILL.md
│   └── mode-exit/
│       └── SKILL.md
├── hooks/
│   ├── hooks.json
│   └── pre-compact-backup.mjs
├── agents/                     # Empty for now — agent definitions come in a future MVP
│   └── .gitkeep
├── scripts/                    # Empty for now
│   └── .gitkeep
├── LICENSE
└── README.md
```

---

## Acceptance Criteria

The implementation must satisfy all of the following. Check each item when complete.

### Execute Mode
- [ ] Tasks run based on dependencies, not one-at-a-time in a fixed order. When multiple tasks are ready, they can run in parallel (Agent Teams) or one at a time (fallback).
- [ ] The plan is followed exactly as written — no deviation, improvisation, or skipping
- [ ] Agent announces on entry (plan name, progress, next task) AND before each task (task number, description, agent)
- [ ] Agent Teams design is documented as a future stub with one-at-a-time fallback for now
- [ ] When a task can't be completed, agent stops and reports the blocker instead of improvising
- [ ] Only the user can exit Execute mode
- [ ] When Agent Teams is unavailable, tasks run one at a time in plan order

### Explore Mode
- [ ] Documentation prompt fires repeatedly at topic changes during exploration (not just when exiting)
- [ ] The framework (Claude itself, not a PM agent) handles the documentation prompting

### Mode Emojis
- [ ] Every agent response starts with the current mode emoji: 🤝 (Collab), ⚡ (Execute), or 🔍 (Explore)

### Agent Declaration
- [ ] Global CLAUDE.md requires all agents to declare themselves in every response
- [ ] Declaration format (`<agent-name>: [skills]`) is referenced, with a note that each agent's definition specifies the exact format

### Handoff Relay
- [ ] Three-part handoff format: Completed / For next / Constraints
- [ ] Document how handoffs flow: one-at-a-time with Claude relaying context (Collab/Explore) vs. shared task list (Execute/Agent Teams)

### Confirmation Format
- [ ] Confirmations include the mode emoji: `🤝 Invoking <AGENT>. (y/n)`

### Routing
- [ ] Global CLAUDE.md does NOT label agents as "intake", "worker", or "utility" — those categories aren't needed because each agent knows its own boundaries
- [ ] Out-of-boundary handling is simply: "say it's outside your boundaries and suggest another agent"

### Project Configuration
- [ ] Before doing work, agents check that `.claude/config/` files exist (active-agents.json, team-context.json, domain-ownership.json) and project CLAUDE.md has a Project-Specific Rules section
- [ ] Before writing files, agents check `.claude/config/domain-ownership.json`
- [ ] Domain ownership restrictions come from project config, not hardcoded in global

### Universal Agent Rules
- [ ] All 8 rules present: declare yourself, show mode emoji, check project config, check domain ownership, check active list, respect dependencies, store docs in ticket system, commit to current branch only

### Mode Commands
- [ ] `/mode-project-initialization` exists as a one-time project setup command
- [ ] `/mode-project-initialization` creates all blocking config files (active-agents.json, team-context.json, domain-ownership.json) and Project CLAUDE.md
- [ ] `/mode-exit` exists as an alias for `/mode-collab`

### Activation
- [ ] Framework does NOT activate unless ALL blocking config exists (project CLAUDE.md with Project-Specific Rules section + all `.claude/config/` JSON files)
- [ ] On unconfigured projects, any framework command responds with: run `/mode-project-initialization`
- [ ] All 4 mode transition commands check for project initialization as step 1 before doing anything else

### Quality Standards
- [ ] Global CLAUDE.md states that DoR, DoD, and ticket structure standards exist and must be followed
- [ ] Global CLAUDE.md does NOT define the specific checklists — those belong to the PC agent's skills
- [ ] Rules cover both ticket creators (self-contained tickets) and ticket executors (follow as written)
