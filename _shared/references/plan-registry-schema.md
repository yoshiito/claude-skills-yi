# Plan Registry Schema

Standard schema for `docs/plans/_registry.json` - the index of all product plans in a project.

## Purpose

The Plan Registry enables Claude to:
1. **Discover existing plans** before creating new ones (avoid duplication)
2. **Understand planned work** when designing architecture or creating tickets
3. **Track plan lifecycle** from draft through completion

## Ownership

- **Owner**: Technical Product Owner (TPO)
- **Consumers**: Solutions Architect, TPgM, all implementation skills

## File Location

```
your-project/
└── docs/
    └── plans/
        ├── _registry.json          # This index file
        ├── 2024-Q1-auth-revamp/
        │   └── mrd.md
        └── 2024-Q2-payments/
            └── mrd.md
```

## Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["project", "last_updated", "plans"],
  "properties": {
    "project": {
      "type": "string",
      "description": "Project identifier"
    },
    "last_updated": {
      "type": "string",
      "format": "date-time",
      "description": "ISO-8601 timestamp of last registry update"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total": { "type": "integer" },
        "by_status": {
          "type": "object",
          "properties": {
            "draft": { "type": "integer" },
            "approved": { "type": "integer" },
            "in_progress": { "type": "integer" },
            "completed": { "type": "integer" },
            "cancelled": { "type": "integer" }
          }
        },
        "by_quarter": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    },
    "plans": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "status", "mrd_path"],
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique plan identifier (e.g., PLAN-2024-001)"
          },
          "title": {
            "type": "string",
            "description": "Human-readable plan name"
          },
          "summary": {
            "type": "string",
            "description": "One-sentence description of the plan"
          },
          "status": {
            "type": "string",
            "enum": ["draft", "approved", "in_progress", "completed", "cancelled"],
            "description": "Current plan lifecycle status"
          },
          "priority": {
            "type": "string",
            "enum": ["P0", "P1", "P2", "P3"],
            "description": "Plan priority level"
          },
          "target_quarter": {
            "type": "string",
            "pattern": "^[0-9]{4}-Q[1-4]$",
            "description": "Target delivery quarter (e.g., 2024-Q2)"
          },
          "mrd_path": {
            "type": "string",
            "description": "Relative path to MRD document"
          },
          "linear_project_id": {
            "type": "string",
            "description": "Linked Linear project ID (if exists)"
          },
          "linear_parent_issue_id": {
            "type": "string",
            "description": "Linked Linear parent issue ID (if exists)"
          },
          "owner": {
            "type": "string",
            "description": "TPO or product owner responsible"
          },
          "created": {
            "type": "string",
            "format": "date",
            "description": "Plan creation date"
          },
          "approved_date": {
            "type": "string",
            "format": "date",
            "description": "Date plan was approved (if applicable)"
          },
          "completed_date": {
            "type": "string",
            "format": "date",
            "description": "Date plan was completed (if applicable)"
          },
          "tags": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Categorization tags (e.g., auth, payments, frontend)"
          },
          "depends_on": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Plan IDs this plan depends on"
          },
          "related_integrations": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Integration IDs from the Integration Catalog"
          }
        }
      }
    }
  }
}
```

## Example Registry

```json
{
  "project": "acme-platform",
  "last_updated": "2024-03-15T14:30:00Z",
  "summary": {
    "total": 4,
    "by_status": {
      "draft": 1,
      "approved": 1,
      "in_progress": 1,
      "completed": 1,
      "cancelled": 0
    },
    "by_quarter": {
      "2024-Q1": 1,
      "2024-Q2": 2,
      "2024-Q3": 1
    }
  },
  "plans": [
    {
      "id": "PLAN-2024-001",
      "title": "Authentication System Revamp",
      "summary": "Replace legacy auth with OAuth2/OIDC supporting SSO and MFA",
      "status": "completed",
      "priority": "P0",
      "target_quarter": "2024-Q1",
      "mrd_path": "docs/plans/2024-Q1-auth-revamp/mrd.md",
      "linear_project_id": "proj_abc123",
      "linear_parent_issue_id": "LIN-456",
      "owner": "product-owner@company.com",
      "created": "2023-11-01",
      "approved_date": "2023-11-15",
      "completed_date": "2024-02-28",
      "tags": ["auth", "security", "infrastructure"],
      "depends_on": [],
      "related_integrations": ["INT-AUTH0", "INT-OKTA"]
    },
    {
      "id": "PLAN-2024-002",
      "title": "Payment Processing V2",
      "summary": "Add support for subscriptions, refunds, and multi-currency",
      "status": "in_progress",
      "priority": "P1",
      "target_quarter": "2024-Q2",
      "mrd_path": "docs/plans/2024-Q2-payments/mrd.md",
      "linear_project_id": "proj_def456",
      "linear_parent_issue_id": "LIN-789",
      "owner": "product-owner@company.com",
      "created": "2024-01-15",
      "approved_date": "2024-02-01",
      "tags": ["payments", "billing", "revenue"],
      "depends_on": ["PLAN-2024-001"],
      "related_integrations": ["INT-STRIPE", "INT-PLAID"]
    },
    {
      "id": "PLAN-2024-003",
      "title": "Real-time Notifications",
      "summary": "WebSocket-based notification system for in-app and push notifications",
      "status": "approved",
      "priority": "P2",
      "target_quarter": "2024-Q2",
      "mrd_path": "docs/plans/2024-Q2-notifications/mrd.md",
      "owner": "product-owner@company.com",
      "created": "2024-02-10",
      "approved_date": "2024-03-01",
      "tags": ["notifications", "realtime", "engagement"],
      "depends_on": [],
      "related_integrations": ["INT-SENDGRID", "INT-FIREBASE"]
    },
    {
      "id": "PLAN-2024-004",
      "title": "Analytics Dashboard V2",
      "summary": "Self-service analytics with custom report builder",
      "status": "draft",
      "priority": "P2",
      "target_quarter": "2024-Q3",
      "mrd_path": "docs/plans/2024-Q3-analytics/mrd.md",
      "owner": "product-owner@company.com",
      "created": "2024-03-10",
      "tags": ["analytics", "reporting", "self-service"],
      "depends_on": ["PLAN-2024-002"]
    }
  ]
}
```

## Status Definitions

| Status | Description | Who Can Transition |
|--------|-------------|-------------------|
| `draft` | Plan is being written, not ready for review | TPO |
| `approved` | Plan reviewed and approved, ready for architecture | TPO + Stakeholders |
| `in_progress` | Active development underway | TPgM (when work starts) |
| `completed` | All planned work delivered | TPgM (when delivered) |
| `cancelled` | Plan abandoned (keep for historical reference) | TPO |

## Usage Patterns

### TPO: Creating a New Plan

```python
# 1. Create MRD document
# 2. Add entry to registry
new_plan = {
    "id": "PLAN-2024-005",
    "title": "Feature Name",
    "summary": "One-sentence description",
    "status": "draft",
    "priority": "P2",
    "target_quarter": "2024-Q3",
    "mrd_path": "docs/plans/2024-Q3-feature/mrd.md",
    "owner": "owner@company.com",
    "created": "2024-03-15",
    "tags": ["relevant", "tags"]
}
# 3. Update summary counts
```

### Solutions Architect: Checking Before Design

```python
# Before designing architecture, check existing plans
registry = read_json("docs/plans/_registry.json")

