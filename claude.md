# Claude Code Skills Library

This repository contains reusable Claude Code skills for software engineering teams. Skills are role-based prompts that guide Claude through specific workflows with consistent quality.

## Project Purpose

Build and maintain a library of AI coding agent skills that:
- Define clear role boundaries (who does what)
- Enforce quality standards (templates, checklists)
- Support agentic workflows (AI Coding Agents + Agent Testers)
- Work with multiple project management systems (Linear, GitHub Projects, plan files)

## Repository Structure

```
skills/
├── _shared/references/       # Shared documentation used by multiple skills
│   ├── ticket-templates.md   # Story/Task and Bug templates (MANDATORY)
│   ├── ticketing-core.md     # Universal ticketing rules
│   ├── ticketing-linear.md   # Linear-specific commands
│   ├── ticketing-github-projects.md  # GitHub Projects commands
│   ├── ticketing-plan-file.md        # No-system tracking
│   └── skill-ecosystem.md    # How skills relate to each other
├── technical-product-owner/  # TPO skill (what/why)
├── solutions-architect/      # SA skill (how it fits together)
├── technical-program-manager/# TPgM skill (delivery coordination)
├── backend-*/                # Backend development skills
├── frontend-*/               # Frontend development skills
├── *-tester/                 # Testing skills
└── [other-skills]/           # Domain-specific skills
```

## Skill File Convention

Each skill follows this structure:
```
{skill-name}/
├── SKILL.md              # Main skill definition (required)
└── references/           # Skill-specific reference files (optional)
```

## Key Concepts

### Acceptance Criteria Format (Hybrid)

All tickets use a hybrid acceptance criteria format:
- **Technical Spec**: MUST/MUST NOT/SHOULD constraints (guardrails for AI Coding Agents)
- **Gherkin Scenarios**: Given/When/Then (validation for Agent Testers)

### INVEST Principle (Agentic)

Sub-issues follow INVEST adapted for AI agents:
- **I**ndependent - Can start without waiting (or set `blockedBy`)
- **N**egotiable - Approach flexible, criteria fixed
- **V**aluable - Moves feature toward "Done"
- **E**stimable - Bounded scope: known files, clear end state
- **S**mall - Single logical change (one PR, one concern)
- **T**estable - Technical Spec + Gherkin scenarios verifiable

### Role Boundaries

| Layer | Roles | Responsibility |
|-------|-------|----------------|
| Product Definition | TPO | What and Why (MRDs) |
| Architecture | Solutions Architect, API Designer | How it fits together (ADRs, contracts) |
| Implementation | Backend/Frontend Developers | Build it |
| Quality | Testers | Verify it |
| Documentation | Tech Doc Writer | Document it |
| Delivery | TPgM | Coordinate it |

## When Editing Skills

1. **Read the existing skill** before making changes
2. **Check `_shared/references/`** for templates and standards
3. **Maintain consistency** with related skills (TPO ↔ SA ↔ TPgM)
4. **Update checklists** when adding new requirements
5. **Test the skill** by invoking it with a sample task

### Contradiction Detection

Before saving any skill edit, check for contradictions with existing skills:

1. **Search for overlapping responsibilities** - grep related skills for similar terms
2. **Compare role boundaries** - ensure no two skills claim the same responsibility
3. **Check ticket ownership** - only one role should create/own each artifact type

**If contradictions found:**
- Present both statements to user
- Ask: "These statements appear to conflict. How should I resolve?"
- Options: Keep existing, use new, merge, or clarify distinction

Example contradictions to catch:
- Two roles claiming to "create sub-issues"
- Conflicting template requirements
- Overlapping workflow phases

## Common Tasks

### Adding a New Skill

**Pre-Creation Checklist:**
- [ ] Role doesn't duplicate existing skill responsibilities
- [ ] Clear boundary with adjacent roles defined
- [ ] No contradictions with existing skills

**Required Sections in SKILL.md:**

```markdown
---
name: skill-name
description: One-line description for skill selection
---

# Skill Name

[Brief purpose statement]

## Usage Notification

**REQUIRED**: When triggered, state: "[emoji] Using [Skill Name] skill - [what you're doing]."

## Core Objective

[What this role does and WHY it exists]

## Role Boundaries

**This role DOES:**
- [Explicit responsibility 1]
- [Explicit responsibility 2]

**This role does NOT do:**
- [Explicit non-responsibility 1] (that's [Other Role])
- [Explicit non-responsibility 2] (that's [Other Role])

## Project Management Integration

This role interacts with project management systems:
- **Creates**: [ticket types this role creates, if any]
- **Updates**: [ticket types this role updates]
- **Reads**: [what this role needs to read]

See `_shared/references/ticketing-core.md` for system-specific commands.

## Workflow

[Phases and steps]

## Quality Checklist

[Role-specific checklist]

## Related Skills

[How this role connects to others]
```

**Post-Creation Steps:**
1. Add to `_shared/references/skill-ecosystem.md`
2. Update related skills' "Related Skills" sections
3. Verify no contradictions introduced

### Updating Ticket Templates
1. Edit `_shared/references/ticket-templates.md`
2. Update corresponding checklists in TPO, SA, TPgM skills
3. Update `ticketing-core.md` INVEST checklist if needed

### Adding a New Ticketing System
1. Create `_shared/references/ticketing-{system}.md`
2. Map 4-level hierarchy (Initiative → Project → Issue → Sub-Issue)
3. Add CLI/MCP commands for CRUD operations
4. Add to system list in `ticketing-core.md`

## Quality Standards

- No open questions in final documents (MRDs, PRDs, ADRs)
- All tickets follow templates from `ticket-templates.md`
- Technical Spec defines guardrails for AI Coding Agents
- Gherkin scenarios define validation for Agent Testers
- Progress comments required at lifecycle points
- All skills must declare themselves when activated (Usage Notification)
- All skills must define explicit boundaries (DOES / does NOT do)
- No contradictory statements across skills
