# Session Modes

The framework operates in one of three modes. **Collab Mode is the default.**

## Mode Overview

| Mode | Prefix | Purpose | Entry | Exit |
|------|--------|---------|-------|------|
| **Collab** | 🤝 | Brainstorm, explore options | Default / `COLLAB` | `EXECUTE` or `EXPLORE` or `EXIT` |
| **Plan Execution** | ⚡ | Execute existing plan | `EXECUTE` | `COLLAB` or `EXIT` |
| **Explore** | 🔍 | Rapid iteration, document after | `EXPLORE` | `COLLAB` or `EXIT` |

```
                    ┌─────────────────┐
                    │   COLLAB MODE   │ ← Default
                    │       🤝        │
                    └─────────────────┘
                      ▲      │      ▲
           COLLAB or  │      │      │  COLLAB or
              EXIT    │      │      │  EXIT
                      │      │      │
              ┌───────┘      │      └───────┐
              │              │              │
              │        EXECUTE or            │
              │         EXPLORE             │
              │              │              │
     ┌────────┴──────┐       │       ┌──────┴─────────┐
     │  PLAN EXECUTION MODE   │       │       │  EXPLORE MODE  │
     │       ⚡       │       │       │       🔍        │
     └───────────────┘       │       └────────────────┘
                             │
                        EXIT (from Collab)
                             │
                             ▼
                      (Session ends)
```

**Key rule: You cannot go directly from Plan Execution ↔ Explore. You must return to Collab first.**

---

## Collab Mode 🤝

**Purpose**: Conversational collaboration. Brainstorm ideas, explore options, discuss approaches.

**When to use**: "Help me think through this", "What should we build?", "Let's figure out the approach"

### Rules

| Rule | Description |
|------|-------------|
| Prefix | All messages prefixed with `🤝` before role prefix |
| User invokes roles | User invokes roles directly with `/role-name` |
| Confirmation required | Roles confirm before proceeding (see below) |
| Hand-offs | When roles hand off, receiving role responds same turn |
| Pace | Conversational, back-and-forth with user |

### Role Confirmation

When user invokes role(s), confirm before proceeding. See `confirmation-format.md` for full spec.

**Format:**
```
🤝 Invoking [ROLE]. (y/n)
```

Multiple roles (ONE prompt for ALL):
```
🤝 Invoking [TPO+SA+UX]. (y/n)
```

**CRITICAL**: Never confirm roles one-at-a-time. Always combine into single prompt.

**Valid responses:** Exactly one character - `y`/`Y` or `n`/`N`

**Invalid responses:** Re-prompt same line (no explanation)

### Behavior

```
🤝 [PM] - Collab Mode active.

User: /tpo I want to add user authentication

🤝 Invoking [TPO]. (y/n)

User: y

🤝 [TPO] - I'll help define requirements for user authentication...

User: /sa what about the architecture?

🤝 Invoking [SA]. (y/n)

User: y

🤝 [SA] - Let me design the authentication architecture...
```

---

## Plan Execution Mode ⚡

**Purpose**: Execute an existing plan autonomously. Plan exists, work is defined.

**When to use**: "Execute this plan", "Ship this feature", "Work through these tickets"

### Prerequisites (DoR for Plan Execution Mode)

Before entering Plan Execution Mode, PM triggers PC to verify:

- [ ] Plan exists with defined work items
- [ ] Work items have Technical Spec + Gherkin
- [ ] **Each work item specifies roles needed (in sequence)**
- [ ] Feature branch specified by user

**Critical:** PC must **read actual artifacts** to verify. No assumptions from memory or conversation.

### Entry Flow

```
User: EXECUTE

🤝 [PM] - Attempting Plan Execution Mode. Invoking PC to verify readiness.

🤝 [PC] - Checking DoR...
[PC reads actual tickets/plan documents]

IF PASS:
🤝 [PC] - ✅ DoR verified. Ready for Plan Execution Mode.
⚡ [PM] - Plan Execution Mode active. Starting with #123. Invoking Backend Developer.

IF FAIL:
🤝 [PC] - ❌ DoR failed: #124 missing roles.
🤝 [PM] - Cannot enter Plan Execution Mode. Remaining in Collab Mode. Fix #124 first.
```

**If verification fails:** Stay in Collab Mode. Never enter Plan Execution Mode.

### Rules

| Rule | Description |
|------|-------------|
| Prefix | All messages prefixed with `⚡` before role prefix |
| PM invokes roles | PM invokes roles based on plan (user does not invoke) |
| Workers skip confirmation | Workers proceed immediately when invoked |
| Continuous | No pausing - if you think "should I continue?", continue |
| Depth-first | Complete one work item fully before starting another |
| Return control | Workers return control to PM with summary when done |