# Find related plans
related = [p for p in registry["plans"]
           if "auth" in p["tags"] or "auth" in p["title"].lower()]

# Check for dependencies
blocking_plans = [p for p in registry["plans"]
                  if p["status"] in ["draft", "approved", "in_progress"]]
```

### TPgM: Before Creating Linear Tickets

```python
# Before creating tickets, verify plan exists and is approved
registry = read_json("docs/plans/_registry.json")
plan = next((p for p in registry["plans"] if p["id"] == "PLAN-2024-002"), None)

if not plan:
    raise Error("Plan not found in registry - TPO must create plan first")

if plan["status"] != "approved":
    raise Error(f"Plan not approved (status: {plan['status']}) - cannot create tickets")

# Safe to create Linear project/issues
# Update registry with Linear IDs after creation
```

## Maintenance

### Registry Update Triggers

| Trigger | Action | Responsibility |
|---------|--------|----------------|
| New plan created | Add entry, update summary | TPO |
| Plan approved | Update status, add approved_date | TPO |
| Work starts | Update status to in_progress, add Linear IDs | TPgM |
| Work completes | Update status to completed, add completed_date | TPgM |
| Plan cancelled | Update status to cancelled | TPO |
| Plan modified | Update fields, update last_updated | TPO |

### Quarterly Cleanup

At the start of each quarter:
1. Archive completed plans older than 2 quarters
2. Review draft plans - still relevant?
3. Update target_quarter for slipped plans
4. Validate Linear project links are still valid
