# Ticketing Core Rules

Universal rules for all ticket systems. System-specific mappings and commands are in separate files.

## PM Tool Enforcement (MANDATORY)

**CRITICAL**: Skills MUST use the project's configured ticket system. Falling back to markdown files when a proper PM tool is configured is a VIOLATION.

### Pre-Work Check (Required Before ANY Ticket Operation)

```
1. READ project's claude.md → find "Ticket System" field
2. IF Ticket System = "linear" → MUST use Linear MCP commands
3. IF Ticket System = "github" → MUST use GitHub Issues/Projects
4. IF Ticket System = "none" → ONLY THEN use plan files
5. IF Ticket System field is MISSING → ASK user to configure it first
```

### Enforcement Rules

| Configured System | Allowed | NOT Allowed |
|-------------------|---------|-------------|
| `linear` | Linear MCP commands | Creating `docs/plans/*.md`, markdown checklists as tickets |
| `github` | `gh` CLI, GitHub API | Creating `docs/plans/*.md`, markdown checklists as tickets |
| `none` | `docs/plans/*.md` | N/A (this is the fallback) |

### Failure Modes to Avoid

**DO NOT**:
- Create a markdown plan file "because Linear is slow"
- Use `docs/plans/` when Linear/GitHub is configured
- Assume "no MCP available" without checking
- Fall back to markdown "temporarily"

**IF PM tool is unavailable** (MCP not connected, API error):
1. STOP and inform user: "Linear MCP is not available. Please connect it or change Ticket System to 'none'."
2. DO NOT proceed with markdown fallback
3. Wait for user decision

### Example Enforcement Check

```python
# Pseudocode every skill should follow:
ticket_system = read_claude_md().get("Ticket System")

if ticket_system == "linear":
    if not mcp_linear_available():
        STOP("Linear MCP not connected. Cannot proceed.")
    use_linear_commands()  # REQUIRED

elif ticket_system == "github":
    if not gh_cli_available():
        STOP("GitHub CLI not available. Cannot proceed.")
    use_github_commands()  # REQUIRED

elif ticket_system == "none":
    use_plan_files()  # OK

else:
    ASK_USER("Ticket System not configured. Please set it in claude.md.")
```

## Hierarchy (4 Levels)

All ticket systems map to this hierarchy:

| Level | Purpose | Created By |
|-------|---------|------------|
| **Initiative** | Strategic company goal | Leadership/TPO |
| **Project** | Time-bound deliverable | TPO |
| **Issue** | User-facing feature | TPO |
| **Sub-Issue** | Implementation work unit | Solutions Architect |

```
Initiative: "Q1 User Growth"
└── Project: "User Authentication System"
    └── Issue: "Implement Password Reset"
        ├── Sub-Issue: [Backend] Password reset API
        ├── Sub-Issue: [Frontend] Reset form UI
        └── Sub-Issue: [Docs] Password reset guide
```

## Sub-Issue Prefixes

| Prefix | Assigned To | Includes |
|--------|-------------|----------|
| `[Backend]` | Backend Developer | Implementation + unit/integration tests |
| `[Frontend]` | Frontend Developer | UI + component/E2E tests |
| `[Docs]` | Tech Doc Writer | Documentation |
| `[API Design]` | API Designer | Contract design (when needed) |
| `[Test]` | Tester | Dedicated QA effort (when needed) |

## Pre-Creation Checklist

**CRITICAL**: Never assume project context. Always confirm before creating.

- [ ] Fetch available options from ticket system (teams, projects)
- [ ] Present options to user for selection
- [ ] Confirm: team, project, assignee
- [ ] If project doesn't exist, create it first

## Sub-Issue Quality Checklist (INVEST)

Before creating any sub-issue:

