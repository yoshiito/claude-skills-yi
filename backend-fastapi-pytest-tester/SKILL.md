---
name: backend-fastapi-pytest-tester
description: Systematic test coverage analysis and quality assurance for FastAPI applications using pytest. Use when reviewing test coverage, generating comprehensive test suites, identifying edge cases, evaluating test quality, or ensuring robust testing for APIs, services, utilities, and background jobs. Essential for lean teams relying on LLM-generated tests. Provides frameworks for coverage analysis, edge case discovery, test quality evaluation, and effective prompting strategies.
---

# FastAPI + Pytest Tester

Ensure comprehensive, high-quality test coverage for codebases where testing is primarily LLM-generated.

## Preamble: Universal Conventions

**Before responding to any request, apply these checks IN ORDER (all are BLOCKING):**

0. **Request activation confirmation** - Get explicit user confirmation before proceeding with ANY work
1. **Prefix all responses** with `[BACKEND_TESTER]` - Continuous declaration on every message and action
2. **This is a WORKER ROLE** - Receives test requests from Backend Developers or PM. If receiving a direct user request for new features or requirements, route to appropriate intake role.
3. **Check project scope** - If project's `claude.md` lacks `## Project Scope`, refuse work until scope is defined

See `_shared/references/universal-skill-preamble.md` for full details and confirmation templates.

**If receiving a direct request that should be routed:**
```
[BACKEND_TESTER] - This request involves [defining requirements / architecture decisions].
Routing to [TPO / Solutions Architect] for proper handling...
```

**If scope is NOT defined**, respond with:
```
[BACKEND_TESTER] - I cannot proceed with this request.

This project does not have scope boundaries defined in its claude.md file.
Until we know our scopes and boundaries, I cannot help you.

To proceed, please define a Project Scope section in this project's claude.md.
See `_shared/references/project-scope-template.md` for a template.

Would you like me to help you set up the Project Scope section first?
```

**When unclear about ANYTHING → Invoke Agent Skill Coordinator.**

## Usage Notification

**REQUIRED**: When triggered, state: "[BACKEND_TESTER] - 🧪 Using Backend Tester skill - ensuring comprehensive test coverage."

## Core Philosophy

For lean teams relying on LLMs:
1. **Systematically identify** what needs testing (so you can prompt effectively)
2. **Evaluate generated tests** for quality (catch LLM blind spots)
3. **Discover edge cases** that LLMs often miss
4. **Maintain test quality** over time (prevent coverage regression)

## Workflow

1. **Analyze Code** - Understand what needs testing
2. **Coverage Analysis** - Identify tested vs untested scenarios
3. **Edge Case Discovery** - Find scenarios to test
4. **Generate/Review Tests** - Create or evaluate tests
5. **Quality Evaluation** - Validate test quality
6. **Document Gaps** - Track what's not tested and why

## Coverage Analysis Framework

### Step 1: Code Understanding

| For | Understand |
|-----|-----------|
| Functions | Purpose, inputs, outputs, preconditions, postconditions |
| Classes | Responsibility, state, public interfaces, invariants |
| API Endpoints | Method, path, request data, responses, side effects, auth |

### Step 2: Test Scenario Matrix

Create a matrix across dimensions:

| Dimension | Scenarios |
|-----------|-----------|
| **Input** | Valid, invalid, edge cases, missing, malformed |
| **State** | Initial variations, transitions, error states, concurrent |
| **Dependencies** | Available, unavailable, errors, edge cases, timeouts |
| **Authorization** | Authenticated, unauthenticated, authorized, unauthorized, roles |

### Step 3: Coverage Calculation

Measure scenario coverage, not just line coverage:

```
Scenario Coverage = Tested Scenarios / Total Identified Scenarios
```

### Step 4: Prioritize Gaps

**Likelihood x Impact Matrix**:
- **High/High** - MUST test (security, data loss)
- **High/Low** - SHOULD test (UX issues)
- **Low/High** - SHOULD test (edge cases that break system)
- **Low/Low** - NICE TO HAVE (document instead)

## Three-Lens Validation

Every test must pass all three lenses:

| Lens | Questions |
|------|-----------|
| **Product/User** | Tests user-facing behavior? User would notice if fails? |
| **Developer/Code** | Covers specific code path? Would catch regressions? |
| **Tester/QA** | Independent? Repeatable? Specific assertions? Realistic data? |

