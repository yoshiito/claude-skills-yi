# Git Workflow

Git workflow for all code-changing roles.

## Branch Management — USER OWNED

**CRITICAL**: Claude Code does NOT manage branches or decide branch targets.

| Responsibility | Owner |
|----------------|-------|
| Create Epic branch | User |
| Create Story branches | User |
| Specify branch targets | User |
| **Merge to Epic branch** | **Code Reviewer** |
| Merge Epic to main | User |
| Delete branches | User |
| **Commit to current branch** | **Claude** |
| **Push current branch** | **Claude** |

**Why**: Branch lifecycle management is unreliable in agentic workflows. Clean separation: user owns git topology, Claude owns code changes within specified branches.

## Branch Hierarchy

```
main
└── feature/password-reset (Epic branch - User creates, User merges to main)
    ├── feature/password-reset/backend-endpoint (Story branch)
    ├── feature/password-reset/frontend-form (Story branch)
    └── feature/password-reset/bugfix-validation (Bug branch)
```

| Branch Level | Created By | Merged By | Target |
|--------------|------------|-----------|--------|
| Epic branch | User | User | main |
| Story/Task/Bug branch | User | Code Reviewer | Epic branch |

## Branch Confirmation Protocol — BLOCKING

**⛔ AGENTS MUST NOT START WORK WITHOUT EXPLICIT BRANCH CONFIRMATION**

Before any `[Dev]` work begins, the agent MUST prompt:

```
⛔ BRANCH CONFIRMATION REQUIRED

I cannot proceed without knowing the target branch.

Please confirm:
  Epic Branch: _________________ (e.g., feature/password-reset)

This branch will be the PR target for all Story/Task/Bug work.

Waiting for your response...
```

**This is a HARD BLOCK.** Do not:
- Assume `main` is the target
- Guess based on ticket names
- Proceed without explicit user confirmation

**Valid responses:**
- `feature/password-reset` → Use this as Epic branch
- `main` → Use main directly (no Epic branch model)
- Branch name from Epic ticket → Use specified branch

## Claude's Git Workflow

```
1. CONFIRM target branch with user (BLOCKING)
2. Check current branch → git branch --show-current
3. Pull latest → git pull
4. Do work → Make changes
5. Commit → git add <files> && git commit
6. Push → git push
7. Create PR → gh pr create --base {epic-branch}
```

**That's it.** No branch creation. No switching. No guessing targets.

## Before Starting Work

```bash
# Just verify where you are
git branch --show-current
git status
```

If user wants work on a different branch, they will switch to it first.

## Commit Message Format

**Pattern**: `type(scope): Brief description`

| Type | Use For |
|------|---------|
| `feat` | New feature/capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructuring |
| `test` | Test additions/changes |

```bash
feat(auth): Add password reset endpoint
fix(api): Handle null user gracefully
docs(readme): Update installation steps
refactor(utils): Extract validation helpers
```

With ticket ID (if ticket system configured):
```bash
feat(auth): [LIN-123] Add password reset endpoint
fix(api): [GH-456] Handle null user gracefully
```

## PR Creation

Claude creates PRs targeting the Epic branch (not main):

```bash
gh pr create --base feature/password-reset --title "feat(auth): Add password reset" --body "Description"
```

**PR Target Rules:**
- Story/Task/Bug PRs → Target Epic branch
- Epic branch → Target main (User merges)

## PR Merging

| PR Type | Merged By | Command |
|---------|-----------|---------|
| Story/Task/Bug → Epic | Code Reviewer | `gh pr merge --squash` |
| Epic → main | User | Manual |

**Code Reviewer merges** Story/Task/Bug PRs to Epic branch after approval.
**User merges** Epic branch to main when feature is complete.

## Git Commands Reference

### Check State
```bash
git branch --show-current    # What branch am I on?
git status                   # What's changed?
git log --oneline -5         # Recent commits
```

### Commit Work
```bash
git add <specific-files>     # Stage specific files (preferred)
git commit -m "type(scope): Description"
git push                     # Push to current branch
```

### If Push Fails (Remote Ahead)
```bash
git pull --rebase            # Pull and rebase local commits
git push                     # Try again
```

## What Claude Does NOT Do

- Create branches
- Switch branches
- Merge Epic branch to main
- Delete branches
- Force push
- Rebase across branches
- **Assume or guess branch targets**

**Code Reviewer CAN**: Merge Story/Task/Bug PRs to Epic branch (after approval).

User handles branch topology (create, switch, delete, Epic→main merge). Claude commits to current branch and creates PRs to user-specified targets.
