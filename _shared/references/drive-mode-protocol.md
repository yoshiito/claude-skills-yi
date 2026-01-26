# Drive Mode Protocol

Drive Mode allows PM to orchestrate work autonomously without requiring user confirmation for each worker invocation.

**Visual Indicator**: During Drive Mode, ALL messages MUST be prefixed with `⚡` before the role prefix (e.g., `⚡ [PM]`, `⚡ [BACKEND_DEVELOPER]`).

## Entering Drive Mode

User must explicitly type `DRIVE` when PM asks for mission mode. No other phrase activates Drive Mode.

**Before Drive Mode activates**, PM MUST verify Definition of Ready (see `definition-of-ready.md`):

### Story/Task/Bug Level (Container with 6 Activity Subtasks)
- All implementation containers have Technical Spec + Gherkin scenarios
- Each `[Backend]`/`[Frontend]`/`[Bug]` container has ALL 6 activity subtasks:
  - `[Dev]` - Implementation
  - `[Code Review]` - Code review
  - `[Test]` - Testing (QA writes all tests)
  - `[Docs]` - Documentation
  - `[SA Review]` - SA technical acceptance
  - `[UAT]` - TPO user acceptance
- `blockedBy` chain set: `[Dev]` → `[Code Review]` → `[Test]` → `[Docs]` → `[SA Review]` → `[UAT]`

### Epic Level
- `[Test] {Feature} E2E Regression` ticket exists
- `[Docs] {Feature} Guide` ticket exists (if user-facing)
- `[SA Review] {Feature} Architecture` ticket exists
- `[UAT] {Feature} Acceptance` ticket exists
- Epic-level `blockedBy` set: `[Test]` → all containers, `[Docs]` → epic `[Test]`, `[SA Review]` → epic `[Docs]`, `[UAT]` → epic `[SA Review]`

**If DoR fails**: PM blocks Drive Mode and routes gaps to SA/TPO.

## Core Rules

1. **PM orchestrates only** — assigns work, tracks progress. NEVER does implementation, design, testing, PR creation, or documentation writing.
2. **Workers skip confirmation** — when invoked by PM in Drive Mode, workers declare themselves and proceed immediately.
3. **Workers return control** — when done, workers MUST return control to PM with a summary (PR link, files changed, etc.).
4. **PM reports status** — when control returns, PM MUST report what was completed in chat.
5. **PM updates tickets at EVERY phase** — PM MUST add ticket comments at each lifecycle transition. This is NOT optional.
6. **No self-invocation** — no role ever invokes itself.

## ⛔ Container Completion Rule (MANDATORY)

**PM MUST complete ALL activity subtasks for ONE container before moving to another container.**

```
✅ CORRECT (depth-first):
   Story A: [Dev] → [Code Review] → [Test] → ... → DONE
   Story B: [Dev] → [Code Review] → [Test] → ... → DONE

❌ WRONG (breadth-first):
   Story A: [Dev] → [Code Review]
   Story B: [Dev] ← VIOLATION: Story A not complete
```

**Exception**: If container is BLOCKED by `[Query]` or external dependency, PM MAY start another container. PM MUST document the block and return to complete it once unblocked.

**Checkpoint before starting NEW container**:
- [ ] Previous container is DONE, OR
- [ ] Previous container is BLOCKED (documented)

## Workflow Sequence

### Per Story/Task/Bug (Container with 6 Activity Subtasks)

Each implementation container follows this sequence through its 6 activity subtasks:

