# Support Engineer Project Configuration

Copy this template to your project and customize it for your specific setup. Reference it from your project's CLAUDE.md.

---

## Sentry Configuration

### Project Details
- **Sentry Organization**: `your-org`
- **Sentry Project**: `your-project`
- **Project Slug**: `your-org/your-project`

### Environments
| Environment | Description | Alert Priority |
|-------------|-------------|----------------|
| `production` | Live users | Critical - immediate |
| `staging` | Pre-release testing | High - same day |
| `development` | Local/dev testing | Low - as needed |

### Critical Issue Labels
Issues with these tags require immediate attention:
- `critical`
- `security`
- `data-loss`

### Ignored Patterns
Known issues that can be deprioritized:
- Browser extension interference (e.g., `chrome-extension://`)
- Bot/crawler errors
- [Add project-specific patterns]

---

## Logging Configuration

### Log Locations
| Component | Path/Source | Format |
|-----------|-------------|--------|
| Backend API | `/var/log/app/api.log` | JSON |
| Background Jobs | `/var/log/app/workers.log` | JSON |
| Database | PostgreSQL logs | Standard |
| Web Server | Nginx/Caddy access logs | Combined |

### Log Format
**Recommended**: Structured JSON logging for easier parsing.

Example log entry:
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "ERROR",
  "logger": "api.auth",
  "message": "Authentication failed",
  "user_id": "user_123",
  "request_id": "req_abc",
  "error": "InvalidTokenError",
  "trace_id": "trace_xyz"
}
```

### Key Fields to Capture
- `timestamp` - When it happened
- `level` - ERROR, WARN, INFO, DEBUG
- `request_id` - Correlation ID for tracing
- `user_id` - Who was affected (if applicable)
- `error` - Error type/code
- `trace_id` - For distributed tracing

### Log Retention
| Environment | Retention |
|-------------|-----------|
| Production | 30 days |
| Staging | 7 days |
| Development | 1 day |

---

## Critical User Flows

Prioritize investigation for issues affecting these flows:

1. **Authentication Flow**
   - Login / Logout
   - Password reset
   - Session management

2. **Core Business Flow** (customize for your app)
   - [Add your primary user journey]
   - [Add secondary flows]

3. **Payment/Billing** (if applicable)
   - Checkout
   - Subscription management
   - Invoice generation

4. **Data Operations**
   - Create/Update operations
   - Data exports
   - Integrations with external systems

---

## Tech Stack Context

Understanding the stack helps with debugging:

| Layer | Technology | Notes |
|-------|------------|-------|
| Frontend | React + TypeScript | [Version, key libraries] |
| Backend | FastAPI + Python | [Version, key packages] |
| Database | PostgreSQL | [Version, hosted where] |
| Cache | Redis | [If applicable] |
| Queue | [Celery/RQ/etc] | [If applicable] |
| Hosting | [AWS/GCP/Vercel/etc] | [Key services used] |

---

## Escalation Contacts

### Technical Escalation
| Role | Contact | When to Escalate |
|------|---------|------------------|
| Tech Lead | [name/handle] | Architectural issues, major bugs |
| On-Call | [rotation/channel] | Production outages |
| Security | [name/handle] | Security vulnerabilities |

### Business Escalation
| Role | Contact | When to Escalate |
|------|---------|------------------|
| Product Owner | [name/handle] | User-impacting decisions |
| Customer Success | [name/handle] | Customer communication needed |

### Communication Channels
- **Incidents**: [Slack channel / PagerDuty / etc]
- **Bug Discussion**: [Slack channel / Linear project]
- **Customer Updates**: [Email template / Status page]

---

## Known Issues & Workarounds

Document recurring issues and their workarounds:

### Issue: [Brief description]
- **Symptoms**: What users see
- **Root Cause**: Why it happens
- **Workaround**: How to temporarily resolve
- **Permanent Fix**: Status of long-term solution

### Issue: [Add more as discovered]
- **Symptoms**:
- **Root Cause**:
- **Workaround**:
- **Permanent Fix**:

---

## Quick Reference Commands

### Sentry Queries
```
# Unresolved issues in last 24h
is:unresolved firstSeen:-24h

# High-frequency errors
is:unresolved times_seen:>100

# Specific user affected
user.id:user_123

# Specific release
release:v1.2.3
```

### Log Search Patterns
```bash
# Search for errors in recent logs
grep -i "error" /var/log/app/api.log | tail -100

# Find by request ID
grep "req_abc123" /var/log/app/*.log

# Count error types
grep -o '"error":"[^"]*"' /var/log/app/api.log | sort | uniq -c | sort -rn
```

---

## Maintenance Notes

- **Last Updated**: [Date]
- **Updated By**: [Name]
- **Next Review**: [Date - recommend quarterly]
