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
| **Technical Product Owner (TPO)** | `[TPO]` | New features, requirements, product decisions (PRDs when asked) |
| **Program Manager (PM)** | `[PM]` | Delivery coordination, status, scheduling, blockers |
| **Solutions Architect** | `[SOLUTIONS_ARCHITECT]` | Architecture decisions, system design, integrations |
| **Support Engineer** | `[SUPPORT_ENGINEER]` | Errors, bugs, incidents, troubleshooting |

### Worker Roles (Receive Work from Intake Roles)

| Role | Prefix | Receives Work From |
|------|--------|--------------------|
| Backend Developer | `[BACKEND_DEVELOPER]` | SA, PM (via tickets) |
| Frontend Developer | `[FRONTEND_DEVELOPER]` | SA, PM (via tickets) |
| Backend Tester | `[BACKEND_TESTER]` | Developers, PM |
| Frontend Tester | `[FRONTEND_TESTER]` | Developers, PM |
| **Code Reviewer** | `[CODE_REVIEWER]` | **Developers (when PR ready)** |
| API Designer | `[API_DESIGNER]` | SA, TPO |
| Data Platform Engineer | `[DATA_PLATFORM_ENGINEER]` | SA |
| AI Integration Engineer | `[AI_INTEGRATION_ENGINEER]` | SA, TPO |
| MCP Server Developer | `[MCP_SERVER_DEVELOPER]` | SA |
| Tech Doc Writer | `[TECH_DOC_WRITER]` | Any role |
| UX Designer | `[UX_DESIGNER]` | TPO, SA |
| SVG Designer | `[SVG_DESIGNER]` | TPO, UX Designer |
| **Market Researcher** | `[MARKET_RESEARCHER]` | TPO, SA, PM (for market research, MRDs) |

### Utility Skills (No User Confirmation Required)

Utility skills operate automatically — any role can invoke them without asking user permission.

| Role | Prefix | Purpose |
|------|--------|---------|
| **Project Coordinator** | `[PROJECT_COORDINATOR]` | Ticket CRUD with quality gate enforcement (DoR/DoD) |
| **Agent Skill Coordinator** | `[AGENT_SKILL_COORDINATOR]` | Role routing queries — who handles what, return paths |

**How utility skills work:**
1. Any role invokes utility skill (no user confirmation)
2. Utility skill performs operation
3. Utility skill returns control to CALLING_ROLE (no user confirmation)

This is like a function call — transparent to the user.

### Request Routing Rules

**PM is the SINGLE default entry point for ALL requests.**

```
User request → PM → (consults Agent Skill Coordinator) → routes to appropriate role
```

**How it works:**
1. All unclear requests default to PM
2. PM consults Agent Skill Coordinator to determine the right role
3. PM routes to that role (TPO, SA, Support Engineer, workers, etc.)
4. Routed role does its work and returns to PM

**Exception — Direct invocation:** Users can still invoke a specific role directly (e.g., `/solutions-architect`) if they know what they want.

When a **worker role** receives a direct user request:
1. Acknowledge with role prefix: `[ROLE_NAME] - This request involves...`
2. Route to PM for proper handling
3. PM determines the correct destination

**Example**:
```
[BACKEND_DEVELOPER] - This request involves defining new feature requirements.
Routing to PM for proper handling...

[PM] - Consulting Agent Skill Coordinator... This is a requirements request.
Routing to TPO...

[TPO] - I'll help define the requirements for this feature...
```

See `_shared/references/universal-skill-preamble.md` for full preamble rules.

## Skill Directory

| Skill | Purpose | Primary Output |
|-------|---------|----------------|
| **Skill Creator** | Manage skills in this library (meta-role) | Validated SKILL.md files, ecosystem updates |
| **Technical Product Owner (TPO)** | Translate business goals into requirements | PRDs (when requested), requirement coordination |
| **Market Researcher** | Conduct market research and business impact assessment | Market Requirements Documents (MRDs) |
| **Solutions Architect** | Design system architecture and integrations | ADRs, system diagrams, API contracts |
| **API Designer** | Design pragmatic, developer-friendly APIs | OpenAPI specs, error catalogs |
| **Backend Developer** | Implement APIs with FastAPI/PostgreSQL | Working endpoints, database schemas |
| **Frontend Developer** | Build React components with atomic design | UI components, Storybook stories |
| **Code Reviewer** | Review PRs against universal principles + stack-specific standards | Review feedback, approval status |
| **Data Platform Engineer** | Design data pipelines and storage | Data models, ETL pipelines, vector search |
| **MCP Server Developer** | Build Model Context Protocol servers | MCP tools, resources, prompts |
| **AI Integration Engineer** | Evaluate and implement AI features | AI patterns, prompt engineering, RAG |
| **Backend Tester** | Ensure API test coverage | pytest test suites, coverage reports |
| **Frontend Tester** | Ensure UI test coverage | RTL tests, Playwright E2E, a11y audits |
| **Tech Doc Writer** | Create and maintain documentation | API docs, guides, runbooks |
| **Program Manager (PM)** | Coordinate delivery across teams | Delivery plans, status updates, Linear tickets |
| **Support Engineer** | Error triage, log analysis, incident investigation | Issue diagnosis, root cause analysis |
| **Material Design UX** | Guide UI/UX decisions | Design patterns, accessibility guidance |
| **SVG Designer** | Create vector graphics | Logos, icons, illustrations |
| **Agent Skill Coordinator** | Role routing queries (utility) | Routing decisions, return paths |
| **Project Coordinator** | Ticket CRUD with quality gates (utility) | Tickets with DoR/DoD enforcement |

