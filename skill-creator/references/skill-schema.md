# Skill YAML Schema

This document defines the schema for `skill.yaml` files and clarifies what is **variable-driven** (structured, validated, generated) vs **raw content** (flexible, pass-through).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     INDIVIDUAL SKILLS                            │
│                                                                  │
│  skill.yaml defines:                                            │
│  - meta (identity)                                              │
│  - role (capabilities)                                          │
│  - boundaries (what I do / don't do)                            │
│  - workflow (my process)                                        │
│  - customSections (my unique content)                           │
│                                                                  │
│  skill.yaml does NOT define:                                    │
│  - Who invokes me (Agent Skill Coordinator owns this)         │
│  - Who I return to (Agent Skill Coordinator owns this)        │
│  - Role relationships (Agent Skill Coordinator owns this)     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   UTILITY ROLES (Centralized)                    │
│                                                                  │
│  ┌─────────────────────┐      ┌─────────────────────────────┐   │
│  │ Project Coordinator │      │ Agent Skill Coordinator   │   │
│  │                     │      │                             │   │
│  │ Owns:               │      │ Owns:                       │   │
│  │ - Ticket CRUD       │      │ - Role registry             │   │
│  │ - DoR/DoD gates     │      │ - Flow rules                │   │
│  │                     │      │ - Invocation permissions    │   │
│  └─────────────────────┘      └─────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Schema: Variable-Driven Sections

These sections are **required** and **validated**. The template generates consistent output from them.

### `meta` (Required)

```yaml
meta:
  name: string              # Skill identifier (kebab-case)
  displayName: string       # Human-readable name
  emoji: string             # Single emoji for notifications
  description: string       # Discovery description (1-3 sentences)
```

### `role` (Required)

```yaml
role:
  prefix: string            # Role prefix for messages (e.g., BACKEND_DEVELOPER)

  capabilities:
    canIntakeUserRequests: boolean      # Can receive direct user requests?
    requiresTicketWithSpec: boolean     # Needs Technical Spec + Gherkin?
    requiresActivationConfirmation: boolean  # Needs user confirmation? (false for utilities)
    requiresProjectScope: boolean       # Needs Project Scope in claude.md?
    isUtility: boolean                  # Is this a utility role?
    isOrchestrator: boolean             # Optional: manages work assignment (PM)
```

**Template uses capabilities to generate:**
- Preamble text (role type declaration)
- Scope check behavior
- Confirmation requirements

### `boundaries` (Required)

```yaml
boundaries:
  # MUST be non-empty - prevents role bleeding
  authorizedActions:
    - string  # What this role EXCLUSIVELY owns
    - string

  # MUST be non-empty - explicit prohibitions (simple strings)
  prohibitions:
    - string  # What this role must NOT do
    - string
    # NOTE: "owner" field is DEPRECATED - Agent Skill Coordinator handles all routing

  # NOTE: routingTable is REMOVED - "Out of scope → Route to Agent Skill Coordinator"
  # is now automatically rendered for all non-utility roles
```

### `workflow` (Required)

```yaml
workflow:
  phases:
    - name: string        # Phase name
      required: boolean   # Optional: is this phase mandatory?
      condition: string   # Optional: when does this phase apply?
      description: string # Optional: phase description
      steps:
        # Simple format (list of strings)
        - string
        - string

        # Or rich format (list of objects)
        - action: string
          description: string
          # Optional rich content (raw markdown)
          checklist: [string]
          template: string
          lookFor: [{file: string, checkFor: string}]
```

### `qualityChecklist` (Required)

```yaml
# Simple format (flat list)
qualityChecklist:
  - string
  - string

# Or categorized format
qualityChecklist:
  sections:
    - name: string
      checks:
        - string
        - string
```

### `references` (Required, can be empty)

```yaml
references:
  local:
    - path: string        # Path relative to skill directory
      purpose: string     # What this file provides

  shared:
    - path: string        # Path to _shared/references/
      purpose: string
```

### `relatedSkills` (Required, can be empty)

```yaml
relatedSkills:
  upstream:
    - skill: string       # Skill name
      provides: string    # What they provide to this role

  downstream:
    - skill: string
      coordination: string  # How this role coordinates with them

  consultationTriggers:   # Optional
    - skill: string
      when: string        # When to consult this skill
```

---

## Schema: Raw Content Sections

These sections accept **raw markdown** and pass through with minimal processing.

### `customSections` (Optional)

```yaml
customSections:
  - id: string            # Unique identifier
    title: string         # Section heading
    content: |            # Raw markdown - passed through as-is
      ## Subsection

      Any markdown content here...

      ```python
      # Code blocks work
      def example():
          pass
      ```

      | Tables | Work |
      |--------|------|
      | Yes    | They do |
```

**Use customSections for:**
- Tech Stack descriptions
- Decision frameworks (SQL vs ORM)
- Ticket workflow details with code examples
- Any role-specific content that varies significantly

### Rich content in workflow steps

```yaml
workflow:
  phases:
    - name: Phase Name
      steps:
        - action: Step name
          template: |     # Raw markdown template
            [ROLE] - Message template here.

            **Details**:
            - Item 1
            - Item 2
```

---

## Schema: Role-Type Specific Sections

Some sections only apply to certain role types.

### `missionModes` (Orchestration roles only)

```yaml
missionModes:
  required: boolean       # Must ask at session start?
  prompt: |               # Raw markdown prompt
    Which mode?
    1. **DRIVE** - Active
    2. **TRACK** - Passive

  modes:
    drive:
      description: string
      behaviors:
        - string
      preConditions:
        - string
      postConditions:
        - string

    track:
      description: string
      behaviors:
        - string
```

### `qualityGates` (Utility roles only)

```yaml
qualityGates:
  definitionOfReady:
    enforceAt: string
    ticketTypes:
      epic:
        titlePrefix: string
        requiredSections:
          - name: string
            verify: string

  definitionOfDone:
    enforceAt: string
    ticketTypes:
      implementation:
        checks:
          - name: string
            verify: string

  rejectionFormat:
    template: |           # Raw markdown
      [ROLE] - ❌ REJECTED
      ...
```

### `invocationModel` (Utility roles only)

```yaml
invocationModel:
  description: string

  callers:
    - role: string
      when: string
      example: string

  pattern:
    onStart: string       # Template: "[ROLE] - Invoked by [CALLING_ROLE]."
    onEnd: string         # Template: "Returning to [CALLING_ROLE]."

  callingRoleTracking:
    required: boolean
```

### `invocationInterface` (Utility roles only)

```yaml
invocationInterface:
  create:
    format: |             # Raw markdown
      [ROLE] Create:
      - Type: ...
    returns: string

  update:
    format: |
      [ROLE] Update #NUM:
      - Field: value
```

### `roleRegistry` (Agent Skill Coordinator only)

```yaml
roleRegistry:
  roles:
    - prefix: string
      displayName: string
      type: definition | orchestration | worker | utility | reactive | meta
      handles:
        - string

  flowRules:
    completionReturn:
      default: string     # Role prefix
      exceptions:
        - from: string
          to: string
          reason: string

    invocationPermissions:
      - role: string | "*"
        canInvoke:
          - string

    requestRouting:
      - keywords: [string]
        routeTo: string
        reason: string
```

---

## Schema: Modes

```yaml
modes:
  supported: [track, drive, collab, explore]  # Which modes this skill supports

  drive:
    skipConfirmation: boolean
    preWorkValidation: boolean

  track:
    requiresExplicitAssignment: boolean

  collab:
    allowsConcurrentWork: boolean

  explore:
    # TBD - explore mode definition
```

---

## Validation Rules

The generator validates:

1. **Required sections exist**: meta, role, boundaries, workflow, references, relatedSkills
2. **Boundaries are non-empty**: authorizedActions and prohibitions must have items
3. **Workflow has phases**: At least one phase required
4. **Role prefix format**: SCREAMING_SNAKE_CASE
5. **No handoff section**: Handoff is owned by Agent Skill Coordinator

---

## Summary: What Goes Where

| Content Type | Location | Format |
|--------------|----------|--------|
| Identity | `meta` | Variable |
| Capabilities | `role.capabilities` | Variable |
| What I do | `boundaries.authorizedActions` | Variable (list) |
| What I don't do | `boundaries.prohibitions` | Variable (list with owner) |
| My process | `workflow.phases` | Variable + raw templates |
| My checklist | `qualityChecklist` | Variable |
| My unique content | `customSections` | Raw markdown |
| Who invokes me | Agent Skill Coordinator | NOT in skill.yaml |
| Who I return to | Agent Skill Coordinator | NOT in skill.yaml |
| Role relationships | Agent Skill Coordinator | NOT in skill.yaml |

---

## Generation Architecture

### What Gets Generated vs What's Data

| SKILL.md Section | Source | To Change |
|------------------|--------|-----------|
| Frontmatter | `meta` in YAML | Edit skill.yaml |
| Title + Description | `meta` in YAML | Edit skill.yaml |
| Preamble | **Template logic** + `role.capabilities` | Edit template OR capabilities |
| Usage Notification | **Template** + `meta.emoji`, `meta.displayName` | Edit template OR meta |
| Invocation Model | `invocationModel` in YAML | Edit skill.yaml |
| Role Boundaries | `boundaries` in YAML | Edit skill.yaml |
| Workflow | `workflow` in YAML | Edit skill.yaml |
| Quality Checklist | `qualityChecklist` in YAML | Edit skill.yaml |
| Custom Sections | `customSections` in YAML | Edit skill.yaml |
| References | `references` in YAML | Edit skill.yaml |
| Related Skills | `relatedSkills` in YAML | Edit skill.yaml |

### Template-Controlled (Consistent Across All Skills)

These sections have **identical structure** across all skills - only data varies:

- **Preamble format** - Role type declaration, numbered checks, scope block
- **Usage Notification format** - `[PREFIX] - emoji Using DisplayName skill - [action]`
- **Boundaries format** - "This role DOES" / "does NOT do" / "When unclear"
- **Section ordering** - Same order in every SKILL.md

**To change these:** Edit `skill-template.md.j2`

### Data-Controlled (Varies Per Skill)

These sections have **skill-specific content** defined in YAML:

- **What the skill does** - `boundaries.authorizedActions`
- **What it doesn't do** - `boundaries.prohibitions`
- **Workflow phases** - `workflow.phases`
- **Checklist items** - `qualityChecklist`
- **Reference files** - `references.local`, `references.shared`

**To change these:** Edit `skill.yaml`

### Flexible (Custom Content)

These sections accept **raw markdown** for truly unique content:

- **Tech Stack descriptions**
- **Decision frameworks** (SQL vs ORM)
- **Response format examples**
- **Unique interfaces** (ASC's query interface, PC's ticket templates)

**To change these:** Edit `customSections` in `skill.yaml`

---

## Maintenance Workflow

### Adding a New Skill

1. Create `{skill-name}/skill.yaml` using example YAMLs as reference
2. Run `python generate-skill.py {skill-name}`
3. Review generated SKILL.md
4. Iterate on skill.yaml until output is correct

### Updating Skill Content

| Change Type | File to Edit | Then |
|-------------|--------------|------|
| Skill-specific content | `skill.yaml` | Regenerate |
| Preamble/format for ALL skills | `skill-template.md.j2` | Regenerate all |
| Role capabilities | `skill.yaml` → `role.capabilities` | Regenerate |

### Updating Template (Affects ALL Skills)

1. Edit `skill-creator/references/skill-template.md.j2`
2. Test with one skill: `python generate-skill.py {skill-name}`
3. Review output
4. Regenerate all: `python generate-skill.py --all`

### Files Involved

```
skill-creator/references/
├── skill-template.md.j2      # Template (controls format)
├── generate-skill.py         # Generator script
├── skill-schema.md           # This documentation
├── example-worker-skill.yaml # Reference for workers
├── example-intake-skill.yaml # Reference for intake roles
└── example-utility-skill.yaml# Reference for utilities

{skill-name}/
├── skill.yaml                # Source of truth (data)
├── SKILL.md                  # Generated output (don't edit)
└── references/               # Skill-specific reference files
```
