---
title: "[Service/Process Name] Runbook"
doc_type: runbook
version: "1.0.0"
status: draft
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
author: ""
reviewers: []
related_docs: []
tags: [runbook, operations]
---

# [Service/Process Name] Runbook

## Quick Reference

| Item | Value |
|------|-------|
| **Service Owner** | [Team/Person] |
| **On-Call Rotation** | [Link to PagerDuty/OpsGenie] |
| **Slack Channel** | #[channel-name] |
| **Dashboard** | [Link to Grafana/Datadog] |
| **Logs** | [Link to log aggregator] |

### Critical Commands

```bash
# Check service status
kubectl get pods -n [namespace] -l app=[service-name]

# View recent logs
kubectl logs -n [namespace] -l app=[service-name] --tail=100

# Restart service
kubectl rollout restart deployment/[service-name] -n [namespace]
```

## Service Overview

Brief description of what this service does and its role in the system.

### Dependencies

| Dependency | Type | Impact if Down |
|------------|------|----------------|
| Database | Critical | Service unavailable |
| Cache | Degraded | Increased latency |
| External API | Degraded | Feature X unavailable |

### Architecture Diagram

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│   LB    │────▶│ Service │────▶│   DB    │
└─────────┘     └─────────┘     └─────────┘
                     │
                     ▼
                ┌─────────┐
                │  Cache  │
                └─────────┘
```

## Monitoring

### Key Metrics

| Metric | Normal Range | Alert Threshold | Dashboard |
|--------|--------------|-----------------|-----------|
| Request rate | 100-500 rps | > 1000 rps | [Link] |
| Error rate | < 0.1% | > 1% | [Link] |
| P95 latency | < 200ms | > 500ms | [Link] |
| CPU usage | 20-40% | > 80% | [Link] |
| Memory usage | 40-60% | > 85% | [Link] |

### Alerts

| Alert Name | Severity | Meaning | Initial Response |
|------------|----------|---------|------------------|
| HighErrorRate | P1 | Error rate > 5% | See [High Error Rate](#high-error-rate) |
| HighLatency | P2 | P95 > 1s | See [High Latency](#high-latency) |
| PodCrashLoop | P1 | Pods restarting | See [Pod Crash Loop](#pod-crash-loop) |

## Incident Response

### High Error Rate

**Symptoms:** Error rate exceeds threshold, users report failures

**Immediate Actions:**
1. Check recent deployments: `kubectl rollout history deployment/[service-name]`
2. Review error logs: `kubectl logs -n [namespace] -l app=[service-name] | grep ERROR`
3. Check dependency health (database, cache, external APIs)

**Diagnosis Steps:**

```bash
# Check pod status
kubectl get pods -n [namespace] -l app=[service-name]

# Check recent events
kubectl get events -n [namespace] --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n [namespace] -l app=[service-name]
```

**Common Causes:**
- Cause 1: [Description] → Solution: [Steps]
- Cause 2: [Description] → Solution: [Steps]
- Cause 3: [Description] → Solution: [Steps]

**Escalation:** If unresolved after 15 minutes, escalate to [team/person]

### High Latency

**Symptoms:** Response times exceed SLA, timeouts reported

**Immediate Actions:**
1. Check database query performance
2. Review cache hit rates
3. Check for resource saturation

**Diagnosis Steps:**

```bash
# Check slow queries (if using PostgreSQL)
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

# Check cache stats
redis-cli INFO stats
```

**Common Causes:**
- Database connection exhaustion → Increase pool size or optimize queries
- Cache miss storm → Warm cache, implement circuit breaker
- Resource saturation → Scale horizontally

### Pod Crash Loop

**Symptoms:** Pods continuously restarting, CrashLoopBackOff status

**Immediate Actions:**
1. Get pod status and restart count
2. Check logs from crashed container
3. Review recent config changes

**Diagnosis Steps:**

```bash
# Get detailed pod info
kubectl describe pod [pod-name] -n [namespace]

# Get logs from previous crash
kubectl logs [pod-name] -n [namespace] --previous

# Check resource limits
kubectl get pod [pod-name] -n [namespace] -o yaml | grep -A5 resources
```

**Common Causes:**
- OOM killed → Increase memory limits
- Failed health checks → Fix health endpoint or adjust probe timing
- Missing config/secrets → Verify ConfigMap and Secret mounts

## Operational Procedures

### Deployment

**Pre-deployment Checklist:**
- [ ] All tests passing
- [ ] Changelog updated
- [ ] Rollback plan reviewed
- [ ] Team notified in Slack

**Deployment Steps:**

```bash
# Deploy new version
kubectl set image deployment/[service-name] \
  [container-name]=[new-image:tag] \
  -n [namespace]

# Monitor rollout
kubectl rollout status deployment/[service-name] -n [namespace]

# Verify health
curl -s https://[service-url]/health | jq .
```

**Rollback:**

```bash
# Rollback to previous version
kubectl rollout undo deployment/[service-name] -n [namespace]

# Rollback to specific revision
kubectl rollout undo deployment/[service-name] --to-revision=[N] -n [namespace]
```

### Scaling

**Horizontal Scaling:**

```bash
# Scale replicas
kubectl scale deployment/[service-name] --replicas=[N] -n [namespace]

# Autoscaling (if HPA configured)
kubectl get hpa -n [namespace]
```

**When to Scale:**
- CPU > 70% sustained for 5+ minutes
- Request queue building up
- Anticipating traffic spike (scheduled events)

### Database Maintenance

**Read Replica Promotion:**

```bash
# Steps for promoting read replica to primary
# 1. Stop writes to application
# 2. Promote replica
# 3. Update connection strings
# 4. Resume writes
```

**Backup Verification:**

```bash
# List recent backups
aws s3 ls s3://[bucket]/backups/ --recursive | tail -5

# Restore test (to non-prod)
# [Restore commands specific to your database]
```

## Maintenance Windows

| Window | Schedule | Duration | Impact |
|--------|----------|----------|--------|
| Patch updates | Sunday 02:00-04:00 UTC | 2 hours | Brief restarts |
| Database maintenance | First Sunday monthly | 4 hours | Read-only mode |

## Contacts

| Role | Name | Contact |
|------|------|---------|
| Service Owner | [Name] | @slack-handle |
| Database Admin | [Name] | @slack-handle |
| Platform Team | [Team] | #platform-oncall |

## See Also

- [Architecture Documentation](./architecture.md)
- [API Documentation](./api-reference.md)
- [Incident Postmortems](./postmortems/)
