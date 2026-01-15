# Collaboration Flags

When requirements reveal complexity beyond TPO scope, flag for human consultation. These flags recommend bringing in expertise - they don't auto-chain to other roles.

## Flag Format

```
⚠️ [FLAG TYPE]
Requirement: [The specific requirement that raised concern]
Concern: [Why this needs additional expertise]
Recommend consulting: [Role/person to consult]
Questions to resolve:
- [Specific question 1]
- [Specific question 2]
```

---

## Technical Feasibility Flag

**Recommend consulting: Solutions Architect**

### When to Trigger

- Performance requirements seem aggressive for the data model
- Complex data relationships or aggregations
- Real-time or streaming requirements
- Integration with unknown or undocumented systems
- Cryptographic or security-sensitive logic
- Unclear infrastructure requirements
- Data migration complexity
- API contract ambiguity

### Example Triggers and Flags

#### Aggressive Performance
```
⚠️ TECHNICAL FEASIBILITY FLAG
Requirement: "Search must return results in under 100ms for 10M+ records"
Concern: Sub-100ms search on large dataset may require specialized indexing, caching, or search infrastructure beyond standard RDBMS
Recommend consulting: Solutions Architect
Questions to resolve:
- Is Elasticsearch/Typesense needed vs PostgreSQL full-text search?
- What's the acceptable indexing delay for new records?
- Can we scope down the searchable dataset (e.g., last 2 years)?
```

#### Complex Data Flow
```
⚠️ TECHNICAL FEASIBILITY FLAG
Requirement: "Dashboard shows real-time aggregate metrics across all user projects"
Concern: Real-time aggregation across large datasets can be expensive; may need pre-computed views, streaming aggregation, or materialized views
Recommend consulting: Solutions Architect
Questions to resolve:
- What's acceptable staleness for "real-time" (1s? 1min? 5min)?
- Expected data volume and growth rate?
- Can we use incremental computation vs full recalculation?
```

#### Unknown Integration
```
⚠️ TECHNICAL FEASIBILITY FLAG
Requirement: "Sync data bidirectionally with customer's Salesforce instance"
Concern: Salesforce integration complexity varies widely; API limits, data model mapping, and conflict resolution patterns unclear
Recommend consulting: Solutions Architect
Questions to resolve:
- Which Salesforce API (REST, Bulk, Streaming)?
- What's the expected sync volume and frequency?
- How are conflicts resolved (our system wins, Salesforce wins, manual)?
- Is there existing Salesforce integration code to reference?
```

#### Security-Sensitive
```
⚠️ TECHNICAL FEASIBILITY FLAG
Requirement: "Support SSO via customer's identity provider"
Concern: SSO integration (SAML, OIDC) has security implications and varies by provider
Recommend consulting: Solutions Architect + Security
Questions to resolve:
- Which protocols must we support (SAML 2.0, OIDC, both)?
- Do we need to support multiple IdPs per customer?
- How is provisioning/deprovisioning handled (SCIM, JIT)?
```

---

## UX Ambiguity Flag

**Recommend consulting: UX Designer**

### When to Trigger

- User flow has multiple valid interpretations
- Error state presentation unclear
- Empty state needs design guidance
- Accessibility approach uncertain
- Complex form interaction patterns
- Mobile vs desktop experience differs significantly
- Progressive disclosure / wizard vs single page unclear
- Competing user mental models

### Example Triggers and Flags

#### Ambiguous Flow
```
⚠️ UX AMBIGUITY FLAG
Requirement: "User can configure notification preferences"
Concern: Unclear if this is per-notification-type granular control, category-based, or simple on/off; affects complexity significantly
Recommend consulting: UX Designer
Questions to resolve:
- What level of granularity do users actually need?
- Is this a full settings page or inline toggles?
- How do defaults work for new notification types?
```

#### Error State Design
```
⚠️ UX AMBIGUITY FLAG
Requirement: "Handle payment failures gracefully"
Concern: Payment failures have multiple causes (card declined, expired, fraud hold) with different recovery paths; error messaging and flow needs design
Recommend consulting: UX Designer
Questions to resolve:
- How do we differentiate "retry same card" vs "use different card" scenarios?
- Inline retry vs redirect to payment settings?
- How much error detail is helpful vs confusing?
```

#### Mobile Experience
```
⚠️ UX AMBIGUITY FLAG
Requirement: "Support data table with 15 columns on mobile"
Concern: 15-column table cannot render meaningfully on mobile; needs alternative presentation strategy
Recommend consulting: UX Designer
Questions to resolve:
- Which columns are essential on mobile?
- Card view, horizontal scroll, or collapsible rows?
- Should mobile have different default columns than desktop?
```

#### Complex Wizard
```
⚠️ UX AMBIGUITY FLAG
Requirement: "Onboarding flow collects company info, team setup, and integrations"
Concern: Multi-step wizard with conditional paths needs careful sequencing and progress communication
Recommend consulting: UX Designer
Questions to resolve:
- Which steps are required vs skippable?
- Can users go back and edit previous steps?
- How do we handle partial completion / save-and-continue-later?
```

---

## Scope/Timeline Flag

**Recommend consulting: Technical Program Manager**

### When to Trigger

- Feature seems large for stated timeline
- Dependencies create scheduling risk
- Multiple teams need coordination
- Scope creep risk is high
- Unclear what's MVP vs nice-to-have
- Feature has multiple valid phasing strategies
- External deadlines create pressure

