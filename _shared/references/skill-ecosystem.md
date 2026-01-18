# Skill Ecosystem Overview

Quick reference for understanding how skills relate and when to invoke each one.

## Meta-Role: Skill Creator

**For the Skills Library Repository Only**

| Role | Prefix | Handles |
|------|--------|---------|
| **Skill Creator** | `[SKILL_CREATOR]` | All skill management: creation, validation, updates, audits |

When working in the skills library itself, Skill Creator is the **default intake role**. It manages all other skills.

---

## Intake Roles vs Worker Roles

**CRITICAL**: Not all skills can receive direct user requests. Skills are divided into two categories:

### Intake Roles (Can Receive Direct Requests)

| Role | Prefix | Handles |
|------|--------|---------|
| **Technical Product Owner (TPO)** | `[TPO]` | New features, requirements, product decisions |
| **Technical Program Manager (TPgM)** | `[TPgM]` | Delivery coordination, status, scheduling, blockers |
| **Solutions Architect** | `[SOLUTIONS_ARCHITECT]` | Architecture decisions, system design, integrations |
| **Support Engineer** | `[SUPPORT_ENGINEER]` | Errors, bugs, incidents, troubleshooting |

### Worker Roles (Receive Work from Intake Roles)

| Role | Prefix | Receives Work From |
|------|--------|--------------------|
| Backend Developer | `[BACKEND_DEVELOPER]` | SA, TPgM (via tickets) |
| Frontend Developer | `[FRONTEND_DEVELOPER]` | SA, TPgM (via tickets) |
| Backend Tester | `[BACKEND_TESTER]` | Developers, TPgM |
| Frontend Tester | `[FRONTEND_TESTER]` | Developers, TPgM |
| API Designer | `[API_DESIGNER]` | SA, TPO |
| Data Platform Engineer | `[DATA_PLATFORM_ENGINEER]` | SA |
| AI Integration Engineer | `[AI_INTEGRATION_ENGINEER]` | SA, TPO |
| MCP Server Developer | `[MCP_SERVER_DEVELOPER]` | SA |
| Tech Doc Writer | `[TECH_DOC_WRITER]` | Any role |
| UX Designer | `[UX_DESIGNER]` | TPO, SA |
| SVG Designer | `[SVG_DESIGNER]` | TPO, UX Designer |

### Request Routing Rules

When a **worker role** receives a direct user request:

1. Acknowledge with role prefix: `[ROLE_NAME] - This request involves...`
2. Identify the appropriate intake role
3. Route and continue with the intake role

**Example**:
```
[BACKEND_DEVELOPER] - This request involves defining new feature requirements.
Routing to Technical Product Owner for requirement definition...

[TPO] - I'll help define the requirements for this feature...
```

See `_shared/references/universal-skill-preamble.md` for full preamble rules.

## Skill Directory

| Skill | Purpose | Primary Output |
|-------|---------|----------------|
| **Skill Creator** | Manage skills in this library (meta-role) | Validated SKILL.md files, ecosystem updates |
| **Technical Product Owner (TPO)** | Translate business goals into requirements | Master Requirement Documents (MRDs) |
| **Solutions Architect** | Design system architecture and integrations | ADRs, system diagrams, API contracts |
| **API Designer** | Design pragmatic, developer-friendly APIs | OpenAPI specs, error catalogs |
| **Backend Developer** | Implement APIs with FastAPI/PostgreSQL | Working endpoints, database schemas |
| **Frontend Developer** | Build React components with atomic design | UI components, Storybook stories |
| **Data Platform Engineer** | Design data pipelines and storage | Data models, ETL pipelines, vector search |
| **MCP Server Developer** | Build Model Context Protocol servers | MCP tools, resources, prompts |
| **AI Integration Engineer** | Evaluate and implement AI features | AI patterns, prompt engineering, RAG |
| **Backend Tester** | Ensure API test coverage | pytest test suites, coverage reports |
| **Frontend Tester** | Ensure UI test coverage | RTL tests, Playwright E2E, a11y audits |
| **Tech Doc Writer** | Create and maintain documentation | API docs, guides, runbooks |
| **Technical Program Manager (TPgM)** | Coordinate delivery across teams | Delivery plans, status updates, Linear tickets |
| **Support Engineer** | Error triage, log analysis, incident investigation | Issue diagnosis, root cause analysis |
| **Material Design UX** | Guide UI/UX decisions | Design patterns, accessibility guidance |
| **SVG Designer** | Create vector graphics | Logos, icons, illustrations |

