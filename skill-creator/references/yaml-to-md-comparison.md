# YAML → Markdown Comparison

This document shows how skill.yaml fields map to generated SKILL.md sections.

## 1. Frontmatter + Title

### YAML Input

```yaml
meta:
  name: backend-fastapi-postgres-sqlmodel-developer
  displayName: FastAPI + PostgreSQL + SQLModel Developer
  emoji: "🔧"
  description: >
    Systematic workflow for implementing CRUD APIs...
```

### Generated MD Output

```markdown
---
name: backend-fastapi-postgres-sqlmodel-developer
description: Systematic workflow for implementing CRUD APIs...
---

# FastAPI + PostgreSQL + SQLModel Developer

Systematic workflow for implementing CRUD APIs...
```

---

## 2. Preamble (Generated from Capabilities)

### YAML Input

```yaml
role:
  prefix: BACKEND_DEVELOPER
  capabilities:
    canIntakeUserRequests: false
    requiresTicketWithSpec: true
    requiresActivationConfirmation: true
    requiresProjectScope: true
    isUtility: false
```

### Generated MD Output

```markdown
## Preamble: Universal Conventions

**Before responding to any request, apply these checks IN ORDER (all are BLOCKING):**

0. **Request activation confirmation** - Get explicit user confirmation...
1. **Prefix all responses** with `[BACKEND_DEVELOPER]` - Continuous declaration...
2. **This is a WORKER ROLE** - Receives tickets from intake roles...
3. **Check project scope** - If project's `claude.md` lacks `## Project Scope`...

**If receiving a direct request that should be routed:**
```
[BACKEND_DEVELOPER] - This request involves [defining requirements].
Routing to [TPO] for proper handling...
```
```

**Note**: The preamble is entirely GENERATED from capabilities. No preamble section in YAML.

---

## 3. Boundaries

### YAML Input

```yaml
boundaries:
  authorizedActions:
    - Implement API endpoints per ticket spec
    - Write database models (SQLModel classes)
    - Write DDL (schema.sql)

  prohibitions:
    - action: Gather or define requirements
      owner: TPO
    - action: Write tests or define test strategy
      owner: Backend Tester
```

### Generated MD Output

```markdown
## Role Boundaries

**This role DOES:**
- Implement API endpoints per ticket spec
- Write database models (SQLModel classes)
- Write DDL (schema.sql)