### Example Triggers and Flags

#### Scope vs Timeline Mismatch
```
⚠️ SCOPE/TIMELINE FLAG
Requirement: "Full audit logging with retention, search, export, and compliance reports - needed in 2 weeks"
Concern: Comprehensive audit system typically requires 4-6 weeks; 2-week timeline suggests scope reduction needed
Recommend consulting: Technical Program Manager
Questions to resolve:
- What's the hard deadline driver (compliance audit, customer contract)?
- Can we phase: basic logging now, search/export in phase 2?
- Which compliance requirements are non-negotiable for launch?
```

#### Multi-Team Dependency
```
⚠️ SCOPE/TIMELINE FLAG
Requirement: "Integrate with billing system for usage-based pricing"
Concern: Billing integration requires coordination with Billing team, Finance for pricing rules, and potentially Legal for contract changes
Recommend consulting: Technical Program Manager
Questions to resolve:
- What's Billing team's availability and sprint commitments?
- Is pricing model finalized or still in flux?
- Can we launch with manual billing reconciliation as stopgap?
```

#### Phasing Strategy Needed
```
⚠️ SCOPE/TIMELINE FLAG
Requirement: "Support for custom fields on all entity types"
Concern: Custom fields across all entities is a platform-level feature; phased rollout likely needed
Recommend consulting: Technical Program Manager
Questions to resolve:
- Which entity types are highest priority for customers?
- Can we launch with 1-2 entity types and expand?
- Is there a customer commitment driving this timeline?
```

#### External Deadline
```
⚠️ SCOPE/TIMELINE FLAG
Requirement: "Feature must launch before industry conference on [date]"
Concern: Conference-driven deadline is fixed; need to right-size scope to achievable target
Recommend consulting: Technical Program Manager
Questions to resolve:
- What's the minimum viable demo for the conference?
- What can be "coming soon" vs fully functional?
- What's the risk/cost of missing the conference deadline?
```

---

## Data/Privacy Flag

**Recommend consulting: Data Platform Engineer**

### When to Trigger

- PII handling involved
- Data retention policies apply
- Cross-system data flow
- Analytics/reporting requirements
- Data model has AI/ML implications
- GDPR/CCPA/HIPAA considerations
- Data migration needed
- Third-party data sharing

### Example Triggers and Flags

#### PII Handling
```
⚠️ DATA/PRIVACY FLAG
Requirement: "Store customer's government ID for verification"
Concern: Government ID is sensitive PII with specific storage, encryption, access logging, and retention requirements
Recommend consulting: Data Platform Engineer + Legal/Compliance
Questions to resolve:
- What's the minimum data needed (full ID vs hash vs verification status only)?
- Retention requirements (delete after verification? Audit trail needs)?
- Encryption at rest requirements?
- Who can access this data and how is access logged?
```

#### Cross-System Data Flow
```
⚠️ DATA/PRIVACY FLAG
Requirement: "Sync user activity data to analytics warehouse for reporting"
Concern: Moving user data to warehouse requires PII handling decisions, consent considerations, and retention alignment
Recommend consulting: Data Platform Engineer
Questions to resolve:
- Which fields should be anonymized/pseudonymized?
- How do user data deletion requests propagate to warehouse?
- What's the data freshness requirement (real-time, daily, weekly)?
```

#### Data for AI/ML
```
⚠️ DATA/PRIVACY FLAG
Requirement: "Use historical user behavior to power recommendations"
Concern: Training data needs proper anonymization, consent framework, and model governance
Recommend consulting: Data Platform Engineer + AI Integration Engineer
Questions to resolve:
- What user consent is needed for behavior-based recommendations?
- How is training data separated from production PII?
- How do we handle users who opt out of personalization?
```

#### Compliance Requirements
```
⚠️ DATA/PRIVACY FLAG
Requirement: "Support GDPR data export and deletion requests"
Concern: GDPR compliance requires systematic data inventory, deletion cascades, and audit trails
Recommend consulting: Data Platform Engineer + Legal
Questions to resolve:
- Do we have a complete inventory of where user data lives?
- What's the SLA for deletion requests (GDPR allows 30 days)?
- How do we handle data in backups and analytics systems?
```

---

## Multiple Flags

Complex requirements may trigger multiple flags. List all that apply:

```
⚠️ TECHNICAL FEASIBILITY FLAG
Requirement: "Real-time collaborative document editing"
Concern: Real-time collaboration requires WebSocket infrastructure, operational transforms or CRDTs, and conflict resolution
Recommend consulting: Solutions Architect
Questions to resolve:
- OT vs CRDT approach?
- Existing infrastructure for WebSockets?
- Expected concurrent editor count?

⚠️ UX AMBIGUITY FLAG  
Requirement: "Real-time collaborative document editing"
Concern: Collaboration UX (cursors, selections, presence, conflict UI) needs design
Recommend consulting: UX Designer
Questions to resolve:
- How do we show other users' presence and cursors?
- How are conflicting edits communicated?
- What happens when users edit offline?

⚠️ SCOPE/TIMELINE FLAG
Requirement: "Real-time collaborative document editing"
Concern: Collaboration is a major feature typically requiring 2-3 months; may need phasing
Recommend consulting: Technical Program Manager
Questions to resolve:
- Is view-only sharing acceptable for MVP?
- Can we launch with turn-based editing (lock-based) first?
- What's the minimum collaboration feature set?
```
