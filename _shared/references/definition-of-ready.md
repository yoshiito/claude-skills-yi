# Definition of Ready (DoR)

**Universal checklist for ticket readiness.** Project Coordinator enforces this at ticket creation time.

## Who Uses This

| Role | Uses DoR For |
|------|--------------|
| **Project Coordinator** | **ENFORCES** - rejects ticket creation if DoR not met |
| **Solutions Architect** | Prepares Features to pass DoR checks |
| **TPO** | Prepares Missions (Epics) to pass DoR checks |
| **PM** | Additional validation before Plan Execution Mode |
| **Workers** | Understands what "ready" looks like |

## Enforcement Point

**Project Coordinator is the enforcer.** When any role invokes `[PROJECT_COORDINATOR] Create`, the coordinator:
1. Parses the provided content
2. Verifies ALL required elements exist
3. **REJECTS with specific gaps** if checks fail
4. Only creates ticket if ALL checks pass

**Roles cannot bypass this gate.** Fix the content and retry.

## Definition of Ready Checklist

### For Parent Issues (Content from TPO)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Feature] {name}` format |
| MRD in description | ✅ | Problem, users, success criteria defined |
| **UAT criteria defined** | ✅ | What TPO will verify before accepting |
| Team assigned | ✅ | From project's `Team Slug` in claude.md |
| No open questions | ✅ | All clarifications resolved |

**UAT Criteria**: TPO must define specific, verifiable criteria that they will check before accepting the feature as complete. Project Coordinator will provide template guidance if missing.

### For Features (Content from SA)

**Features are quality-bounded work units** - the largest scope where quality can be guaranteed.

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Type] {description}` - Type: Backend/Frontend/Bug |
| Parent linked | ✅ | Native field, not body text (links to Mission) |
| Technical Spec | ✅ | MUST/MUST NOT/SHOULD constraints |
| Gherkin scenarios | ✅ | Given/When/Then for validation |
| Testing Notes | ✅ | What tests to write, edge cases to cover |
| Dependencies | ✅ | `blockedBy` set via native field (or explicitly "None") |
| Feature branch | ✅ | User-provided branch name (BLOCKING) |
| Mission statement | ✅ | Clear, singular outcome defining "done" |
| No open questions | ✅ | All clarifications resolved in ticket |
| Quality-bounded | ✅ | See checklist below |
| **No unresolved Queries** | ✅ | All linked `[Query]` tickets must be resolved |

**Note**: Dev subtasks are OPTIONAL - only create if implementation needs breakdown.

### For Query Tickets (Content from Any Role)

| Check | Required | Validation |
|-------|----------|------------|
| Title | ✅ | `[Query] {Subject} ({Target Team})` format |
| Parent (Epic) | ✅ | Linked via native parent field |
| Originating Ticket | ✅ | Linked via `relatesTo` field |
| Target Team | ✅ | Specified in body |
| Gap Description | ✅ | "What We Found" section not empty |
| Technical Details | ✅ | Section exists with context |
| Questions | ✅ | At least one question for target team |

**Note**: Query has no workflow phases - it is resolved through human discussion.

### Quality-Bounded Feature Checklist (Verified by SA)

**Features are quality-bounded** - sized so all quality activities can happen comprehensively at the Feature level.

**Quality Boundary Checklist:**

| Criterion | Question | If NO |
|-----------|----------|-------|
| **Reviewable** | Can code review validate this comprehensively in one session? | Split into smaller Features |
| **Testable** | Can tests cover this feature completely? | Split into smaller Features |
| **UAT-able** | Can TPO verify the outcome in one pass? | Split into smaller Features |
| **Architecturally coherent** | Can SA review compliance holistically? | Split into smaller Features |
| **Mission-driven** | Is there ONE clear statement of what "done" looks like? | Clarify or split |

**Workflow Phases (at Feature level, NOT separate tickets):**

| Phase | Worker | When |
|-------|--------|------|
| Development | Developer | After Feature branch confirmed |
| Code Review | Code Reviewer | After PR created |
| Test | Tester | After Code Review approved |
| Docs | Tech Doc Writer | After Test complete |
| SA Review | Solutions Architect | After Docs complete |
| UAT | TPO | After SA Review complete |

**Dev Subtasks (OPTIONAL):**
- Only create `[Dev]` subtasks if implementation is complex and needs breakdown
- Dev subtasks are for organizing implementation work, not for quality phases
- Quality phases (Code Review, Test, etc.) always happen at Feature level

**Query as Dynamic Blocker**: When a `[Query]` is raised against a Feature, it blocks that Feature's development. The Feature cannot proceed while any linked Query is open.

### For Mission-Level Completeness (Verified by SA/PM)

**In addition to Feature-level workflow phases**, each Mission (Epic) MUST have cross-cutting tickets:

| Mission-Level Ticket | Required | Purpose |
|---------------------|----------|---------|
| `[Test] {Mission} E2E Regression` | ✅ ALWAYS | Full integration/regression testing across all Features |
| `[Docs] {Mission} Guide` | ✅ for user-facing | Comprehensive documentation for the Mission |
| `[SA Review] {Mission} Architecture` | ✅ ALWAYS | Architecture compliance across all Features |
| `[UAT] {Mission} Acceptance` | ✅ ALWAYS | Mission acceptance by TPO |

**blockedBy relationships:**
- Mission `[Test]` → blockedBy all Feature containers
- Mission `[Docs]` → blockedBy Mission `[Test]`
- Mission `[SA Review]` → blockedBy Mission `[Docs]`
- Mission `[UAT]` → blockedBy Mission `[SA Review]`

### Why Quality-Bounded Features?

**Feature-Level Quality Phases:**
- Each Feature is quality-bounded - reviewable, testable, UAT-able in one pass
- Workflow phases happen at Feature level, reducing context switching
- Larger scope means fewer handoffs and better coherence
- Dev subtasks (if used) are for implementation organization only

**Mission-Level Cross-Cutting:**
- Integration/E2E testing across all Features
- Regression testing for the whole Mission
- Architecture compliance verification across all Features
- Mission acceptance by TPO
- Catches issues that only appear when Features interact

**If Feature is too large to review/test comprehensively**: Split into smaller Features until quality can be guaranteed.

### Quality Boundary Checklist (Features Only)

- [ ] **Reviewable**: Code review can comprehensively validate in one session
- [ ] **Testable**: Tests can cover this feature completely
- [ ] **UAT-able**: TPO can verify the outcome in one pass
- [ ] **Architecturally coherent**: SA can review compliance holistically
- [ ] **Mission-driven**: ONE clear statement of what "done" looks like
- [ ] **Feature branch**: User has provided branch name (BLOCKING)

## DoR Enforcement

### When Creating Features (SA)

Before `create_issue`, verify ALL checks pass. If any fail:

```
❌ FEATURE CREATION BLOCKED