**This role does NOT do:**
- Gather or define requirements (that's TPO)
- Write tests or define test strategy (that's Backend Tester)
```

---

## 4. Quality Gates (Utility Role Example)

### YAML Input

```yaml
qualityGates:
  definitionOfReady:
    enforceAt: Before creating ANY ticket
    ticketTypes:
      epic:
        titlePrefix: "[Feature]"
        requiredSections:
          - name: Problem Statement
            verify: Body contains "Problem Statement" section
          - name: Target Users
            verify: Body contains "Target Users" section
```

### Generated MD Output

```markdown
## Quality Gates

### Definition of Ready (On Create)

**Enforce at**: Before creating ANY ticket

#### For Epic

| Check | How to Verify | Reject If |
|-------|---------------|-----------|
| Title prefix | Title starts with `[Feature]` | Missing prefix |
| Problem Statement | Body contains "Problem Statement" section | Missing or empty |
| Target Users | Body contains "Target Users" section | Missing or empty |
```

---

## 5. Mission Modes (PM Example)

### YAML Input

```yaml
missionModes:
  required: true
  prompt: |
    Which mode should I operate in?

    1. **PLAN EXECUTION MODE** - Actively push work to completion
    2. **TRACK MODE** - Passively monitor and report

  modes:
    plan_execution:
      description: Execute existing plan per ticket checklist
      behaviors:
        - Assign tickets to workers and invoke their skills
        - Push work forward continuously
      preConditions:
        - All work must pass Definition of Ready
```

### Generated MD Output

```markdown
## Mission Mode Selection (MANDATORY - ASK FIRST)

**CRITICAL**: At session start, PM MUST ask the user which mission mode to operate in.

```
Which mode should I operate in?

1. **PLAN EXECUTION MODE** - Actively push work to completion
2. **TRACK MODE** - Passively monitor and report
```

**DO NOT PROCEED** until user selects a mode. This is non-negotiable.

### Plan Execution Mode

Execute existing plan per ticket checklist

**Behaviors:**
- Assign tickets to workers and invoke their skills
- Push work forward continuously

**Pre-conditions:**
- All work must pass Definition of Ready
```

---

## 6. Workflow

### YAML Input

```yaml
workflow:
  phases:
    - name: Review Ticket Spec
      required: true
      steps:
        - Verify ticket has Technical Spec + Gherkin
        - Check for resource name, fields, ownership model
        - Route to SA if spec incomplete

    - name: Implementation
      required: true
      steps:
        - action: SQLModel classes
          location: app/models/<resource>.py
        - action: DDL
          location: sql/schema.sql
```

### Generated MD Output

```markdown
## Workflow

### Phase 1: Review Ticket Spec

1. Verify ticket has Technical Spec + Gherkin
2. Check for resource name, fields, ownership model
3. Route to SA if spec incomplete

### Phase 2: Implementation

1. **SQLModel classes** - app/models/<resource>.py
2. **DDL** - sql/schema.sql
```

---

## 7. Custom Sections

### YAML Input

```yaml
customSections:
  - id: tech-stack
    title: Tech Stack
    content: |
      - **FastAPI**: Python web framework with automatic OpenAPI docs
      - **PostgreSQL**: Relational database with strong consistency

  - id: sql-vs-orm
    title: Raw SQL vs ORM Decision
    content: |
      **DEFAULT**: Use SQLModel ORM for 95% of operations.

      | Use SQLModel ORM | Use Raw SQL |
      |------------------|-------------|
      | Standard CRUD | Complex aggregations |
```

### Generated MD Output

```markdown
## Tech Stack

- **FastAPI**: Python web framework with automatic OpenAPI docs
- **PostgreSQL**: Relational database with strong consistency

## Raw SQL vs ORM Decision

**DEFAULT**: Use SQLModel ORM for 95% of operations.

| Use SQLModel ORM | Use Raw SQL |
|------------------|-------------|
| Standard CRUD | Complex aggregations |
```

---

## 8. Handoff Patterns

### YAML Input

```yaml
handoff:
  receivesWorkFrom:
    - PM
    - Solutions Architect
  returnsTo: PM
  canInvoke:
    - Code Reviewer
    - Project Coordinator
  invokedBy:
    - PM
```

### Generated MD Output

```markdown
## Handoff Patterns

**Receives work from**: PM, Solutions Architect
**Returns completed work to**: PM
**Can invoke**: Code Reviewer, Project Coordinator
**Invoked by**: PM
```

---

## Summary: What YAML Captures vs What Template Generates

| Aspect | YAML Captures | Template Generates |
|--------|---------------|-------------------|
| **Frontmatter** | Raw values | Formatted frontmatter |
| **Preamble** | Capability flags | Full preamble text with correct role type |
| **Boundaries** | Lists | Formatted sections with "that's X" attribution |
| **Quality Gates** | Structured checks | Tables with verification columns |
| **Mission Modes** | Mode definitions | Full prompt + mode details |
| **Workflow** | Phase/step lists | Numbered sections with proper formatting |
| **Custom Sections** | Raw markdown | Inserted at correct positions |
| **Handoff** | Lists | Formatted summary |
| **References** | Path + purpose | Formatted lists |
| **Related Skills** | Structured data | Tables by relationship type |

## Benefits of This Approach

1. **Single source of truth** — YAML is authoritative, MD is generated
2. **Explicit boundaries** — `authorizedActions` and `prohibitions` are required fields
3. **No preamble drift** — Preamble generated from capabilities, always consistent
4. **Validation possible** — Schema can be checked before generation
5. **Bulk updates** — Change template → regenerate all skills
6. **Nothing lost** — Custom sections preserve skill-specific content
