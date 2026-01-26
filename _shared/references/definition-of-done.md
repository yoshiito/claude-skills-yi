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
| **Merge PR to main** | **User** | **No** |
| **Delete branch** | **User** | **No** |
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
| No Critical/High issues | Yes | All blocking issues resolved |
| PR approved | Yes | Approval confirmed in comment |

**Note**: After approval, **user merges PR and deletes branch**. This is a user action.

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
| Technical acceptance | Yes | SA approval confirmed |

### `[UAT]` - TPO User Acceptance

| Check | Required | Validation |
|-------|----------|------------|
| UAT criteria verified | Yes | Each criterion checked |
| User acceptance confirmed | Yes | TPO approval confirmed |
| No open issues | Yes | No user-facing issues remain |

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
| Code not merged | **User action** - not an agent DoD check |
| Branch not deleted | **User action** - not an agent DoD check |
| No code review approval | Worker must get Code Reviewer approval |
| Tests missing | Worker must write tests per Gherkin scenarios |
| Tests failing | Worker must fix failures |
| Spec not met | Worker must address MUST/MUST NOT violations |
| Activity subtasks incomplete | Complete all 6 activities before closing container |
| UAT not verified | TPO must verify and add UAT comment |

## Related References

- `definition-of-ready.md` - Pre-work checklist
- `project-coordinator/references/ticket-templates.md` - Full templates with DoR/DoD
- `drive-mode-protocol.md` - Verification templates for Drive Mode
