# Git Workflow

Standard Git workflow for all code-changing roles. Supports branching from and merging to any specified base branch.

## Base Branch Confirmation (REQUIRED)

**CRITICAL**: Before starting any work that involves branching, you MUST ask the user to confirm the base branch.

### When to Ask

Ask when:
- Starting work on a new ticket/task
- Creating a new feature branch
- Creating a PR

### How to Ask

Use the AskUserQuestion tool:

```
Question: "Which branch should I branch from and merge back to?"
Options:
- main (Recommended)
- develop
- Other (specify)
```

### Remember the Answer

Once the user specifies the base branch for a task, use it consistently for:
1. Creating the feature branch (`git checkout {base_branch} && git pull`)
2. Targeting the PR (`base: {base_branch}`)
3. Documenting in progress comments

## Branch Workflow

```
1. Start from base branch → git checkout {base_branch} && git pull
2. Create feature branch → git checkout -b {branch-name}
3. Do work → Commit with ticket ID prefix
4. Push branch → git push -u origin {branch-name}
5. Create PR → Target: {base_branch}
6. PR merged → Branch merged to {base_branch}
```

## Branch Naming

**Pattern**: `{type}/{team}/{TICKET-ID}-{description}`

| Component | Values |
|-----------|--------|
| `type` | `feature`, `fix`, `refactor`, `docs`, `test` |
| `team` | From project's `claude.md` (e.g., `platform`, `portal`) |
| `TICKET-ID` | System-specific (e.g., `LIN-101`, `GH-101`, or omit if none) |
| `description` | Brief slug (e.g., `password-reset-api`) |

**Examples**:
```bash
feature/platform/LIN-101-password-reset-api   # Linear
feature/platform/GH-101-password-reset-api    # GitHub
feature/platform/password-reset-api           # No ticket system
```

## Commit Message Format

**Pattern**: `[TICKET-ID] Brief description`

```bash
[LIN-123] Add password reset endpoint      # Linear
[GH-123] Add password reset endpoint       # GitHub
Add password reset endpoint                # No system (describe clearly)
```

Include ticket link in commit body when helpful:
```
[LIN-123] Add password reset endpoint

- Implement POST /api/v1/auth/reset
- Add email notification service call

Ticket: https://linear.app/team/issue/LIN-123
```

## PR Creation

When creating a PR:
- **Source branch**: Your feature branch
- **Target branch**: The configured base branch (not always `main`)
- **Title**: Include ticket ID (e.g., `[LIN-123] Add password reset endpoint`)

## Code Review Before Merge (MANDATORY)

**CRITICAL**: Code-altering roles (`[Backend]`, `[Frontend]`, `[Test]`) MUST NOT:
- Merge PR to base branch before Code Review passes
- Push directly to main/base branch (always use feature branch + PR)
- Self-approve and merge

**Workflow**:
1. Create PR on feature branch
2. Return control to TPgM (in Drive Mode) or request Code Review
3. Wait for Code Review approval
4. Only after approval → PR can be merged

## Starting Work Comment

When you begin work, include the base branch context:

```markdown
🚀 **Started work**
- Branch: `feature/platform/LIN-XXX-password-reset-api`
- Base: `{base_branch}` (confirmed with user)
- Approach: [Brief implementation approach]
```

## Git Commands Reference

### Starting Work
```bash
# Ensure base branch is up to date
git checkout {base_branch}
git pull origin {base_branch}

# Create feature branch
git checkout -b feature/{team}/LIN-XXX-description
```

### During Work
```bash
# Commit with ticket reference
git add .
git commit -m "[LIN-XXX] Description of change"

# Push to remote
git push -u origin feature/{team}/LIN-XXX-description
```

### Keeping Up to Date
```bash
# If base branch has moved ahead, rebase or merge
git fetch origin
git rebase origin/{base_branch}
# or
git merge origin/{base_branch}
```

## Role-Specific Notes

All code-changing roles follow this workflow:
- **Backend Developer**: Implementation + tests
- **Frontend Developer**: UI + component/E2E tests
- **Backend Tester**: Dedicated test suites
- **Frontend Tester**: Dedicated test suites
- **Tech Doc Writer**: Documentation files
- **MCP Server Developer**: MCP server code

## Summary

1. **Always ask the user** which base branch to use before branching
2. Branch from and merge back to the **user-specified base branch**
3. Document the base branch in progress comments
4. Target PRs to the specified base branch
