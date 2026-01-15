---
title: "[Feature/Component] Testing Approach"
doc_type: testing
version: "1.0.0"
status: draft
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
author: ""
reviewers: []
related_docs: []
tags: [testing, qa]
---

# [Feature/Component] Testing Approach

This document outlines the testing strategy for [feature/component name].

## Overview

Brief description of what is being tested and the testing objectives.

### Scope

**In Scope:**
- Component/feature 1
- Component/feature 2
- Integration point 1

**Out of Scope:**
- Component handled by other tests
- Third-party service internals

### Testing Objectives

1. Verify [specific functionality]
2. Ensure [quality attribute] meets requirements
3. Validate [integration behavior]

## Test Levels

### Unit Tests

Unit tests verify individual functions and methods in isolation.

**Coverage Target:** 80%+ line coverage

**Key Areas:**
- Business logic functions
- Data transformation utilities
- Validation functions

**Example:**

```javascript
describe('calculateTotal', () => {
  it('should sum items correctly', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle negative values', () => {
    const items = [{ price: 10 }, { price: -5 }];
    expect(calculateTotal(items)).toBe(5);
  });
});
```

### Integration Tests

Integration tests verify component interactions and API contracts.

**Key Scenarios:**

| Scenario | Components | Expected Outcome |
|----------|------------|------------------|
| Create flow | API + DB | Record persisted correctly |
| Update flow | API + Cache + DB | Cache invalidated, DB updated |
| Delete flow | API + Queue + DB | Event published, record removed |

**Example:**

```javascript
describe('POST /api/orders', () => {
  it('should create order and publish event', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ items: [{ id: 1, qty: 2 }] });

    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();

    // Verify side effects
    const order = await db.orders.findById(response.body.id);
    expect(order).toBeDefined();

    const events = await queue.getMessages('orders');
    expect(events).toContainEqual(
      expect.objectContaining({ type: 'order.created' })
    );
  });
});
```

### End-to-End Tests

E2E tests verify complete user workflows.

**Critical Paths:**

1. **User Registration Flow**
   - Navigate to signup
   - Fill registration form
   - Verify email confirmation
   - Complete profile setup

2. **Purchase Flow**
   - Browse products
   - Add to cart
   - Checkout
   - Verify order confirmation

**Test Data Requirements:**
- Test user accounts
- Sample product catalog
- Mock payment credentials

## Test Data Strategy

### Test Data Sources

| Environment | Data Source | Refresh Frequency |
|-------------|-------------|-------------------|
| Local | SQLite seed | Per test run |
| CI | Docker containers | Per pipeline |
| Staging | Anonymized prod | Weekly |

### Data Factories

```javascript
// factories/user.factory.js
const createUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  email: faker.internet.email(),
  name: faker.name.fullName(),
  createdAt: new Date(),
  ...overrides,
});
```

### Sensitive Data Handling

- Never use real PII in tests
- Use faker/chance for generated data
- Mask sensitive fields in logs

## Test Environments

| Environment | Purpose | Data | External Services |
|-------------|---------|------|-------------------|
| Local | Development | Mocked | Mocked |
| CI | Automated tests | Seeded | Stubbed |
| Staging | Pre-production | Anonymized | Sandbox |

### Environment Setup

```bash
# Local environment
docker-compose up -d
npm run db:seed
npm test

# CI environment
# Handled by CI pipeline (see .github/workflows/test.yml)
```

## Mocking Strategy

### External Service Mocks

```javascript
// Mock payment service
jest.mock('../services/payment', () => ({
  processPayment: jest.fn().mockResolvedValue({
    transactionId: 'mock_txn_123',
    status: 'completed',
  }),
}));
```

### API Mocks (MSW)

```javascript
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/external/users/:id', (req, res, ctx) => {
    return res(
      ctx.json({
        id: req.params.id,
        name: 'Test User',
      })
    );
  }),
];
```

## Performance Testing

### Load Test Scenarios

| Scenario | Users | Duration | Target Response Time |
|----------|-------|----------|---------------------|
| Normal load | 100 | 10 min | < 200ms (p95) |
| Peak load | 500 | 5 min | < 500ms (p95) |
| Stress test | 1000 | 2 min | < 1s (p95) |

### Performance Benchmarks

```javascript
// Example k6 script
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 100,
  duration: '10m',
};

export default function () {
  const res = http.get('https://api.example.com/endpoint');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
}
```

## Test Execution

### Running Tests

```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# With coverage
npm run test:coverage
```

### CI Pipeline Integration

Tests run automatically on:
- Pull request creation/update
- Merge to main branch
- Nightly scheduled runs

### Test Reports

Reports are generated in:
- `coverage/` - Code coverage (HTML, lcov)
- `reports/` - Test results (JUnit XML)

## Defect Tracking

### Bug Report Template

When a test fails, create a bug report with:
- Test name and file
- Expected vs actual behavior
- Steps to reproduce
- Environment details
- Relevant logs/screenshots

### Flaky Test Policy

1. Mark flaky tests with `@flaky` tag
2. Create ticket to investigate
3. Fix within 1 sprint or skip
4. Never ignore without tracking

## See Also

- [Development Guidelines](./development-guidelines.md)
- [CI/CD Pipeline](./cicd-pipeline.md)
- [Quality Standards](./quality-standards.md)
