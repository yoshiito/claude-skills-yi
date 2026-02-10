Global CLAUDE.md -- The Operating System
This is the only file that defines HOW the framework behaves. Everything behavioral that carries from project to project lives here and ONLY here.
Owns:

Mode system -- definitions of Collab, Plan Execution, Explore. What each mode means. What's allowed and prohibited in each. Default is Collab. How modes get invoked and exited.
Role behavioral contracts -- every role must declare itself, every role must check scope, every role must respect boundaries. The "solving a problem by violating boundaries is mission failure" principle. Worker role vs intake role classification.
Pre-action verification -- the checklist every role runs before doing anything (am I the right role, am I in the right mode, is this within my boundaries)
Session state protocol -- how and when to write/read state for crash recovery and compaction resilience
Framework vocabulary -- what "ticket" means, what "handoff" means, what "scope" means, so every skill interprets terms the same way

Does NOT own:

Which roles are active (that's project)
What any specific role knows or does (that's skill)
Tech stack, project scope, plan locations (that's project)

The test: "If I delete all projects and all skills, does this file still make sense on its own?" If yes, it belongs here.

Project CLAUDE.md -- The Project Charter
This is the configuration file. It tells the framework what to load and what context to operate in for THIS project.
Owns:

Active roster -- "This project uses: TPO, Backend Dev, API Designer, Tester" (drawn from the global fleet)
Current mode -- "Default mode: Collab" or "This project is in Plan Execution mode, plan at /docs/plans/xyz.md"
Project scope -- what we're building, what's in/out of scope (the section skills check before proceeding)
Tech stack and constraints -- FastAPI, React, PostgreSQL, OpenAPI 3.1, etc.
Project-specific coordination rules -- "API Designer signs off before Backend implements" or "All PRs need Tester review"
Project-specific mode overrides -- "In Explore mode for this project, findings go to /docs/explorations/"
Active plan reference -- when in Plan Execution mode, where the plan lives

Does NOT own:

What modes mean or how they work (that's global)
How roles behave generically (that's global)
What any role's expertise is (that's skill)

The test: "Does this change when I start a different project?" If yes, it belongs here.

SKILL.md -- The Job Description
This is pure expertise and identity. No framework mechanics, no mode logic, no behavioral preambles.
Owns:

Role identity -- "You are the Backend Developer specializing in FastAPI"
Boundary lists -- DOES and DOES NOT, specific to this role
Domain expertise -- patterns, best practices, quality standards this role knows
Output formats -- what this role produces, templates, file formats
Tools and references -- which MCP tools, reference files, templates this role uses
Upstream/downstream -- who feeds this role work, who receives this role's output

Does NOT own:

The preamble (that's global -- remove it from every skill)
Mode behavior (that's global)
Scope checking logic (that's global)
Role declaration requirement (that's global)
Mission priority hierarchy (that's global)
Whether this role is active in a given project (that's project)

The test: "If someone asked 'what does a Backend Developer do?', is the answer in this file and ONLY this file?" If yes, it belongs here.

What Gets Eliminated
The universal-skill-preamble.md and the duplicated preamble block in every SKILL.md both go away. That content moves to Global CLAUDE.md, stated once. Each SKILL.md gets lighter because it only carries expertise and boundaries, not framework mechanics.
ContentCurrently LivesMoves To"Prefix all responses with [ROLE]"Every SKILL.md + preambleGlobal CLAUDE.md (once)"This is a WORKER ROLE"Every SKILL.md + preambleGlobal CLAUDE.md (once)"Check project scope before proceeding"Every SKILL.md + preambleGlobal CLAUDE.md (once)"Boundary > problem solving" mission priorityEvery SKILL.mdGlobal CLAUDE.md (once)Mode definitions and rulesNot clearly ownedGlobal CLAUDE.md (once)"This project uses roles X, Y, Z"Project CLAUDE.mdStays in Project CLAUDE.md"This role DOES / DOES NOT"SKILL.mdStays in SKILL.mdScope checking templatesPreamble + SKILL.mdGlobal CLAUDE.md (once)

The Compaction Problem
This architecture helps with compaction because it reduces total token volume per skill (no more duplicated preambles) and concentrates the "must not forget" rules in Global CLAUDE.md, which is always loaded. But it doesn't fully solve the drift problem on its own -- that's a separate concern about how to make critical instructions survive compaction. Want to tackle that as the next piece once you're aligned on this structure?