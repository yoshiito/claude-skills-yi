# Claude Code Skills

A collection of specialized skills for Claude Code that enable role-based AI assistance across the software development lifecycle.

## Quick Start

### 1. Set Up Global Configuration

Copy `_shared/references/boilerplate-global-claude-md.md` to `~/.claude/CLAUDE.md`

This contains universal framework rules that activate conditionally based on project opt-in.

### 2. Set Up Project Configuration

Copy `_shared/references/boilerplate-project-claude-md.md` to your project as `claude.md`

Fill in the `[placeholders]`:
- `[Project Name]` — Your project name
- `[skills-path]` — Path to this skills library (e.g., `~/.claude/skills`)
- `[slug]` — Team slug for tickets
- Domain ownership and active roles

### 3. Framework Activation

The project `claude.md` declares `uses: yoshi-skills-framework` which activates the global rules. Projects without this declaration use normal Claude behavior.

## How It Works

**Program Manager (PM) is the entry point for ALL requests.**

```
User request → PM → Agent Skill Coordinator → recommended role (immediate, no pause)
```

1. PM receives request, invokes Agent Skill Coordinator
2. ASC returns the appropriate role
3. PM immediately invokes that role (no pause, no waiting)
4. Role handles the request with `[ROLE_NAME]` prefix

### Intake vs Worker Roles

| Type | Skills | Accepts |
|------|--------|---------|
| **Intake** | TPO, Solutions Architect, PM, Support Engineer | Direct user requests |
| **Worker** | All others | Only tickets with Technical Spec + Gherkin |

Worker skills route new feature requests to intake roles.

## Available Skills

| Skill | Purpose |
|-------|---------|
| **program-manager** | Entry point, routes via ASC, verifies DoR/DoD |
| **technical-product-owner** | Translate business goals into MRDs and coordinate PRD development |
| **solutions-architect** | Design system architecture, ADRs, and integration patterns |
| **api-designer** | Create pragmatic REST API designs with OpenAPI specs |
| **backend-fastapi-postgres-sqlmodel-developer** | Implement CRUD APIs with FastAPI and PostgreSQL |
| **backend-fastapi-pytest-tester** | Backend test coverage analysis and test generation |
| **frontend-tester** | React component testing, Playwright E2E, accessibility |
| **frontend-atomic-design-engineer** | Enforce atomic design principles in React components |
| **data-platform-engineer** | Design data pipelines, storage, and vector search |
| **ai-integration-engineer** | Evaluate and implement AI-powered features |
| **mcp-server-developer** | Build Model Context Protocol servers |
| **tech-doc-writer-manager** | Technical documentation authoring and maintenance |
| **support-engineer** | Error triage, log analysis, and incident investigation |
| **material-ux-designer** | UI/UX guidance based on Material Design |
| **svg-designer** | Create logos, icons, and vector illustrations |

### Utility Skills (No confirmation required)

| Skill | Purpose |
|-------|---------|
| **project-coordinator** | Ticket CRUD with DoR/DoD enforcement |
| **agent-skill-coordinator** | Role registry and routing decisions |

## Skill Workflow Layers

```
LAYER 1: PRODUCT DEFINITION
  └── Technical Product Owner → MRDs (what/why)

LAYER 2: ARCHITECTURE & DESIGN
  ├── Solutions Architect → ADRs, system diagrams
  ├── API Designer → OpenAPI specs
  └── Material Design UX → UI patterns

LAYER 3: IMPLEMENTATION
  ├── Backend Developer → FastAPI endpoints
  ├── Frontend Developer → React components
  └── Data Platform Engineer → Data pipelines

LAYER 4: QUALITY ASSURANCE
  ├── Backend Tester → pytest suites
  └── Frontend Tester → RTL, Playwright, a11y

LAYER 5: DOCUMENTATION & DELIVERY
  ├── Tech Doc Writer → API docs, guides
  └── Program Manager → Delivery coordination
```

## Structure

```
skills/
├── _shared/references/
│   ├── boilerplate-global-claude-md.md   # → ~/.claude/CLAUDE.md
│   ├── boilerplate-project-claude-md.md  # → project/claude.md
│   ├── definition-of-ready.md
│   └── definition-of-done.md
├── <skill-name>/
│   ├── SKILL.md          # Main skill definition
│   ├── skill.yaml        # Skill configuration (source of truth)
│   └── references/       # Skill-specific guidelines
```

## Configuration Files

### Global (`~/.claude/CLAUDE.md`)

Universal framework rules:
- PM as entry point
- Role declaration (`[ROLE_NAME]` prefix)
- Routing flow (PM → ASC → role, no pause)
- Drive/Collab mode protocols
- Skill boundary enforcement
- Role categories and activation rules

### Project (`claude.md`)

Project-specific configuration:
- `uses: yoshi-skills-framework` — Activates global rules
- Skills Path — Where to find skill files
- Team Context — Slug, ticket system, main branch
- Domain Ownership — Who owns what
- Active Roles — Which skills are enabled
- Coding Standards — Project-specific rules

## Modes

### Standard Mode
Roles require user confirmation before proceeding.

### Drive Mode
User types `DRIVE` to activate. Workers skip confirmation and proceed immediately. PM verifies DoR/DoD.

### Collab Mode
Multiple roles collaborate. Messages prefixed with `🤝` before role prefix.

### Exploration Mode
User-directed discovery. PM tracks and documents afterward.

## Invocation

Skills are invoked via slash commands: `/program-manager`, `/technical-product-owner`, `/solutions-architect`, etc.

Default entry: All requests go to PM first, which routes via ASC.