Title: "[Backend] User API"

Missing:
- Technical Spec: Not defined
- Gherkin scenarios: Missing
- Feature branch: Not provided by user
- Mission statement: Not defined

Action: Complete these before creating Feature.
```

### When Entering Plan Execution Mode (PM)

Before driving, verify ALL Features pass DoR. If any fail:

```
[PM] - ⛔ Cannot enter Plan Execution Mode

Definition of Ready not met:

| Feature | Missing | Route To |
|---------|---------|----------|
| [ID-1] | Technical Spec | SA |
| [ID-2] | Feature branch | User (BLOCKING) |

Fix these gaps, then invoke Plan Execution Mode again.
```

### Routing When DoR Fails

| Missing Item | Route To |
|--------------|----------|
| MRD/Requirements | TPO |
| UAT criteria | TPO |
| Technical Spec | Solutions Architect |
| Gherkin scenarios | Solutions Architect |
| Dependencies | Solutions Architect |
| Feature branch | User (BLOCKING - work cannot start) |
| Mission statement | Solutions Architect |
| Mission-level tickets (`[Test]`, `[Docs]`, `[SA Review]`, `[UAT]`) | Solutions Architect |
| Unresolved `[Query]` tickets | Target Team (human resolution required) |
| Test strategy | Tester |
| Documentation plan | Tech Doc Writer |

## Common Issues

| Issue | Fix |
|-------|-----|
| Vague acceptance criteria | Add MUST/MUST NOT/SHOULD constraints |
| Missing dependencies | SA reviews Feature ordering |
| No Gherkin scenarios | SA adds Given/When/Then |
| Open questions in Feature | Resolve via comments, then update Feature |
| Title missing prefix | Use `[Backend]`, `[Frontend]`, `[Bug]` |
| No UAT criteria (Mission) | TPO adds verifiable UAT checklist |
| Feature too large to review | Split into smaller quality-bounded Features |
| No Feature branch | User MUST provide branch (BLOCKING) |
| Unresolved Query blocking Feature | Resolve Query with target team before proceeding |
| Query missing target team | Specify team/domain in Query body |

## Related References

- `definition-of-done.md` - Completion checklist
- `project-coordinator/SKILL.md` - Ticket operations and quality enforcement