## Workflow Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LAYER 1: PRODUCT DEFINITION                      │
│                                                                          │
│   ┌──────────────────┐    ┌──────────────────┐                         │
│   │ Technical Product │    │ Market Researcher│                         │
│   │ Owner (TPO)       │◄───│                  │                         │
│   │ Defines WHAT      │    │ Creates MRDs     │                         │
│   │ Output: PRDs      │    │ via web research │                         │
│   └────────┬─────────┘    └──────────────────┘                         │
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
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│   │ Backend Tester   │  │ Frontend Tester  │  │ Code Reviewer    │     │
│   │ (pytest)         │  │ (RTL, Playwright)│  │ (PR Standards)   │     │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                          │
│   Code Reviewer: Quality gate invoked by developers before "Done"       │
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
│   │ Program Manager  │  Coordinates across all layers                   │
│   │ (PM)             │  Tracks in Linear, manages delivery              │
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
1. Market Researcher → Conduct market research (MRD)
2. TPO              → Define requirements (PRD, if requested)
3. Solutions Architect → Design system architecture
4. API Designer     → Design API contracts (if APIs needed)
5. PM               → Create Linear tickets, plan delivery
```

### Implementing Backend
```
1. Backend Developer → Implement endpoints, database
2. Backend Tester    → Write test coverage
3. Code Reviewer     → Review PR before merge
4. Tech Doc Writer   → Document APIs
```

### Implementing Frontend
```
1. Frontend Developer → Build components (atomic design)
2. Frontend Tester    → Write component/E2E tests
3. Code Reviewer      → Review PR before merge
4. Material Design UX → Consult for UI patterns
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
4. PM                → Track issue in Linear if escalation needed
5. Tech Doc Writer     → Update runbooks with resolution
```

## Skill Relationships Matrix

### Who Provides Input to Whom

| Skill | Receives Input From |
|-------|---------------------|
| Market Researcher | TPO, SA, PM (research requests) |
| Solutions Architect | TPO, Market Researcher, Data Platform Engineer, AI Integration Engineer |
| API Designer | TPO, Solutions Architect |
| Backend Developer | TPO, Solutions Architect, API Designer, Support Engineer (bug reports) |
| Frontend Developer | TPO, Solutions Architect, Material Design UX, Support Engineer (bug reports) |
| Data Platform Engineer | TPO, Solutions Architect |
| MCP Server Developer | TPO, Solutions Architect |
| Backend Tester | Backend Developer |
| Frontend Tester | Frontend Developer |
| Tech Doc Writer | API Designer, Solutions Architect, TPO, Support Engineer (runbook updates) |
| PM | All skills (for status tracking) |
| Support Engineer | Sentry (errors), logs, user reports |

### Who Consumes Output From Whom

| Skill | Output Consumed By |
|-------|-------------------|
| Market Researcher | TPO (MRDs for PRD elaboration), SA (market context) |
| TPO | All downstream skills |
| Solutions Architect | All implementation skills, Tech Doc Writer |
| API Designer | Backend Developer, Frontend Developer, Tech Doc Writer |
| Backend Developer | Backend Tester, Frontend Developer (API consumer) |
| Frontend Developer | Frontend Tester |
| Data Platform Engineer | Backend Developer, AI Integration Engineer |
| Backend Tester | PM (quality gates) |
| Frontend Tester | PM (quality gates) |
| Tech Doc Writer | External consumers, Support Engineer (runbooks) |
| Support Engineer | Backend Developer, Frontend Developer (bug fixes), PM (escalations) |

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

### Code Review Flow (Declared Standards)

**Code Reviewer uses a three-tier standards system with EXPLICIT project declaration:**

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: Universal Principles (Always Enforced)              │
│ Source: _shared/references/universal-review-principles.md    │
│ - 22 language-agnostic principles                           │
│ - Security, error handling, code quality, architecture      │
│ - Testing, performance                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ TIER 2: Stack-Specific Standards (Declared in claude.md)    │
│ Source: Project's claude.md → ## Coding Standards           │
│                                                              │
│ Project explicitly enables standards with checkboxes:       │
│                                                              │
│ #### Frontend Standards                                     │
│ - ✅ Atomic Design Hierarchy          ← ENFORCED            │
│ - ❌ Storybook Stories                ← SKIPPED             │
│ - ✅ Component Prop Types             ← ENFORCED            │
│                                                              │
│ #### Backend Standards                                      │
│ - ✅ API Conventions                  ← ENFORCED            │
│ - ✅ Database Patterns                ← ENFORCED            │
│                                                              │
│ Code Reviewer enforces ONLY checked (✅) items              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: Project-Specific Rules (Always Enforced)            │
│ Source: Project's claude.md → ## Coding Standards           │
│                                                              │
│ Custom rules defined by project:                            │
│ - "Use snake_case for all variables"                        │
│ - "Minimum 85% test coverage"                               │
│ - "All API errors include error_code field"                 │
└─────────────────────────────────────────────────────────────┘
```

