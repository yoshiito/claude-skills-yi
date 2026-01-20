# Ticketing Core Rules

Universal rules for all ticket systems. System-specific mappings and commands are in separate files.

## PM Tool Enforcement (MANDATORY)

**CRITICAL**: Skills MUST use the project's configured ticket system. Falling back to markdown files when a proper PM tool is configured is a VIOLATION.

### Pre-Work Check (Required Before ANY Ticket Operation)

```
1. READ project's claude.md → find "Ticket System" field
2. IF Ticket System = "linear" → MUST use Linear MCP commands
3. IF Ticket System = "github" → MUST use GitHub Issues/Projects
4. IF Ticket System = "none" → ONLY THEN use plan files
5. IF Ticket System field is MISSING → ASK user to configure it first
```

### Enforcement Rules

| Configured System | Allowed | NOT Allowed |
|-------------------|---------|-------------|
| `linear` | Linear MCP commands | Creating `docs/plans/*.md`, markdown checklists as tickets |
| `github` | `gh` CLI, GitHub API | Creating `docs/plans/*.md`, markdown checklists as tickets |
| `none` | `docs/plans/*.md` | N/A (this is the fallback) |

### Failure Modes to Avoid

**DO NOT**:
- Create a markdown plan file "because Linear is slow"
- Use `docs/plans/` when Linear/GitHub is configured
- Assume "no MCP available" without checking
- Fall back to markdown "temporarily"
- Create local MRD/PRD/ADR files when ticketing system is configured
- Create `questions.md` files when ticketing system is configured

**IF PM tool is unavailable** (MCP not connected, API error):
1. STOP and inform user: "Linear MCP is not available. Please connect it or change Ticket System to 'none'."
2. DO NOT proceed with markdown fallback
3. Wait for user decision

## Documentation Storage Rules (MANDATORY)

**CRITICAL**: ALL documentation content must be stored in the ticketing system when one is configured.

### What Goes Where

| Ticket System | MRD/PRD | ADRs | Questions | Specs |
|---------------|---------|------|-----------|-------|
| `linear` | Parent Issue description | Sub-issue descriptions or comments | Issue comments | Sub-issue descriptions |
| `github` | Parent Issue description | Sub-issue descriptions or comments | Issue comments | Sub-issue descriptions |
| `none` | `docs/plans/{name}/mrd.md` | `docs/integrations/{vendor}/adr.md` | `docs/plans/{name}/questions.md` | Local files |

### Enforcement

When `Ticket System = "linear"` or `"github"`:

```
✅ ALLOWED:
- Store MRD content in parent Issue description
- Store PRD content in parent Issue description (updated)
- Store ADRs in sub-issue descriptions or linked comments
- Track questions in Issue comments
- Store Technical Specs in sub-issue descriptions

❌ NOT ALLOWED:
- Create docs/plans/*.md files
- Create docs/integrations/*.md files
- Create questions.md files
- Create mrd.md or prd.md files
- Create any local documentation files
```

### Why This Matters

1. **Single source of truth** - All context lives in ticketing system
2. **Traceability** - Direct link from requirements to implementation
3. **AI agent efficiency** - Agents find context in tickets, not scattered files
4. **No orphaned docs** - Documentation doesn't get out of sync with tickets

### Example Enforcement Check

```python
# Pseudocode every skill should follow:
ticket_system = read_claude_md().get("Ticket System")

if ticket_system == "linear":
    if not mcp_linear_available():
        STOP("Linear MCP not connected. Cannot proceed.")
    use_linear_commands()  # REQUIRED

elif ticket_system == "github":
    if not gh_cli_available():
        STOP("GitHub CLI not available. Cannot proceed.")
    use_github_commands()  # REQUIRED

elif ticket_system == "none":
    use_plan_files()  # OK

else:
    ASK_USER("Ticket System not configured. Please set it in claude.md.")
```

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

## Pre-Creation Checklist

**CRITICAL**: Never assume project context. Always confirm before creating.

