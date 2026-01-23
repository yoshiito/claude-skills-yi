# Ticketing Core Rules

Universal rules for all ticket systems. All ticket operations go through Project Coordinator skill.

## Single Rule

**ALL ticket operations go through Project Coordinator skill.**

Project Coordinator is a **UTILITY skill** - any role can invoke it directly without permission.

| Role | When | Invoke Project Coordinator With |
|------|------|--------------------------------|
| TPO | After defining feature | Create: Type=parent |
| SA | After architecture breakdown | Create: Type=sub-issue, Parent, BlockedBy |
| Support | After identifying bug | Create: Type=bug |
| TPgM | Before Drive Mode | Verify: Expect Parent, Expect Blockers |
| Workers | During implementation | Update: Status, Comment |

## Invocation

Any role needing a ticket operation:
1. Invokes Project Coordinator with structured request
2. **Project Coordinator verifies quality gates** (DoR for create, DoD for done)
3. If gates pass: executes the operation
4. If gates fail: **REJECTS with specific gaps** - calling role must fix and retry
5. Control returns to calling role

**No TPgM permission required.** This is a utility, not a workflow gate.

## Quality Enforcement (AUTOMATIC)

**Project Coordinator enforces Definition of Ready and Definition of Done.**

| Operation | Gate | On Fail |
|-----------|------|---------|
| Create sub-issue | DoR: Technical Spec, Gherkin, Testing Notes, Parent | REJECT - list missing items |
| Create parent | DoR: Title prefix, MRD content | REJECT - list missing items |
| Create bug | DoR: Required sections | REJECT - list missing items |
| Update status=done | DoD: PR link, Code Review, tests | REJECT - list missing evidence |

**Roles cannot bypass these gates.** Prepare complete content before invoking.

## DO NOT

- Use `gh issue create` directly
- Use Linear MCP directly
- Create plan files directly
- Read ticketing-github-projects.md (it moved to Project Coordinator)

Project Coordinator handles all tool-specific complexity.

---

## PM Tool Enforcement (MANDATORY)

**CRITICAL**: Skills MUST use the project's configured ticket system. Falling back to markdown files when a proper PM tool is configured is a VIOLATION.

### Pre-Work Check (Required Before ANY Ticket Operation)

```
1. READ project's claude.md → find "Ticket System" field
2. IF Ticket System = "linear" → Invoke Project Coordinator
3. IF Ticket System = "github" → Invoke Project Coordinator
4. IF Ticket System = "none" → Invoke Project Coordinator (uses plan files)
5. IF Ticket System field is MISSING → ASK user to configure it first
```

### Failure Modes to Avoid

**DO NOT**:
- Create a markdown plan file "because Linear is slow"
- Use `docs/plans/` when Linear/GitHub is configured
- Assume "no MCP available" without checking
- Fall back to markdown "temporarily"
- Create local MRD/PRD/ADR files when ticketing system is configured
- Create `questions.md` files when ticketing system is configured

**IF PM tool is unavailable** (MCP not connected, API error):
1. STOP and inform user: "PM tool is not available. Please connect it or change Ticket System to 'none'."
2. DO NOT proceed with markdown fallback
3. Wait for user decision

---

## Hierarchy (4 Levels)

All ticket systems map to this hierarchy:

| Level | Purpose | Created By |
|-------|---------|------------|
| **Initiative** | Strategic company goal | Leadership/TPO |
| **Project** | Time-bound deliverable | TPO |
| **Issue** | User-facing feature | TPO |
| **Sub-Issue** | Implementation work unit | Solutions Architect |

```
Initiative: "Q1 User Growth"
└── Project: "User Authentication System"
    └── Issue: "Implement Password Reset"
        ├── Sub-Issue: [Backend] Password reset API
        ├── Sub-Issue: [Frontend] Reset form UI
        └── Sub-Issue: [Docs] Password reset guide
```

## Sub-Issue Prefixes

| Prefix | Assigned To (exact skill name) | Includes |
|--------|--------------------------------|----------|
| `[Backend]` | `backend-fastapi-postgres-sqlmodel-developer` | Implementation + unit/integration tests |
| `[Frontend]` | `frontend-atomic-design-engineer` | UI + component/E2E tests |
| `[Docs]` | `tech-doc-writer-manager` | Documentation |
| `[API Design]` | `api-designer` | Contract design (when needed) |
| `[Test]` | `backend-fastapi-pytest-tester` or `frontend-tester` | Dedicated QA effort (when needed) |

---

## Sub-Issue Quality Checklist (INVEST) - MANDATORY

**BLOCKING**: Sub-issues that fail INVEST checks MUST be revised before creation.

