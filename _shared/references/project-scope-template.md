# Project Scope Template for claude.md

Copy this section into your project's `claude.md` file and customize for your project.

---

## Project Scope: [Project Name]

### Linear Context

**IMPORTANT**: Before creating any Linear issues, fetch available options from Linear and let the user select.

#### Default Pre-selections (Optional)

If this project typically uses specific Team/Project, list them here for pre-selection:

| Field | Default Value | Notes |
|-------|---------------|-------|
| Team | [Team Name] | Pre-selected but user confirms |
| Project | [Project Name] | Pre-selected but user confirms |
| Initiative | [Initiative Name or "None"] | If workspace has Initiatives |

#### Issue Creation Workflow

When creating issues, roles must:

1. **Fetch options from Linear** (`list_teams`, `list_projects`)
2. **Present options to user** with defaults pre-selected (if defined above)
3. **Let user select or create new** - never assume
4. **Create issue with confirmed context**

```
Before creating this issue, please select:

**Team**: (fetched from Linear)
1. Platform Team ← (default)
2. Portal Team
3. [Other]

**Project**: (fetched from Linear)
1. User Auth System ← (default)
2. Q1 Improvements
3. [Create new]

Which should I use?
```

### Domain Ownership

Define who owns what on this project. Each row should have ONE owner - avoid shared ownership.

| Domain | Owner Role | Owner Name/Team | Notes |
|--------|-----------|-----------------|-------|
| Frontend Architecture | Solutions Architect | @frontend-sa | Portal team UI |
| Frontend Implementation | Frontend Developer | Portal Team | - |
| Backend APIs | Solutions Architect | @backend-sa | Platform team |
| Backend Implementation | Backend Developer | Platform Team | - |
| Data Pipeline | Data Platform Engineer | @data-dpe | Analytics |
| AI Features | AI Integration Engineer | @ai-engineer | Search & recommendations |
| API Contracts | API Designer | @api-designer | Customer-facing APIs |
| Product Requirements (Portal) | TPO | @portal-tpo | Customer portal features |
| Product Requirements (Admin) | TPO | @admin-tpo | Admin dashboard features |
| Delivery Coordination | TPgM | @tpgm | All workstreams |

### Active Roles on This Project

List which skill roles are active and who fills them:

| Role | Person/Team | Scope |
|------|-------------|-------|
| Solutions Architect | @sa-name | Frontend + Backend architecture |
| TPO | @tpo-name | Customer Portal features only |
| TPgM | @tpgm-name | All workstreams |
| API Designer | @api-name | /api/v1/* endpoints |
| Data Platform Engineer | @dpe-name | Customer DB, Analytics DW |

### Cross-Domain Protocol

When working outside your owned domain:

1. **Document** the gap, dependency, or observation
2. **Tag** the domain owner in Linear or documentation
3. **Do NOT** create tickets, propose implementations, or make decisions for that domain

### Scope Clarifications

Add project-specific clarifications here:

```
- Frontend Architecture decisions require SA sign-off
- Any database schema changes must go through DPE review
- AI feature requests should be routed to AI Integration Engineer
- All API contract changes need API Designer approval
```

### Domain Boundaries Diagram (Optional)

```
┌─────────────────────────────────────────────────────────┐
│                    Customer Portal                       │
│  ┌─────────────────┐    ┌─────────────────┐             │
│  │   Frontend      │    │    Backend      │             │
│  │   @frontend-sa  │◄──►│    @backend-sa  │             │
│  │   Portal Team   │    │   Platform Team │             │
│  └─────────────────┘    └────────┬────────┘             │
│                                  │                       │
│                         ┌────────▼────────┐             │
│                         │     Data        │             │
│                         │   @data-dpe     │             │
│                         │   Data Team     │             │
│                         └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

---

## Usage Notes

### When to Update This Section

- New team member joins the project
- Role ownership changes
- New domain is added (e.g., mobile app)
- Domain boundaries need clarification

### How Roles Should Use This

Each role with a "Scope Boundaries" section in their SKILL.md will:
1. Read this section before taking action
2. Check if their proposed work falls within their owned domain
3. Use the Cross-Domain Protocol for out-of-scope work

### Common Questions

**Q: What if a domain has no owner listed?**
A: Route to project lead / TPgM to assign ownership before proceeding.

**Q: What if I disagree with current boundaries?**
A: Discuss with project lead. Don't act outside boundaries without agreement.

**Q: What if it's urgent and owner is unavailable?**
A: Document the action taken, notify owner immediately when available, and flag as "boundary exception" in the ticket.
