# Drive Mode Protocol

Drive Mode allows PM to orchestrate work autonomously without requiring user confirmation for each worker invocation.

**Visual Indicator**: During Drive Mode, ALL messages MUST be prefixed with `⚡` before the role prefix (e.g., `⚡ [PM]`, `⚡ [BACKEND_DEVELOPER]`).

## Entering Drive Mode

User must explicitly type `DRIVE` when PM asks for mission mode. No other phrase activates Drive Mode.

**Before Drive Mode activates**, PM MUST verify Definition of Ready (see `definition-of-ready.md`):

### Feature Level (Quality-Bounded Work Unit)
- All Features have Technical Spec + Gherkin scenarios
- All Features have Mission Statement defining "done"
- All Features have Feature Branch specified by user
- If implementation is complex, optional `[Dev]` subtasks are created
- Workflow Phases checklist present in each Feature

### Mission Level
- `[Test] {Mission} E2E Regression` ticket exists
- `[Docs] {Mission} Guide` ticket exists (if user-facing)
- `[SA Review] {Mission} Architecture` ticket exists
- `[UAT] {Mission} Acceptance` ticket exists
- Mission-level `blockedBy` set: `[Test]` → all Features, `[Docs]` → Mission `[Test]`, `[SA Review]` → Mission `[Docs]`, `[UAT]` → Mission `[SA Review]`

**If DoR fails**: PM blocks Drive Mode and routes gaps to SA/TPO.

## Core Rules

1. **PM orchestrates only** — assigns work, tracks progress. NEVER does implementation, design, testing, PR creation, or documentation writing.
2. **Workers skip confirmation** — when invoked by PM in Drive Mode, workers declare themselves and proceed immediately.
3. **Workers return control** — when done, workers MUST return control to PM with a summary (PR link, files changed, etc.).
4. **PM reports status** — when control returns, PM MUST report what was completed in chat.
5. **PM updates tickets at EVERY phase** — PM MUST add ticket comments at each lifecycle transition. This is NOT optional.
6. **No self-invocation** — no role ever invokes itself.

## ⛔ Feature Completion Rule (MANDATORY)

**PM MUST complete ALL workflow phases for ONE Feature before moving to another Feature.**

> **Mirrored Constraint**: Worker skills have a matching "Single-Ticket Constraint" enforcing that workers work on ONE assigned ticket at a time. See individual worker SKILL.md files.

```
✅ CORRECT (depth-first):
   Feature A: Development → Code Review → Test → ... → DONE
   Feature B: Development → Code Review → Test → ... → DONE

❌ WRONG (breadth-first):
   Feature A: Development → Code Review
   Feature B: Development ← VIOLATION: Feature A not complete
```

**Exception**: If Feature is BLOCKED by `[Query]` or external dependency, PM MAY start another Feature. PM MUST document the block and return to complete it once unblocked.

**Checkpoint before starting NEW Feature**:
- [ ] Previous Feature is DONE, OR
- [ ] Previous Feature is BLOCKED (documented)

## Workflow Sequence

### Per Feature (Quality-Bounded Work Unit)

Each Feature follows this workflow phase sequence:

```
┌───────────────────────────────────────────────────────────────────────────┐
│  [Backend] Add password reset endpoint                     (Feature)      │
│                                                                           │
│  Optional: [Dev] subtasks if implementation needs breakdown               │
│                                                                           │
│  Workflow Phases (tracked at Feature level):                              │
│                                                                           │
│  1. Development ──► 2. Code Review ──► 3. Test ──► 4. Docs               │
│       Developer        Code Reviewer     Tester     Tech Doc             │
│                                                                           │
│  ──► 5. SA Review ──► 6. UAT ──► Feature Done                            │
│            SA            TPO           PM                                 │
└───────────────────────────────────────────────────────────────────────────┘
```

**Workflow per Feature:**
1. PM assigns Development to Developer (includes all `[Dev]` subtasks if any)
2. Developer completes → PM verifies DoD → Update Feature comment
3. PM assigns Code Review to Code Reviewer
4. Code Review passes → PM verifies DoD → Update Feature comment
   - If issues found → PM sends Developer back to fix, repeat from step 1
