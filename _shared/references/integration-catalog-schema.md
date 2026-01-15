# Integration Catalog Schema

Standard schema for `docs/integrations/_catalog.json` - the index of all external integrations in a project.

## Purpose

The Integration Catalog enables Claude to:
1. **Discover existing integrations** before designing new ones
2. **Understand external dependencies** when planning features
3. **Track integration health** and maintenance requirements

## Ownership

- **Owner**: Solutions Architect
- **Consumers**: TPO, TPgM, Backend Developer, Tech Doc Writer

## File Location

```
your-project/
└── docs/
    └── integrations/
        ├── _catalog.json           # This index file
        ├── stripe/
        │   ├── integration.md      # Integration documentation
        │   └── adr-001-stripe-selection.md
        └── sendgrid/
            └── integration.md
```

## Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["project", "last_updated", "integrations"],
  "properties": {
    "project": {
      "type": "string",
      "description": "Project identifier"
    },
    "last_updated": {
      "type": "string",
      "format": "date-time",
      "description": "ISO-8601 timestamp of last catalog update"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total": { "type": "integer" },
        "by_status": {
          "type": "object",
          "properties": {
            "active": { "type": "integer" },
            "deprecated": { "type": "integer" },
            "planned": { "type": "integer" },
            "inactive": { "type": "integer" }
          }
        },
        "by_category": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    },
    "integrations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "vendor", "category", "status"],
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique integration identifier (e.g., INT-STRIPE)"
          },
          "name": {
            "type": "string",
            "description": "Human-readable integration name"
          },
          "vendor": {
            "type": "string",
            "description": "Vendor/provider name"
          },
          "category": {
            "type": "string",
            "enum": ["payments", "auth", "email", "sms", "analytics", "storage", "ai", "monitoring", "infrastructure", "other"],
            "description": "Integration category"
          },
          "purpose": {
            "type": "string",
            "description": "Why this integration exists (business value)"
          },
          "status": {
            "type": "string",
            "enum": ["active", "deprecated", "planned", "inactive"],
            "description": "Current integration status"
          },
          "criticality": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"],
            "description": "Business criticality if integration fails"
          },
          "api_version": {
            "type": "string",
            "description": "Current API version in use"
          },
          "latest_api_version": {
            "type": "string",
            "description": "Latest available API version from vendor"
          },
          "docs_path": {
            "type": "string",
            "description": "Relative path to integration documentation"
          },
          "adr_path": {
            "type": "string",
            "description": "Relative path to ADR explaining selection"
          },
          "credentials_location": {
            "type": "string",
            "description": "Where credentials are stored (e.g., 'AWS Secrets Manager: prod/stripe')"
          },
          "environments": {
            "type": "object",
            "properties": {
              "production": { "type": "boolean" },
              "staging": { "type": "boolean" },
              "development": { "type": "boolean" }
            }
          },
          "owner": {
            "type": "string",
            "description": "Team or person responsible for this integration"
          },
          "contract": {
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "enum": ["free", "paid", "enterprise"],
                "description": "Contract type"
              },
              "renewal_date": {
                "type": "string",
                "format": "date",
                "description": "Contract renewal date"
              },
              "monthly_cost": {
                "type": "string",
                "description": "Approximate monthly cost"
              }
            }
          },
          "sla": {
            "type": "object",
            "properties": {
              "uptime": {
                "type": "string",
                "description": "Vendor SLA uptime guarantee (e.g., 99.9%)"
              },
              "support_tier": {
                "type": "string",
                "description": "Support level (e.g., 'Business', 'Enterprise')"
              },
              "response_time": {
                "type": "string",
                "description": "Guaranteed response time for issues"
              }
            }
          },
          "fallback": {
            "type": "object",
            "properties": {
              "strategy": {
                "type": "string",
                "enum": ["none", "queue", "alternative_provider", "graceful_degradation"],
                "description": "What happens when integration fails"
              },
              "alternative": {
                "type": "string",
                "description": "Alternative provider if applicable"
              },
              "documented": {
                "type": "boolean",
                "description": "Is fallback documented in runbook?"
              }
            }
          },
          "data_flow": {
            "type": "object",
            "properties": {
              "direction": {
                "type": "string",
                "enum": ["inbound", "outbound", "bidirectional"],
                "description": "Data flow direction"
              },
              "pii_involved": {
                "type": "boolean",
                "description": "Does this integration handle PII?"
              },
              "data_types": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Types of data exchanged"
              }
            }
          },
          "added_date": {
            "type": "string",
            "format": "date",
            "description": "When integration was added"
          },
          "last_reviewed": {
            "type": "string",
            "format": "date",
            "description": "Last review/audit date"
          },
          "related_plans": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Plan IDs that use this integration"
          },
          "tags": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Searchable tags"
          }
        }
      }
    }
  }
}
```

## Example Catalog

```json
{
  "project": "acme-platform",
  "last_updated": "2024-03-15T14:30:00Z",
  "summary": {
    "total": 5,
    "by_status": {
      "active": 4,
      "deprecated": 1,
      "planned": 0,
      "inactive": 0
    },
    "by_category": {
      "payments": 2,
      "email": 1,
      "auth": 1,
      "monitoring": 1
    }
  },
  "integrations": [
    {
      "id": "INT-STRIPE",
      "name": "Stripe Payments",
      "vendor": "Stripe",
      "category": "payments",
      "purpose": "Primary payment processor for subscriptions, one-time payments, and refunds",
      "status": "active",
      "criticality": "critical",
      "api_version": "2023-10-16",
      "latest_api_version": "2024-01-18",
      "docs_path": "docs/integrations/stripe/integration.md",
      "adr_path": "docs/integrations/stripe/adr-001-stripe-selection.md",
      "credentials_location": "AWS Secrets Manager: prod/stripe-api-key",
      "environments": {
        "production": true,
        "staging": true,
        "development": true
      },
      "owner": "payments-team",
      "contract": {
        "type": "paid",
        "renewal_date": "2025-01-01",
        "monthly_cost": "$2,500 + 2.9% per transaction"
      },
      "sla": {
        "uptime": "99.99%",
        "support_tier": "Business",
        "response_time": "4 hours"
      },
      "fallback": {
        "strategy": "queue",
        "alternative": "INT-BRAINTREE (backup)",
        "documented": true
      },
      "data_flow": {
        "direction": "bidirectional",
        "pii_involved": true,
        "data_types": ["payment_method", "customer_email", "billing_address"]
      },
      "added_date": "2022-01-15",
      "last_reviewed": "2024-02-01",
      "related_plans": ["PLAN-2024-002"],
      "tags": ["payments", "subscriptions", "billing", "pci"]
    },
    {
      "id": "INT-SENDGRID",
      "name": "SendGrid Email",
      "vendor": "Twilio SendGrid",
      "category": "email",
      "purpose": "Transactional email delivery (password resets, notifications, receipts)",
      "status": "active",
      "criticality": "high",
      "api_version": "v3",
      "latest_api_version": "v3",
      "docs_path": "docs/integrations/sendgrid/integration.md",
      "credentials_location": "AWS Secrets Manager: prod/sendgrid-api-key",
      "environments": {
        "production": true,
        "staging": true,
        "development": false
      },
      "owner": "platform-team",
      "contract": {
        "type": "paid",
        "renewal_date": "2024-06-01",
        "monthly_cost": "$89.95"
      },
      "sla": {
        "uptime": "99.95%",
        "support_tier": "Pro",
        "response_time": "24 hours"
      },
      "fallback": {
        "strategy": "queue",
        "alternative": null,
        "documented": true
      },
      "data_flow": {
        "direction": "outbound",
        "pii_involved": true,
        "data_types": ["email_address", "user_name"]
      },
      "added_date": "2022-03-01",
      "last_reviewed": "2024-01-15",
      "related_plans": ["PLAN-2024-001", "PLAN-2024-003"],
      "tags": ["email", "notifications", "transactional"]
    },
    {
      "id": "INT-AUTH0",
      "name": "Auth0 Identity",
      "vendor": "Okta (Auth0)",
      "category": "auth",
      "purpose": "SSO, social login, and MFA for enterprise customers",
      "status": "active",
      "criticality": "critical",
      "api_version": "v2",
      "latest_api_version": "v2",
      "docs_path": "docs/integrations/auth0/integration.md",
      "adr_path": "docs/integrations/auth0/adr-002-auth0-selection.md",
      "credentials_location": "AWS Secrets Manager: prod/auth0-credentials",
      "environments": {
        "production": true,
        "staging": true,
        "development": true
      },
      "owner": "security-team",
      "contract": {
        "type": "enterprise",
        "renewal_date": "2024-12-01",
        "monthly_cost": "$1,200"
      },
      "sla": {
        "uptime": "99.99%",
        "support_tier": "Enterprise",
        "response_time": "1 hour"
      },
      "fallback": {
        "strategy": "graceful_degradation",
        "alternative": "Local auth fallback",
        "documented": true
      },
      "data_flow": {
        "direction": "bidirectional",
        "pii_involved": true,
        "data_types": ["user_identity", "email", "profile"]
      },
      "added_date": "2023-06-01",
      "last_reviewed": "2024-02-15",
      "related_plans": ["PLAN-2024-001"],
      "tags": ["auth", "sso", "mfa", "security"]
    },
    {
      "id": "INT-DATADOG",
      "name": "Datadog APM",
      "vendor": "Datadog",
      "category": "monitoring",
      "purpose": "Application performance monitoring, logging, and alerting",
      "status": "active",
      "criticality": "high",
      "api_version": "v2",
      "latest_api_version": "v2",
      "docs_path": "docs/integrations/datadog/integration.md",
      "credentials_location": "AWS Secrets Manager: prod/datadog-api-key",
      "environments": {
        "production": true,
        "staging": true,
        "development": false
      },
      "owner": "platform-team",
      "contract": {
        "type": "paid",
        "renewal_date": "2024-09-01",
        "monthly_cost": "$850"
      },
      "sla": {
        "uptime": "99.9%",
        "support_tier": "Pro",
        "response_time": "4 hours"
      },
      "fallback": {
        "strategy": "graceful_degradation",
        "alternative": "CloudWatch fallback",
        "documented": true
      },
      "data_flow": {
        "direction": "outbound",
        "pii_involved": false,
        "data_types": ["metrics", "logs", "traces"]
      },
      "added_date": "2022-06-01",
      "last_reviewed": "2024-01-01",
      "related_plans": [],
      "tags": ["monitoring", "apm", "logging", "observability"]
    },
    {
      "id": "INT-BRAINTREE",
      "name": "Braintree Payments (Legacy)",
      "vendor": "PayPal (Braintree)",
      "category": "payments",
      "purpose": "Legacy payment processor - being phased out in favor of Stripe",
      "status": "deprecated",
      "criticality": "medium",
      "api_version": "2.x",
      "latest_api_version": "3.x",
      "docs_path": "docs/integrations/braintree/integration.md",
      "credentials_location": "AWS Secrets Manager: prod/braintree-credentials",
      "environments": {
        "production": true,
        "staging": false,
        "development": false
      },
      "owner": "payments-team",
      "contract": {
        "type": "paid",
        "renewal_date": "2024-06-01",
        "monthly_cost": "$500"
      },
      "fallback": {
        "strategy": "alternative_provider",
        "alternative": "INT-STRIPE",
        "documented": true
      },
      "data_flow": {
        "direction": "bidirectional",
        "pii_involved": true,
        "data_types": ["payment_method", "customer_email"]
      },
      "added_date": "2020-01-01",
      "last_reviewed": "2024-01-01",
      "related_plans": [],
      "tags": ["payments", "legacy", "deprecated"]
    }
  ]
}
```

## Status Definitions

| Status | Description | Action Required |
|--------|-------------|-----------------|
| `active` | Integration in production use | Regular maintenance |
| `deprecated` | Being phased out, avoid new usage | Migration plan needed |
| `planned` | Not yet implemented, in roadmap | Development needed |
| `inactive` | Disabled but not removed | Review for removal |

## Criticality Levels

| Level | Definition | Failure Impact |
|-------|------------|----------------|
| `critical` | Core business function | Service outage |
| `high` | Important feature | Degraded experience |
| `medium` | Secondary feature | Workaround available |
| `low` | Nice-to-have | Minimal impact |

## Usage Patterns

### Solutions Architect: Adding New Integration

```python
# 1. Create integration documentation
# 2. Write ADR explaining selection
# 3. Add entry to catalog
new_integration = {
    "id": "INT-TWILIO",
    "name": "Twilio SMS",
    "vendor": "Twilio",
    "category": "sms",
    "purpose": "SMS notifications and 2FA verification codes",
    "status": "planned",
    "criticality": "medium",
    # ... rest of fields
}
# 4. Update summary counts
```

### TPO: Checking Before Planning Feature

```python
# Before writing MRD, check available integrations
catalog = read_json("docs/integrations/_catalog.json")

