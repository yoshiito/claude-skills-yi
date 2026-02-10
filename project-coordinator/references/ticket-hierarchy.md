# Ticket Hierarchy and Relationships

**Project Coordinator enforces these structures.** This document defines the hierarchy model, relationships, and role assignments across all ticket types.

## Template Overview

| Level | Template | Content From | Use Case |
|-------|----------|--------------|----------|
| **Mission** | `[Mission]` | TPO | High-level goal (Epic equivalent) |
| **Feature** | `[Backend]`/`[Frontend]` | SA | Quality-bounded work unit |
| **Bug** | `[Bug]` | Support Engineer | Bug fix (quality-bounded) |
| **Dev Subtask** | `[Dev]` | SA | Implementation breakdown (OPTIONAL) |
| **Communication** | `[Query]` | Any Role | Cross-team/intra-team gap discovery |
| **Mission-Level** | `[Test]`, `[Docs]`, `[SA Review]`, `[UAT]` | SA | Cross-cutting activities |

**Note**: All tickets are created by **Project Coordinator**. The "Content From" column indicates which role provides the ticket content when invoking PC.

**Key Change**: Quality phases (Code Review, Test, Docs, SA Review, UAT) are **workflow phases at Feature level**, NOT separate tickets. Only Dev can optionally have subtasks.

## Ticket Hierarchy Model

**Features are Quality-Bounded** - sized so all quality activities can happen comprehensively at the Feature level, not as separate tickets.

### Feature Structure (Quality-Bounded Work Unit)

```
[Backend] Add password reset endpoint        ← Feature (quality-bounded unit)
├── [Dev] Token generation logic             ← Dev subtask (OPTIONAL)
├── [Dev] Email integration                  ← Dev subtask (OPTIONAL)
└── Workflow phases (tracked in Feature, NOT separate tickets):
    Development → Code Review → Test → Docs → SA Review → UAT
```

**Quality phases are tracked as workflow states within the Feature ticket, not as child tickets.**

| Phase | Worker | Tracked As |
|-------|--------|------------|
| Development | Developer | Feature status + PR |
| Code Review | Code Reviewer | PR review |
| Test | Tester | Test completion checklist |
| Docs | Tech Doc Writer | Docs completion checklist |
| SA Review | Solutions Architect | SA approval comment |
| UAT | TPO | UAT approval comment |

### Mission Level (Cross-Cutting)

```
Mission: Password Reset Capability
├── [Backend] Add reset endpoint             ← Feature
│   ├── [Dev] subtasks (if needed)
│   └── Workflow phases at Feature level
├── [Frontend] Add reset form                ← Feature
│   └── ...
├── [Bug] Fix validation edge case           ← Feature (bug)
│   └── ...
├── [Query] API rate limit unclear (Backend) ← Communication (no subtasks)
│   └── (relatesTo: [Frontend], blocks it)
├── [Test] Password Reset E2E Regression     ← Mission-level activity
├── [Docs] Password Reset Guide              ← Mission-level activity
├── [SA Review] Password Reset Architecture  ← Mission-level activity
└── [UAT] Password Reset Acceptance          ← Mission-level activity
```

| Mission-Level Ticket | Purpose |
|---------------------|---------|
| `[Query] {Subject} ({Target Team})` | Cross-team/intra-team gap discovery and resolution |
| `[Test] {Mission} E2E Regression` | Full integration/regression testing across all Features |
| `[Docs] {Mission} Guide` | Comprehensive Mission documentation |
| `[SA Review] {Mission} Architecture` | SA validates architecture compliance across all Features |
| `[UAT] {Mission} Acceptance` | TPO acceptance of complete Mission |

**Note**: `[Query]` has no workflow phases. It is resolved through human discussion, not implementation.

## blockedBy Relationships

| Ticket | blockedBy |
|--------|-----------|
| Feature | Any open `[Query]` blockers |
| `[Dev]` subtasks | Other `[Dev]` subtasks if sequential |
| Mission `[Test]` | All Feature containers |
| Mission `[Docs]` | Mission `[Test]` |
| Mission `[SA Review]` | Mission `[Docs]` |
| Mission `[UAT]` | Mission `[SA Review]` |

### Query as Dynamic Blocker

When a `[Query]` ticket is created:
1. **PC auto-links** the Query to the originating Feature via `blockedBy`
2. **Feature cannot proceed** while any linked Query is open
3. **Query resolution** removes the blocker relationship automatically

## Role Assignments

### Feature Tickets

| Ticket Prefix | Created By | Purpose |
|---------------|------------|---------|
| `[Backend]` | SA | Backend Feature |
| `[Frontend]` | SA | Frontend Feature |
| `[Bug]` | Support Engineer | Bug fix Feature |

### Communication Tickets (No Subtasks)

| Ticket Prefix | Created By | Purpose |
|---------------|------------|---------|
| `[Query]` | Any role | Cross-team/intra-team gap discovery (human-resolved) |

### Dev Subtasks (OPTIONAL - only if implementation needs breakdown)

| Subtask | Skill Name | Purpose |
|---------|------------|---------|
| `[Dev]` | `backend-fastapi-postgres-sqlmodel-developer` / `frontend-atomic-design-engineer` | Implementation component |

### Workflow Phase Workers (at Feature level, NOT separate tickets)

| Phase | Skill Name | Purpose |
|-------|------------|---------|
| Development | `backend-fastapi-postgres-sqlmodel-developer` / `frontend-atomic-design-engineer` | Implementation |
| Code Review | `code-reviewer` | Code review |
| Test | `backend-fastapi-pytest-tester` / `frontend-tester` | Testing |
| Docs | `tech-doc-writer-manager` | Documentation |
| SA Review | `solutions-architect` | Technical acceptance |
| UAT | `technical-product-owner` | User acceptance |

### Mission-Level Cross-Cutting Tickets

| Ticket | Skill Name | Purpose |
|--------|------------|---------|
| `[Test] {Mission} E2E Regression` | `backend-fastapi-pytest-tester` / `frontend-tester` | Full Mission regression |
| `[Docs] {Mission} Guide` | `tech-doc-writer-manager` | Comprehensive Mission docs |
| `[SA Review] {Mission} Architecture` | `solutions-architect` | Architecture compliance |
| `[UAT] {Mission} Acceptance` | `technical-product-owner` | Mission acceptance |

## Relationship Fields

**All relationships set via Project Coordinator** using native ticket system fields.

| System | Parent Field | Blocked By Field | Relates To Field |
|--------|--------------|------------------|------------------|
| Linear | `parentId` | `blockedBy` | `relatedIssues` |
| GitHub | `addSubIssue` GraphQL | `addBlockedBy` GraphQL | `convertedNoteToIssue` links |
| Plan Files | N/A | `(blockedBy: ...)` | `(relatesTo: ...)` |

**DO NOT** put relationship info in ticket body text. PC sets native fields.

### Query-Specific Relationships

When creating a `[Query]` ticket, PC sets:
1. **Parent**: Mission (same as originating Feature)
2. **Relates To**: The originating Feature where gap was discovered
3. **Blocked By (on target)**: PC adds Query to originating Feature's blockedBy list
