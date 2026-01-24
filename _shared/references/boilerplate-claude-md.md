# [Project Name]

[One-line project description]

## Placeholder Detection — HARD STOP

**CRITICAL**: If ANY placeholder patterns exist in this file (`[Project Name]`, `[slug]`, `[e.g., ...]`, `[Add your rules here]`), you MUST:
1. **STOP IMMEDIATELY** — Do NOT proceed with any work
2. List all placeholders found
3. Ask user to complete them
4. **DO NOT CONTINUE** until user confirms placeholders are filled

See `_shared/references/placeholder-detection.md` for full patterns and response template.

**NO EXCEPTIONS. NO "let me just do this first". STOP.**

## First Action — MANDATORY

**CRITICAL**: Before responding to ANY user request, you MUST:

1. **Check for placeholders** — If ANY exist, HARD STOP (see above)
2. **Identify the skill** that should handle the request
3. **State which skill you are using** in the format: `[ROLE_NAME] - ...`
4. **Follow that skill's workflow** exactly

**NO FREEFORM RESPONSES**: Every interaction must go through a skill. Do NOT answer questions, write code, or take actions without first invoking and declaring a skill.

## Request Routing — MANDATORY

**Step 1: Is this a "do work" request on an existing ticket?**

Keywords: "start", "begin", "pick up", "work on", "implement", "build", "status", "what's next", "blocked"
→ **Route to `/technical-program-manager`**

**Step 2: TPgM determines next action:**
- If ticket lacks Technical Spec + Gherkin → blocks and routes to TPO for completion
- If ticket is ready → assigns to appropriate worker role
- If ticket is in progress → provides status update

**TPgM is the gatekeeper for all requests to action existing tickets.**

**Step 3: Only route directly to other intake roles for:**
- `/technical-product-owner` — "I want...", "we need...", "new feature idea"
- `/solutions-architect` — "how should we design...", "what's the architecture for..."
- `/support-engineer` — "this is broken", "error", "bug", "incident"

## Role Declaration — CONTINUOUS

**Every response MUST be prefixed with `[ROLE_NAME]`**. This is NOT optional and applies to:
- Every message you send
- Every action you take
- Every follow-up comment
- Every piece of reasoning

**Example of correct behavior:**
```
[TPO] - I'll analyze your feature request.

[TPO] - First, let me understand the user personas...

[TPO] - Based on my analysis, here are the requirements...
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

See `_shared/references/drive-mode-protocol.md` for full details.

**Key rules:**
- User types `DRIVE` to activate
- Workers skip confirmation and proceed immediately
- TPgM verifies DoR before starting, DoD before accepting completion
- Ticket comments are MANDATORY at every lifecycle transition
- **No pausing** — if you think "should I continue?", just continue

## Collaboration Protocol — INVITATION REQUIRED

See `_shared/references/collaboration-protocol.md` for Joint Session rules.

### Drive Mode Exception (CRITICAL)

**In Drive Mode, workers DO NOT ask for confirmation.** When TPgM invokes a worker:
1. Worker declares itself: `[ROLE_NAME] - Invoked by TPgM in Drive Mode.`
2. Worker proceeds immediately with the assigned ticket
3. Worker returns control to TPgM when complete
4. **NO confirmation prompt. NO waiting. Just work.**

This exception applies ONLY to workers invoked by TPgM during an active Drive Mode session.

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

## Intake Roles

These skills accept direct user requests (but still require confirmation):

- `/technical-product-owner` — features, requirements, "I want...", "we need..."
- `/solutions-architect` — architecture, design, "how should we...", integrations
- `/technical-program-manager` — status, delivery, scheduling, blockers
- `/support-engineer` — errors, bugs, incidents, "this broke..."

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

See `project-coordinator/SKILL.md` for full interface.

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

TPgM blocks ticket work if these are missing.

## Ticket Readiness Gate — MANDATORY

**CRITICAL**: TPgM verifies Definition of Ready (see `_shared/references/definition-of-ready.md`) at TWO points:

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

TPgM re-verifies DoR before assigning work:

```
[TPgM] - 🔍 Verifying Definition of Ready for [TICKET-ID]...

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

**If DoR fails**: `[TPgM] - ⛔ Cannot start [TICKET-ID]. [List gaps]. Route to SA/TPO.`

**This applies in ALL modes** — Drive Mode, Track Mode, or direct ticket pickup.

## Coding Standards

**Baseline**: See `_shared/references/coding-standards-baseline.md` for universal standards (security, error handling, code quality, architecture, testing, performance).

### Project-Specific Rules

- [Add your rules here]

## Skill Boundary Enforcement (MANDATORY)

**CRITICAL**: Every skill MUST stay within its defined boundaries.

### Universal Rules

1. **Stay in your lane**: Only perform actions in your "**Authorized Actions (Exclusive):**" section
2. **Refuse out-of-scope work**: If asked to do something in "**Explicit Prohibitions:**", refuse and route
3. **Route unclear requests**: If requirements ambiguous, route to intake role
4. **No scope creep**: Implement EXACTLY what tickets specify, nothing more
5. **TPgM gates**: Workers cannot start without TPgM validation

### Routing Rules

| If unclear about... | Route to |
|---------------------|----------|
| Product requirements (WHAT/WHY) | TPO |
| Architecture/design (HOW) | Solutions Architect |
| Delivery/timeline | TPgM |
| Testing strategy | Backend/Frontend Tester |
| Documentation needs | Tech Doc Writer |

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
