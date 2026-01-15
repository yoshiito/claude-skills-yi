# Architecture Decision Record Template

Comprehensive template for documenting technical decisions.

## ADR Format

```markdown
# ADR-[XXX]: [Short Title]

**Date**: [YYYY-MM-DD]
**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Deciders**: [List of people involved in decision]
**Technical Story**: [Link to MRD, ticket, or feature]

## Context

[Describe the situation that requires a decision. Include:
- What problem are we trying to solve?
- What constraints exist?
- What forces are at play?
Be factual and neutral - don't advocate for a solution yet.]

## Decision Drivers

- [Driver 1: e.g., "Must support 10K concurrent users"]
- [Driver 2: e.g., "Team has no experience with technology X"]
- [Driver 3: e.g., "Budget constraint of $X/month"]
- [Driver 4: e.g., "Must integrate with existing system Y"]

## Considered Options

### Option 1: [Name]
[Brief description]

### Option 2: [Name]
[Brief description]

### Option 3: [Name]
[Brief description]

## Decision

[State the decision clearly. Use active voice: "We will use X for Y."]

## Rationale

[Explain why this option was chosen. Reference the decision drivers. Address why other options were not selected.]

## Consequences

### Positive
- [Good outcome 1]
- [Good outcome 2]

### Negative
- [Trade-off or downside 1]
- [Trade-off or downside 2]

### Neutral
- [Side effect that's neither good nor bad]

## Implementation Notes

[Any specific guidance for implementing this decision]

## Related Decisions

- [ADR-XXX: Related decision]
- [ADR-YYY: Superseded decision]

## References

- [Link to relevant documentation]
- [Link to proof of concept]
- [Link to external resources]
```

---

## ADR Examples

### Example 1: Database Selection

```markdown
# ADR-001: PostgreSQL for Primary Data Store

**Date**: 2025-01-15
**Status**: Accepted
**Deciders**: Tech Lead, Solutions Architect, Backend Lead
**Technical Story**: MRD-042 User Management System

## Context

We need a primary data store for our user management system. The system will handle user profiles, authentication data, team memberships, and activity logs. Expected scale is 100K users within the first year, growing to 1M within three years.

## Decision Drivers

- Must support ACID transactions for user and billing data
- Team has strong SQL/relational database experience
- Need good tooling and ORM support for Python/FastAPI stack
- Budget-conscious: prefer open source with managed options available
- Must support full-text search for user directory

## Considered Options

### Option 1: PostgreSQL
Mature relational database with strong ecosystem.

### Option 2: MySQL
Popular relational database, widely used.

### Option 3: MongoDB
Document database with flexible schema.

## Decision

We will use PostgreSQL as our primary data store, deployed on Railway with the option to migrate to AWS RDS for production scaling.

## Rationale

PostgreSQL was selected because:
1. **ACID compliance** meets our requirement for transactional integrity
2. **Team expertise** - all backend engineers have PostgreSQL experience
3. **SQLModel/SQLAlchemy support** - excellent ORM integration with our FastAPI stack
4. **Full-text search** - built-in FTS eliminates need for separate search service initially
5. **pgvector extension** - provides path to vector search for future AI features
6. **Cost effective** - open source with multiple managed hosting options

MySQL was not selected because PostgreSQL's JSON support and extension ecosystem (pgvector, PostGIS) offer more flexibility for future features.

MongoDB was not selected because our data model is inherently relational (users, teams, memberships) and the team lacks NoSQL experience.

## Consequences

### Positive
- Leverages existing team expertise
- Strong consistency guarantees
- Single database handles relational data + search + vectors
- Mature tooling and debugging support

### Negative
- Vertical scaling limits before sharding needed
- Schema migrations require careful planning
- Less flexibility for unstructured data

### Neutral
- Will need to implement connection pooling for high concurrency

## Implementation Notes

- Use SQLModel for ORM (Pydantic integration)
- Enable pgvector extension from start even if not immediately used
- Set up connection pooling with PgBouncer at >50 concurrent connections
- Use JSONB columns for flexible metadata fields

## Related Decisions

- ADR-005: Caching Strategy (addresses read scaling)
- ADR-008: Search Architecture (may revisit if FTS insufficient)
```

### Example 2: Authentication Strategy

