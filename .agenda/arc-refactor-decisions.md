# Architecture Refactor - Alignment Decisions

This document captures decisions made during architecture alignment discussions. Survives context compaction.

---

## 3-Layer Architecture

| Layer | Purpose | Analogy |
|-------|---------|---------|
| **Global CLAUDE.md** | Behavioral rules (fixed) + config slots (Projects must fill) | Operating System |
| **Project CLAUDE.md** | Required configuration for this project | Project Charter |
| **SKILL.md** | Pure expertise, no framework mechanics | Job Description |

---

## Gap #1: Loading & Activation - ALIGNED

| Decision | Outcome |
|----------|---------|
| Skill discovery | Implicit (Claude Code infrastructure handles it) |
| Activation trigger | No change - explicit `/skill-name` invocation |
| Roster enforcement | **Hard block** - if skill not in active roster, refuse invocation |
| Load sequence | System handles: Global → Project → Skill |
| Precedence | **Global > Project > Skill** (OS wins, most general wins) |
| Global's role | Defines **walls** (fixed rules) and **knobs** (configurable slots) |

---

## Gap #2: Override Precedence - ALIGNED

| Decision | Outcome |
|----------|---------|
| Precedence | `Global > Project > Skill` |
| Project's role | Not "override" - it's **required configuration** |
| Philosophy | **Explicit configuration, no silent defaults** |
| Enforcement | Placeholder detection blocks until ALL slots configured |
| Global's job | Define behavior + declare required config slots |

---

## Gap #3: Compaction Paradox - ALIGNED

| Decision | Outcome |
|----------|---------|
| Preamble location | Move to Global (single source of truth) |
| Size target | **Global < 300 lines** (target), 500 hard limit |
| Benefit | Consistency + compaction survival (Global always loaded fresh) |
| Feasibility | Yes - estimated ~175 lines for core behavioral content |
| Approach | Complete rewrite, not retrofit |

---

## Gap #4: Cross-Skill Handoffs - ALIGNED

| Decision | Outcome |
|----------|---------|
| Handoff format | **Structured** (Completed / For you / Constraints) |
| Collab mode | User declares session (`/tpo+ux`), skills hand off within session |
| Plan Execution | Autonomous per plan, no user intervention between skills |
| Explore mode | Auto-triggers documentation (time + event + skill-initiated) |
| Where defined | Global (format/protocol), Project (choreography rules) |

### Structured Handoff Format

```
<ROLE_A> Handing off to <ROLE_B>.

**Completed:**
- [What was done]

**For you:**
- [What's needed from receiving role]

**Constraints:**
- [Key limitations/decisions to respect]
```

---

## Gap #5: Utility Skills & Orchestration - ALIGNED

| Decision | Outcome |
|----------|---------|
| Role categories | Regular skills + Utility skills |
| Behavior model | Mode-dependent (not category-dependent) |
| Utility pattern | "Autonomy = more rigor" principle |
| Ticket system access | PC handles all ticket operations (other skills invoke PC) |
| Mode management | Framework behavior (Global) |
| PM role | Absorbed into Framework + PC |

### Role Categories

**Regular skills**: Follow mode rules (confirmation in Collab, no confirmation in Plan Execution/Explore)

**Utility skills**: PC only - special invocation pattern, no confirmation in ANY mode, called BY other skills

**Key insight**: Behavior is mode-dependent, not category-dependent. A Developer in Explore mode works without tickets. A Developer in Plan Execution mode works per plan.

### Why PC Exists

Problems before PC:
- Tickets didn't follow templates
- DoR not enforced → work started before ready
- DoD not enforced → work marked done but incomplete
- Multiple skills touching ticket systems inconsistently

Solution: PC handles all ticket operations, enforces quality, and knows how to interact with each system.

### PM Role Eliminated

Original PM responsibilities redistributed:

| Responsibility | Now Handled By |
|----------------|----------------|
| Mode state tracking | Framework (Global) |
| Mode transitions (EXECUTE/EXPLORE/EXIT) | Framework commands |
| Mode prefix enforcement | Global rule (all skills follow) |
| DoR check before Plan Execution | Framework invokes PC |
| Orchestration in Plan Execution | **Pull-based** - PC enforces sequence |
| Explore documentation triggers | **Skill-initiated** prompts |

### Orchestration Model: Pull-Based (Plan Execution)

**Instead of PM pushing work to skills, skills pull work when dependencies clear.**

```
Plan structure with explicit dependencies:
  Step 1: Backend Dev [status: done]
  Step 2: Tester [blocked-by: Step 1] → unblocked when Step 1 done
  Step 3: Code Reviewer [blocked-by: Step 2]
```

- Skills attempt to work on their assigned step
- PC enforces: "Is this step's dependency met?"
- If blocked → PC rejects
- If unblocked → PC allows

**Tradeoff:** Requires more rigorous ticket/plan structure upfront.

DoR for plans must include:
- Each step has explicit `blocked-by` dependencies
- Each step has assigned role
- No ambiguous sequencing

### Explore Mode: Skill-Initiated Documentation

Skills self-report key findings:
```
🔍 <ROLE> Key finding: [summary]. Document now? (y/n)
```

No watcher role needed. Skills prompt when they think something is worth documenting.

