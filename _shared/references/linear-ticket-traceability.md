# Linear Ticket Traceability Guide

Comprehensive guide for using Linear to track work from requirements through implementation and verification.

## Linear Hierarchy Model

Linear uses a specific hierarchy different from traditional tools like Jira:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LINEAR HIERARCHY                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INITIATIVE (Company Objective) ─── Optional, Enterprise/Plus feature   │
│  └── PROJECT (Deliverable/Feature Set)                                   │
│       └── ISSUE (Parent - Feature/Story)                                 │
│            └── SUB-ISSUE (Task - Implementation Unit)                    │
│                                                                          │
│  Example:                                                                │
│  Initiative: "Q1 2025 User Growth" (if enabled)                          │
│  └── Project: "User Authentication System"                               │
│       └── Issue: "Implement Password Reset Flow"                         │
│            ├── Sub-issue: [Backend] Password reset API (incl. tests)     │
│            ├── Sub-issue: [Frontend] Reset password UI (incl. tests)     │
│            └── Sub-issue: [Docs] Password reset documentation            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Initiative Availability

**Note**: Initiatives are a Linear feature available on certain plans. If your workspace doesn't have Initiatives:
- Project becomes the top-level container
- Use Project description or labels to track strategic alignment

### Hierarchy Mapping (Linear vs Jira Equivalent)

| Linear Concept | Jira Equivalent | Created By | Purpose | Availability |
|----------------|-----------------|------------|---------|--------------|
| **Initiative** | Epic (high-level) | Leadership/TPO | Company objectives | Enterprise/Plus |
| **Project** | Epic | TPO | Time-bound deliverable | All plans |
| **Issue** | Story/Feature | TPO | User-facing feature | All plans |
| **Sub-Issue** | Task/Sub-task | Solutions Architect | Implementation work unit | All plans |

### When to Use Each Level

| Level | Use When | Example |
|-------|----------|---------|
| **Initiative** | Strategic company goal spanning months (if available) | "Improve User Retention" |
| **Project** | Feature set with defined scope and timeline | "User Settings Redesign" |
| **Issue (Parent)** | Single feature a user would recognize | "Add dark mode toggle" |
| **Sub-Issue** | Technical work unit for one person | "[Backend] Dark mode API" |

### Issue Breakdown Decision

```
Is this a company-wide objective? → Initiative (if available) or Project
Is this a multi-feature deliverable? → Project
Is this something a user would notice? → Issue (Parent)
Is this technical implementation work? → Sub-Issue
```

## Confirmation Before Creating Issues

**CRITICAL**: Never assume which Initiative, Project, or Team an issue belongs to. Fetch options from Linear and let the user choose.

### Pre-Creation Workflow

Before creating any Issue or Sub-issue:

**Step 1: Fetch available options from Linear**

```python
# Get teams
teams = mcp.list_teams()

# Get projects (optionally filtered by team)
projects = mcp.list_projects(team="TeamName")
```

**Step 2: Present options to user for selection**

```
Before creating this issue, please select the Linear context:

Issue: "[Title of the issue]"

**Team**: (fetched from Linear)
1. Platform Team
2. Portal Team
3. Data Team

**Project**: (fetched from Linear)
1. User Authentication System
2. Q1 Platform Improvements
3. Customer Portal Redesign
4. [Create new project]

**Initiative** (if available):
1. Q1 2025 User Growth
2. Platform Reliability
3. [None / Not applicable]

Which options should I use? (or specify different values)
```

**Step 3: Handle "Create new" if needed**

If the user needs a new Project that doesn't exist, create it first:
```python
mcp.create_project(name="New Project Name", team="TeamName")
```

### Why Fetch from Linear

- Shows **actual available options**, not guessed defaults
- Options change as projects complete or start
- Prevents typos in project/team names
- User can make informed choice from real data

### MCP Tools for Fetching Options

```python
# List all teams
teams = mcp.list_teams()
# → [{"name": "Platform Team", "id": "..."}, ...]

# List projects (all or filtered)
projects = mcp.list_projects()
projects = mcp.list_projects(team="Platform Team")
projects = mcp.list_projects(state="started")  # Active only

# Get specific project details
project = mcp.get_project(query="User Authentication")
```

### Optional: Pre-select with Defaults

You can define defaults in `claude.md` to **pre-select** (not skip confirmation):

```markdown
### Linear Context Defaults
| Field | Default Value |
|-------|---------------|
| Team | Platform Team |
| Project | User Authentication System |
```

When defaults exist, show them as pre-selected but still present all options.

## INVEST Principle for Sub-Issues

Every sub-issue should follow the INVEST principle to enable independent developer work:

