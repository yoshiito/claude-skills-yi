# Plan Execution Mode Protocol

**Plan Execution Mode executes an existing ticket. Nothing else.**

The ticket IS the plan. Read it. Execute it literally. Do not interpret, analyze, or create your own plan.

**Visual Indicator**: During Plan Execution Mode, ALL messages MUST be prefixed with `⚡` before the role prefix (e.g., `⚡ [PM]`, `⚡ [BACKEND_DEVELOPER]`).

## What This Mode Does

1. Verifies a ticket exists and meets Definition of Ready
2. Executes the ticket's checklist exactly as written
3. That's it. Nothing else.

## What This Mode Does NOT Do

- Create plans
- Interpret requirements
- Analyze gaps
- Make decisions
- Do anything not explicitly in the ticket

**If the ticket is unclear → Mode cannot activate. Fix the ticket first.**

## Entering Plan Execution Mode

User types `EXECUTE`.

**Before mode activates**, PM MUST:

1. Invoke PC to verify Definition of Ready
2. PC reads the actual ticket (not from memory)
3. If DoR passes → Enter Plan Execution Mode
4. If DoR fails → Stay in Collab Mode, report what's missing

**DoR Checks (PC verifies these by reading the ticket):**

| Check | Required |
|-------|----------|
| Technical Spec (MUST/MUST NOT/SHOULD) | Yes |
| Gherkin scenarios | Yes |
| Mission Statement | Yes |
| Feature Branch specified | Yes |
| Checklist of work items | Yes |

**If ANY check fails**: Mode cannot activate. Route to TPO/SA to fix the ticket.

## PM Behavior in Plan Execution Mode

**PM's ONLY responsibilities:**

1. Invoke PC to verify DoR
2. Invoke roles per the ticket's checklist
3. Verify DoD when workers return
4. Add ticket comments at phase transitions

**PM is PROHIBITED from:**

- Reading code or files
- Analyzing gaps
- Assessing what's missing
- Creating plans or checklists
- Doing any work that isn't invoking roles or verifying DoD

**The ticket checklist IS the plan. PM invokes roles to execute it. That's all.**

### PM Invocation Pattern

```
⚡ [PM] - Invoking [ROLE] for ticket #123, checklist item: "[item text]"
```

PM invokes the role and gets out of the way. The worker does the work.

## Worker Behavior in Plan Execution Mode

**When invoked by PM:**

```
⚡ [WORKER_ROLE] - Invoked by PM in Plan Execution Mode.

[Reads ticket checklist item]
[Does exactly what it says]
[Returns to PM with summary]
```

**Workers MUST:**

1. Read the ticket/checklist item assigned
2. Execute exactly what it says
3. Return to PM with deliverable summary

**Workers are PROHIBITED from:**

- Creating their own plans
- Doing "exploration" phases
- Analyzing or interpreting beyond the ticket
- Working on items not assigned by PM

**The ticket tells you what to do. Do that. Nothing else.**

### Worker Return Pattern

```
⚡ [WORKER_ROLE] - Complete.

**Summary for ticket update:**
- PR: #123 (link)
- Files changed: [list]
- Implementation: [brief summary]

Returning control to PM.
```

## Execution Rules

### Rule 1: Ticket = Instructions

The ticket contains your instructions. Read it. Execute it literally.

- Do NOT interpret
- Do NOT analyze
- Do NOT create your own plan
- Just do what the ticket says, in the order it says

### Rule 2: No Pausing

Plan Execution Mode is CONTINUOUS. Do not pause for confirmation.

- Workers invoked by PM proceed immediately
- When workers complete, they return control to PM
- PM immediately invokes the next role per the checklist
- Only pause for actual blockers (failing tests, missing info)

**If you find yourself asking "should I continue?" — DON'T. Just continue.**

### Rule 3: Depth-First Execution

Complete ONE ticket before starting another.

```
CORRECT:
  Ticket A: All checklist items complete → DONE
  Ticket B: Start → All items → DONE

WRONG:
  Ticket A: Partial work
  Ticket B: Start ← VIOLATION
```

### Rule 4: Gates Still Apply

Plan Execution Mode = autonomous execution. Quality gates STILL apply.

- DoR verification is MANDATORY before starting
- DoD verification is MANDATORY before completing
- Ticket comments are MANDATORY at transitions

## Ticket Comments

**PM adds comments at each transition** (based on ticket system):

- `github`: `gh issue comment ISSUE_NUMBER --body "comment"`
- `linear`: Use Linear MCP tools
- `none`: Update local plan file

| Phase | Comment |
|-------|---------|
| Start | `🚀 **Started** - Working on: [checklist item]` |
| Complete | `✅ **Complete** - [summary of deliverable]` |
| Blocked | `⚠️ **Blocked** - [reason], Action: [next step]` |

## Exiting Plan Execution Mode

**Only USER can exit.** PM may prompt but must wait for approval.

```
⚡ [PM] - Ticket checklist complete. Exit Plan Execution Mode? (y/n)
```

On exit:
```
[PM] - Back to Collab Mode.
```

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| PM reading code | PM doing worker's job | PM only invokes roles |
| PM "analyzing gaps" | PM planning instead of executing | Ticket IS the plan |
| Worker creating plan | Worker has planning phases | Remove planning from worker skill |
| Re-reading ticket repeatedly | Not executing | Read once, execute, done |
| "Should I continue?" prompts | Pausing unnecessarily | Just continue |