---

## Gap #6: Migration Path - ALIGNED

**Approach:** Complete restart, not incremental migration.

Write to separate directory, then move into place when complete.

### Creation Order (Dependency Chain)

```
1. Global CLAUDE.md       ← Defines the rules (top of chain)
2. Global reference files ← Details that Global references
3. Project boilerplate    ← Configuration slots constrained BY Global
4. Individual skills      ← Operate WITHIN Global's rules (bottom of chain)
```

Skills are at the BOTTOM - they follow rules defined above them.

---

## Gap #7: Testing Strategy - ALIGNED

| Decision | Outcome |
|----------|---------|
| Approach | **Test the walls, not every room** |
| Scope | ~20 core scenarios (not hundreds) |
| Timing | Define tests AFTER Global/Project written (tests derive from rules) |
| Categories | Global enforcement, Category behavior, Mode transitions, Blocking, Handoffs |

### Sample Test Categories (to be finalized after rules written)

- **Global Enforcement** (~5): Role prefix, out-of-scope refusal, precedence, compaction recovery, handoff format
- **Mode-Dependent Behavior** (~5): Collab confirmation, Plan Execution no confirmation, Explore no confirmation, Utility never confirms
- **Mode Transitions** (~5): Default Collab, EXECUTE flow, EXPLORE flow, EXIT flow, DoR blocking
- **Blocking Conditions** (~3): Placeholder blocks, Roster blocks, Scope undefined blocks
- **Handoffs** (~3): Collab structured, Plan Execution autonomous, Explore skill-initiated documentation

---

## Gap #8: Session Entry & Default Intake - ALIGNED

| Decision | Outcome |
|----------|---------|
| Framework activation | Project-level opt-in (boilerplate configures it) |
| Default mode | Collab (framework active immediately when project configured) |
| Default Intake | **Required config slot** - must be explicitly set |
| Options | `tpo`, `support-engineer`, `solutions-architect`, or `none` |
| If `none` | Framework prompts user to invoke a skill |
| Explicit invocation | Always works - `/skill-name` bypasses default intake |

### Required Configuration = Blocking

**ALL required config must be set before framework operates.**

If any required field is missing:
```
⚠️ BLOCKED - Configuration incomplete.

Missing required fields in claude.md:
- [ ] Default Intake
- [ ] [other missing fields]

Please configure these fields before proceeding.
```

### Confirmation Format (STRICT)

**ALL skill invocations require confirmation.**

| Rule | Behavior |
|------|----------|
| Format | `🤝 Invoking <ROLE>. (y/n)` or `🤝 Routing to <ROLE>. (y/n)` |
| Multiple roles | `🤝 Invoking <TPO+UX>. (y/n)` (ONE prompt for all) |
| **Valid responses** | **Only `y` or `n`** (single character, lowercase) |
| Invalid responses | Re-prompt same line, no explanation |

**NOT accepted:**
- `yes`, `Yes`, `Y`, `YES` ❌
- `no`, `No`, `N`, `NO` ❌
- `yes, I would like to...` ❌
- `yeah`, `sure`, `ok` ❌

**Only accepted:**
- `y` ✓
- `n` ✓

### Multi-Skill Session (Collab Mode)

**When user invokes multiple skills:** `/tpo+ux`

| Step | What Happens |
|------|--------------|
| 1 | Framework: `🤝 Invoking <TPO+UX>. (y/n)` |
| 2 | User: `y` |
| 3 | **Both skills loaded immediately** |
| 4 | First listed skill (TPO) handles initial request |
| 5 | Free handoffs between declared skills (no additional confirmation) |

**Key rules:**
- ONE confirmation for all declared skills
- All skills are **equal participants** (no primary/secondary)
- Handoffs within session don't require confirmation
- First skill listed handles initial request

### Session Flow (Collab Mode)

```
User opens project (configured)
  ↓
Framework: 🤝 Collab Mode.
  ↓
User says something without /skill-name
  ↓
If Default Intake = tpo/sa/se:
  → Framework: 🤝 Routing to <TPO>. (y/n)
  → User: y (strict)
  → TPO proceeds
  ↓
If Default Intake = none:
  → Framework: 🤝 Invoke a skill to proceed.
  ↓
User explicitly invokes /skill-name or /skill1+skill2:
  → Framework: 🤝 Invoking <SKILL(S)>. (y/n)
  → User: y (strict)
  → Skill(s) loaded, first listed handles request
```

---

## Pending Discussion Items

### Universal Rules Definition
- Before writing anything, fully define:
  1. What goes in Global (the universal rules)
  2. What reference files Global needs
  3. What configuration slots Project must fill
  4. What each skill category must contain

---

## Key Principles Established

1. **Global > Project > Skill** - Precedence order, OS wins
2. **Explicit configuration, no defaults** - Projects must fill all slots or framework blocks
3. **Autonomy = more rigor** - Utility skills without confirmation must be MORE strict
4. **PC owns ticket operations** - All ticket system access goes through PC
5. **Structured handoffs** - Context must survive compaction and skill transitions
6. **< 300 lines target** - Keep files focused for context efficiency
7. **Mode-dependent, not category-dependent** - Behavior varies by mode, not by role type (except Utility)