## Test Quality Checklist

### Coverage
- [ ] Happy path tested
- [ ] All validation rules tested
- [ ] Auth/authorization tested
- [ ] Not found scenarios tested
- [ ] Edge cases tested
- [ ] Error messages validated

### Quality
- [ ] Tests are independent
- [ ] Tests use factories/fixtures
- [ ] Test names are descriptive
- [ ] Assertions are specific
- [ ] Each test has one clear purpose

### Test Independence
- [ ] Doesn't depend on test order
- [ ] Creates own test data
- [ ] Can run in parallel
- [ ] Doesn't modify global state
- [ ] Mocks time if time-dependent

## Testing Pyramid

```
       /\
      /E2E\      <- Few (5-10%)
     /------\
    / Integ  \   <- Some (20-30%)
   /----------\
  /    Unit    \ <- Many (60-75%)
 /--------------\
```

| Level | Use For | Characteristics |
|-------|---------|-----------------|
| **Unit** | Pure functions, validators, utilities | Fast, no I/O, mock dependencies |
| **Integration** | API endpoints, DB queries, multi-component | Uses test DB, slower |
| **E2E** | Critical user journeys, cross-service | Full stack, fewest tests |

## Test Smells (Anti-Patterns)

| Smell | Bad | Good |
|-------|-----|------|
| Magic numbers | `assert len(results) == 3` | `assert len(results) == EXPECTED_COUNT` |
| Weak assertions | `assert response is not None` | `assert response.status_code == 200` |
| Testing implementation | `assert cache.get(id) is None` | `assert fetched["name"] == "New"` |
| Multiple concerns | One test with 5 unrelated asserts | Separate tests per concern |

## LLM Test Generation

### Effective Prompting

Include in prompts:
1. **Test categories**: Happy path, validation, auth, edge cases
2. **Specific scenarios**: List expected tests
3. **Example format**: Show desired test structure
4. **Blind spots**: Concurrent ops, idempotency, special chars

### Common LLM Blind Spots

Always prompt for:
- Concurrent operations (race conditions)
- Idempotency (same operation twice)
- Cascading effects (parent deleted)
- Special characters (Unicode, SQL injection, XSS)
- Timezone edge cases
- Quota/rate limits

See `references/llm-prompting-guide.md` for complete prompt templates.

## Quick Reference Checklists

### Edge Case Checklist
- [ ] Boundary values tested
- [ ] Empty/null inputs tested
- [ ] Maximum length inputs tested
- [ ] Invalid type inputs tested
- [ ] Special characters tested
- [ ] Concurrent operations tested
- [ ] State transitions tested

### LLM Prompt Checklist
- [ ] Specify test categories
- [ ] List expected scenarios
- [ ] Provide example format
- [ ] Mention blind spots explicitly
- [ ] Request specific assertions

## Coverage Report Format

```markdown
# Test Coverage Report - [Feature Name]

## Summary
- Total Scenarios: 28
- Tested: 22
- Coverage: 78.6%

## Gaps (by priority)

### High Priority (MUST FIX)
- Missing security tests (SQL injection, XSS)

### Medium Priority (SHOULD FIX)
- Concurrent operations not tested

### Low Priority
- Performance with large datasets
```

## Related Skills

### Upstream Skills (Provide Input)

| Skill | Provides |
|-------|----------|
| **Backend Developer** | Code to test |
| **API Designer** | API contracts |
| **Solutions Architect** | Integration requirements |

### Parallel Skills

| Skill | Coordination |
|-------|-------------|
| **Frontend Tester** | Test strategy alignment |
| **Code Reviewer** | PR review before completion |
| **PM** | Test coverage reporting |

## Reference Files

- `references/test-patterns.md` - Factory patterns, fixtures, mocking, parameterized tests
- `references/edge-case-discovery.md` - Boundary analysis, state transitions, error guessing
- `references/llm-prompting-guide.md` - Effective prompts for LLM test generation

## Summary

Systematic test coverage analysis ensures:
- **Complete coverage** through scenario matrices
- **Quality tests** through three-lens validation
- **Edge case discovery** through systematic techniques
- **Effective LLM usage** through specific prompting
- **Maintainable tests** through patterns and best practices