| Principle | Description | Validation |
|-----------|-------------|------------|
| **I**ndependent | Can be worked on without blocking/being blocked by other sub-issues | Dependencies tracked via Linear's `blockedBy`/`blocks` relations |
| **N**egotiable | Details can be discussed between architect and developer | Implementation approach is flexible, acceptance criteria is fixed |
| **V**aluable | Delivers tangible value toward parent issue completion | Moves the feature closer to "Done" |
| **E**stimable | Scope is clear enough to estimate effort | Developer can provide time estimate |
| **S**mall | Completable within a sprint (ideally 1-3 days) | If larger, break into smaller sub-issues |
| **T**estable | Has clear acceptance criteria that can be verified | Includes specific test scenarios |

### Sub-Issue Quality Checklist

Before creating a sub-issue, verify:

- [ ] **Independent**: Can developer start without waiting for other sub-issues? (If not, set `blockedBy`)
- [ ] **Clear scope**: Does the description define what's in/out of scope?
- [ ] **Testable**: Are acceptance criteria specific and verifiable?
- [ ] **Right size**: Can this be completed in 1-3 days?
- [ ] **Context provided**: Links to parent issue, ADRs, API specs included?

## Ticket Lifecycle Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TICKET LIFECYCLE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TPO creates                Solutions Architect                          │
│  feature ticket  ──────────► breaks down into    ──────────► Workers     │
│  (parent)                    sub-issues                       assigned   │
│                                                                          │
│  Sub-issues created for:                                                 │
│  • Backend work (assigned to Backend Developer)                          │
│  • Frontend work (assigned to Frontend Developer)                        │
│  • Tests (assigned to Backend/Frontend Tester)                           │
│  • Documentation (assigned to Tech Doc Writer)                           │
│                                                                          │
│  Each worker:                                                            │
│  1. Moves ticket to "In Progress"                                        │
│  2. Does work, commits with [LIN-XXX]                                    │
│  3. Updates ticket with progress comment                                 │
│  4. Moves to "In Review" when PR created                                 │
│  5. Moves to "Done" when merged                                          │
│                                                                          │
│  Parent auto-closes when all sub-issues complete                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Issue Breakdown Workflow

### Phase 1: TPO Creates Parent Issue

The Technical Product Owner creates the main feature/work item:

```markdown
Title: [Feature Name]
Description:
  - User story
  - Acceptance criteria
  - Out of scope items
Labels: Feature | Bug | Improvement
```

### Phase 2: Solutions Architect Creates Sub-Issues

After architecture design, break down into logical work units.

**Standard Sub-Issues (Implementation includes tests):**

| Sub-Issue Prefix | Assigned To | Includes |
|------------------|-------------|----------|
| `[Backend]` | Backend Developer | API implementation + unit/integration tests |
| `[Frontend]` | Frontend Developer | UI components + component/E2E tests |
| `[Docs]` | Tech Doc Writer | API docs, guides |

**Optional Sub-Issues (when needed):**

| Sub-Issue Prefix | When to Create |
|------------------|----------------|
| `[API Design]` | New/complex API needing contract design first |
| `[Test]` | Large features needing dedicated QA effort |
| `[Integration Test]` | Cross-component E2E testing |

**Key Principle:** Developers own their tests. Separate test sub-issues only for dedicated QA efforts or cross-component integration testing.

**Sub-Issue Creation Checklist:**
- [ ] Each sub-issue has clear acceptance criteria
- [ ] Dependencies between sub-issues are noted
- [ ] Appropriate assignee set
- [ ] Parent issue linked
- [ ] Estimate provided if possible

### Phase 3: Workers Execute and Track

Each assigned worker follows this workflow:

```
1. Accept work → Move to "In Progress"
2. Do work → Commit with [LIN-XXX]
3. Track progress → Add comment on ticket
4. Complete work → Create PR, move to "In Review"
5. PR merged → Move to "Done"
```

## Commit Message Format

```
[LIN-XXX] Brief description of change

- Detail 1
- Detail 2

Ticket: https://linear.app/team/issue/LIN-XXX
```

**Example:**
```
[LIN-123] Add user authentication endpoint

- Implement JWT token generation
- Add password hashing with bcrypt
- Create login/logout routes

Ticket: https://linear.app/acme/issue/LIN-123
```

## Branch Naming

```
feature/LIN-XXX-brief-description
fix/LIN-XXX-brief-description
refactor/LIN-XXX-brief-description
```

## Progress Comments

Workers MUST add comments to their assigned tickets to track state:

### When Starting Work
```markdown
🚀 **Started work**
- Branch: `feature/LIN-XXX-description`
- Approach: [Brief description of implementation approach]
```

### During Work (for longer tasks)
```markdown
📝 **Progress update**
- Completed: [What's done]
- In progress: [Current focus]
- Blockers: [Any issues]
```

### When PR Created
```markdown
🔍 **Ready for review**
- PR: [link to PR]
- Changes: [Brief summary]
- Test coverage: [What's tested]
```

### When Complete
```markdown
✅ **Completed**
- PR merged: [link]
- Files changed: [key files]
- Notes for QA: [Any testing notes]
```

## Role-Specific Guidelines

### TPO (Technical Product Owner)

**Creates:**
- Parent feature/bug issues with clear requirements
- Links to design docs, MRD if applicable

