# Branching Standards

**Universal rules for branch structure.** All ticket-creating roles enforce these at ticket creation; TPgM validates at DoR.

## The Rule: Max Depth 2

```
Level 0: main
Level 1: feature/{team}/{TICKET-ID}-{name}     ← Feature branch (OK to branch FROM)
Level 2: feature/{team}/{TICKET-ID}-{name}     ← Sub-feature (NEVER branch from this)
```

**Sub-issues branch from their parent's branch, never from siblings.**

## Correct Pattern

```
feature/tj_be/102-match-entry (Level 1 - parent issue branch)
    ├─ feature/tj_fe/139-radiogroup-molecule    (Level 2, base: 102)
    ├─ feature/tj_fe/140-set-type-selection     (Level 2, base: 102, blockedBy: #139)
    ├─ feature/tj_fe/141-matchdetail-break      (Level 2, base: 102, blockedBy: #140)
    └─ feature/tj_fe/145-radiogroup-tests       (Level 2, base: 102, blockedBy: #139)
```

All sub-issues are **siblings** from the same parent. Dependencies expressed via `blockedBy`, not branch nesting.

## Incorrect Pattern (NEVER DO THIS)

```
feature/tj_be/102-match-entry (Level 1)
    └─ feature/tj_fe/139-radiogroup-molecule (Level 2)
        └─ feature/tj_fe/140-set-type-selection (Level 3 ❌)
            └─ feature/tj_fe/141-matchdetail-break (Level 4 ❌)
```

Deep chaining causes: merge hell, rebase cascades, blocked work, noisy PR diffs.

## Workflow

### When Dependencies Exist Between Sub-Issues

1. Sub-issue #139 completes → merges into parent branch (`102-match-entry`)
2. Sub-issue #140 (which depends on #139) rebases from `102-match-entry` → now has #139's code
3. Sub-issue #140 completes → merges into parent branch
4. Repeat for remaining sub-issues

### Branch Information in Tickets

Every ticket MUST specify:

| Field | Description | Example |
|-------|-------------|---------|
| **Base Branch** | Branch to create from | `feature/tj_be/102-match-entry` or `main` |
| **Target Branch** | Branch for this work | `feature/tj_fe/139-radiogroup-molecule` |

## Determining Base Branch

| Scenario | Base Branch |
|----------|-------------|
| Top-level feature (no parent issue) | `main` |
| Sub-issue of a feature | Parent issue's branch |
| Sub-issue depends on sibling | Still parent's branch (use `blockedBy` for ordering) |

**NEVER** set base branch to a sibling sub-issue's branch.

## Validation

### At Ticket Creation (SA/TPO)

Before creating any ticket:

- [ ] Base Branch specified
- [ ] Base Branch is `main` OR a Level 1 feature branch
- [ ] Base Branch is NOT a sibling sub-issue's branch
- [ ] If depends on sibling: `blockedBy` set, NOT branch nesting

### At DoR Check (TPgM)

| Check | Required |
|-------|----------|
| Branch Information section exists | ✅ |
| Base Branch is max Level 1 | ✅ |
| Base Branch is not a sibling | ✅ |

**On failure**: `[TPgM] - ⛔ Invalid branch structure. Base branch targets Level 2+. Use parent issue's branch instead.`

## When Ticket System = "none"

Track branch strategy in plan file:

```markdown
## Branch Strategy

- **Feature Base**: feature/{team}/{name}
- **Sub-tasks**:
  | Task | Branch | Base | Blocked By |
  |------|--------|------|------------|
  | RadioGroup | feature/tj_fe/139-radiogroup | Feature Base | None |
  | SetType | feature/tj_fe/140-settype | Feature Base | #139 |
```

## Why This Matters

| Problem with Deep Chaining | Impact |
|---------------------------|--------|
| Merge order dependency | Must merge in exact sequence |
| Rebase cascade | Change to #139 requires rebasing #140, #141, etc. |
| PR noise | Each PR contains all ancestor changes |
| Blocked parallelism | Can't work on #141 until #140 merges |

Flat siblings with `blockedBy` allows parallel work, cleaner PRs, simpler merges.
