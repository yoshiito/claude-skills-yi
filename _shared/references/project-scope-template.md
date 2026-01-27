# Project Scope Template for claude.md

Copy this section into your project's `claude.md` file and customize for your project.

---

## Project Scope: [Project Name]

### Team Context

**REQUIRED**: Define the team that owns this codebase. This drives ticket system and Git conventions.

| Field | Value | Notes |
|-------|-------|-------|
| **Team** | `[team-slug]` | Lowercase, used in branch names |
| **Team Name** | [Team Display Name] | Human-readable name |
| **Ticket System** | `linear` / `github` / `none` | **ENFORCED** - skills MUST use this system |
| **Main Branch** | `main` | Default branch for PRs |

**Key Principle**: One team owns one codebase. The team slug is used consistently across:
- Git branch names (`feature/{team}/...`)
- Ticket system Team assignment (if applicable)
- Code ownership

### Git Branching

**Branch at Feature level** - each Feature gets its own branch from Mission branch or `main`.

#### Branch Pattern

The pattern varies based on your ticket system:

| Ticket System | Pattern | Example |
|---------------|---------|---------|
| `linear` | `{type}/{team}/{LIN-XXX}-{description}` | `feature/platform/LIN-101-password-api` |
| `github` | `{type}/{team}/{GH-XXX}-{description}` | `feature/platform/GH-101-password-api` |
| `none` | `{type}/{team}/{description}` | `feature/platform/password-api` |

| Component | Source | Example |
|-----------|--------|---------|
| `type` | Work type | `feature`, `fix`, `refactor`, `docs`, `test` |
| `team` | Team Context above | `platform`, `portal`, `data` |
| `{ID}` | Ticket ID (if using ticket system) | `LIN-101`, `GH-101` |
| `description` | Brief slug | `password-reset-api` |

#### Examples by Ticket System

```bash
# With Linear
feature/platform/LIN-101-password-reset-api
fix/portal/LIN-102-login-validation

# With GitHub Issues
feature/platform/GH-101-password-reset-api
fix/portal/GH-102-login-validation

# Without ticket system
feature/platform/password-reset-api
fix/portal/login-validation
```

#### Workflow

```
main ─────────────────────────────────────────────────►
  │
  ├─ feature/platform/LIN-101-backend-api ──► PR → main
  ├─ feature/platform/LIN-102-frontend-ui ──► PR → main
  └─ docs/platform/LIN-103-documentation ──► PR → main
```

### Ticket System Context