**Tracks:**
- Overall feature completion via sub-issue rollup
- Verifies acceptance criteria met before closing parent

### Solutions Architect

**Creates:**
- Sub-issues for each work unit after architecture design
- Architecture Decision Records (ADRs) linked to issues
- Technical dependencies noted between sub-issues

**Comment Template:**
```markdown
## Architecture Breakdown

### Sub-issues created:
- LIN-XXX: Backend API implementation
- LIN-XXX: Frontend components
- LIN-XXX: Backend tests
- LIN-XXX: Frontend tests
- LIN-XXX: Documentation

### Dependencies:
- Frontend depends on Backend API completion
- Tests depend on implementation completion
- Docs depend on API finalization

### Technical Notes:
[Key architectural decisions, patterns to follow]
```

### Backend/Frontend Developer

**Commits:**
- Every logical change with `[LIN-XXX]` prefix
- Reference ticket in PR title and description

**Comments:**
- Start, progress, and completion updates
- Any implementation decisions made
- Known limitations or technical debt

**Updates ticket with:**
```markdown
## Implementation Complete

### Files changed:
- `app/api/v1/routes/users.py` - New endpoints
- `app/models/user.py` - User model
- `sql/schema.sql` - DDL changes

### API endpoints added:
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user

### Notes:
- Used JWT with 24h expiry
- Added rate limiting (100 req/min)
```

### Backend/Frontend Tester

**Commits:**
- Test files with `[LIN-XXX]` prefix
- Reference parent feature ticket

**Comments:**
```markdown
## Test Coverage Complete

### Test files:
- `tests/test_users.py` - 15 tests
- `tests/test_users_integration.py` - 8 tests

### Coverage:
- Happy path: ✅
- Validation errors: ✅
- Auth/authz: ✅
- Edge cases: ✅
- Coverage: 94%

### Scenarios tested:
- Create user success
- Create user validation errors
- Unauthorized access
- User not found
- [etc.]
```

### Tech Doc Writer

**Commits:**
- Documentation with `[LIN-XXX]` prefix

**Comments:**
```markdown
## Documentation Complete

### Files updated:
- `docs/api/users.md` - API reference
- `docs/guides/auth-quickstart.md` - Quick start

### Documentation includes:
- Endpoint reference
- Request/response examples
- Error codes
- Authentication guide

### PR: [link]
```

### TPgM (Technical Program Manager)

**Tracks:**
- All sub-tasks reference parent ticket
- Progress across all sub-issues
- Blockers and dependencies

**Verifies before closing:**
- All commits trace back to tickets
- All PRs linked to issues
- Test coverage verified
- Documentation complete

**Comment Template (for parent issue):**
```markdown
## Delivery Status

### Sub-issue Status:
| Issue | Assignee | Status |
|-------|----------|--------|
| LIN-101 Backend | @dev | ✅ Done |
| LIN-102 Frontend | @dev | 🔄 In Progress |
| LIN-103 Tests | @tester | ⏳ Pending |
| LIN-104 Docs | @writer | ⏳ Pending |

### Blockers:
- None currently

### ETA: [Date]
```

## Linear MCP Integration

When using Linear MCP tools:

### Creating Sub-Issues
```python
# Create sub-issue linked to parent
mcp.create_issue(
    title="[Backend] Implement user API",
    team="TeamName",
    parentId="parent-issue-id",
    assignee="developer@email.com",
    description="Implementation sub-task for LIN-XXX"
)
```

### Adding Progress Comments
```python
# Add progress comment
mcp.create_comment(
    issueId="LIN-XXX",
    body="🚀 **Started work**\n- Branch: `feature/LIN-XXX-user-api`"
)
```

### Updating Status
```python
# Move to In Progress
mcp.update_issue(
    id="LIN-XXX",
    state="In Progress"
)
```

## Ticket Status Flow

| Work Stage | Ticket Status | Updated By |
|------------|---------------|------------|
| Issue created | Backlog/Todo | TPO/Architect |
| Work started | In Progress | Worker |
| PR created | In Review | Worker |
| PR merged | Done | Worker/Auto |
| Parent complete | Done | Auto (all sub-issues done) |

## Why This Matters

- **Traceability**: Track what code implements which requirements
- **Visibility**: Everyone sees progress in real-time
- **Review Context**: Reviewers understand the "why" behind changes
- **Accountability**: Clear ownership of each work unit
- **Debugging**: Quickly find related tickets when investigating issues
- **Delivery Tracking**: TPgM can track feature completion accurately
- **Knowledge Transfer**: New team members understand history

## Checklist for Workers

Before marking work as done:

- [ ] All commits reference `[LIN-XXX]`
- [ ] PR title includes `[LIN-XXX]`
- [ ] Started comment added to ticket
- [ ] Completion comment added with details
- [ ] Ticket status updated to reflect reality
- [ ] Any blockers or notes documented

## Related References

- **Ticket Templates**: See `ticket-templates.md` for Story/Task and Bug templates
- **INVEST Principle**: Sub-issue quality validation (see above)