5. PM assigns Test to Tester
6. Tester writes + runs tests → PM verifies DoD → Update Feature comment
7. PM assigns Docs to Tech Doc Writer (if user-facing)
8. Tech Doc Writer completes → PM verifies DoD → Update Feature comment
9. PM assigns SA Review to Solutions Architect
10. SA reviews technical compliance → PM verifies DoD → Update Feature comment
11. PM assigns UAT to TPO
12. TPO completes user acceptance → PM verifies DoD → Update Feature comment
13. All workflow phases complete → PM marks Feature Done
14. PM moves to next Feature

### Mission-Level (After All Features Complete)

```
All Features Done
       ↓
[Test] E2E Regression ──► [Docs] Mission Guide ──► [SA Review] Architecture ──► [UAT] Acceptance ──► Mission Done
        Tester               Tech Doc Writer              SA                         TPO
```

**Workflow:**
1. PM assigns Mission `[Test]` to Tester (regression/E2E)
2. Tester completes → PM verifies DoD → Mark Mission `[Test]` Done
3. PM assigns Mission `[Docs]` to Tech Doc Writer
4. Tech Doc Writer completes → PM verifies DoD → Mark Mission `[Docs]` Done
5. PM assigns Mission `[SA Review]` to Solutions Architect
6. SA verifies architecture compliance across all Features → PM verifies DoD → Mark Mission `[SA Review]` Done
7. PM assigns Mission `[UAT]` to TPO
8. TPO completes Mission acceptance → PM verifies DoD → Mark Mission `[UAT]` Done
9. Mission Done

## No Pausing Rule

**Drive Mode is CONTINUOUS.** Neither PM nor workers should pause for user confirmation:
- Workers invoked by PM proceed immediately (no confirmation prompt)
- When workers complete, they return control to PM
- PM immediately assigns the next workflow phase
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

### For Development Phase (Developer)

1. Developer returns with PR link (and all Dev subtask PRs if any)
2. PM verifies DoD → Update Feature with Development completion comment
3. **PM immediately assigns Code Review phase** to Code Reviewer

### For Code Review Phase (Code Reviewer)

1. Code Reviewer returns with review results
2. If ANY issues found (Critical, High, Medium, or Minor) → PM sends Developer back to fix, repeat
3. If Code Review passes (zero issues) → PM verifies DoD → Update Feature comment
4. **PM immediately assigns Test phase** to Tester

### For Test Phase (Tester)

1. Tester returns with test PR link
2. PM verifies DoD → Update Feature comment
3. **PM immediately assigns Docs phase** to Tech Doc Writer (if user-facing)

### For Docs Phase (Tech Doc Writer)

1. Tech Doc Writer returns with docs PR link
2. PM verifies DoD → Update Feature comment
3. **PM immediately assigns SA Review phase** to Solutions Architect

### For SA Review Phase (Solutions Architect)

1. SA returns with technical compliance review
2. If issues found → PM routes to appropriate worker to fix, then re-review
3. If SA Review passes → PM verifies DoD → Update Feature comment
4. **PM immediately assigns UAT phase** to TPO

### For UAT Phase (TPO)

1. TPO returns with user acceptance results
2. If issues found → PM routes to appropriate worker to fix, then re-UAT
3. If UAT passes → PM verifies DoD → Update Feature comment
4. All workflow phases complete → PM marks Feature Done
5. **PM moves to next Feature**

### For Mission-Level Tickets

1. Worker returns with deliverable
2. PM verifies DoD → Mark done
3. If Mission `[Test]` just completed → PM assigns Mission `[Docs]`
4. If Mission `[Docs]` just completed → PM assigns Mission `[SA Review]`
5. If Mission `[SA Review]` just completed → PM assigns Mission `[UAT]`
6. If Mission `[UAT]` just completed → Mission Done

### DoD Verification

#### For Development Phase