**ENFORCEMENT**: The `Ticket System` field above is MANDATORY. Skills will:
- **REFUSE** to create markdown plan files if `linear` or `github` is configured
- **STOP** and ask for configuration if this field is missing
- **FAIL** explicitly if the configured tool is unavailable (won't silently fall back)

Configure based on your `Ticket System` setting above.

#### If using Linear (`linear`)

**IMPORTANT**: Before creating any Linear issues, fetch available options from Linear and let the user select.

| Field | Default Value | Notes |
|-------|---------------|-------|
| Linear Team | [Team Name] | Must match Linear exactly |
| Project | [Project Name] | Pre-selected but user confirms |
| Initiative | [Initiative Name or "None"] | If workspace has Initiatives |

**Issue Creation Workflow:**
1. **Fetch options from Linear** (`list_teams`, `list_projects`)
2. **Present options to user** with defaults pre-selected
3. **Let user select or create new** - never assume
4. **Create issue with confirmed context**

#### If using GitHub Issues (`github`)

| Field | Default Value | Notes |
|-------|---------------|-------|
| Repository | [owner/repo] | GitHub repository |
| Labels | [label1, label2] | Default labels for issues |

**Issue Creation Workflow:**
1. Create issue in the repository
2. Use `GH-XXX` (issue number) in branch names and commits
3. Link PRs to issues using `Closes #XXX` in PR description

#### If using no ticket system (`none`)

- Use descriptive branch names without ticket IDs
- Track work through PR descriptions and commit messages
- Document requirements in `docs/` or project wiki

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
| Delivery Coordination | PM | @pm-name | All workstreams |

### Active Roles on This Project

List which skill roles are active and who fills them:

| Role | Person/Team | Scope |
|------|-------------|-------|
| Solutions Architect | @sa-name | Frontend + Backend architecture |
| TPO | @tpo-name | Customer Portal features only |
| PM | @pm-name | All workstreams |
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

---

## Coding Standards

**REQUIRED for Code Reviewer**: This section defines project-specific coding standards that Code Reviewer enforces alongside baseline standards.

### Standards Hierarchy

Code Reviewer uses:
1. **Baseline Standards** (always apply) - `_shared/references/coding-standards-baseline.md`
2. **Project Standards** (this section) - Override or extend baseline

### Architecture Patterns

Define your project's architecture patterns:

```markdown
| Pattern | Rule | Example |
|---------|------|---------|
| Data Access | Repository pattern | `UserRepository`, not direct DB calls |
| Business Logic | Service layer | `UserService.create()`, not in controllers |
| API Structure | Controller → Service → Repository | No skipping layers |
| Dependency Injection | Constructor injection | No `new Service()` in business logic |
```

### Naming Conventions

Define project-specific naming:

```markdown
| Element | Convention | Example |
|---------|------------|---------|
| Files | kebab-case | `user-service.ts`, `order-repository.py` |
| Classes | PascalCase | `UserService`, `OrderRepository` |
| Functions | camelCase (TS/JS) or snake_case (Python) | `getUserById`, `get_user_by_id` |
| Variables | Same as functions | `userId`, `user_id` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT` |
| Database tables | snake_case, plural | `users`, `order_items` |
| API endpoints | kebab-case | `/api/v1/user-profiles` |
```

### API Standards

Define your API conventions:

```markdown
- **Authentication**: All endpoints authenticated except `/health`, `/docs`
- **Versioning**: URL prefix `/api/v1/`
- **Error Format**: RFC 7807 Problem Details
- **Pagination**: Cursor-based, max 100 items
- **Rate Limiting**: 100 req/min per user
```

### Testing Requirements

Define testing expectations:

```markdown
| Type | Coverage | Required For |
|------|----------|--------------|
| Unit Tests | 80%+ | Business logic, utilities |
| Integration Tests | Required | All API endpoints |
| E2E Tests | Required | Critical user flows |
| Performance Tests | Optional | High-traffic endpoints |

**Test Naming**: `test_<function>_<condition>_<expected_result>`
Example: `test_create_user_with_duplicate_email_returns_409`
```

### Code Review Criteria

Define what Code Reviewer should specifically check:

```markdown
**Always Check:**
- [ ] Follows Repository/Service/Controller pattern
- [ ] No business logic in controllers
- [ ] Database queries use ORM, no raw SQL
- [ ] API responses match OpenAPI spec
- [ ] Error handling returns proper HTTP codes
- [ ] New endpoints have integration tests

**Project-Specific Rules:**
- [ ] [Add your project-specific rules]
- [ ] [Add your project-specific rules]
```

### Overrides from Baseline

If you need to override baseline standards, document explicitly:

```markdown
| Baseline Rule | Project Override | Rationale |
|---------------|------------------|-----------|
| 80% test coverage | 70% for legacy modules | Migration in progress |
| No raw SQL | Raw SQL allowed in reports/ | Performance-critical queries |
```

### Approved Libraries/Patterns

List pre-approved choices to avoid bikeshedding:

```markdown
| Category | Approved Choice | Alternatives Rejected |
|----------|-----------------|----------------------|
| HTTP Client | axios | fetch (no interceptors), request (deprecated) |
| ORM | SQLAlchemy | Django ORM (not using Django) |
| Testing | pytest | unittest (less readable) |
| Validation | Pydantic | marshmallow (slower) |
| Logging | structlog | stdlib logging (no structure) |
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
A: Route to project lead / PM to assign ownership before proceeding.

**Q: What if I disagree with current boundaries?**
A: Discuss with project lead. Don't act outside boundaries without agreement.

**Q: What if it's urgent and owner is unavailable?**
A: Document the action taken, notify owner immediately when available, and flag as "boundary exception" in the ticket.