## Workflow Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LAYER 1: PRODUCT DEFINITION                      │
│                                                                          │
│   ┌──────────────────┐                                                  │
│   │ Technical Product │  Defines WHAT to build                          │
│   │ Owner (TPO)       │  Output: MRDs with requirements                 │
│   └────────┬─────────┘                                                  │
│            │                                                             │
└────────────│─────────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      LAYER 2: ARCHITECTURE & DESIGN                      │
│                                                                          │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐ │
│   │ Solutions        │◄──►│ API Designer     │    │ Material Design  │ │
│   │ Architect        │    │                  │    │ UX               │ │
│   └────────┬─────────┘    └────────┬─────────┘    └──────────────────┘ │
│            │                       │                                    │
│   Defines HOW systems fit      Defines HOW APIs              UI/UX     │
│   Output: ADRs, diagrams       Output: OpenAPI specs        patterns   │
│                                                                          │
└────────────┼───────────────────────┼─────────────────────────────────────┘
             │                       │
             ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        LAYER 3: IMPLEMENTATION                           │
│                                                                          │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐ │
│   │ Backend          │    │ Frontend         │    │ Data Platform    │ │
│   │ Developer        │    │ Developer        │    │ Engineer         │ │
│   └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘ │
│            │                       │                       │            │
│   ┌──────────────────┐    ┌──────────────────┐                         │
│   │ MCP Server       │    │ AI Integration   │                         │
│   │ Developer        │    │ Engineer         │                         │
│   └──────────────────┘    └──────────────────┘                         │
│                                                                          │
└────────────┼───────────────────────┼───────────────────────┼─────────────┘
             │                       │                       │
             ▼                       ▼                       │
┌─────────────────────────────────────────────────────────────────────────┐
│                         LAYER 4: QUALITY & TESTING                       │
│                                                                          │
│   ┌──────────────────┐    ┌──────────────────┐                         │
│   │ Backend Tester   │    │ Frontend Tester  │                         │
│   │ (pytest)         │    │ (RTL, Playwright)│                         │
│   └──────────────────┘    └──────────────────┘                         │
│                                                                          │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        LAYER 5: DOCUMENTATION                            │
│                                                                          │
│   ┌──────────────────┐                                                  │
│   │ Tech Doc Writer  │  Creates API docs, guides, runbooks              │
│   │ Manager          │                                                  │
│   └──────────────────┘                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    CROSS-CUTTING: DELIVERY MANAGEMENT                    │
│                                                                          │
│   ┌──────────────────┐                                                  │
│   │ Technical Program│  Coordinates across all layers                   │
│   │ Manager (TPgM)   │  Tracks in Linear, manages delivery              │
│   └──────────────────┘                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    CROSS-CUTTING: OPERATIONS & SUPPORT                   │
│                                                                          │
│   ┌──────────────────┐                                                  │
│   │ Support Engineer │  Error triage, log analysis, debugging           │
│   │                  │  Uses Sentry MCP, reads logs, escalates          │
│   └──────────────────┘                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## When to Use Each Skill

### Starting a New Feature
```
1. TPO           → Define requirements (MRD)
2. Solutions Architect → Design system architecture
3. API Designer  → Design API contracts (if APIs needed)
4. TPgM          → Create Linear tickets, plan delivery
```

### Implementing Backend
```
1. Backend Developer → Implement endpoints, database
2. Backend Tester    → Write test coverage
3. Tech Doc Writer   → Document APIs
```

### Implementing Frontend
```
1. Frontend Developer → Build components (atomic design)
2. Frontend Tester    → Write component/E2E tests
3. Material Design UX → Consult for UI patterns
```

### Adding AI Features
```
1. AI Integration Engineer → Evaluate if AI is right solution
2. Data Platform Engineer  → Design RAG/vector storage if needed
3. MCP Server Developer    → Build tool integrations if needed
```

### Exposing Tools to AI
```
1. MCP Server Developer → Build MCP server
2. Solutions Architect  → Review integration patterns
```

### Investigating Issues
```
1. Support Engineer    → Triage errors (Sentry), analyze logs
2. Backend Developer   → Fix code issues if identified
3. Frontend Developer  → Fix UI issues if identified
4. TPgM                → Track issue in Linear if escalation needed
5. Tech Doc Writer     → Update runbooks with resolution
```

## Skill Relationships Matrix

### Who Provides Input to Whom

| Skill | Receives Input From |
|-------|---------------------|
| Solutions Architect | TPO, Data Platform Engineer, AI Integration Engineer |
| API Designer | TPO, Solutions Architect |
| Backend Developer | TPO, Solutions Architect, API Designer, Support Engineer (bug reports) |
| Frontend Developer | TPO, Solutions Architect, Material Design UX, Support Engineer (bug reports) |
| Data Platform Engineer | TPO, Solutions Architect |
| MCP Server Developer | TPO, Solutions Architect |
| Backend Tester | Backend Developer |
| Frontend Tester | Frontend Developer |
| Tech Doc Writer | API Designer, Solutions Architect, TPO, Support Engineer (runbook updates) |
| TPgM | All skills (for status tracking) |
| Support Engineer | Sentry (errors), logs, user reports |