```
┌───────────────────────────────────────────────────────────────────────────┐
│  [Backend] Add password reset endpoint                     (Container)    │
│                                                                           │
│  ├── [Dev] Add password reset endpoint                                    │
│  │   1. Implementation ──► Mark [Dev] Done                                │
│  │        Developer           PM                                          │
│  │                                                                        │
│  ├── [Code Review] Add password reset endpoint                            │
│  │   2. Review PR ──► Mark [Code Review] Done                             │
│  │       Code Reviewer     PM                                             │
│  │                                                                        │
│  ├── [Test] Add password reset endpoint                                   │
│  │   3. Write Tests ──► Run Tests ──► Mark [Test] Done                    │
│  │        Tester          Tester         PM                               │
│  │                                                                        │
│  ├── [Docs] Add password reset endpoint                                   │
│  │   4. Documentation ──► Mark [Docs] Done                                │
│  │        Tech Doc Writer     PM                                          │
│  │                                                                        │
│  ├── [SA Review] Add password reset endpoint                              │
│  │   5. Technical Review ──► Mark [SA Review] Done                        │
│  │        Solutions Architect    PM                                       │
│  │                                                                        │
│  └── [UAT] Add password reset endpoint                                    │
│      6. User Acceptance ──► Mark [UAT] Done ──► Mark Container Done       │
│           TPO                  PM                  PM                     │
└───────────────────────────────────────────────────────────────────────────┘
```

**Workflow per container:**
1. PM assigns `[Dev]` subtask to Developer
2. Developer completes → PM verifies DoD → Mark `[Dev]` Done
3. PM assigns `[Code Review]` subtask to Code Reviewer
4. Code Review passes → PM verifies DoD → Mark `[Code Review]` Done
   - If issues found → PM sends Developer back to fix, repeat from step 1
5. PM assigns `[Test]` subtask to Tester
6. Tester writes + runs tests → PM verifies DoD → Mark `[Test]` Done
7. PM assigns `[Docs]` subtask to Tech Doc Writer
8. Tech Doc Writer completes → PM verifies DoD → Mark `[Docs]` Done
9. PM assigns `[SA Review]` subtask to Solutions Architect
10. SA reviews technical compliance → PM verifies DoD → Mark `[SA Review]` Done
11. PM assigns `[UAT]` subtask to TPO
12. TPO completes user acceptance → PM verifies DoD → Mark `[UAT]` Done
13. All 6 subtasks Done → PM marks Container Done
14. PM moves to next Story/Task/Bug container

### Epic-Level (After All Containers Complete)

```
All Story/Task/Bug Containers Done
              ↓
[Test] E2E Regression ──► [Docs] Feature Guide ──► [SA Review] Architecture ──► [UAT] Acceptance ──► Epic Done
        Tester               Tech Doc Writer              SA                         TPO
```

**Workflow:**
1. PM assigns Epic `[Test]` to Tester (regression/E2E)
2. Tester completes → PM verifies DoD → Mark Epic `[Test]` Done
3. PM assigns Epic `[Docs]` to Tech Doc Writer
4. Tech Doc Writer completes → PM verifies DoD → Mark Epic `[Docs]` Done
5. PM assigns Epic `[SA Review]` to Solutions Architect
6. SA verifies architecture compliance across all stories → PM verifies DoD → Mark Epic `[SA Review]` Done
7. PM assigns Epic `[UAT]` to TPO
8. TPO completes feature acceptance → PM verifies DoD → Mark Epic `[UAT]` Done
9. Epic Done

## No Pausing Rule

**Drive Mode is CONTINUOUS.** Neither PM nor workers should pause for user confirmation:
- Workers invoked by PM proceed immediately (no confirmation prompt)
- When workers complete, they return control to PM
- PM immediately assigns the next ticket
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

When invoked by PM:

```
⚡ [WORKER_ROLE] - Invoked by PM in Drive Mode.

[Does the work...]

⚡ [WORKER_ROLE] - ✅ Complete.

**Summary for ticket update:**
- PR: #123 (link)
- Branch: feature/team/TICKET-ID-description
- Files changed: [list key files]
- Implementation: [brief summary]

Returning control to PM.
```

**Workers do NOT update tickets directly** — they return this info to PM.

## PM Behavior After Worker Returns

### For `[Dev]` Subtask (Developer)

1. Developer returns with PR link
2. PM verifies DoD for `[Dev]` → Mark `[Dev]` Done
3. **PM immediately assigns `[Code Review]` subtask** to Code Reviewer

### For `[Code Review]` Subtask (Code Reviewer)

