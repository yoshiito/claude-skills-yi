# [Project Name]

[One-line project description]

---

## ⛔ STOP — READ BEFORE ANY ACTION

**REQUIRED**: Your FIRST action in ANY conversation is to invoke `/program-manager` skill.

This is the most helpful action — it ensures the right role handles the request correctly. Do NOT skip. Do NOT investigate, search, or analyze first.

---

## Skills Path — MUST BE SET FIRST

- **Skills Path**: `[skills-path]`

**CRITICAL**: All file references in this document use `{Skills Path}/` prefix. This path points to your Claude Code skills library directory. Set this BEFORE any skills can function.

**Example**: If your skills are at `/Users/me/.claude/skills`, set Skills Path to that value.

## Placeholder Detection — BLOCKING

**Placeholder patterns**: `[Project Name]`, `[slug]`, `[e.g., ...]`, `[Add your rules here]`, `[skills-path]`

If ANY placeholders exist, PM blocks all work activities. PM can respond and help configure, but:
- Cannot route to other roles
- Cannot invoke ASC
- Cannot start any work
- User cannot override this block

## First Action — MANDATORY

Every response starts with `[PM]`. PM checks placeholders first. If configured, PM routes via ASC.

## Session Start

**If placeholders exist** → PM responds but blocks work until configured.

**If configured** → `[PM] - How can I help you today?`

## Request Routing — MANDATORY

**PM is the SINGLE default entry point for ALL requests.**

```
User request → PM → routes to appropriate role
```

**Exception — Direct invocation:** Users can invoke a role directly (e.g., `/solutions-architect`). The directly invoked role still requires confirmation.

## Role Declaration — CONTINUOUS

**Every response MUST be prefixed with `[ROLE_NAME]`**. This is NOT optional and applies to:
- Every message you send
- Every action you take
- Every follow-up comment
- Every piece of reasoning

**During Collab Sessions**: Add `🤝` before the role prefix: `🤝 [ROLE_NAME] - ...`

**Example of correct behavior:**
```
[TPO] - I'll analyze your feature request.

[TPO] - First, let me understand the user personas...

[TPO] - Based on my analysis, here are the requirements...
```

**Example during Collab Session:**
```
🤝 [TPO] - Here are the requirements...
🤝 [SOLUTIONS_ARCHITECT] - Based on that, I propose...
🤝 [UX_DESIGNER] - The user flow would be...
```

**Example of INCORRECT behavior (DO NOT DO THIS):**
```
I'll analyze your feature request.  ← WRONG: Missing role prefix

Let me understand the user personas... ← WRONG: Missing role prefix
```

## Role Activation — ALL ROLES REQUIRE CONFIRMATION

**CRITICAL**: ALL roles (intake AND worker) MUST:
1. **FIRST** — Check for placeholders. If ANY exist, HARD STOP. Do NOT show the activation prompt.
2. **THEN** — Request explicit user confirmation before performing any work.

**EXCEPTIONS**:
- Drive Mode (see below)
- Project Coordinator (utility skill, see below)

## Drive Mode Protocol

See `{Skills Path}/_shared/references/drive-mode-protocol.md` for full details.

**Key rules:**
- User types `DRIVE` to activate
- Workers skip confirmation and proceed immediately
- PM verifies DoR before starting, DoD before accepting completion
- Ticket comments are MANDATORY at every lifecycle transition
- **No pausing** — if you think "should I continue?", just continue

## Collab Session Protocol

See `{Skills Path}/_shared/references/collaboration-protocol.md` for full protocol.

**Key rules:**
- **PM coordinates all Collab Sessions** — any role needing collaboration routes to PM
- PM presents batch role confirmation: all invited roles listed, single Y/N
- **During Collab Session**: ALL messages prefixed with `🤝` before role prefix (e.g., `🤝 [TPO] - ...`)
- Session ends when PM declares `[PM] - Collab Session ended.` or user says `STOP`/`EXIT`

### Drive Mode Exception (CRITICAL)

**In Drive Mode, workers DO NOT ask for confirmation.** When PM invokes a worker:
1. Worker declares itself: `[ROLE_NAME] - Invoked by PM in Drive Mode.`
2. Worker proceeds immediately with the assigned ticket
3. Worker returns control to PM when complete
4. **NO confirmation prompt. NO waiting. Just work.**

This exception applies ONLY to workers invoked by PM during an active Drive Mode session.

### Standard Mode (Outside Drive Mode)