Before creating any sub-issue, verify ALL items:

### Independence Check
- [ ] Can start without waiting for others?
  - **If YES**: Mark as independent (no blockedBy)
  - **If NO**: Set `blockedBy` via Project Coordinator
- [ ] Dependencies set via Project Coordinator (not in issue body text)

### Negotiable Check
- [ ] Approach is flexible (HOW is negotiable)?
- [ ] Acceptance criteria is fixed (WHAT is non-negotiable)?
- [ ] Technical Spec has MUST/MUST NOT/SHOULD constraints?

### Valuable Check
- [ ] Moves feature toward "Done"?
- [ ] Delivers user-visible or developer-visible value?
- [ ] Not just a "refactor for the sake of refactoring"?

### Estimable Check
- [ ] Bounded scope with known files?
- [ ] Clear end state defined?
- [ ] No open questions in the ticket?

### Small Check
- [ ] Single logical change?
- [ ] One PR, one concern?
- [ ] Can be completed in 1-3 days max?
- [ ] **If larger**: Break down into smaller sub-issues

### Testable Check
- [ ] Technical Spec defines verifiable constraints?
- [ ] Gherkin scenarios provide Given/When/Then validation?
- [ ] Agent Tester can verify completion without ambiguity?

### Context Check
- [ ] Parent relationship identified (Project Coordinator will set via native field)
- [ ] ADRs linked if architectural decisions involved?
- [ ] API specs linked if API work involved?

**STOP**: If any check fails, revise the sub-issue before creation.

---

## TPgM Mission Modes

**CRITICAL**: TPgM operates in one of two modes, selected at session start.

### Drive Mode (Active)

**PREREQUISITE**: Before Drive Mode can start, TPgM verifies **Definition of Ready** for ALL tickets.

See `definition-of-ready.md` for full checklist. Key checks:
- Parent Issue exists with MRD
- Sub-issues have Technical Spec + Gherkin scenarios + Testing Notes
- Dependencies set via native fields (verified via Project Coordinator)
- Assigned skill prefix (`[Backend]`, `[Frontend]`, etc.)
- No open questions
- `[Test]` sub-issue exists (MANDATORY - validates Gherkin scenarios)
- `[Docs]` sub-issue exists (for user-facing features)

**If DoR fails**: TPgM routes back to SA/TPO to complete definitions. Cannot drive incomplete work.

**If DoR passes**: TPgM actively pushes work to completion.

### Track Mode (Passive)

In Track Mode, TPgM responds to requests:
1. Validates tickets when asked
2. Reports status when asked
3. Waits for workers to initiate

---

## Mandatory Progress Updates

**All workers MUST update ticket status AND add comments at these points.**

Invoke Project Coordinator for all updates:

### When Starting Work (After TPgM Validation)

**Status**: Move ticket to **In Progress**

**Comment**:
```markdown
🚀 **Started**
- Branch: `{branch-name}`
- Base: `{base_branch}` (confirmed with user)
- Approach: [Brief implementation approach]
```

### When PR Created

**Status**: Move ticket to **In Review**

**Comment**:
```markdown
🔍 **Ready for review**
- PR: [link] (targeting {base_branch})
- Changes: [Brief summary]
- Tests: [What's covered]
```

### When Complete

**Status**: Move ticket to **Done**

**Comment**:
```markdown
✅ **Completed**
- PR merged: [link]
- Files: [Key files changed]
- Notes: [Anything for QA/next steps]
```

---

## Ticket Status Flow

| Stage | Status | Updated By |
|-------|--------|------------|
| Created | Backlog/Todo | TPO/Architect |
| Work started | In Progress | Worker (via Project Coordinator) |
| PR created | In Review | Worker (via Project Coordinator) |
| PR merged | Done | Worker (via Project Coordinator) |

---

## Role Responsibilities

### Ticket Creator Roles (Who Creates Tickets)

| Skill Name | Creates | Via |
|------------|---------|-----|
| `technical-product-owner` | Parent Issues | Project Coordinator |
| `solutions-architect` | Sub-Issues | Project Coordinator |
| `support-engineer` | Bug reports | Project Coordinator |

**Only these 3 roles create tickets.** All other roles work on existing tickets.

### Worker Roles (Who Works on Tickets)

Workers update tickets via Project Coordinator. They do NOT create new tickets.

---

## Git Workflow

See `git-workflow.md` for complete Git workflow including:
- **Base branch confirmation** (MUST ask user before branching)
- Branch naming conventions
- Commit message format
- PR creation guidelines

**Key point**: Always ask the user which branch to branch from and merge back to. Do not assume `main`.

---

## Ticket Templates

See `ticket-templates.md` for Story/Task and Bug templates.