1. Code Reviewer returns with review results
2. If ANY issues found (Critical, High, Medium, or Minor) → PM sends Developer back to fix, repeat
3. If Code Review passes (zero issues) → PM verifies DoD → Mark `[Code Review]` Done
4. **PM immediately assigns `[Test]` subtask** to Tester

### For `[Test]` Subtask (Tester)

1. Tester returns with test PR link
2. PM verifies DoD for `[Test]` → Mark `[Test]` Done
3. **PM immediately assigns `[Docs]` subtask** to Tech Doc Writer

### For `[Docs]` Subtask (Tech Doc Writer)

1. Tech Doc Writer returns with docs PR link
2. PM verifies DoD for `[Docs]` → Mark `[Docs]` Done
3. **PM immediately assigns `[SA Review]` subtask** to Solutions Architect

### For `[SA Review]` Subtask (Solutions Architect)

1. SA returns with technical compliance review
2. If issues found → PM routes to appropriate worker to fix, then re-review
3. If SA Review passes → PM verifies DoD → Mark `[SA Review]` Done
4. **PM immediately assigns `[UAT]` subtask** to TPO

### For `[UAT]` Subtask (TPO)

1. TPO returns with user acceptance results
2. If issues found → PM routes to appropriate worker to fix, then re-UAT
3. If UAT passes → PM verifies DoD → Mark `[UAT]` Done
4. All 6 subtasks Done → PM marks Container Done
5. **PM moves to next Story/Task/Bug container**

### For Epic-Level Tickets

1. Worker returns with deliverable
2. PM verifies DoD → Mark done
3. If Epic `[Test]` just completed → PM assigns Epic `[Docs]`
4. If Epic `[Docs]` just completed → PM assigns Epic `[SA Review]`
5. If Epic `[SA Review]` just completed → PM assigns Epic `[UAT]`
6. If Epic `[UAT]` just completed → Epic Done

### DoD Verification