```
⚡ [PM] - 🔍 Verifying Development completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| PR created | ✅ / ❌ |
| Dev subtasks complete (if any) | ✅ / ❌ |
| Branch follows convention | ✅ / ❌ |
| Technical Spec satisfied | ✅ / ❌ |
| No open questions | ✅ / ❌ |
```

#### For Code Review Phase

```
⚡ [PM] - 🔍 Verifying Code Review completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Code review completed | ✅ / ❌ |
| All issues resolved | ✅ / ❌ |
| PR approved | ✅ / ❌ |
```

**Note**: User merges PR after Code Review approval.

#### For Test Phase

```
⚡ [PM] - 🔍 Verifying Test completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Unit tests written | ✅ / ❌ |
| Functional tests written | ✅ / ❌ |
| All tests passing | ✅ / ❌ |
| Gherkin scenarios covered | ✅ / ❌ |
| Test PR created | ✅ / ❌ |
```

**Note**: User merges test PR.

#### For Docs Phase

```
⚡ [PM] - 🔍 Verifying Docs completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Documentation created | ✅ / ❌ |
| Matches implementation | ✅ / ❌ |
| Review completed | ✅ / ❌ |
| Docs PR created | ✅ / ❌ |
```

**Note**: User merges docs PR.

#### For SA Review Phase

```
⚡ [PM] - 🔍 Verifying SA Review completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| Architecture compliance verified | ✅ / ❌ |
| ADR patterns followed | ✅ / ❌ |
| Integration points validated | ✅ / ❌ |
| No technical debt introduced | ✅ / ❌ |
```

#### For UAT Phase

```
⚡ [PM] - 🔍 Verifying UAT completion for [TICKET-ID]...

| Check | Status |
|-------|--------|
| UAT criteria verified | ✅ / ❌ |
| User acceptance confirmed | ✅ / ❌ |
| No open user-facing issues | ✅ / ❌ |
```

#### For Feature Tickets (`[Backend]`, `[Frontend]`, `[Bug]`)

```
⚡ [PM] - 🔍 Verifying Feature completion for [TICKET-ID]...

| Workflow Phase | Status |
|----------------|--------|
| Development | ✅ / ❌ |
| Code Review | ✅ / ❌ |
| Test | ✅ / ❌ |
| Docs | ✅ / ❌ (or N/A) |
| SA Review | ✅ / ❌ |
| UAT | ✅ / ❌ |
```

**If DoD passes**: `⚡ [PM] - ✅ [TICKET-ID] verified complete. Moving to next task.`

**If DoD fails**: `⚡ [PM] - ⛔ [TICKET-ID] NOT complete. [List gaps]. Address and report back.`

## Ticket Comment Requirements

**How to add comments** (based on Ticket System):
- `github`: `gh issue comment ISSUE_NUMBER --body "comment"`
- `linear`: Use Linear MCP tools
- `none`: Update local plan file

**Do NOT move to next task until comment is added.**

### Feature Workflow Phase Comments

| Phase | Status | Comment Template |
|-------|--------|------------------|
| Development starts | → In Progress | `🚀 **Development Started** - Branch: {branch}, Approach: {summary}` |
| PR created | → In Review | `🔍 **PR Ready** - PR: {link}, Changes: {summary}` |
| Development complete | (update comment) | `✅ **Development Complete** - PR: {link}, Files: {list}` |
| Code Review complete | (update comment) | `✅ **Code Review Passed** - Approved by {reviewer}` |
| Test complete | (update comment) | `✅ **Test Complete** - {X} tests, {Y}% coverage, PR: {link}` |
| Docs complete | (update comment) | `✅ **Docs Complete** - PR: {link}, Pages: {list}` |
| SA Review complete | (update comment) | `✅ **SA Review Passed** - Architecture compliant` |
| UAT complete | → Done | `✅ **Feature Complete** - All workflow phases done` |
| Blocked | (keep current) | `⚠️ **Blocked** - Blocker: {description}, Action: {next step}` |

**All issues must be resolved.** Code Reviewer rejects PRs with ANY unresolved issues. No exceptions for Minor/Medium.

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