- [ ] Fetch available options from ticket system (teams, projects)
- [ ] Present options to user for selection
- [ ] Confirm: team, project, assignee
- [ ] If project doesn't exist, create it first

## Sub-Issue Quality Checklist (INVEST) - MANDATORY

**BLOCKING**: Sub-issues that fail INVEST checks MUST be revised before creation.

Before creating any sub-issue, verify ALL items:

### Independence Check
- [ ] Can start without waiting for others?
  - **If YES**: Mark as independent (no blockedBy)
  - **If NO**: Set `blockedBy` via native field (Linear: `blockedBy`, GitHub: GraphQL `addBlockedBy`)
- [ ] Dependencies set via native fields, NOT in issue body text

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
- [ ] Parent relationship set via native field (Linear: `parentId`, GitHub: GraphQL `addSubIssue` mutation)
- [ ] ADRs linked if architectural decisions involved?
- [ ] API specs linked if API work involved?

**STOP**: If any check fails, revise the sub-issue before creation.

## TPgM Mission Modes

**CRITICAL**: TPgM operates in one of two modes, selected at session start.

### Drive Mode (Active)

**PREREQUISITE**: Before Drive Mode can start, TPgM verifies **Definition of Ready** for ALL tickets.

See `definition-of-ready.md` for full checklist. Key checks:
- Parent Issue exists with MRD
- Sub-issues have Technical Spec + Gherkin scenarios + Testing Notes
- Dependencies set via native fields
- Assigned skill prefix (`[Backend]`, `[Frontend]`, etc.)
- No open questions
- `[Test]` sub-issue exists (MANDATORY - validates Gherkin scenarios)
- `[Docs]` sub-issue exists (for user-facing features)

**If DoR fails**: TPgM routes back to SA/TPO to complete definitions. Cannot drive incomplete work.

**If DoR passes**: TPgM actively pushes work to completion:

1. **Assigns tickets** to appropriate worker skills
2. **Invokes worker skills** directly to start work
3. **Monitors progress** and pushes for completion
4. **Resolves blockers** immediately - doesn't wait
5. **Validates completion** before moving to next ticket

**Workers in Drive Mode**: TPgM tells you what to do. Execute and report back.

### Track Mode (Passive)

In Track Mode, TPgM responds to requests:

1. Validates tickets when asked
2. Reports status when asked
3. Waits for workers to initiate

## TPgM Validation Gate (MANDATORY - Both Modes)

**CRITICAL**: No ticket moves to "In Progress" without TPgM validation.

### Before Starting Work (ALL Workers)

1. Verify TPgM has validated the ticket
2. Check no `blockedBy` issues are incomplete
3. Get TPgM clearance before moving to "In Progress"

**If TPgM has not validated:**
```
[WORKER_ROLE] - Cannot start work on this ticket.

TPgM validation required before moving to "In Progress".

Requesting TPgM validation...
```

## Mandatory Progress Updates

**All workers MUST update ticket status AND add comments at these points.**

### When Starting Work (After TPgM Validation)

**Status**: Move ticket to **In Progress**

**Comment**:
```markdown
🚀 **Started**
- Branch: `{branch-name}`
- Base: `{base_branch}` (confirmed with user)
- Approach: [Brief implementation approach]
```

### During Work (for tasks > 1 day)

**Status**: Keep as **In Progress**