#### For `[Dev]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| PR created | ✅ / ❌ |
| Branch follows convention | ✅ / ❌ |
| Technical Spec satisfied | ✅ / ❌ |
| No open questions | ✅ / ❌ |
```

#### For `[Code Review]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Code review completed | ✅ / ❌ |
| All issues resolved | ✅ / ❌ |
| PR approved | ✅ / ❌ |
| PR merged to Epic branch | ✅ / ❌ |
```

**Note**: User merges PR and deletes branch after Code Review approval.

#### For `[Test]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Unit tests written | ✅ / ❌ |
| Functional tests written | ✅ / ❌ |
| All tests passing | ✅ / ❌ |
| Gherkin scenarios covered | ✅ / ❌ |
| Test PR created | ✅ / ❌ |
```

**Note**: User merges test PR.

#### For `[Docs]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Documentation created | ✅ / ❌ |
| Matches implementation | ✅ / ❌ |
| Review completed | ✅ / ❌ |
| Docs PR created | ✅ / ❌ |
```

**Note**: User merges docs PR.

#### For `[SA Review]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Architecture compliance verified | ✅ / ❌ |
| ADR patterns followed | ✅ / ❌ |
| Integration points validated | ✅ / ❌ |
| No technical debt introduced | ✅ / ❌ |
```

#### For `[UAT]` Subtask

```
⚡ [PM] - 🔍 Verifying completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| UAT criteria verified | ✅ / ❌ |
| User acceptance confirmed | ✅ / ❌ |
| No open user-facing issues | ✅ / ❌ |
```

#### For Container Tickets (`[Backend]`, `[Frontend]`, `[Bug]`)

```
⚡ [PM] - 🔍 Verifying container completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| [Dev] subtask Done | ✅ / ❌ |
| [Code Review] subtask Done | ✅ / ❌ |
| [Test] subtask Done | ✅ / ❌ |
| [Docs] subtask Done | ✅ / ❌ |
| [SA Review] subtask Done | ✅ / ❌ |
| [UAT] subtask Done | ✅ / ❌ |
```

**If DoD passes**: `⚡ [PM] - ✅ [TICKET-ID] verified complete. Moving to next task.`

**If DoD fails**: `⚡ [PM] - ⛔ [TICKET-ID] NOT complete. [List gaps]. Address and report back.`

## Ticket Comment Requirements

**How to add comments** (based on Ticket System):
- `github`: `gh issue comment ISSUE_NUMBER --body "comment"`
- `linear`: Use Linear MCP tools
- `none`: Update local plan file

**Do NOT move to next task until comment is added.**

### `[Dev]` Subtasks (Implementation)

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Work starts | → In Progress | `🚀 **Dev Started** - Branch: {branch}, Approach: {summary}` |
| PR created | → In Review | `🔍 **PR Ready** - PR: {link}, Changes: {summary}` |
| Work complete | → Done | `✅ **Dev Complete** - PR: {link}, Files: {list}` |
| Blocked | (keep current) | `⚠️ **Blocked** - Blocker: {description}, Action: {next step}` |

### `[Code Review]` Subtasks

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Review starts | → In Progress | `🔍 **Code Review Started** - PR: {link}` |
| Issues found | (keep In Progress) | `⚠️ **Issues Found** - {count} issues, returning to Developer` |
| Review passed | → Done | `✅ **Code Review Passed** - PR approved and merged to Epic branch: {link}` |

**All issues must be resolved.** Code Reviewer rejects PRs with ANY unresolved issues. No exceptions for Minor/Medium.

### `[Test]` Subtasks

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Testing starts | → In Progress | `🧪 **Testing Started** - Scope: {what's being tested}` |
| Tests written | (keep In Progress) | `📝 **Tests Written** - Coverage: {summary}, PR: {link}` |
| Tests passing | → In Review | `🔍 **Tests Ready for Review** - All scenarios covered` |
| Testing complete | → Done | `✅ **Testing Complete** - {X} tests, {Y}% coverage, PR: {link}` |

### `[Docs]` Subtasks

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Docs starts | → In Progress | `📝 **Docs Started** - Scope: {what's being documented}` |
| Draft ready | → In Review | `🔍 **Draft Ready** - PR: {link}, Pages: {list}` |
| Docs complete | → Done | `✅ **Docs Complete** - PR: {link}, Published: {location}` |

### `[SA Review]` Subtasks

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Review starts | → In Progress | `🏗️ **SA Review Started** - Checking architecture compliance` |
| Issues found | (keep In Progress) | `⚠️ **Architecture Issues** - {description}, returning to {role}` |
| Review passed | → Done | `✅ **SA Review Passed** - Architecture compliant` |

### `[UAT]` Subtasks

| Phase | Status | Comment Template |
|-------|--------|------------------|
| UAT starts | → In Progress | `👤 **UAT Started** - Verifying: {criteria}` |
| Issues found | (keep In Progress) | `⚠️ **UAT Issues** - {description}, returning to {role}` |
| UAT passed | → Done | `✅ **UAT Passed** - User acceptance confirmed` |

### Container Tickets (`[Backend]`, `[Frontend]`, `[Bug]`)

| Phase | Status | Comment Template |
|-------|--------|------------------|
| First subtask starts | → In Progress | `🚀 **Container Started** - Beginning activity chain` |
| All subtasks done | → Done | `✅ **Container Complete** - All 6 activities finished` |

## Exiting Drive Mode

**CRITICAL: Only the USER can end Drive Mode.** The AI cannot decide to exit on its own.

Drive Mode ends ONLY when:
- User says `STOP` or `EXIT DRIVE`
- User explicitly approves ending the session

**AI may PROMPT to end, but must WAIT for user approval:**
```
⚡ [PM] - Work queue complete. Would you like to exit Drive Mode?

1. EXIT - Yes, exit Drive Mode
2. CONTINUE - No, stay in Drive Mode (assign more work)
```

**WAIT for user response.** Do NOT assume or auto-exit.

**When user confirms exit, stop using the ⚡ prefix:**
```
⚡ [PM] - Exiting Drive Mode.

[PM] - Back to standard mode. All tasks completed successfully.
```
