nk# Git Workflow

Git workflow for all code-changing roles.

## Branch Management — USER OWNED

**CRITICAL**: Claude Code does NOT manage branches.

| Responsibility | Owner |
|----------------|-------|
| Create branches | User |
| Switch branches | User |
| Merge branches | User |
| Delete branches | User |
| **Commit to current branch** | **Claude** |
| **Push current branch** | **Claude** |

**Why**: Branch lifecycle management (create → work → merge → delete) is unreliable in agentic workflows. Clean separation: user owns git topology, Claude owns code changes.

## Claude's Git Workflow

```
1. Check current branch → git branch --show-current
2. Pull latest → git pull
3. Do work → Make changes
4. Commit → git add <files> && git commit
5. Push → git push
```

**That's it.** No branch creation. No merging. No switching.

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

## PR Creation (Optional)

Claude can create PRs if requested:

```bash
gh pr create --title "feat(auth): Add password reset" --body "Description"
```

**User decides** when/whether to merge. Claude does not merge PRs.

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
- Merge branches
- Delete branches
- Force push
- Rebase across branches

User handles all branch topology. Claude commits to wherever it is.
