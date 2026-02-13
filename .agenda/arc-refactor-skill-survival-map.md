# Skill Survival Map — Agent-Based Architecture Migration

**Companion to**: `arc-refactor-agent-based-proposal.md`

**Status**: Aligned on skills and agents. Next: Define MVP test plan.

---

## Agreed Decisions

### Design Principles

1. **Agent exists when tools or workflow differ.** Same tools + same workflow = knowledge skill, not agent.
2. **Skills are composable units.** Multiple skills per agent. Skills have references/ for deep detail.
3. **Three knowledge loading modes**: Always embedded, LSP auto-loaded, explicitly declared.
4. **Current file structure is irrelevant.** Patterns and knowledge are what matter.
5. **Program Manager is eliminated.** Mode transitions become slash-command skills. CLAUDE.md handles orchestration.
6. **Specialist backend roles merge into backend-developer.** MCP, AI, Data become knowledge skills loaded via LSP.
7. **Testers stay split** (BE/FE). Different workflows despite same tools.
8. **UX + SVG merge into designer.** Same workflow (design), same tools.
9. **Market researcher is a new agent.** Different tools (WebSearch/WebFetch) and different workflow from PO.
10. **Two doc writers.** Technical (developer-facing) and User (end-user-facing). Different tools (user needs Playwright).
11. **Plans live in PM system.** PO defines priority, SA maps dependencies, PC creates tickets.
12. **git-workflow is not a skill.** Two lines in coding-standards: work on current branch, merge before ticket done.

### Write Domain Restrictions

| Domain | Write Access | Everyone Else |
|---|---|---|
| Source code | backend-developer, frontend-developer, backend-tester, frontend-tester | Read-only |
| Project management | project-coordinator only (MCP) | No access |
| Technical docs | technical-doc-writer | Read-only |
| User docs | user-doc-writer | Read-only |
| Requirements | product-owner, market-researcher | Read-only |
| Architecture | solutions-architect | Read-only |
| Design | designer | Read-only |

---

## 13 Agents

| # | Agent | Category | Key Tool Differences | Blocking Config |
|---|---|---|---|---|
| 1 | product-owner | Intake | Read, Write, Edit, Glob, Grep | — |
| 2 | market-researcher | Intake | + WebSearch, WebFetch | — |
| 3 | solutions-architect | Intake | Read, Write, Edit, Glob, Grep | — |
| 4 | support-engineer | Intake | + Sentry MCP | — |
| 5 | project-coordinator | Gateway | + Bash, GitHub/Linear MCP | `team.ticketSystem` |
| 6 | backend-developer | Worker | + Bash | — |
| 7 | frontend-developer | Worker | + Bash | `conventions.componentArchitecture` |
| 8 | backend-tester | Worker | + Bash | — |
| 9 | frontend-tester | Worker | + Bash, Playwright MCP | — |
| 10 | designer | Worker | + Penpot MCP, Playwright MCP | `design.system` |
| 11 | code-reviewer | Review | Read, Glob, Grep only | — |
| 12 | technical-doc-writer | Worker | + Bash | — |
| 13 | user-doc-writer | Worker | + Bash, Playwright MCP | — |

---

## 26 Knowledge Skills

### Development Patterns

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `fastapi-patterns` | LSP auto-load | backend-developer, code-reviewer | Strong |
| `react-patterns` | LSP auto-load | frontend-developer, code-reviewer | Moderate — missing accessibility, TS, CSS |
| `ai-patterns` | LSP auto-load | backend-developer | Weak — missing reference files |
| `mcp-patterns` | LSP auto-load | backend-developer | Strong |
| `data-patterns` | LSP auto-load | backend-developer | Moderate — missing vector search |
| `api-design-patterns` | Always embedded | solutions-architect, backend-developer | Strongest (9/10) |

### Testing Patterns

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `pytest-patterns` | LSP auto-load | backend-tester, code-reviewer | Strong |
| `playwright-patterns` | LSP auto-load | frontend-tester, code-reviewer | Moderate |

### Standards & Conventions

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `coding-standards` | Always embedded | All devs, testers, code-reviewer | Moderate |
| `atomic-design` | Explicit config | frontend-developer, code-reviewer | Strong |
| `material-design` | Explicit config | designer | Strong (needs extraction from UX skill) |

### Review & Quality

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `review-patterns` | Always embedded | code-reviewer | Weak — operationally hollow |
| `definition-of-ready` | Always embedded | project-coordinator | Strong |
| `definition-of-done` | Always embedded | project-coordinator | Strong |

### Requirements & Research

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `prd-patterns` | Always embedded | product-owner | Strong |
| `mrd-patterns` | Always embedded | market-researcher | New — needs creation |

### Architecture

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `architecture-patterns` | Always embedded | solutions-architect | Strong |

### Support & Triage

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `triage-patterns` | Always embedded | support-engineer | Moderate |

### Project Coordination

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `ticket-management` | Always embedded | project-coordinator | Strong |
| `github-operations` | Conditional (`ticketSystem`) | project-coordinator | Strong |
| `linear-operations` | Conditional (`ticketSystem`) | project-coordinator | Moderate |

### Design

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `design-patterns` | Always embedded | designer | Strong |
| `penpot-patterns` | Always embedded | designer | Strong |
| `svg-patterns` | Always embedded | designer | Strong |

### Documentation

| Skill | Loading Mode | Agents | Assessment |
|---|---|---|---|
| `tech-doc-patterns` | Always embedded | technical-doc-writer | Moderate |
| `user-doc-patterns` | Always embedded | user-doc-writer | New — needs creation |

---

## Open: MVP Test Plan

What's the minimum we need to build and test to validate this architecture works?

(To be defined)