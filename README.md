# Claude Code Skills

A collection of specialized skills for Claude Code that enable role-based AI assistance across the software development lifecycle.

## Quick Start

To use these skills in your project:

1. Copy `_shared/references/boilerplate-claude-md.md` to your project as `claude.md`
2. Fill in the `[placeholders]` for your project
3. Skills will enforce the rules defined in your `claude.md`

## How It Works

**Every interaction goes through a skill.** No freeform responses.

1. User makes a request
2. Claude selects and invokes the appropriate skill
3. Skill checks project scope (refuses if undefined)
4. Skill verifies domain ownership before acting
5. Skill prefixes response with `[ROLE_NAME]`

### Intake vs Worker Roles

| Type | Skills | Accepts |
|------|--------|---------|
| **Intake** | TPO, Solutions Architect, PM, Support Engineer | Direct user requests |
| **Worker** | All others | Only tickets with Technical Spec + Gherkin |

Worker skills route new feature requests to intake roles.

## Available Skills

| Skill | Purpose |
|-------|---------|
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
| **program-manager** | Cross-functional delivery coordination with Linear |
| **support-engineer** | Error triage, log analysis, and incident investigation |
| **material-ux-designer** | UI/UX guidance based on Material Design |
| **svg-designer** | Create logos, icons, and vector illustrations |

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
  └── Program Manager → Linear tickets, delivery
```

## Structure

```
skills/
├── _shared/              # Cross-skill references and templates
│   └── references/
├── <skill-name>/
│   ├── SKILL.md          # Main skill definition
│   ├── references/       # Skill-specific guidelines
│   └── assets/           # Templates and schemas
```

## Using the Boilerplate

The boilerplate (`_shared/references/boilerplate-claude-md.md`) is a template for your project's `claude.md`. It enforces:

### First Action
Skills must be invoked before any response. No freeform chat.

### Project Scope
Required sections that skills check before acting:

- **Team Context** — Team slug for branch names, ticket system (`linear`/`github`/`none`), main branch
- **Domain Ownership** — Who owns what. Skills cannot create tickets or make decisions outside owned domains.
- **Active Roles** — Which skills are enabled. Skills not listed cannot be invoked.
- **Cross-Domain Protocol** — How to handle work outside your domain (flag, don't action)

### Naming Rules
- Plan names: Feature description only. No dates/quarters/sprints.
- Branch names: `{type}/{team-slug}/{TICKET-ID}-{description}`

### Ticket Requirements
All tickets need Technical Spec (MUST/MUST NOT/SHOULD) + Gherkin scenarios. PM blocks creation without these.

### Skill Behavior
1. Prefix responses with `[ROLE_NAME]`
2. Refuse work if Project Scope undefined
3. Check domain ownership before acting
4. Confirm base branch before creating feature branches

## Invocation

Skills are invoked via slash commands: `/technical-product-owner`, `/solutions-architect`, etc.