```markdown
# ADR-002: JWT with Refresh Tokens for API Authentication

**Date**: 2025-01-15
**Status**: Accepted
**Deciders**: Solutions Architect, Security Lead, Backend Lead
**Technical Story**: MRD-042 User Management System

## Context

We need an authentication mechanism for our API. The API will be consumed by our web frontend (SPA), mobile apps (future), and potentially third-party integrations. We need to balance security, user experience (avoiding frequent re-logins), and implementation complexity.

## Decision Drivers

- Must support stateless API servers for horizontal scaling
- Must work across web and mobile clients
- Session duration: users should stay logged in for reasonable periods
- Must be revocable in case of security incident
- Team has experience with JWT

## Considered Options

### Option 1: JWT with Refresh Tokens
Short-lived access tokens + longer-lived refresh tokens.

### Option 2: Session-based with Redis
Server-side sessions stored in Redis.

### Option 3: JWT Only (Long-lived)
Single long-lived JWT token.

## Decision

We will use JWT with refresh tokens:
- Access token: 15 minutes expiry, contains user ID and roles
- Refresh token: 7 days expiry, stored in database, rotated on use

## Rationale

JWT with refresh tokens was selected because:
1. **Stateless access tokens** enable horizontal scaling without shared session store
2. **Short access token lifetime** limits exposure window if token is compromised
3. **Database-backed refresh tokens** enable revocation for security incidents
4. **Refresh token rotation** detects token theft (reuse of old token)
5. **Works across platforms** - same mechanism for web and mobile

Session-based was not selected because it requires shared state (Redis) and complicates horizontal scaling, though it would be simpler to implement.

Long-lived JWT was not selected because tokens cannot be revoked and long lifetime increases risk if compromised.

## Consequences

### Positive
- Horizontal scaling without session store
- Tokens can be revoked via refresh token invalidation
- Standard approach with good library support
- Works for both web and mobile clients

### Negative
- More complex than simple sessions
- Access token valid until expiry even if user logged out (mitigated by short expiry)
- Must handle token refresh flow in all clients

### Neutral
- Refresh tokens require database storage (small table)

## Implementation Notes

- Store refresh tokens in `refresh_tokens` table with user_id, token_hash, expires_at, revoked_at
- Implement token rotation: issue new refresh token on each refresh, invalidate old one
- Access token payload: `{sub: user_id, roles: [], exp: timestamp}`
- Use secure, httpOnly cookies for web; secure storage for mobile
- Implement /auth/logout that revokes all refresh tokens for user

## Related Decisions

- ADR-003: Authorization Model (RBAC)
```

### Example 3: Async Communication

```markdown
# ADR-003: Redis Pub/Sub for Internal Events

**Date**: 2025-01-16
**Status**: Accepted
**Deciders**: Solutions Architect, Backend Lead
**Technical Story**: MRD-045 Notification System

## Context

We need a mechanism for internal service communication. When certain events occur (user signup, payment completed, etc.), multiple services need to react (send email, update analytics, trigger workflows). Currently all services are in a monolith, but we want to prepare for future service extraction.

## Decision Drivers

- Low latency for time-sensitive notifications
- At-least-once delivery for critical events
- Simple operational model (small team)
- Budget-conscious
- Must work with existing Railway infrastructure

## Considered Options

### Option 1: Redis Pub/Sub
Simple publish/subscribe using existing Redis instance.

### Option 2: RabbitMQ
Dedicated message broker with queuing.

### Option 3: Kafka
Distributed event streaming platform.

### Option 4: PostgreSQL LISTEN/NOTIFY
Database-native pub/sub.

## Decision

We will use Redis Pub/Sub for internal event communication, with a wrapper that persists events to PostgreSQL for reliability.

## Rationale

Redis Pub/Sub was selected because:
1. **Already deployed** - we have Redis for caching, no new infrastructure
2. **Low latency** - in-memory pub/sub is fast
3. **Simple** - minimal configuration, easy to debug
4. **Sufficient for current scale** - works well for our volume

The PostgreSQL persistence layer addresses Redis Pub/Sub's lack of durability:
- Events written to `events` table before publishing
- Background worker retries failed deliveries
- Provides audit trail

RabbitMQ/Kafka not selected because operational complexity outweighs benefits at our current scale. We can migrate if volume requires it.

PostgreSQL NOTIFY alone not selected because it doesn't scale as well for high-frequency events.

## Consequences

### Positive
- No new infrastructure to manage
- Low latency event delivery
- Simple debugging (Redis CLI)
- PostgreSQL backup provides durability

### Negative
- Redis Pub/Sub doesn't persist messages (mitigated by DB layer)
- Must build reliability wrapper ourselves
- Will need to migrate to dedicated broker at higher scale

### Neutral
- Events table will grow (need retention policy)

## Implementation Notes

```python
# Event flow:
# 1. Write event to PostgreSQL events table (status: pending)
# 2. Publish to Redis channel
# 3. Subscriber processes event
# 4. Subscriber marks event as processed in DB
# 5. Background worker retries pending events older than 5 minutes
```

Event schema:
- id, event_type, payload (JSONB), status, created_at, processed_at, retry_count

## Related Decisions

- ADR-007: Event Schema Standards
- Future: ADR for message broker migration when volume exceeds 10K events/minute
```

---

## ADR Lifecycle

### Statuses

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion, not yet decided |
| **Accepted** | Decision made, should be followed |
| **Deprecated** | No longer recommended, but not replaced |
| **Superseded** | Replaced by a newer ADR |

### When to Update an ADR

- **Never modify accepted ADRs** (they're historical records)
- **Create new ADR** that supersedes the old one
- **Update status** of old ADR to "Superseded by ADR-XXX"

### ADR Numbering

- Sequential: ADR-001, ADR-002, ADR-003
- Include leading zeros for sorting
- Never reuse numbers

---

## Quick ADR (Lightweight)

For smaller decisions, use abbreviated format:

```markdown
# ADR-XXX: [Title]

**Status**: Accepted | **Date**: YYYY-MM-DD

## Context
[2-3 sentences]

## Decision
[1-2 sentences]

## Consequences
- [Consequence 1]
- [Consequence 2]
```
