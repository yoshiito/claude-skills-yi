# Skill Ecosystem Overview

Quick reference for understanding how skills relate and when to invoke each one.

## Skill Directory

| Skill | Purpose | Primary Output |
|-------|---------|----------------|
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

## Skill Relationships Matrix

### Who Provides Input to Whom

| Skill | Receives Input From |
|-------|---------------------|
| Solutions Architect | TPO, Data Platform Engineer, AI Integration Engineer |
| API Designer | TPO, Solutions Architect |
| Backend Developer | TPO, Solutions Architect, API Designer |
| Frontend Developer | TPO, Solutions Architect, Material Design UX |
| Data Platform Engineer | TPO, Solutions Architect |
| MCP Server Developer | TPO, Solutions Architect |
| Backend Tester | Backend Developer |
| Frontend Tester | Frontend Developer |
| Tech Doc Writer | API Designer, Solutions Architect, TPO |
| TPgM | All skills (for status tracking) |

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
| Tech Doc Writer | External consumers, support teams |

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

## Linear Ticket Traceability

All implementation skills (developers, testers, TPgM) should follow the conventions in `linear-ticket-traceability.md` to ensure code commits reference tickets.