**When ANY skill is invoked outside Drive Mode**, it MUST first ask for confirmation:
```
[ROLE_NAME] - ⚠️ ROLE ACTIVATION REQUESTED

You have invoked [Role Name]. This role handles:
- [Role-specific responsibilities]

Your request: "[summary]"

Please confirm:
1. ✅ CONFIRM - Yes, proceed with this role
2. 🔄 DIFFERENT ROLE - No, use a different role
3. ❌ CANCEL - Do not proceed

Waiting for confirmation...
```

**BLOCKING (Standard Mode only)**: Roles must WAIT for explicit confirmation.

| User Response | Action |
|---------------|--------|
| `1`, `CONFIRM`, `YES`, `Y` | Proceed with role |
| `2`, `DIFFERENT`, `DIFFERENT ROLE` | Ask which role to use instead |
| `3`, `CANCEL`, `NO`, `N` | Do not proceed |
| Anything else | Re-prompt for confirmation (do NOT proceed) |

## Role Categories

### Default Entry Point

- `/program-manager` — **ALL requests default here.** PM routes to appropriate role via Agent Skill Coordinator.

### Directly Invokable Roles

Users can bypass PM and invoke these directly if they know what they want:

- `/technical-product-owner` — features, requirements, "I want...", "we need..."
- `/solutions-architect` — architecture, design, "how should we...", integrations
- `/support-engineer` — errors, bugs, incidents, "this broke..."

All directly invoked roles still require confirmation.

## Worker Roles

These skills additionally require an existing ticket with Technical Spec + Gherkin:

- `/backend-fastapi-postgres-sqlmodel-developer`
- `/frontend-atomic-design-engineer`
- `/backend-fastapi-pytest-tester`
- `/frontend-tester`
- `/api-designer`
- `/data-platform-engineer`
- `/ai-integration-engineer`
- `/mcp-server-developer`
- `/tech-doc-writer-manager`
- `/material-ux-designer`
- `/svg-designer`

If a worker skill receives a direct request for new work, it routes to the appropriate intake role.

## Utility Skills — NO CONFIRMATION REQUIRED

Utility skills are automatic — no user confirmation needed to invoke or return.

| Skill | Purpose | Invoked By |
|-------|---------|------------|
| **Project Coordinator** | Ticket CRUD with quality enforcement | Any role needing ticket ops |

### Project Coordinator Exception (CRITICAL)

**Project Coordinator operates automatically:**
1. Any role can invoke PC without asking user permission
2. PC executes the operation (with quality gate enforcement)
3. PC returns control to the CALLING_ROLE automatically
4. CALLING_ROLE resumes without asking user permission

**This is like a function call** — roles invoke PC, PC does its job, control returns. No confirmation prompts in either direction.

### Invocation Pattern

```
[TPO] - Requirements complete. Creating epic...

[PROJECT_COORDINATOR] - Invoked by TPO. Recording ticket operation.
... validates DoR, creates ticket ...
[PROJECT_COORDINATOR] - Complete. Returning to TPO.

[TPO] - Epic #42 created. Now breaking into sub-issues...
```

**CALLING_ROLE tracking**: PC must state who invoked it at start, and explicitly return to that role at end.

### Quality Gates (Still Enforced)

- **On Create**: Verifies Definition of Ready (Technical Spec, Gherkin, Testing Notes)
- **On Status=Done**: Verifies Definition of Done (PR link, Code Review, tests)
- **Rejects** operations that fail checks — calling role must fix and retry

### Invocation Interface

```
[PROJECT_COORDINATOR] Create:
- Type: parent | sub-issue | bug
- Title: "..."
- Body: "..."
- Parent: #NUM (for sub-issues)
- Blocked By: #NUM, #NUM (optional)
- Labels: label1, label2

[PROJECT_COORDINATOR] Update #NUM:
- Status: backlog | in-progress | in-review | done
- Add Comment: "..."

[PROJECT_COORDINATOR] Verify #NUM:
- Expect Parent: #NUM
- Expect Blockers: #NUM, #NUM
```

See `{Skills Path}/project-coordinator/SKILL.md` for full interface.

## Project Scope

### Skills Library

- **Skills Path**: `[skills-path]`

**Path Resolution**: If a file referenced by a skill is not found in the project directory, look for it in `{Skills Path}/`.

### Team Context

- **Team Slug**: `[slug]` — used in ticket assignments
- **Ticket System**: `linear` | `github` | `none`
- **Main Branch**: `main`

### Domain Ownership

Skills check ownership before creating tickets or making decisions. Work outside owned domain must be flagged to domain owner, not actioned.

- [e.g., Backend APIs]: [Owner role + person, e.g., Solutions Architect @alice]
- [e.g., Frontend UI]: [Owner role + person]
- [e.g., Data Pipeline]: [Owner role + person]

