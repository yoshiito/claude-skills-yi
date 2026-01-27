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
| Write code, create PR | Agent (Development phase) | Yes |
| Review code, approve | Agent (Code Review phase) | Yes |
| **Merge Feature PR** | **User** | **No** |
| **Merge Mission branch to main** | **User** | **No** |
| **Specify Feature branch** | **User** | **No** (but required before Dev) |
| Write tests | Agent (Test phase) | Yes |
| Write docs | Agent (Docs phase) | Yes |
| SA technical review | Agent (SA Review phase) | Yes |
| UAT acceptance | Agent (UAT phase) | Yes |

## DoD by Workflow Phase (at Feature Level)

Quality phases are tracked at Feature level via workflow checklists, NOT as separate tickets.

### Development Phase

| Check | Required | Validation |
|-------|----------|------------|
| PR created | Yes | Link in Feature comment |
| Branch convention followed | Yes | team naming convention |
| Technical Spec satisfied | Yes | All MUST/MUST NOT met |
| Dev subtasks complete | If any | All `[Dev]` children Done |

**Note**: User merges Feature PR.

### Code Review Phase

| Check | Required | Validation |
|-------|----------|------------|
| Code review completed | Yes | Review documented in Feature comment |
| **All issues resolved** | Yes | No issues remain (Critical, High, Medium, or Minor) |
| PR approved | Yes | Approval confirmed in Feature comment |

**User merges after approval.**

### Test Phase

| Check | Required | Validation |
|-------|----------|------------|
| Unit tests written | Yes | Tests documented |
| Functional tests written | Yes | Covers Gherkin scenarios |
| All tests passing | Yes | CI green or manual confirmation |
| Test PR created | Yes | Link in Feature comment |

**Note**: User merges test PR.

### Docs Phase

| Check | Required | Validation |
|-------|----------|------------|
| Documentation created | Yes | Link or location provided |
| Matches implementation | Yes | Reflects actual behavior |
| Review completed | Yes | Technical review done |
| Docs PR created | Yes | Link in Feature comment |

**Note**: User merges docs PR.

### SA Review Phase

| Check | Required | Validation |
|-------|----------|------------|
| Architecture compliance | Yes | ADR patterns followed |
| Integration validated | Yes | Integration points correct |
| Query resolutions integrated | If any | Queries resolved and incorporated |
| Technical acceptance | Yes | SA approval confirmed in Feature comment |

### UAT Phase

| Check | Required | Validation |
|-------|----------|------------|
| UAT criteria verified | Yes | Each criterion checked |
| User acceptance confirmed | Yes | TPO approval confirmed in Feature comment |
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

**Note**: When Query is marked Done, PC automatically removes it from the originating Feature's blockedBy list.

## DoD for Feature Tickets

### `[Backend]`, `[Frontend]`, `[Bug]` Features

**Features are Done when ALL workflow phases are complete.**

| Check | Required |
|-------|----------|
| Development phase complete | Yes |
| Code Review phase complete | Yes |
| Test phase complete | Yes |
| Docs phase complete | Yes (if user-facing) |
| SA Review phase complete | Yes |
| UAT phase complete | Yes |
| Dev subtasks Done | If any |

## DoD for Mission

| Check | Required | Validation |
|-------|----------|------------|
| All Features Done | Yes | Every child Feature Done |
| Mission `[Test]` Done | Yes | E2E regression complete |
| Mission `[Docs]` Done | Yes | Mission guide complete |
| Mission `[SA Review]` Done | Yes | Architecture verified |
| Mission `[UAT]` Done | Yes | TPO acceptance complete |
| Caller is TPO | Yes | Only TPO can close Missions |

## DoD Enforcement Flow

### Feature Completion

```
[PROJECT_COORDINATOR] - Verifying Definition of Done for Feature #NUM...

| Workflow Phase | Status | Evidence |
|----------------|--------|----------|
| Development | Pass/Fail | PR link found |
| Code Review | Pass/Fail | Approval comment found |
| Test | Pass/Fail | Test completion comment |
| Docs | Pass/Fail | Docs completion comment |
| SA Review | Pass/Fail | SA approval comment |
| UAT | Pass/Fail | UAT approval comment |
```

**If checks fail**: REJECT with missing items, do NOT update status.

### Feature with Dev Subtasks

```
[PROJECT_COORDINATOR] - Verifying Feature DoD for #NUM...

| Dev Subtask | Status |
|-------------|--------|
| [Dev] Component 1 #X | Done/Not Done |
| [Dev] Component 2 #Y | Done/Not Done |

| Workflow Phase | Status |
|----------------|--------|
| Development | All Dev subtasks complete |
| Code Review | Approved |
| Test | Complete |
| Docs | Complete |
| SA Review | Approved |
| UAT | Accepted |
```

**Feature cannot be marked Done until ALL workflow phases complete and all Dev subtasks (if any) are Done.**

## Common Gaps

| Gap | Resolution |
|-----|------------|
| No PR link | Worker must provide PR link in Feature comment |
| Feature PR not merged | **User action** - not an agent DoD check |
| Mission branch not merged to main | **User action** - not an agent DoD check |
| No code review approval | Worker must get Code Reviewer approval |
| **Minor/Medium issues unresolved** | Code Reviewer rejects - ALL issues must be fixed |
| Tests missing | Worker must write tests per Gherkin scenarios |
| Tests failing | Worker must fix failures |
| Spec not met | Worker must address MUST/MUST NOT violations |
| Workflow phase incomplete | Complete all phases before closing Feature |
| Dev subtask incomplete | Complete all Dev subtasks before Feature phases |
| UAT not verified | TPO must verify and add UAT comment |
| Open Query blocking Feature | Resolve Query before proceeding |
| Query missing Resolution Summary | Add structured resolution comment before closing |

## Related References

- `definition-of-ready.md` - Pre-work checklist
- `project-coordinator/references/ticket-templates.md` - Full templates with DoR/DoD
- `drive-mode-protocol.md` - Verification templates for Drive Mode
