---
title: "ADR-[NUMBER]: [Decision Title]"
doc_type: architecture
version: "1.0.0"
status: draft
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
author: ""
reviewers: []
related_docs: []
tags: [adr, architecture]
---

# ADR-[NUMBER]: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context

Describe the issue motivating this decision. What is the problem we are trying to solve? Include relevant constraints, requirements, and forces at play.

Key questions to answer:
- What is the current state?
- What problem are we solving?
- What are the constraints?
- Who are the stakeholders?

## Decision Drivers

- Driver 1: [e.g., performance requirements]
- Driver 2: [e.g., team expertise]
- Driver 3: [e.g., cost constraints]
- Driver 4: [e.g., time to market]

## Considered Options

### Option 1: [Name]

Brief description of this option.

**Pros:**
- Advantage 1
- Advantage 2

**Cons:**
- Disadvantage 1
- Disadvantage 2

**Estimated effort:** [Low | Medium | High]

### Option 2: [Name]

Brief description of this option.

**Pros:**
- Advantage 1
- Advantage 2

**Cons:**
- Disadvantage 1
- Disadvantage 2

**Estimated effort:** [Low | Medium | High]

### Option 3: [Name]

Brief description of this option.

**Pros:**
- Advantage 1
- Advantage 2

**Cons:**
- Disadvantage 1
- Disadvantage 2

**Estimated effort:** [Low | Medium | High]

## Decision

We will implement **Option X: [Name]**.

### Rationale

Explain why this option was chosen over the alternatives. Reference the decision drivers and explain how this option best addresses them.

## Consequences

### Positive

- Benefit 1: Explanation
- Benefit 2: Explanation
- Benefit 3: Explanation

### Negative

- Tradeoff 1: Explanation and mitigation strategy
- Tradeoff 2: Explanation and mitigation strategy

### Neutral

- Side effect 1: Explanation
- Side effect 2: Explanation

## Implementation

### High-Level Approach

Outline the implementation strategy:

1. Phase 1: [Description]
2. Phase 2: [Description]
3. Phase 3: [Description]

### Technical Details

Include relevant technical details, diagrams, or code snippets:

```
┌─────────────┐     ┌─────────────┐
│ Component A │────▶│ Component B │
└─────────────┘     └─────────────┘
```

### Migration Plan

If replacing existing functionality:

1. Step 1: [Migration step]
2. Step 2: [Migration step]
3. Step 3: [Migration step]

**Rollback strategy:** Describe how to revert if needed

### Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Design review | YYYY-MM-DD | |
| Implementation start | YYYY-MM-DD | |
| Testing complete | YYYY-MM-DD | |
| Production rollout | YYYY-MM-DD | |

## Validation

### Success Metrics

How will we know this decision was successful?

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Metric 1 | X | Y | How to measure |
| Metric 2 | X | Y | How to measure |

### Review Schedule

- Initial review: [date] - Assess early implementation
- Mid-point review: [date] - Evaluate progress
- Final review: [date] - Measure against success criteria

## References

- [Link to relevant documentation]
- [Link to related ADRs]
- [Link to external resources]

## Changelog

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | [Name] | Initial draft |
| YYYY-MM-DD | [Name] | Updated after review |
