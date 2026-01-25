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
- All participating roles talk to each other **freely WITHOUT asking the user**
- No confirmation prompts between participating roles
- Roles collaborate in the same response
- Any number of roles can participate
- Continue until work is complete or user revokes

**Correct behavior:**
```
[UX_DESIGNER] - Here's the component layout...

[SOLUTIONS_ARCHITECT] - That works. Adjusting data flow...

[FRONTEND_DEVELOPER] - I can implement that pattern...

[UX_DESIGNER] - One concern about loading state...

[SOLUTIONS_ARCHITECT] - Good point. Let's address that...
```

**WRONG behavior (do NOT do this):**
```
[UX_DESIGNER] - Here's my recommendation...

[SOLUTIONS_ARCHITECT] - Should I respond? ← WRONG - just respond
```

## Step 4: Adding More Roles Mid-Session

To add another role to an active Collab Session:
1. Any participating role can suggest inviting new role(s)
2. User must approve (`1` or `APPROVE`)
3. New role(s) confirm joining (`Y` or `YES`)
4. New role(s) join the active session

## Step 5: Ending the Session

Collab Session ends when:
- User says `STOP` or `EXIT`
- Work is complete and roles sign off
