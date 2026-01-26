# Definition of Done (DoD)

**Universal checklist for ticket completion.** Project Coordinator enforces this when updating status to "Done".

## Who Uses This

| Role | Uses DoD For |
|------|--------------|
| **Project Coordinator** | **ENFORCES** - rejects status=done if DoD not met |
| **PM** | Additional verification after coordinator accepts |
| **Workers** | Understands what "complete" means before claiming done |

## Enforcement Point

**Project Coordinator is the enforcer.** When any role invokes `[PROJECT_COORDINATOR] Update #NUM: Status=done`, the coordinator:
1. Fetches the actual ticket from the system
2. Reads comments and description for evidence
3. **REJECTS with specific gaps** if checks fail
4. Only updates status if ALL checks pass

**Workers cannot mark done without evidence.** Add PR link, review confirmation, test results to ticket comments first.

## Agent vs User Responsibilities

**Agents track what agents control. User actions are NOT part of agent DoD.**

| Action | Who Controls | In Agent DoD? |
|--------|-------------|---------------|
| Write code, create PR | Agent (`[Dev]`) | Yes |
| Review code, approve | Agent (`[Code Review]`) | Yes |
| **Merge Story PR to Epic branch** | **Agent (`[Code Review]`)** | **Yes** |
| **Merge Epic branch to main** | **User** | **No** |
| **Specify Epic branch** | **User** | **No** (but required before Dev) |
| Write tests | Agent (`[Test]`) | Yes |
| Write docs | Agent (`[Docs]`) | Yes |
| SA technical review | Agent (`[SA Review]`) | Yes |
| UAT acceptance | Agent (`[UAT]`) | Yes |

## DoD by Activity Subtask

### `[Dev]` - Implementation

| Check | Required | Validation |
|-------|----------|------------|
| PR created | Yes | Link in completion comment |
| Branch convention followed | Yes | team naming convention |
| Technical Spec satisfied | Yes | All MUST/MUST NOT met |

**Note**: PR merging happens AFTER Code Review approval (user action, not agent DoD).

### `[Code Review]` - Code Review

| Check | Required | Validation |
|-------|----------|------------|
| Code review completed | Yes | Review documented in comment |
| **All issues resolved** | Yes | No issues remain (Critical, High, Medium, or Minor) |
| PR approved | Yes | Approval confirmed in comment |
| **PR merged to Epic Branch** | Yes | Code Reviewer merges after approval |

**Code Reviewer Merge Responsibility**: After approval, Code Reviewer merges the PR to Epic branch using `gh pr merge --squash --delete-branch`. User only merges Epic branch to main.

### `[Test]` - Testing

| Check | Required | Validation |
|-------|----------|------------|
| Unit tests written | Yes | Tests documented |
| Functional tests written | Yes | Covers Gherkin scenarios |
| All tests passing | Yes | CI green or manual confirmation |
| Test PR created | Yes | Link in completion comment |

**Note**: User merges test PR.

### `[Docs]` - Documentation

| Check | Required | Validation |
|-------|----------|------------|
| Documentation created | Yes | Link or location provided |
| Matches implementation | Yes | Reflects actual behavior |
| Review completed | Yes | Technical review done |
| Docs PR created | Yes | Link in completion comment |

**Note**: User merges docs PR.

### `[SA Review]` - SA Technical Acceptance

| Check | Required | Validation |
|-------|----------|------------|
| Architecture compliance | Yes | ADR patterns followed |
| Integration validated | Yes | Integration points correct |
| Query resolutions integrated | If any | Queries resolved and incorporated |
| Technical acceptance | Yes | SA approval confirmed |

### `[UAT]` - TPO User Acceptance

| Check | Required | Validation |
|-------|----------|------------|
| UAT criteria verified | Yes | Each criterion checked |
| User acceptance confirmed | Yes | TPO approval confirmed |
| No open issues | Yes | No user-facing issues remain |

## DoD for Query Tickets

`[Query]` tickets are resolved through human discussion, not implementation.