**Comment**:
```markdown
📝 **Progress**
- Done: [What's completed]
- Next: [Current focus]
- Blockers: [Any issues]
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

**Status**: Move ticket to **Done** (or let auto-close on PR merge if supported)

**Comment**:
```markdown
✅ **Completed**
- PR merged: [link]
- Files: [Key files changed]
- Notes: [Anything for QA/next steps]
```

## Git Workflow

See `git-workflow.md` for complete Git workflow including:
- **Base branch confirmation** (MUST ask user before branching)
- Branch naming conventions
- Commit message format
- PR creation guidelines

**Key point**: Always ask the user which branch to branch from and merge back to. Do not assume `main`.

## Ticket Status Flow

| Stage | Status | Updated By |
|-------|--------|------------|
| Created | Backlog/Todo | TPO/Architect |
| Work started | In Progress | Worker |
| PR created | In Review | Worker |
| PR merged | Done | Worker/Auto |

## Role Responsibilities: Ticket Creators vs Workers

### Ticket Creator Roles (Who Creates Tickets)

| Skill Name | Creates | Template | INVEST Required |
|------------|---------|----------|-----------------|
| `technical-product-owner` | Parent Issues | MRD in description | N/A (parent issues) |
| `solutions-architect` | Sub-Issues | Story/Task template | **YES - MANDATORY** |
| `support-engineer` | Bug reports | Bug template | N/A (bugs) |

**Only these 3 roles create tickets.** All other roles work on existing tickets.

### Worker Roles (Who Works on Tickets)

| Skill Name | Works On | Updates | Does NOT Create |
|------------|----------|---------|-----------------|
| `backend-fastapi-postgres-sqlmodel-developer` | Sub-issues assigned to them | Status, progress comments | New sub-issues |
| `frontend-atomic-design-engineer` | Sub-issues assigned to them | Status, progress comments | New sub-issues |
| `backend-fastapi-pytest-tester` | Test sub-issues | Test coverage notes | Implementation tickets |
| `frontend-tester` | Test sub-issues | Test coverage notes | Implementation tickets |
| `tech-doc-writer-manager` | Doc sub-issues | Documentation links | Implementation tickets |
| `technical-program-manager` | Tracks all tickets | Delivery status | Implementation tickets |

### Role-Specific Responsibilities

**`technical-product-owner`**
- Creates parent Issues with MRD requirements
- Reviews sub-issues for alignment with requirements
- Verifies acceptance criteria before closing feature
- Does NOT create sub-issues (that's `solutions-architect`)

**`solutions-architect`**
- Breaks parent Issues into Sub-Issues after architecture design
- **MUST pass INVEST checklist** before creating any sub-issue
- Sets `parent` and `blockedBy` via native fields (not issue body)
- Links ADRs and technical specs

**`backend-fastapi-postgres-sqlmodel-developer` / `frontend-atomic-design-engineer`**
- Works on assigned sub-issues only
- Posts mandatory progress comments
- Commits with ticket ID prefix
- Updates status as work progresses
- Does NOT create new tickets (requests new work via TPO/SA)

**`backend-fastapi-pytest-tester` / `frontend-tester`**
- Works on test sub-issues assigned by SA
- Posts test coverage summary on completion
- Documents tested scenarios
- Does NOT create implementation tickets

**`tech-doc-writer-manager`**
- Works on doc sub-issues assigned by SA
- Posts documentation summary on completion
- Links to created/updated docs
- Does NOT create implementation tickets

**`technical-program-manager`**
- **In Drive Mode**: Actively assigns work, invokes worker skills, pushes to completion
- **In Track Mode**: Passively monitors, validates on request, reports status
- Validates tickets meet quality standards before work begins
- Verifies traceability before closing parent
- Escalates blockers
- Does NOT create implementation sub-issues
- Does NOT define requirements or architecture (routes to TPO/SA)

## Scope Boundary Check

Before creating tickets, verify ownership per project's `claude.md`:

- [ ] This domain is within my ownership?
- [ ] If NO: Document gap, tag domain owner, do NOT create ticket

## Worker Completion Checklist

Before marking any work as done:

- [ ] All commits reference ticket ID
- [ ] PR title includes ticket ID
- [ ] "Started" comment posted
- [ ] "Completed" comment posted
- [ ] Ticket status reflects reality
- [ ] Blockers/notes documented

## Ticket Templates

See `ticket-templates.md` for Story/Task and Bug templates.

## System-Specific References

- **Linear**: See `ticketing-linear.md`
- **GitHub Projects**: See `ticketing-github-projects.md`
- **No system**: See `ticketing-plan-file.md`