**Benefits of this approach:**
- ✅ **No stack lock-in** - projects pick exactly what they want
- ✅ **No false assumptions** - explicit checkboxes, no auto-detection
- ✅ **Maximum clarity** - everyone knows what will be enforced
- ✅ **Simple logic** - read checkboxes, no complex detection
- ✅ **Forces intentionality** - projects must think about their standards

**Example**:
```markdown
## Coding Standards in project's claude.md

### Stack-Specific Standards
- ✅ Atomic Design Hierarchy
- ❌ Storybook Stories (we don't use Storybook)
- ✅ Component Prop Types
- ✅ API Conventions
- ✅ Database Patterns

### Project-Specific Rules
- "Use snake_case for all Python variables (PEP 8)"
- "Minimum 85% test coverage for new backend code"

→ Code Reviewer will enforce:
  1. Universal: 22 principles (always)
  2. Stack: Atomic Design, Prop Types, API Conventions, Database Patterns
  3. Project: snake_case rule, 85% coverage requirement
```

**CRITICAL**: Code Reviewer REFUSES to review PRs if `## Coding Standards` section contains placeholders.

## Project Documentation Registries

Two key registries maintain project knowledge across sessions:

### Plan Registry (`docs/plans/_registry.json`)

| Aspect | Detail |
|--------|--------|
| **Owner** | TPO (creates/updates plans) |
| **Consumers** | Solutions Architect, PM, all skills |
| **Purpose** | Index of all product plans, MRDs, and their status |
| **Schema** | See `plan-registry-schema.md` |

### Integration Catalog (`docs/integrations/_catalog.json`)

| Aspect | Detail |
|--------|--------|
| **Owner** | Solutions Architect (creates/updates integrations) |
| **Consumers** | TPO, PM, Backend Developer, Tech Doc Writer |
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
                                        │       PM          │
                                        │ (updates status,    │
                                        │  creates tickets)   │
                                        └─────────────────────┘
```

## Consultation Triggers

Quick reference for when to involve other skills:

| Situation | Consult |
|-----------|---------|
| Market research needed | Market Researcher |
| Requirements unclear | TPO |
| System design needed | Solutions Architect |
| API contract design | API Designer |
| Database schema design | Data Platform Engineer |
| AI/ML features | AI Integration Engineer |
| Tool integrations for AI | MCP Server Developer |
| UI/UX decisions | Material Design UX |
| Test strategy | Backend/Frontend Tester |
| **PR ready for review** | **Code Reviewer** |
| Documentation needed | Tech Doc Writer |
| Delivery planning | PM |
| Vector search/RAG | Data Platform Engineer |
| Prompt engineering | AI Integration Engineer |
| Error investigation | Support Engineer |
| Log analysis needed | Support Engineer |
| Incident response | Support Engineer |
| **Check existing plans** | Read `docs/plans/_registry.json` |
| **Check existing integrations** | Read `docs/integrations/_catalog.json` |

## Ticket Traceability

All implementation skills (developers, testers, PM) must follow ticketing conventions to ensure code commits reference work items.

**All ticket operations go through Project Coordinator.** See `project-coordinator/SKILL.md`.

Project Coordinator handles tool-specific complexity internally via its reference files:
- `project-coordinator/references/github-operations.md`
- `project-coordinator/references/linear-operations.md`
- `project-coordinator/references/plan-file-operations.md`
- `project-coordinator/references/ticket-templates.md`

Configure your ticket system in project's `claude.md` under Team Context.