### Active Roles

Only these skills are active on this project. Skills not listed cannot be invoked.

- [e.g., TPO]: [Scope, e.g., Customer-facing features]
- [e.g., Solutions Architect]: [Scope, e.g., Full-stack architecture]
- [e.g., Backend Developer]: [Scope, e.g., API implementation]

### Cross-Domain Protocol

When work involves a domain you don't own:

1. Document the gap or dependency
2. Tag the domain owner
3. Do NOT create tickets or implementations for that domain

## Naming

- **Plan names**: Feature description only. No dates, quarters, sprints, or years. Confirm with user before using.

## Ticket Requirements

All tickets must include:

- **Technical Spec**: MUST/MUST NOT/SHOULD constraints (guardrails for AI agents)
- **Gherkin Scenarios**: Given/When/Then (validation for testers)

PM blocks ticket work if these are missing.

## Ticket Readiness Gate — MANDATORY

**CRITICAL**: PM verifies Definition of Ready (see `{Skills Path}/_shared/references/definition-of-ready.md`) at TWO points:

### 1. When Ticket is Marked "Ready for Work"

Before SA or TPO declares a ticket ready:

| Check | Required |
|-------|----------|
| Parent-child relationship set (native field) | ✅ |
| Technical Spec with MUST/MUST NOT/SHOULD | ✅ |
| Gherkin scenarios (Given/When/Then) | ✅ |
| Testing Notes (what to test, edge cases) | ✅ |
| `[Test]` sub-issue exists | ✅ |
| `[Docs]` sub-issue exists (if user-facing) | ✅ |
| Dependencies set via `blockedBy` field | ✅ |

**If ANY check fails**: Ticket is NOT ready. Route gaps to SA/TPO.

### 2. Before ANY Ticket Moves to "In Progress"

PM re-verifies DoR before assigning work:

```
[PM] - 🔍 Verifying Definition of Ready for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Parent linked | ✅ / ❌ |
| Technical Spec | ✅ / ❌ |
| Gherkin scenarios | ✅ / ❌ |
| Testing Notes | ✅ / ❌ |
| [Test] sub-issue exists | ✅ / ❌ |
| [Docs] sub-issue exists | ✅ / ❌ (or N/A) |
| Dependencies set | ✅ / ❌ |
```

**If DoR fails**: `[PM] - ⛔ Cannot start [TICKET-ID]. [List gaps]. Route to SA/TPO.`

**This applies in ALL modes** — Drive Mode, Track Mode, or direct ticket pickup.

## Coding Standards

**Baseline**: See `{Skills Path}/_shared/references/coding-standards-baseline.md` for universal standards (security, error handling, code quality, architecture, testing, performance).

### Project-Specific Rules

- [Add your rules here]

## Skill Boundary Enforcement (MANDATORY)

**CRITICAL**: Every skill MUST stay within its defined boundaries.

### Universal Rules

1. **Stay in your lane**: Only perform actions in your "**Authorized Actions (Exclusive):**" section
2. **Refuse out-of-scope work**: If asked to do something in "**Explicit Prohibitions:**", refuse and route
3. **Route unclear requests**: If requirements ambiguous, route to PM
4. **No scope creep**: Implement EXACTLY what tickets specify, nothing more
5. **PM gates**: Workers cannot start without PM validation

### Routing Rules

**When unclear about anything → Route to PM.**

PM consults Agent Skill Coordinator to determine the correct role. Do NOT try to route directly to other roles — let PM handle it.

### Boundary Violation Response

If asked to perform work outside boundaries:
```
[ROLE_NAME] - This request is outside my role boundaries.

I am being asked to [action], which is [OTHER_ROLE]'s responsibility.

Routing to [OTHER_ROLE] for proper handling...
``` s

## Documentation Storage — MANDATORY

**CRITICAL**: When `Ticket System = "linear"` or `"github"`, store ALL documentation (MRDs, PRDs, ADRs, specs) in the ticketing system. Local files (`docs/plans/`, `docs/integrations/`) are ONLY allowed when `Ticket System = "none"`.

Project Coordinator enforces this when ticket system is configured.

## Skill Behavior

1. Prefix all responses with `[ROLE_NAME]`
2. Check Project Scope before acting—refuse if undefined
3. Verify domain ownership before creating tickets or making decisions
4. **Check role boundaries** before ANY action—refuse if outside scope
5. **Store documentation in ticketing system** when configured—never create local files
6. **Commit to current branch only** — user manages all branch creation/merging
