# Dev Subtask Template (OPTIONAL)

**Content from**: Solutions Architect (during work breakdown)
**Title format**: `[Dev] {component description}`
**Only create `[Dev]` subtasks if implementation needs breakdown.**

## `[Dev]` - Implementation Subtask

**Assigned to**: Developer (Backend/Frontend)
**Use when**: Implementation is complex and needs to be broken into independent components

## DoR: Definition of Ready (Before Start)

| Check | Required | PC Validates |
|-------|----------|--------------|
| Parent Feature exists | ✅ | ✅ Enforced |
| Technical Spec available | ✅ | ✅ Enforced |
| **Feature Branch confirmed** | ✅ (BLOCKING) | ✅ Enforced |

## DoD: Definition of Done (Before Complete)

| Check | Required | PC Validates |
|-------|----------|--------------|
| PR created | ✅ Link in comment | ✅ Enforced |
| PR targets Feature Branch | ✅ Verified | ✅ Enforced |
| Component complete | ✅ Confirmed in comment | ✅ Enforced |

## Branch Confirmation Protocol (BLOCKING)

Before starting ANY work, prompt user:

```
⛔ BRANCH CONFIRMATION REQUIRED

I cannot proceed without knowing the target branch.

Please confirm:
  Feature Branch: _________________ (e.g., feature/password-reset-backend)

This branch will be the PR target for this work.

Waiting for your response...
```

**Do NOT proceed until user provides explicit branch name.**

## Completion Comment Format

```markdown
✅ **[Dev] Subtask Complete**
- PR: [link] (targets `{feature-branch}`)
- Component: [What this subtask implemented]
- Files: [Key files changed]
- Ready for: Other Dev subtasks or Feature-level Code Review
```

**Note**: Dev subtasks contribute to the parent Feature. Quality phases (Code Review, Test, etc.) happen at Feature level, not per Dev subtask.

## When to Create Dev Subtasks

| Situation | Create `[Dev]` Subtasks? |
|-----------|-------------------------|
| Multiple independent components | ✅ Yes |
| Different expertise needed for parts | ✅ Yes |
| Large implementation, but quality phases work at Feature level | ✅ Yes |
| Simple, straightforward implementation | ❌ No |
| Single developer can complete in one session | ❌ No |
| No natural component boundaries | ❌ No |

## Example: When to Use Dev Subtasks

```
[Backend] Add password reset endpoint        ← Feature
├── [Dev] Token generation and validation    ← Complex crypto logic
├── [Dev] Email integration                  ← Separate service integration
└── [Dev] Rate limiting                      ← Distinct security component
```

Each `[Dev]` subtask produces a PR. The Feature-level Code Review happens once all Dev subtasks are complete.