- [ ] **Independent**: Can start without waiting for others? (If not, set dependency)
- [ ] **Negotiable**: Approach is flexible, acceptance criteria is fixed?
- [ ] **Valuable**: Moves feature toward "Done"?
- [ ] **Estimable**: Bounded scope with known files and clear end state?
- [ ] **Small**: Single logical change (one PR, one concern)?
- [ ] **Testable**: Technical Spec + Gherkin scenarios are specific and verifiable?
- [ ] **Context linked**: Parent issue, ADRs, specs included?

## Mandatory Progress Updates

**All workers MUST update ticket status AND add comments at these points.**

### When Starting Work

**Status**: Move ticket to **In Progress**

**Comment**:
```markdown
🚀 **Started**
- Branch: `{branch-name}`
- Base: `{base_branch}` (confirmed with user)
- Approach: [Brief implementation approach]
```

### During Work (for tasks > 1 day)

**Status**: Keep as **In Progress**

**Comment**:
```markdown
📝 **Progress**
- Done: [What's completed]
- Next: [Current focus]
- Blockers: [Any issues]
```

### When PR Created

**Status**: Move ticket to **In Review**

**Comment**:
```markdown
🔍 **Ready for review**
- PR: [link] (targeting {base_branch})
- Changes: [Brief summary]
- Tests: [What's covered]
```

### When Complete

**Status**: Move ticket to **Done** (or let auto-close on PR merge if supported)

**Comment**:
```markdown
✅ **Completed**
- PR merged: [link]
- Files: [Key files changed]
- Notes: [Anything for QA/next steps]
```

## Git Workflow

See `git-workflow.md` for complete Git workflow including:
- **Base branch confirmation** (MUST ask user before branching)
- Branch naming conventions
- Commit message format
- PR creation guidelines

**Key point**: Always ask the user which branch to branch from and merge back to. Do not assume `main`.

## Ticket Status Flow

| Stage | Status | Updated By |
|-------|--------|------------|
| Created | Backlog/Todo | TPO/Architect |
| Work started | In Progress | Worker |
| PR created | In Review | Worker |
| PR merged | Done | Worker/Auto |

## Role Responsibilities

### TPO (Technical Product Owner)
- Creates parent Issues with requirements
- Links to MRD, design docs
- Verifies acceptance criteria before closing

### Solutions Architect
- Breaks Issues into Sub-Issues after design
- Sets dependencies between sub-issues
- Links ADRs and technical specs

### Developers (Backend/Frontend)
- Posts progress comments (mandatory)
- Commits with ticket ID prefix
- Updates status as work progresses

### Testers
- Posts test coverage summary on completion
- Documents tested scenarios

### Tech Doc Writer
- Posts documentation summary on completion
- Links to created/updated docs

### TPgM (Technical Program Manager)
- Tracks progress across all sub-issues
- Verifies traceability before closing parent
- Escalates blockers

## Scope Boundary Check

Before creating tickets, verify ownership per project's `claude.md`:

- [ ] This domain is within my ownership?
- [ ] If NO: Document gap, tag domain owner, do NOT create ticket

## Worker Completion Checklist

Before marking any work as done:

- [ ] All commits reference ticket ID
- [ ] PR title includes ticket ID
- [ ] "Started" comment posted
- [ ] "Completed" comment posted
- [ ] Ticket status reflects reality
- [ ] Blockers/notes documented

## Ticket Templates

### Story/Task Template

```markdown
## Description
[What needs to be implemented]

## Context
- Parent Issue: [TICKET-ID - Parent name]
- ADR: [Link if applicable]
- API Spec: [Link if applicable]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

## Implementation Notes
[Technical guidance, patterns to follow]

## Testing
[Scenarios to cover, edge cases]
```

### Bug Template

```markdown
## Environment
[Platform, version, environment]

## Impact
[Critical/High/Medium/Low - business impact]

## Steps to Reproduce
1. [Step]
2. [Step]

## Actual Result
[What happens]

## Expected Result
[What should happen]

## Testing Notes
[How to verify fix]
```

## System-Specific References

- **Linear**: See `ticketing-linear.md`
- **GitHub Projects**: See `ticketing-github-projects.md`
- **No system**: See `ticketing-plan-file.md`