# Find payment integrations
payment_integrations = [i for i in catalog["integrations"]
                        if i["category"] == "payments" and i["status"] == "active"]

# Check if integration already exists before proposing new vendor
existing_email = next((i for i in catalog["integrations"]
                       if i["category"] == "email" and i["status"] == "active"), None)
```

### TPgM: Before Creating Delivery Plan

```python
# Check integration dependencies for the feature
catalog = read_json("docs/integrations/_catalog.json")

# Find integrations related to the plan
plan_integrations = [i for i in catalog["integrations"]
                     if "PLAN-2024-002" in (i.get("related_plans") or [])]

# Check for deprecated integrations that need migration
deprecated = [i for i in plan_integrations if i["status"] == "deprecated"]
if deprecated:
    raise Warning(f"Plan uses deprecated integrations: {deprecated}")

# Check API versions
outdated = [i for i in plan_integrations
            if i.get("api_version") != i.get("latest_api_version")]
```

### Tech Doc Writer: Finding Integration Docs

```python
# Find all integration docs that need updating
catalog = read_json("docs/integrations/_catalog.json")

# Get doc paths for active integrations
doc_paths = [i["docs_path"] for i in catalog["integrations"]
             if i["status"] == "active" and i.get("docs_path")]
```

## Maintenance

### Catalog Update Triggers

| Trigger | Action | Responsibility |
|---------|--------|----------------|
| New integration added | Add entry, create docs, write ADR | Solutions Architect |
| Integration deprecated | Update status, document migration | Solutions Architect |
| API version updated | Update api_version field | Backend Developer |
| Contract renewed | Update contract info | TPgM |
| Quarterly review | Update last_reviewed, verify all fields | Solutions Architect |

### Quarterly Review Checklist

- [ ] All active integrations reviewed
- [ ] API versions checked against latest
- [ ] Contract renewal dates verified
- [ ] Deprecated integrations migration progress tracked
- [ ] Credentials rotation verified
- [ ] Fallback strategies tested
- [ ] Documentation current
