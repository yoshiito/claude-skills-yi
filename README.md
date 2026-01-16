# Claude Code Skills

A collection of specialized skills for Claude Code that enable role-based AI assistance across the software development lifecycle.

## What Are Skills?

Skills are domain-specific prompts that give Claude Code expertise in particular areas. Each skill defines:
- **Role boundaries** - What it does and doesn't do
- **Workflows** - Step-by-step processes to follow
- **References** - Templates, schemas, and guidelines
- **Integration points** - How it connects with other skills

## Available Skills

| Skill | Purpose |
|-------|---------|
| **technical-product-owner** | Translate business goals into MRDs and coordinate PRD development |
| **solutions-architect** | Design system architecture, ADRs, and integration patterns |
| **api-designer** | Create pragmatic REST API designs with OpenAPI specs |
| **fastapi-postgres-sqlmodel-developer** | Implement CRUD APIs with FastAPI and PostgreSQL |
| **fastapi-pytest-tester** | Backend test coverage analysis and test generation |
| **frontend-tester** | React component testing, Playwright E2E, accessibility |
| **frontend-atomic-design-engineer** | Enforce atomic design principles in React components |
| **data-platform-engineer** | Design data pipelines, storage, and vector search |
| **ai-integration-engineer** | Evaluate and implement AI-powered features |
| **mcp-server-developer** | Build Model Context Protocol servers |
| **tech-doc-writer-manager** | Technical documentation authoring and maintenance |
| **technical-program-manager** | Cross-functional delivery coordination with Linear |
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
  └── Technical Program Manager → Linear tickets, delivery
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

## Usage

Skills are invoked automatically by Claude Code based on task context, or explicitly via slash commands (e.g., `/technical-product-owner`).
