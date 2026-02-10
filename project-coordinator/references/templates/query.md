# Query Template (Communication Protocol)

**Content from**: Any role discovering a gap
**Title format**: `[Query] {Subject} ({Target Team})`
**Purpose**: Formalize discovery gaps that require cross-team or intra-team resolution

## Hierarchy Position

Query is at the **same level as Features** - a child of Mission:

```
[Mission] Password Reset Capability
├── [Backend] Add reset endpoint (Feature)
├── [Frontend] Add reset form (Feature)  ← Gap discovered here
├── [Bug] Fix validation (Bug Feature)
└── [Query] API rate limit unclear (Backend Team)  ← Sibling to Features
```

**Key differences from Features:**
- **No subtasks** - Query is resolved through discussion, not implementation
- **No workflow phases** - Query is resolved through human discussion
- **Has "Originating Ticket" link** - Separate from parent; links to the Feature where gap was found
- **Blocks originating Feature** - Dynamic blocker until resolved

## When to Use

| Situation | Use [Query]? |
|-----------|--------------|
| Frontend discovers Backend API limitation | ✅ Yes |
| Dev finds unclear spec during implementation | ✅ Yes |
| Tester identifies missing edge case coverage | ✅ Yes |
| SA needs clarification from another domain | ✅ Yes |
| Simple bug in own team's code | ❌ No - use `[Bug]` |
| Missing requirement | ❌ No - route to TPO |

## Template Structure

```markdown
## Originating Context
- **Originating Ticket**: [TICKET-ID] - [Title]
- **Originating Role**: [Role that discovered the gap]
- **Discovery Phase**: [Planning / Dev / Test / Review]

## Target
- **Target Team**: [Team slug or name]
- **Target Domain**: [Backend API / Frontend / Data / Infrastructure / etc.]

## Gap Description

### What We Found
[Describe the technical gap or limitation discovered]

### What We Expected
[What the originating team expected to exist or work]

### Why This Matters
[Impact on the originating work - why this blocks progress]

## Technical Details
[Include relevant code snippets, API calls, error messages, specs referenced]

## Questions for Target Team
1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3]

## Proposed Solutions (Optional)
[If the originating team has suggestions]

## References
- Related ADR: [Link if applicable]
- Related API Spec: [Link if applicable]
```

## DoR: Definition of Ready (Before Creation)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Title format | `[Query] {Subject} ({Target Team})` | ✅ Enforced |
| Parent (Epic) | Linked via native parent field | ✅ Enforced |
| Originating Ticket | Linked via `relatesTo` field (separate from parent) | ✅ Enforced |
| Target Team | Specified in body | ✅ Enforced |
| Gap Description | "What We Found" not empty | ✅ Enforced |
| Technical Details | Section exists | ✅ Enforced |
| At least one question | Questions section not empty | ✅ Enforced |

## DoD: Definition of Done (Before Closing)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Resolution provided | Target team answered questions | ✅ Enforced |
| Resolution Summary comment | Structured summary added | ✅ Enforced |
| Caller is resolver | Human in the loop closes after resolution | ✅ Enforced |

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

## Automatic Blocker Behavior

**When PC creates a `[Query]` ticket:**

1. Set parent to the Mission (same parent as originating Feature)
2. Set `relatesTo` link to the originating Feature
3. **Add Query to originating Feature's `blockedBy` list**
4. Log the blocker relationship

**Workflow Constraint**: Feature cannot proceed while it has an open `[Query]` blocker.

**When PC marks a `[Query]` as Done:**

1. **Remove Query from Feature's `blockedBy` list**
2. Verify Resolution Summary comment exists
3. Mark Query as Done
