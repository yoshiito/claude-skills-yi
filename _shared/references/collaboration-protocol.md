# Collaboration Protocol — Collab Sessions

When roles need to collaborate, a Collab Session must be established.

## Step 1: Starting a Collab Session

A Collab Session can start in two ways:

**Option A — User requests it:**
```
User: "I want SA, UX Designer, and Frontend Dev to work together"
```

**Option B — Skill suggests it:**
```
[CURRENT_ROLE] - This task requires collaboration.

**Requesting permission to start a Collab Session with:**
- [ROLE_1] for [reason]
- [ROLE_2] for [reason]
- (add more as needed)

1. ✅ APPROVE
2. ❌ DENY
```

**WAIT for user response.**

| Valid Response | Action |
|----------------|--------|
| `1`, `APPROVE` | Start Collab Session |
| `2`, `DENY` | Do not start |
| Anything else | Re-prompt (do NOT proceed) |

## Step 2: Joining Confirmation

Once user approves, each invited role confirms joining:

```
[INVITED_ROLE] - Joining Collab Session. (Y/N)
```

**WAIT for user response.**

| Valid Response | Action |
|----------------|--------|
| `Y`, `YES` | Role joins session |
| `N`, `NO` | Role does not join |
| Anything else | Re-prompt (do NOT proceed) |

## Step 3: Active Collab Session

**Once user confirms Y, the role joins the active Collab Session.**

**During an active Collab Session:**
- **ALL messages MUST be prefixed with `🤝` before the role prefix** (e.g., `🤝 [UX_DESIGNER]`)
- All participating roles talk to each other **freely WITHOUT asking the user**
- No confirmation prompts between participating roles
- Roles collaborate in the same response
- Any number of roles can participate
- Continue until work is complete or user revokes

**Correct behavior:**
```
🤝 [UX_DESIGNER] - Here's the component layout...

🤝 [SOLUTIONS_ARCHITECT] - That works. Adjusting data flow...

🤝 [FRONTEND_DEVELOPER] - I can implement that pattern...

🤝 [UX_DESIGNER] - One concern about loading state...

🤝 [SOLUTIONS_ARCHITECT] - Good point. Let's address that...
```

**WRONG behavior (do NOT do this):**
```
[UX_DESIGNER] - Here's my recommendation... ← WRONG - missing 🤝 prefix

🤝 [SOLUTIONS_ARCHITECT] - Should I respond? ← WRONG - just respond, don't ask
```

## Step 4: Adding More Roles Mid-Session

To add another role to an active Collab Session:
1. Any participating role can suggest inviting new role(s) (with 🤝 prefix)
2. User must approve (`1` or `APPROVE`)
3. New role(s) confirm joining (`Y` or `YES`)
4. New role(s) join and use 🤝 prefix from that point forward

## Step 5: Ending the Session

**CRITICAL: Only the USER can end a Collab Session.** The AI cannot decide to exit on its own.

Collab Session ends ONLY when:
- User says `STOP` or `EXIT`
- User explicitly approves ending the session

**AI may PROMPT to end, but must WAIT for user approval:**
```
🤝 [PM] - Work appears complete. Would you like to end the Collab Session?

1. END SESSION - Yes, end Collab Session
2. CONTINUE - No, stay in Collab Session
```

**WAIT for user response.** Do NOT assume or auto-end.

**When user confirms ending, stop using the 🤝 prefix:**
```
🤝 [PM] - Collab Session ended.

[PM] - Back to standard mode. What would you like to do next?
```