| Check | Required | Validation |
|-------|----------|------------|
| Resolution provided | Yes | Target team answered questions |
| Resolution Summary comment | Yes | Structured summary with decision |
| Spec/ADR updates noted | Yes | Either links provided or "No updates required" |
| Impact documented | Yes | How originating ticket should proceed |
| Caller is resolver | Yes | Human who resolved closes the Query |

**Resolution Summary Comment Format:**
```markdown
✅ **Query Resolved**

## Resolution
[Technical answer to the gap/questions]

## Decision
[What was decided - proceed as-is, change needed, workaround, etc.]

## Spec/ADR Updates
- [Link to updated spec/ADR if applicable]
- [Or "No updates required" with rationale]

## Impact on Originating Ticket
[How the originating work should proceed given this resolution]

Resolved by: [Name/role]
```

**Note**: When Query is marked Done, PC automatically removes it from the originating ticket's `[Dev]` subtask's blockedBy list.

## DoD for Container Tickets

### `[Backend]`, `[Frontend]`, `[Bug]` Containers

**Containers are Done when ALL 6 activity subtasks are Done.**

| Check | Required |
|-------|----------|
| `[Dev]` subtask Done | Yes |
| `[Code Review]` subtask Done | Yes |
| `[Test]` subtask Done | Yes |
| `[Docs]` subtask Done | Yes |
| `[SA Review]` subtask Done | Yes |
| `[UAT]` subtask Done | Yes |

## DoD for Epic/Feature

| Check | Required | Validation |
|-------|----------|------------|
| All containers Done | Yes | Every child container Done |
| Epic `[Test]` Done | Yes | E2E regression complete |
| Epic `[Docs]` Done | Yes | Feature guide complete |
| Epic `[SA Review]` Done | Yes | Architecture verified |
| Epic `[UAT]` Done | Yes | TPO acceptance complete |
| Caller is TPO | Yes | Only TPO can close epics |

## DoD Enforcement Flow

### Activity Subtask Completion

```
[PROJECT_COORDINATOR] - Verifying Definition of Done for #NUM...

| Check | Status | Evidence |
|-------|--------|----------|
| [check 1] | Pass/Fail | [where found] |
| [check 2] | Pass/Fail | [where found] |
```

**If checks fail**: REJECT with missing items, do NOT update status.

### Container Completion

```
[PROJECT_COORDINATOR] - Verifying container DoD for #NUM...

| Activity Subtask | Status |
|------------------|--------|
| [Dev] #X | Done/Not Done |
| [Code Review] #X | Done/Not Done |
| [Test] #X | Done/Not Done |
| [Docs] #X | Done/Not Done |
| [SA Review] #X | Done/Not Done |
| [UAT] #X | Done/Not Done |
```

**Container cannot be marked Done until ALL 6 activity subtasks are Done.**

## Common Gaps

| Gap | Resolution |
|-----|------------|
| No PR link | Worker must provide PR link in comment |
| Story PR not merged | Code Reviewer merges to Epic branch after approval |
| Epic not merged to main | **User action** - not an agent DoD check |
| Branch not deleted | Handled by `--delete-branch` flag during merge |
| No code review approval | Worker must get Code Reviewer approval |
| **Minor/Medium issues unresolved** | Code Reviewer rejects - ALL issues must be fixed |
| Tests missing | Worker must write tests per Gherkin scenarios |
| Tests failing | Worker must fix failures |
| Spec not met | Worker must address MUST/MUST NOT violations |
| Activity subtasks incomplete | Complete all activities before closing container |
| UAT not verified | TPO must verify and add UAT comment |
| Open Query blocking `[Dev]` | Resolve Query before marking `[Dev]` Done |
| Query missing Resolution Summary | Add structured resolution comment before closing |

## Related References

- `definition-of-ready.md` - Pre-work checklist
- `project-coordinator/references/ticket-templates.md` - Full templates with DoR/DoD
- `drive-mode-protocol.md` - Verification templates for Drive Mode
