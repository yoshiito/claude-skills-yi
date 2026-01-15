# Scope Boundaries Framework

This document defines how roles manage their boundaries on a project-by-project basis.

## The Problem

Roles like Solutions Architect, TPgM, and TPO often work across multiple domains. On Project A, an SA might own Frontend architecture. On Project B, they might only advise. Without clear boundaries, roles may:

- Create work items for teams outside their scope
- Make architectural decisions for domains they don't own
- Blur accountability across teams

## When Project Scope Is Not Defined

**CRITICAL**: If the project's `claude.md` does not have a "Project Scope" section, prompt the user to set it up before proceeding with scope-sensitive actions.

### Detection

Check for the Project Scope section in `claude.md`:
```
Look for: "## Project Scope" or "### Domain Ownership" in claude.md
```

### Prompt Template

If scope is not defined, ask:

```
I notice this project doesn't have scope boundaries defined in claude.md yet.

Before I [create issues / design architecture / etc.], I'd like to understand:

1. **What domains exist in this project?**
   (e.g., Frontend, Backend APIs, Data Pipeline, AI Features)

2. **Who owns each domain?**
   (e.g., "I own Frontend architecture" or "Platform Team owns Backend")

3. **What's the Linear context?**
   - Which Team should issues go to?
   - Which Project should they be linked to?

Would you like me to help you set up a Project Scope section in claude.md?
I can use the template from `_shared/references/project-scope-template.md`.
```

### After User Responds

1. Create or update the `## Project Scope` section in `claude.md`
2. Include Domain Ownership table
3. Include Linear Context defaults
4. Then proceed with the original task

## The Solution: Project Scope Definition + Role Boundary Checks

### 1. Project Scope Definition (in claude.md or project config)

Each project should define scope ownership:

```markdown
## Project Scope: [Project Name]

### Domain Ownership

| Domain | Owner Role | Owner Team | Advisor Role |
|--------|-----------|------------|--------------|
| Frontend Architecture | Solutions Architect | Portal Team | - |
| Backend APIs | Solutions Architect | Platform Team | - |
| Data Pipeline | Data Platform Engineer | Data Team | Solutions Architect |
| AI Features | AI Integration Engineer | ML Team | Solutions Architect |

### Cross-Domain Protocol

When working outside your owned domain:
1. **Document** - Note the gap/dependency/recommendation
2. **Tag** - Mention the domain owner in Linear comment
3. **Do NOT** - Create tickets, propose implementations, or make decisions

### Scope Notes
- Portal Team owns all customer-facing UI decisions
- Platform Team owns all API contract decisions
- Data Team owns all database schema decisions
```

### 2. Role Boundary Checks (in each SKILL.md)

Each role that can cross boundaries includes a pre-output checklist:

```markdown
## Scope Boundary Check

Before proposing work items, creating tickets, or making recommendations:

1. **Check project scope** - Review scope ownership in project's claude.md
2. **Verify your domain** - Confirm this work falls within domains you own
3. **Cross-domain work**:
   - Document the gap or dependency
   - Tag the domain owner for their action
   - Do NOT create implementation tickets for other domains
   - Do NOT propose specific solutions for other domains

### What You CAN Do Outside Your Scope
- Identify gaps and dependencies
- Document observations and concerns
- Recommend escalation or consultation
- Ask questions to domain owners

### What You CANNOT Do Outside Your Scope
- Create Linear issues/sub-issues
- Propose implementation approaches
- Make architectural decisions
- Define acceptance criteria
```

## Role-Specific Boundaries

### Solutions Architect

**Owns**: Technical architecture for assigned domains
**Boundary Check**: Before creating sub-issues, verify each component falls within owned domains

```
If creating [Backend] sub-issue:
  → Check: Am I the SA for Backend on this project?
  → If NO: Document as dependency, tag Backend SA

If creating [Frontend] sub-issue:
  → Check: Am I the SA for Frontend on this project?
  → If NO: Document as dependency, tag Frontend SA
```

### Technical Program Manager

**Owns**: Delivery coordination, status tracking, escalation
**Boundary Check**: TPgM tracks all domains but creates issues only after domain owners define them

```
Creating issues: ONLY after domain owner (SA, TPO) has defined requirements
Tracking issues: All domains OK
Making decisions: Only on process, escalation, timeline - NOT technical approach
```

### Technical Product Owner

**Owns**: Requirements for assigned product areas
**Boundary Check**: Before creating parent issues, verify the product area is owned

```
If defining requirements for Feature X:
  → Check: Am I the TPO for this product area?
  → If NO: Flag to appropriate TPO, document dependency
```

### API Designer

**Owns**: API contracts for assigned services
**Boundary Check**: Before defining contracts, verify service ownership

```
If designing API for Service X:
  → Check: Am I the API Designer for this service?
  → If NO: Document API needs, tag appropriate designer
```

### Data Platform Engineer

**Owns**: Data architecture for assigned data stores
**Boundary Check**: Before designing schemas, verify ownership

```
If designing schema for Database X:
  → Check: Am I the DPE for this data store?
  → If NO: Document data requirements, tag appropriate DPE
```

### AI Integration Engineer

**Owns**: AI/ML architecture for assigned features
**Boundary Check**: Before designing AI features, verify ownership

```
If designing AI for Feature X:
  → Check: Am I the AI Engineer for this feature?
  → If NO: Document AI needs, tag appropriate engineer
```

### Support Engineer

**Owns**: Investigation, triage, documentation of findings
**Boundary Check**: Investigations span all domains, but fixes do not

```
Investigation: All domains OK
Root cause documentation: All domains OK
Fix recommendations: Must route to domain owner
Creating fix tickets: ONLY for domains you own
```

## Cross-Domain Communication Templates

### Flagging a Gap (for domain you don't own)

```markdown
## Cross-Domain Dependency

**From**: [Your Role] ([Your Team])
**To**: [Domain Owner Role] ([Domain Owner Team])
**Project**: [Project Name]

### Observation
[What you noticed that needs attention]

### Impact on Your Domain
[How this affects the work you own]

### Recommended Action
[What the domain owner should consider - NOT how to implement]

### Urgency
[How this affects your timeline]
```

### Requesting Consultation

```markdown
## Consultation Request

**From**: [Your Role]
**To**: [Domain Expert Role]
**Topic**: [Brief description]

### Context
[Why you need input]

### Questions
1. [Specific question]
2. [Specific question]

### Your Current Understanding
[What you think, for validation]
```

## Project Setup Checklist

When starting a new project:

1. [ ] Define domain ownership table in claude.md
2. [ ] Identify which roles are active on this project
3. [ ] Map each active role to their owned domains
4. [ ] Document cross-domain protocol
5. [ ] Share with all team members

## Summary

- Scope boundaries are **project-specific**, not role-specific
- Roles must **check ownership** before creating work items
- Cross-domain work should **flag, not fix**
- Project claude.md is the **source of truth** for scope
