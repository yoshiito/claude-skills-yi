# Release Checklist

Comprehensive readiness gates for production releases.

## Pre-Release Checklist

### Code Complete

**Feature Implementation**
- [ ] All user stories in MRD implemented
- [ ] All acceptance criteria verified
- [ ] All functional rules enforced
- [ ] Edge cases handled per specification

**Code Quality**
- [ ] All code reviews approved
- [ ] No TODO/FIXME/HACK comments remaining (or documented exceptions)
- [ ] Code follows team style guide
- [ ] No commented-out code
- [ ] Logging appropriate (not excessive, sensitive data masked)

**Dependencies**
- [ ] All package dependencies locked (package-lock.json, requirements.txt)
- [ ] No known vulnerable dependencies (npm audit, safety check)
- [ ] License compliance verified for new dependencies

---

### Testing Complete

**Unit Tests**
- [ ] Unit test coverage >80%
- [ ] All unit tests passing
- [ ] Critical paths have >90% coverage
- [ ] Edge cases covered

**Integration Tests**
- [ ] API integration tests passing
- [ ] Database integration tests passing
- [ ] External service integration tests passing (or mocked appropriately)

**End-to-End Tests**
- [ ] Critical user journeys automated and passing
- [ ] Cross-browser testing complete (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive testing complete
- [ ] Happy path scenarios verified
- [ ] Error scenarios verified

**Performance Tests**
- [ ] Load testing complete
- [ ] NFR latency targets met (p50, p95, p99)
- [ ] NFR throughput targets met
- [ ] No memory leaks identified
- [ ] Database query performance acceptable

**Security Tests**
- [ ] OWASP Top 10 vulnerabilities checked
- [ ] Authentication/authorization tested
- [ ] Input validation tested
- [ ] SQL injection tested
- [ ] XSS tested
- [ ] CSRF protection verified
- [ ] Secrets not exposed in code/logs
- [ ] Security scan passed (Snyk, SonarQube, etc.)

**Accessibility Tests**
- [ ] WCAG 2.1 AA compliance verified
- [ ] Screen reader testing complete
- [ ] Keyboard navigation working
- [ ] Color contrast requirements met
- [ ] Focus indicators visible

**Bug Status**
- [ ] No Critical bugs open
- [ ] No High bugs open (or documented exceptions with mitigation)
- [ ] Medium/Low bugs triaged and documented
- [ ] All release-blocking bugs resolved

---

### Documentation Complete

**Technical Documentation**
- [ ] API documentation updated (OpenAPI/Swagger)
- [ ] API changelog updated
- [ ] Database schema documentation current
- [ ] Architecture decision records (ADRs) complete
- [ ] Integration guides updated

**Operational Documentation**
- [ ] Runbook created/updated
  - [ ] Common procedures documented
  - [ ] Troubleshooting steps included
  - [ ] Escalation paths defined
- [ ] Monitoring guide updated
  - [ ] Key metrics identified
  - [ ] Alert thresholds documented
  - [ ] Dashboard locations noted
- [ ] Incident response procedures updated
- [ ] On-call handoff documentation ready

**User Documentation**
- [ ] Feature documentation written
- [ ] User guides/tutorials updated
- [ ] FAQ updated
- [ ] Help center articles created
- [ ] In-app help text finalized

**Release Documentation**
- [ ] Release notes drafted
- [ ] Breaking changes documented
- [ ] Migration guide (if applicable)
- [ ] Known issues documented

---

### Operations Ready

**Infrastructure**
- [ ] Production environment provisioned
- [ ] Environment variables configured
- [ ] Secrets stored securely (vault, AWS Secrets Manager, etc.)
- [ ] SSL certificates valid and not expiring soon
- [ ] DNS configured correctly
- [ ] CDN configured (if applicable)
- [ ] Load balancer configured
- [ ] Auto-scaling configured (if applicable)

**Database**
- [ ] Database migrations tested on staging
- [ ] Database migrations tested on production replica
- [ ] Migration rollback tested
- [ ] Database backup verified
- [ ] Database capacity sufficient
- [ ] Index performance verified

**Monitoring & Alerting**
- [ ] Application metrics configured
- [ ] Business metrics configured
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Log aggregation configured
- [ ] Alerts configured for critical metrics
- [ ] Alert recipients verified
- [ ] Dashboard created/updated
- [ ] SLO/SLA monitoring in place

**Rollback Plan**
- [ ] Rollback procedure documented
- [ ] Rollback tested on staging
- [ ] Rollback time estimated
- [ ] Rollback triggers defined
- [ ] Data rollback plan (if applicable)
- [ ] Feature flags configured for gradual rollout (if applicable)

**Deployment**
- [ ] Deployment pipeline tested
- [ ] Zero-downtime deployment verified (if required)
- [ ] Blue-green or canary deployment ready (if applicable)
- [ ] Deployment runbook updated
- [ ] Deployment schedule confirmed

---

### Approvals Collected

**Required Sign-offs**
- [ ] Product Owner approval
- [ ] Engineering Lead approval
- [ ] QA Lead approval
- [ ] Security approval (if security-relevant changes)
- [ ] Legal approval (if legal/compliance-relevant)
- [ ] Privacy/DPO approval (if PII changes)
- [ ] Operations/SRE approval

**Stakeholder Notification**
- [ ] Customer Success notified
- [ ] Support team notified and trained
- [ ] Marketing notified (if public launch)
- [ ] Sales notified (if affects sales process)

---

## Go/No-Go Meeting

### Agenda

```
1. Readiness Review (15 min)
   - Code status
   - Testing status
   - Documentation status
   - Operations status
   - Approvals status

2. Open Risks (10 min)
   - Outstanding risks
   - Mitigation plans

3. Rollback Readiness (5 min)
   - Rollback plan review
   - Rollback triggers

4. Decision (5 min)
   - Go / No-Go / Conditional Go

5. Launch Plan (if Go) (10 min)
   - Deployment time
   - Monitoring assignments
   - Communication plan
```

### Go/No-Go Decision Record

```markdown
# Go/No-Go Decision

**Release**: [Name] v[Version]
**Date**: [Date]
**Decision**: [GO / NO-GO / CONDITIONAL GO]

## Attendees
| Name | Role | Vote |
|------|------|------|
| [Name] | [Role] | [Go/No-Go/Abstain] |

## Readiness Summary
| Area | Status | Notes |
|------|--------|-------|
| Code | [🟢/🟡/🔴] | [Notes] |
| Testing | [🟢/🟡/🔴] | [Notes] |
| Documentation | [🟢/🟡/🔴] | [Notes] |
| Operations | [🟢/🟡/🔴] | [Notes] |
| Approvals | [🟢/🟡/🔴] | [Notes] |

## Open Risks Accepted
| Risk | Mitigation | Accepted By |
|------|------------|-------------|
| [Risk] | [Mitigation] | [Name] |

## Conditions (if Conditional Go)
- [ ] [Condition 1] - Must be met by [Date/Time]
- [ ] [Condition 2] - Must be met by [Date/Time]

## Rollback Triggers
- [Condition 1 that triggers rollback]
- [Condition 2 that triggers rollback]

## Launch Plan
- **Deployment Time**: [Date/Time]
- **Deployer**: [Name]
- **Monitor**: [Name]
- **Rollback Authority**: [Name]
```

---

## Post-Release Checklist

### Immediate (0-1 hour)

- [ ] Deployment completed successfully
- [ ] Smoke tests passing
- [ ] No critical alerts firing
- [ ] Key metrics within normal range
- [ ] No error rate spike
- [ ] Spot check critical user flows

### Short-term (1-24 hours)

- [ ] Error rates stable
- [ ] Performance metrics stable
- [ ] User feedback monitored
- [ ] Support ticket volume normal
- [ ] No rollback triggered
- [ ] Release notes published
- [ ] Stakeholders notified of successful launch

### Follow-up (24-72 hours)

- [ ] Retrospective scheduled
- [ ] Metrics review complete
- [ ] Any hotfixes deployed
- [ ] Documentation gaps identified and addressed
- [ ] Lessons learned documented
- [ ] Success metrics tracking confirmed

---

## Rollback Procedure

### When to Rollback

**Automatic Rollback Triggers**:
- Error rate > [X]% for > [Y] minutes
- p99 latency > [X]ms for > [Y] minutes
- Critical business metric drops > [X]%

**Manual Rollback Triggers**:
- Data corruption detected
- Security vulnerability discovered
- Critical functionality broken
- Customer-impacting bug with no quick fix

### Rollback Steps

```markdown
1. **Announce**: Post in #incidents: "Initiating rollback of [release]"
2. **Confirm**: Get verbal approval from [rollback authority]
3. **Execute**: Run rollback procedure
   - [ ] Revert deployment to previous version
   - [ ] Revert database migrations (if applicable)
   - [ ] Clear caches (if applicable)
   - [ ] Verify rollback complete
4. **Validate**: 
   - [ ] Smoke tests passing
   - [ ] Error rates returning to normal
   - [ ] Key flows working
5. **Communicate**:
   - [ ] Update #incidents with status
   - [ ] Notify stakeholders
   - [ ] Create incident ticket
6. **Post-mortem**: Schedule within 48 hours
```

### Rollback Communication Template

```markdown
🚨 **Release Rollback Notice**

**Release**: [Name] v[Version]
**Rollback Time**: [Time]
**Rollback Reason**: [Brief reason]

**Impact**:
- [What users experienced]
- [Duration of impact]

**Current Status**:
- System restored to previous version
- Monitoring shows [normal/stabilizing]

**Next Steps**:
- Root cause analysis in progress
- Fix ETA: [TBD / Date]
- Post-mortem scheduled: [Date]

**Questions**: Contact [Name] in #[channel]
```
