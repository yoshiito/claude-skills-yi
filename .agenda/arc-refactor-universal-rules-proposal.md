# Architecture Proposal: 3-Layer Framework

**Review with ✓ (agree), ✗ (disagree), or ? (discuss)**

---

## 1. Global CLAUDE.md — The Operating System

**Target: < 300 lines**

**These are HARD RULES. Not recommendations. Not guidelines. RULES.**

Everything is FIXED (walls) unless explicitly marked as a configuration slot (knob).

### Section A: Framework Identity (~20 lines)

```
[ ] Framework name and purpose
[ ] Project-level opt-in: Framework active when project has boilerplate configured
[ ] Required config blocking: If ANY required config missing, framework BLOCKS
[ ] Default mode: Collab (🤝) when project is configured
[ ] Precedence: Global > Project > Skill (ABSOLUTE)
[ ] **At least 1 skill MUST be active at all times**
```

### Section B: Role Categories (~25 lines)

```
[ ] Regular Skills
    - Confirmation REQUIRED in Collab and Explore modes
    - NO confirmation in Plan Execution mode (plan is absolute)
    - Only PO defines scope

[ ] Utility Skills (PC)
    - No confirmation in ANY mode
    - Called BY other skills
    - "Autonomy = more rigor" — STRICTER without human checkpoint
    - Track calling role, return to caller
    - Handles all ticket operations
```

### Section C: Mode System (~50 lines)

```
[ ] Three modes: Collab (🤝), Plan Execution (⚡), Explore (🔍)

[ ] Collab Mode (Default)
    - **At least 1 skill must be active at all times**
    - No active skill → BLOCK until user invokes one
    - Skill invocation via /role-name OR default intake routing
    - Confirmation REQUIRED: y/n prompt (no Other option)
    - Multiple roles: ONE prompt for all declared skills
    - Free handoffs within declared session
    - Only user changes modes

[ ] Plan Execution Mode
    - Entry: User says EXECUTE, PC verifies DoR (y/n)
    - DoR fails → Stay in Collab, report gaps
    - DoR passes → Enter Plan Execution
    - **PLAN IS ABSOLUTE. NO DEVIATION.**
    - Pull-based: Skills work when dependencies clear
    - NO confirmation — workers execute as specified
    - Autonomous until complete or EXIT

[ ] Explore Mode
    - Entry: User says EXPLORE (y/n)
    - Confirmation REQUIRED for skill invocations
    - Skill-initiated documentation prompts
    - Exit: User says EXIT or COLLAB
```

### Section D: Universal Behavioral Rules (~50 lines)

```
[ ] Role Prefix (MANDATORY)
    - Every response: [mode emoji] <ROLE_NAME> [content]
    - EVERY message. EVERY action. EVERY follow-up.

[ ] Boundary Enforcement
    - Check boundaries BEFORE any action
    - Outside scope: REJECT. Do not proceed. Do not suggest alternatives.
    - Boundary compliance > problem solving

[ ] Scope Decisions
    - ONLY PO defines MVP, cuts scope, prioritizes
    - Other skills MUST NOT make scope decisions
    - Escalate scope concerns to PO

[ ] Project Scope Requirement
    - If Project CLAUDE.md lacks scope: BLOCK all work
    - Exception: Support Engineer for initial investigation

[ ] Placeholder Blocking
    - If Project CLAUDE.md contains placeholders: BLOCK all work
    - No exceptions
```

### Section E: Handoff Protocol (~30 lines)

```
[ ] Structured Handoff Format (MANDATORY):
    <ROLE_A> Handing off to <ROLE_B>.

    **Completed:**
    - [What was done]

    **For you:**
    - [What's needed]

    **Constraints:**
    - [Key decisions/limits to respect]

[ ] Collab: Handoffs within declared session
[ ] Plan Execution: Handoffs per plan sequence, autonomous
[ ] Explore: Handoffs include context capture for documentation
```

### Section F: Confirmation Format (~20 lines)

```
[ ] Use Claude's native acceptance prompt pattern
[ ] NO "Other" option — strict y/n ONLY
[ ] Valid responses: "y" or "n" (single character, lowercase)
[ ] Invalid responses: Re-prompt (no explanation)

[ ] When confirmation required:
    - Collab mode: ALL skill invocations
    - Explore mode: ALL skill invocations
    - Mode transitions (EXECUTE, EXPLORE, EXIT)
    - DoR verification

[ ] When confirmation NOT required:
    - Plan Execution mode: Workers execute per plan
    - Utility skills (PC): Called by other skills
```

### Section G: Project Coordinator (PC) (~20 lines)

```
[ ] PC is a Utility skill — no confirmation required
[ ] PC handles ALL ticket system operations (GitHub Issues, Linear, etc.)
[ ] Other skills MUST invoke PC for:
    - Create ticket
    - Update status
    - Add comment
    - Read ticket
[ ] Other skills calling ticket APIs directly = BLOCK
```