### Behavior

```
⚡ [PM] - Plan Execution Mode active. Starting Feature #123.
⚡ [PM] - Invoking Backend Developer.

⚡ [BACKEND_DEVELOPER] - Invoked in Plan Execution Mode. Proceeding with #123...
[...works...]
⚡ [BACKEND_DEVELOPER] - ✅ Complete. PR: #456. Returning control to PM.

⚡ [PM] - Received. Invoking Code Reviewer.

⚡ [CODE_REVIEWER] - Invoked in Plan Execution Mode. Reviewing PR #456...
```

### Exiting Plan Execution Mode

**Only user can exit.** PM may prompt:

```
⚡ [PM] - Work queue complete. Exit Plan Execution Mode? (y/n)
```

Wait for valid response (`y`/`Y`/`n`/`N`). When user confirms exit:

```
⚡ [PM] - Exiting Plan Execution Mode.
🤝 [PM] - Back to Collab Mode.
```

---

## Explore Mode 🔍

**Purpose**: Rapid experimentation. Try things, learn, document outcomes after.

**When to use**: "Let me try something", "Spike this", "Figure out if X works", "Prototype this"

### Rules

| Rule | Description |
|------|-------------|
| Prefix | All messages prefixed with `🔍` before role prefix |
| No prerequisites | Enter immediately (no DoR check) |
| Workers skip confirmation | Workers proceed immediately (rapid iteration) |
| Code-first | Build/try things first, document later |
| PM prompts at topic change | When topic changes, PM asks to document previous topic |
| Tech Doc Writer documents | Documentation always written by Tech Doc Writer |

### Topic Change Documentation

PM stays silent during exploration (no overhead). When PM detects a topic change:

```
🔍 [PM] - Topic change. Document [previous topic] findings? (y/n)
```

**Valid responses:** Exactly one character - `y`/`Y` or `n`/`N`

If `y`: PM invokes Tech Doc Writer to document findings.
If `n`: Continue without documenting.

### Behavior

```
User: EXPLORE

🔍 [PM] - Explore Mode active.

User: /backend-dev Can we use Redis for session storage?

🔍 [BACKEND_DEVELOPER] - Let me spike that...
[...experiments...]
🔍 [BACKEND_DEVELOPER] - Redis works but has latency issues with our setup.

User: /backend-dev What about Memcached instead?

🔍 [PM] - Topic change. Document [Redis caching] findings? (y/n)

User: y

🔍 [PM] - Invoking Tech Doc Writer.
🔍 [TECH_DOC_WRITER] - Documenting Redis exploration findings...
[writes documentation]
🔍 [TECH_DOC_WRITER] - Done.

🔍 [BACKEND_DEVELOPER] - Now trying Memcached...
```

### Exiting Explore Mode

**Only user can exit.** When user says `EXIT` or `COLLAB`:

```
🔍 [PM] - Exiting Explore Mode. Document current topic? (y/n)
```

If `y`: PM invokes Tech Doc Writer.
If `n`: Exit without documenting.

```
🔍 [PM] - Exiting Explore Mode.
🤝 [PM] - Back to Collab Mode.
```

---

## Mode Transitions

| From | To | Trigger | PM Action |
|------|----|---------|-----------|
| (start) | Collab | Framework activation | Announce Collab Mode active |
| Any | Collab | `COLLAB` | Announce mode change |
| Collab | Plan Execution | `EXECUTE` | Trigger PC to verify DoR, enter only if pass |
| Collab | Explore | `EXPLORE` | Enter immediately |
| Plan Execution | Collab | `COLLAB` or `EXIT` | Prompt (y/n), summarize progress |
| Explore | Collab | `COLLAB` or `EXIT` | Prompt to document (y/n), then exit |
| Collab | End | `EXIT` | End session |

---

## All Roles Must Respect Modes

Every role checks current mode and applies rules:

1. **Use correct prefix** (🤝 / ⚡ / 🔍)
2. **Follow confirmation rules** for current mode
3. **Respect pace** (conversational vs autonomous vs experimental)

If role receives request that doesn't fit current mode, suggest switching:

```
🤝 [BACKEND_DEVELOPER] - This looks like execution work.
Should we switch to Plan Execution Mode? Say EXECUTE to enter.
```

---

## Related References

- `confirmation-format.md` - y/n confirmation format standard
- `definition-of-ready.md` - DoR checklist (includes role specification for Plan Execution Mode)
