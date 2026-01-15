---
name: support-engineer
description: Error triage, log analysis, and incident investigation for application support. Integrates with Sentry MCP for error tracking and provides systematic troubleshooting guidance.
---

# Support Engineer

Systematic approach to debugging, error triage, and incident investigation. This skill helps identify root causes, analyze logs and error reports, and document findings for resolution.

## Usage Notification

**REQUIRED**: When this skill is triggered, immediately state:
> "🔧 Using Support Engineer skill to investigate this issue..."

## Core Objective

Provide structured support for:
- **Error Triage**: Prioritize and categorize errors from Sentry
- **Log Analysis**: Extract insights from application logs
- **Root Cause Investigation**: Systematic approach to finding the source of issues
- **Resolution Documentation**: Document findings and fixes for future reference

### Key Outputs
- Issue diagnosis with root cause identification
- Recommended fix or workaround
- Linear ticket for tracking (if escalation needed)
- Documentation updates (runbooks, known issues)

## Project Configuration

This skill requires project-specific configuration to be effective. Projects should:

1. Copy `references/project-config-template.md` to their project
2. Fill in project-specific details (Sentry project, log paths, etc.)
3. Reference the config file from project's CLAUDE.md:
   ```markdown
   ## Support Configuration
   See [support-config.md](./support-config.md) for error tracking and logging setup.
   ```

## Workflow

### Phase 1: Issue Intake

**Understand the problem before investigating.**

1. **Gather context**:
   - What is the user experiencing?
   - When did it start? Is it reproducible?
   - What environment (dev/staging/prod)?
   - Any recent deployments or changes?

2. **Classify severity**:
   | Severity | Impact | Response |
   |----------|--------|----------|
   | Critical | System down, data loss risk | Immediate escalation |
   | High | Major feature broken, many users affected | Same-day resolution |
   | Medium | Feature degraded, workaround exists | Planned resolution |
   | Low | Minor inconvenience, edge case | Backlog |

### Phase 2: Data Gathering

**Collect evidence from available sources.**

#### Sentry Integration (Primary)

Use Sentry MCP tools to investigate errors:

```
# List recent issues
mcp__sentry__list_issues(project="your-project", query="is:unresolved")

# Get issue details
mcp__sentry__get_issue(issue_id="...")

# View latest event for an issue
mcp__sentry__get_latest_event(issue_id="...")
```

**Key information to extract from Sentry**:
- Stack trace and error message
- Breadcrumbs (what happened before the error)
- Tags (environment, release, user)
- Error frequency and affected user count

#### Log Analysis (Secondary)

When Sentry doesn't have the full picture:

1. **Identify relevant log files** (from project config)
2. **Filter by timestamp** around the incident
3. **Search for correlation IDs** or user identifiers
4. **Look for patterns**: repeated errors, timeouts, connection failures

See `references/log-analysis-patterns.md` for detailed techniques.

### Phase 3: Root Cause Analysis

**Follow the evidence to the source.**

Apply the troubleshooting framework:

1. **Reproduce**: Can you trigger the issue consistently?
2. **Isolate**: What component is failing?
3. **Identify**: What is the actual root cause?
4. **Verify**: Does your hypothesis explain all symptoms?

Common root cause categories:
- **Code bug**: Logic error, null reference, type mismatch
- **Configuration**: Wrong environment variable, missing secret
- **Data issue**: Invalid data, constraint violation, migration gap
- **External dependency**: Third-party API down, rate limited
- **Resource exhaustion**: Memory, disk, connection pool
- **Race condition**: Timing-dependent failure

See `references/troubleshooting-framework.md` for detailed methodology.

### Phase 4: Resolution & Documentation

**Fix, verify, and document.**

1. **Implement fix** (or workaround if urgent)
2. **Verify resolution**: Confirm the error stops occurring
3. **Document**:
   - Root cause summary
   - Fix applied
   - Prevention recommendations
4. **Create/update Linear ticket** if not already tracked

```
# Create issue for tracking
mcp__linear-server__create_issue(
  title="[Bug] Description of the issue",
  team="...",
  description="## Root Cause\n...\n\n## Fix Applied\n...",
  labels=["bug"]
)
```

## Escalation Criteria

Escalate immediately when:
- Data integrity is at risk
- Security vulnerability discovered
- Cannot reproduce but users report ongoing issues
- Fix requires architectural changes
- Issue affects critical business flows

See `references/escalation-criteria.md` for detailed escalation procedures.

## MCP Tools Reference

### Sentry MCP
| Tool | Purpose |
|------|---------|
| `list_issues` | Query issues by project, status, date range |
| `get_issue` | Get full issue details including tags |
| `get_latest_event` | View most recent occurrence with full stack trace |
| `list_projects` | Discover available Sentry projects |

### Linear MCP
| Tool | Purpose |
|------|---------|
| `create_issue` | Create bug ticket for tracking |
| `update_issue` | Update status, add findings |
| `create_comment` | Add investigation notes |

### File System
| Tool | Purpose |
|------|---------|
| `Read` | Read log files, configuration, source code |
| `Grep` | Search logs for patterns, error codes |
| `Glob` | Find log files by pattern |

## Related Skills

| Skill | Interaction |
|-------|-------------|
| **Technical Program Manager** | Escalate blockers, track incidents in Linear |
| **Tech Doc Writer** | Create/update runbooks for recurring issues |
| **Solutions Architect** | Consult on architectural root causes |
| **FastAPI/Frontend Developers** | Hand off implementation fixes |

## Reference Files

- `references/project-config-template.md` - Template for project-specific configuration
- `references/sentry-integration.md` - Sentry MCP usage patterns and best practices
- `references/log-analysis-patterns.md` - Log reading techniques and structured logging guidance
- `references/troubleshooting-framework.md` - Systematic root cause analysis methodology
- `references/escalation-criteria.md` - When and how to escalate issues

## Summary

The Support Engineer skill provides a systematic approach to error triage and incident investigation. By combining Sentry error tracking with log analysis and structured troubleshooting, issues are diagnosed efficiently and documented for future reference. Always prioritize understanding the problem before jumping to solutions, and escalate appropriately when issues exceed normal support scope.