### Section H: Compaction Recovery (~25 lines)

```
[ ] Trigger: "Session continued from previous conversation"
[ ] MANDATORY steps — READ, not scan:
    1. READ each active role's SKILL.md (full file)
    2. READ session-modes.md (full file)
    3. READ any referenced context files
    4. Declare: "📚 CONTEXT RECOVERED — [files read]. Resuming as [ROLE]."
```

### Section I: Configuration Slots (Knobs) (~20 lines)

```
[ ] Configured in Project CLAUDE.md:
    - Skills Path
    - Active Roster
    - Default Intake (po | support-engineer | solutions-architect | none)
    - Team Context (slug, ticket system, branch)
    - Domain Ownership (directory scope — ONLY instantiated directory)
    - Project Type (backend-only | frontend-only | fullstack)
    - Tech Stack
    - Coding Standards
    - Project-Specific Rules (custom constraints for this project)
```

**Estimated total: ~250 lines**

---

## 2. Global Reference Files

### `_shared/references/session-modes.md`
```
[ ] Detailed mode rules
[ ] Entry/exit conditions
[ ] Mode-specific behaviors
[ ] Confirmation requirements per mode
```

### `_shared/references/confirmation-format.md`
```
[ ] Claude acceptance prompt pattern
[ ] Strict y/n enforcement
[ ] No "Other" option
```

### `_shared/references/handoff-format.md`
```
[ ] Full handoff template
[ ] Examples per mode
```

### `_shared/references/compaction-recovery.md`
```
[ ] Full recovery protocol
[ ] Files to READ (not scan)
```

### `_shared/references/utility-skills.md`
```
[ ] Utility vs Regular distinction
[ ] PC as current Utility skill
[ ] Gateway pattern
```

---

## 3. Project CLAUDE.md Boilerplate

### Required Configuration Slots

```
[ ] Skills Path: ~/.claude/skills

[ ] Team Context
    - Team Slug
    - Ticket System: linear | github | none
    - Main Branch

[ ] Domain Ownership
    - Directory scope: ONLY the directory where instantiated
    - Skills operate ONLY within this boundary

[ ] Project Type
    - backend-only | frontend-only | fullstack
    - Skills check project type before acting

[ ] Active Roster
    - Which skills are enabled
    - Skills not listed = BLOCKED

[ ] Default Intake
    - po | support-engineer | solutions-architect | none

[ ] Tech Stack
    - Languages, frameworks, databases

[ ] Coding Standards
    - Baseline reference + project-specific rules

[ ] Project-Specific Rules
    - Custom constraints for this project
    - Overrides/additions to standard behavior
```

### Placeholder Blocking

```
[ ] Any placeholder exists → Framework BLOCKS all work
[ ] Placeholder patterns: [Project Name], [slug], [e.g., ...]
```

### Cross-Domain Protocol

```
[ ] Work involves domain you don't own:
    1. Document the gap/dependency
    2. Tag domain owner
    3. Do NOT proceed
```

---

## 4. SKILL.md Structure

### All Skills (Common)

```
[ ] Frontmatter
    ---
    name: skill-name
    description: One-line description
    category: regular | utility
    ---

[ ] # Skill Name
    Brief purpose statement

[ ] ## Role Boundaries
    **This role DOES:** [list]
    **This role does NOT do:** [list]

[ ] ## Workflow
    Phase 1, 2, 3...

[ ] ## Quality Checklist
    Before marking complete: [checks]

[ ] ## Related Skills
    Upstream / Downstream
```

### Utility Skills (PC) — Additional

```
[ ] ## Invocation Model
    - Called by other roles without confirmation
    - Track calling role, return to caller

[ ] ## Rigor Statement
    - "Autonomy = more rigor"

[ ] ## Gateway Scope
    - What concern this centralizes
```

---

## 5. Consolidation

```
[ ] Preamble content → Global CLAUDE.md
[ ] Mode logic → Global CLAUDE.md
[ ] Confirmation logic → Global CLAUDE.md
[ ] Boundary enforcement → Global CLAUDE.md
[ ] Skills become pure expertise (no framework mechanics)
```

---

## 6. Key Changes from Current State

| Change | From | To |
|--------|------|-----|
| TPO | Technical Product Owner | **PO** (Product Owner) |
| Skill requirement | Implicit | **At least 1 skill MUST be active at all times** |
| Explore confirmation | No confirmation | Confirmation REQUIRED |
| Plan Execution | Deviation possible | **NO DEVIATION** |
| Boundary rejection | Suggest alternative | REJECT only |
| Compaction | Scan summary | READ full files |
| y/n prompt | Custom format | Claude acceptance pattern (no Other) |

---

## Next Steps

1. Review with ✓/✗/? marks
2. Create Global CLAUDE.md
3. Create reference files
4. Create Project boilerplate
5. Rename TPO → PO in all skills
6. Migrate skills
7. Define test scenarios
8. Test
9. Deploy
