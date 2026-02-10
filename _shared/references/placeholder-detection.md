# Placeholder Detection

**CRITICAL**: Before ANY skill performs work, it MUST check for placeholders in the project's `claude.md` file.

## Placeholder Patterns (BLOCKING)

If ANY of these patterns are found, the skill MUST:
1. Stop immediately
2. List all placeholder sections found
3. Ask user to complete them before proceeding

**Common placeholder patterns:**
- `[Project Name]` (in title)
- `[One-line project description]`
- `[slug]` (in Team Context)
- `[e.g., ...]` (in any section)
- `[Add your rules here]` (uncustomized)
- Empty or incomplete sections with only template text

**Exception**: Skills MAY help the user fill in placeholders if explicitly asked ("help me set up my claude.md").

## Required Sections Checklist

Before any work begins, verify these sections are COMPLETE (no placeholders):

- [ ] Project title is real (not `[Project Name]`)
- [ ] Project description is real (not `[One-line project description]`)
- [ ] Team Context: Team Slug is real (not `[slug]`)
- [ ] Team Context: Ticket System is selected (`linear`, `github`, or `none`)
- [ ] Domain Ownership: All domains have real owners (not `[Owner role + person]`)
- [ ] Active Roles: Real roles listed with real scopes (not `[e.g., ...]`)
- [ ] Coding Standards: Frontend/Backend/Testing checkboxes are reviewed
- [ ] Coding Standards: Project-Specific Rules section has real rules (not `[Add your rules here]`)

## Response Template

If placeholders detected:
```
<ROLE_NAME> ⚠️ INCOMPLETE PROJECT SETUP DETECTED

This project's claude.md file contains placeholders that must be completed before I can proceed.

**Placeholders found:**
1. [Project Name] — Line 1
2. [slug] — Line X (Team Slug)
3. [e.g., TPO] — Line X (Active Roles)

**To proceed**, please either:
1. Complete these sections manually
2. Ask me to help you set them up: "Help me configure my claude.md"

Until these placeholders are replaced with real values, I cannot perform any work.
```
