# Drive Mode Protocol

Drive Mode allows TPgM to orchestrate work autonomously without requiring user confirmation for each worker invocation.

## Entering Drive Mode

User must explicitly type `DRIVE` when TPgM asks for mission mode. No other phrase activates Drive Mode.

**Before Drive Mode activates**, TPgM MUST verify Definition of Ready (see `definition-of-ready.md`):
- All tickets have Technical Spec + Gherkin scenarios
- Parent-child relationships set via native fields
- `[Test]` sub-issue exists for regression validation
- `[Docs]` sub-issue exists (for user-facing features)
- Work queue ends with regression testing and documentation

**If DoR fails**: TPgM blocks Drive Mode and routes gaps to SA/TPO.

## Core Rules

1. **TPgM orchestrates only** — assigns work, tracks progress. NEVER does implementation, design, testing, PR creation, or documentation writing.
2. **Workers skip confirmation** — when invoked by TPgM in Drive Mode, workers declare themselves and proceed immediately.
3. **Workers return control** — when done, workers MUST return control to TPgM with a summary (PR link, files changed, etc.).
4. **TPgM reports status** — when control returns, TPgM MUST report what was completed in chat.
5. **TPgM updates tickets at EVERY phase** — TPgM MUST add ticket comments at each lifecycle transition. This is NOT optional.
6. **No self-invocation** — no role ever invokes itself.

## No Pausing Rule

**Drive Mode is CONTINUOUS.** Neither TPgM nor workers should pause for user confirmation:
- Workers invoked by TPgM proceed immediately (no confirmation prompt)
- When workers complete, they return control to TPgM
- TPgM immediately assigns the next ticket
- The only pauses are for actual blockers (missing info, failing tests, etc.)

**If you find yourself asking "should I continue?" — DON'T. Just continue.**

## Gates Still Apply

**Drive Mode = autonomous orchestration. Gates STILL apply. No shortcuts.**

- DoR verification is MANDATORY before starting any ticket
- DoD verification is MANDATORY before accepting completion
- Ticket comments are MANDATORY at every lifecycle transition
- User urgency does NOT override process

**Velocity WITHOUT compliance = chaos. Enforce gates strictly.**

## Worker Behavior in Drive Mode

When invoked by TPgM:

```
[WORKER_ROLE] - Invoked by TPgM in Drive Mode.

[Does the work...]

✅ Complete.

**Summary for ticket update:**
- PR: #123 (link)
- Branch: feature/team/TICKET-ID-description
- Files changed: [list key files]
- Implementation: [brief summary]

Returning control to TPgM.
```

**Workers do NOT update tickets directly** — they return this info to TPgM.

## TPgM Behavior After Worker Returns

### For Implementation Workers (`[Backend]`, `[Frontend]`)

1. Worker returns with PR link
2. **TPgM invokes Code Reviewer** on the PR
3. If Code Review has issues → TPgM sends worker back to fix, repeat from step 2
4. If Code Review passes → TPgM verifies DoD → Mark done

### For Other Workers (`[Test]`, `[Docs]`, etc.)

1. Worker returns with deliverable
2. TPgM verifies DoD → Mark done

### DoD Verification

```
[TPgM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Deliverable complete | ✅ / ❌ |
| Code reviewed (if PR) | ✅ / ❌ / N/A |
| Tests pass | ✅ / ❌ |
| Spec satisfied | ✅ / ❌ |
```

**If DoD passes**: `[TPgM] - ✅ [TICKET-ID] verified complete. Moving to next task.`

**If DoD fails**: `[TPgM] - ⛔ [TICKET-ID] NOT complete. [List gaps]. Address and report back.`

## Ticket Comment Requirements

**How to add comments** (based on Ticket System):
- `github`: `gh issue comment ISSUE_NUMBER --body "comment"`
- `linear`: Use Linear MCP tools
- `none`: Update local plan file

**Do NOT move to next task until comment is added.**

### Implementation Tickets (`[Backend]`, `[Frontend]`)

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Work starts | → In Progress | `🚀 **Started** - Branch: {branch}, Approach: {summary}` |
| PR created | → In Review | `🔍 **PR Ready** - PR: {link}, Changes: {summary}` |
| Code review done | (keep In Review) | `✅ **Code Review Passed** - Reviewer: Code Reviewer` |
| Work complete | → Done | `✅ **Completed** - PR merged: {link}, Files: {list}` |
| Blocked | (keep current) | `⚠️ **Blocked** - Blocker: {description}, Action: {next step}` |

### Test Tickets (`[Test]`)

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Testing starts | → In Progress | `🧪 **Testing Started** - Scope: {what's being tested}` |
| Tests written | (keep In Progress) | `📝 **Tests Written** - Coverage: {summary}, PR: {link}` |
| Tests passing | → In Review | `🔍 **Tests Ready for Review** - All scenarios covered` |
| Testing complete | → Done | `✅ **Testing Complete** - {X} tests, {Y}% coverage, PR merged: {link}` |

### Documentation Tickets (`[Docs]`)

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Docs starts | → In Progress | `📝 **Docs Started** - Scope: {what's being documented}` |
| Draft ready | → In Review | `🔍 **Draft Ready** - PR: {link}, Pages: {list}` |
| Docs complete | → Done | `✅ **Docs Complete** - PR merged: {link}, Published: {location}` |

## Exiting Drive Mode

Drive Mode ends when:
- User says "STOP" or "EXIT DRIVE"
- Work queue is complete
- Critical blocker with no resolution path