### Who Consumes Output From Whom

| Skill | Output Consumed By |
|-------|-------------------|
| TPO | All downstream skills |
| Solutions Architect | All implementation skills, Tech Doc Writer |
| API Designer | Backend Developer, Frontend Developer, Tech Doc Writer |
| Backend Developer | Backend Tester, Frontend Developer (API consumer) |
| Frontend Developer | Frontend Tester |
| Data Platform Engineer | Backend Developer, AI Integration Engineer |
| Backend Tester | TPgM (quality gates) |
| Frontend Tester | TPgM (quality gates) |
| Tech Doc Writer | External consumers, Support Engineer (runbooks) |
| Support Engineer | Backend Developer, Frontend Developer (bug fixes), TPgM (escalations) |

## Common Collaboration Patterns

### API Development Flow
```
TPO (requirements)
  ↓
Solutions Architect (system design)
  ↓
API Designer (contract design) ←→ Solutions Architect (review)
  ↓
Backend Developer (implementation)
  ↓
Backend Tester (test coverage)
  ↓
Tech Doc Writer (documentation)
```

### Frontend Development Flow
```
TPO (requirements)
  ↓
Solutions Architect (data flow)
  ↓
Material Design UX (UI patterns)
  ↓
Frontend Developer (components)
  ↓
Frontend Tester (component + E2E tests)
```

### AI Feature Flow
```
TPO (requirements)
  ↓
AI Integration Engineer (evaluate approach)
  ↓
├── Data Platform Engineer (if RAG/data needed)
├── MCP Server Developer (if tool use needed)
└── Backend Developer (API integration)
```

## Project Documentation Registries

Two key registries maintain project knowledge across sessions:

### Plan Registry (`docs/plans/_registry.json`)

| Aspect | Detail |
|--------|--------|
| **Owner** | TPO (creates/updates plans) |
| **Consumers** | Solutions Architect, TPgM, all skills |
| **Purpose** | Index of all product plans, MRDs, and their status |
| **Schema** | See `plan-registry-schema.md` |

### Integration Catalog (`docs/integrations/_catalog.json`)

| Aspect | Detail |
|--------|--------|
| **Owner** | Solutions Architect (creates/updates integrations) |
| **Consumers** | TPO, TPgM, Backend Developer, Tech Doc Writer |
| **Purpose** | Index of all external integrations, vendors, and dependencies |
| **Schema** | See `integration-catalog-schema.md` |

### Registry Workflow

```
┌─────────────┐     creates plan      ┌─────────────────────┐
│     TPO     │──────────────────────▶│ docs/plans/         │
│             │                       │   _registry.json    │
└─────────────┘                       └──────────┬──────────┘
                                                 │
                                                 │ consumes
                                                 ▼
┌─────────────┐    creates integration  ┌─────────────────────┐
│  Solutions  │────────────────────────▶│ docs/integrations/  │
│  Architect  │                         │   _catalog.json     │
└─────────────┘                         └──────────┬──────────┘
                                                   │
                                                   │ consumes
                                                   ▼
                                        ┌─────────────────────┐
                                        │       TPgM          │
                                        │ (updates status,    │
                                        │  creates tickets)   │
                                        └─────────────────────┘
```

## Consultation Triggers

Quick reference for when to involve other skills:

| Situation | Consult |
|-----------|---------|
| Requirements unclear | TPO |
| System design needed | Solutions Architect |
| API contract design | API Designer |
| Database schema design | Data Platform Engineer |
| AI/ML features | AI Integration Engineer |
| Tool integrations for AI | MCP Server Developer |
| UI/UX decisions | Material Design UX |
| Test strategy | Backend/Frontend Tester |
| Documentation needed | Tech Doc Writer |
| Delivery planning | TPgM |
| Vector search/RAG | Data Platform Engineer |
| Prompt engineering | AI Integration Engineer |
| Error investigation | Support Engineer |
| Log analysis needed | Support Engineer |
| Incident response | Support Engineer |
| **Check existing plans** | Read `docs/plans/_registry.json` |
| **Check existing integrations** | Read `docs/integrations/_catalog.json` |

## Ticket Traceability

All implementation skills (developers, testers, TPgM) must follow ticketing conventions to ensure code commits reference work items.

### Ticketing References

| File | When to Use |
|------|-------------|
| `ticketing-core.md` | Universal rules (always read first) |
| `ticketing-linear.md` | Linear ticket system |
| `ticketing-github-projects.md` | GitHub Projects |
| `ticketing-plan-file.md` | No external ticket system |

Configure your ticket system in project's `claude.md` under Team Context.
