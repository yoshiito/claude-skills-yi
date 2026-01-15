---
name: fastapi-pytest-tester
description: Systematic test coverage analysis and quality assurance for FastAPI applications using pytest. Use when reviewing test coverage, generating comprehensive test suites, identifying edge cases, evaluating test quality, or ensuring robust testing for APIs, services, utilities, and background jobs. Essential for lean teams relying on LLM-generated tests. Provides frameworks for coverage analysis, edge case discovery, test quality evaluation, and effective prompting strategies.
---

# FastAPI + Pytest Tester

Ensure comprehensive, high-quality test coverage for codebases where testing is primarily LLM-generated. This skill provides systematic frameworks for coverage analysis, edge case discovery, test evaluation, and quality assurance.

## Core Philosophy

**For lean teams relying on LLMs**: Since you're depending on AI to generate tests, this skill helps you:
1. **Systematically identify what needs testing** (so you can prompt effectively)
2. **Evaluate generated tests for quality** (catch LLM blind spots)
3. **Discover edge cases** (that LLMs often miss)
4. **Maintain test quality over time** (prevent regression in coverage)

## Quick Start Guide

### When to Use This Skill

**New Code**:
- Before considering code complete
- After implementing a feature
- When adding tests to untested code

**Code Review**:
- Reviewing PRs for test coverage
- Analyzing test quality
- Identifying missing test scenarios

**Refactoring**:
- Ensuring tests still cover edge cases
- Validating test suite after changes
- Improving existing test suites

### Workflow

1. **Analyze Code** - Understand what needs testing
2. **Coverage Analysis** - Identify tested vs untested scenarios
3. **Edge Case Discovery** - Find scenarios to test
4. **Generate/Review Tests** - Create or evaluate tests
5. **Quality Evaluation** - Validate test quality
6. **Document Gaps** - Track what's not tested and why

## Coverage Analysis Framework

### Step 1: Code Understanding

Before analyzing coverage, understand what the code does:

**For Functions/Methods**:
- What is the primary purpose?
- What are the inputs (parameters, dependencies)?
- What are the outputs (return values, side effects)?
- What are the preconditions (required state)?
- What are the postconditions (guaranteed state)?

**For Classes**:
- What is the class responsibility?
- What state does it manage?
- What are the public interfaces?
- What invariants must be maintained?

**For API Endpoints**:
- What HTTP method and path?
- What request data is accepted?
- What responses are possible?
- What side effects occur?
- What authorization is required?

### Step 2: Test Scenario Matrix

Create a matrix of scenarios to test:

**Input Dimensions**:
- Valid inputs (happy path)
- Invalid inputs (validation errors)
- Edge cases (boundaries, limits)
- Missing inputs (null, undefined, empty)
- Malformed inputs (wrong types, format)

**State Dimensions**:
- Initial state variations
- Intermediate state transitions
- Error states
- Concurrent state changes

**Dependency Dimensions**:
- Dependencies available
- Dependencies unavailable
- Dependencies return errors
- Dependencies return edge cases
- Dependencies are slow/timeout

**Authorization Dimensions**:
- Authenticated users
- Unauthenticated users
- Authorized users (correct permissions)
- Unauthorized users (wrong permissions)
- Different user roles

### Step 3: Coverage Calculation

**Not just line coverage** - measure scenario coverage:

```
Scenario Coverage = Tested Scenarios / Total Identified Scenarios
```

Example for an API endpoint:

```
Total Scenarios Identified: 24
- Happy path: 2 scenarios
- Validation errors: 8 scenarios
- Auth errors: 3 scenarios
- Not found errors: 2 scenarios
- Edge cases: 6 scenarios
- Concurrent operations: 3 scenarios

Tests Written: 15
Scenario Coverage: 15/24 = 62.5%

Missing Coverage:
- Validation: missing 3 scenarios
- Edge cases: missing 4 scenarios
- Concurrent: missing 2 scenarios
```

### Step 4: Prioritize Gaps

Not all gaps are equal. Prioritize by:

**Likelihood × Impact Matrix**:
- **High likelihood, high impact** - MUST test (security, data loss)
- **High likelihood, low impact** - SHOULD test (UX issues)
- **Low likelihood, high impact** - SHOULD test (edge cases that break system)
- **Low likelihood, low impact** - NICE TO HAVE (document instead)

## Edge Case Discovery Techniques

### Boundary Value Analysis

Test at boundaries, just inside, and just outside:

**Numeric boundaries**:
```python
# For a function accepting age 0-120
test_age_zero()           # Lower boundary
test_age_one()            # Just inside lower
test_age_minus_one()      # Just outside lower
test_age_120()            # Upper boundary
test_age_119()            # Just inside upper
test_age_121()            # Just outside upper
```

**String length boundaries**:
```python
# For a field with max length 255
test_empty_string()       # Empty
test_one_char()           # Minimum content
test_254_chars()          # Just under limit
test_255_chars()          # At limit
test_256_chars()          # Over limit
test_very_long_string()   # Way over limit (10000 chars)
```

**Collection boundaries**:
```python
test_empty_list()         # Empty collection
test_one_item()           # Single item
test_many_items()         # Normal case
test_max_items()          # At limit
test_over_limit()         # Exceeds limit
```

**Date/time boundaries**:
```python
test_past_date()          # Before valid range
test_today()              # Current day
test_future_date()        # After valid range
test_epoch()              # Unix epoch (1970-01-01)
test_year_2038()          # 32-bit overflow
test_leap_year()          # Feb 29
test_timezone_edge()      # DST transition
```

### Equivalence Partitioning

Group inputs into classes that should behave the same way:

**Example: Status field**
```python
# Valid statuses (one test per partition)
test_status_active()      # Partition: active states
test_status_inactive()    # Partition: inactive states
test_status_pending()     # Partition: transitional states

# Invalid statuses
test_status_empty()       # Partition: empty/null
test_status_unknown()     # Partition: not in enum
test_status_wrong_type()  # Partition: type error
```

### State Transition Testing

For stateful systems, test all valid and invalid transitions:

```python
# Valid transitions
test_pending_to_active()
test_active_to_inactive()
test_inactive_to_archived()

# Invalid transitions
test_pending_to_archived()      # Skip states
test_archived_to_active()       # Reverse flow
test_deleted_to_anything()      # Terminal state

# Edge cases
test_transition_twice()         # Idempotent
test_concurrent_transitions()   # Race conditions
```

### Error Guessing

Use experience to guess where errors hide:

**Common patterns that often have bugs**:
- Off-by-one errors in loops/indexes
- Null/undefined handling
- Timezone conversions
- Character encoding (Unicode, emoji)
- Floating point precision
- Integer overflow
- Concurrent access to shared state
- Resource cleanup (connections, files)
- Cascading deletes
- Cache invalidation

**Test for these specifically**:
```python
test_unicode_in_name()           # 名前, François, 🎉
test_sql_injection_attempt()     # "Robert'); DROP TABLE--"
test_xss_attempt()               # <script>alert('XSS')</script>
test_very_long_input()           # DoS via large payloads
test_null_bytes()                # \x00 in strings
test_negative_numbers()          # When only positive expected
test_concurrent_updates()        # Race conditions
test_orphaned_records()          # Parent deleted, child remains
```

### Input Combination Testing

Test combinations of inputs, not just individual fields:

```python
# Individual validation works, but combinations?
test_valid_email_invalid_phone()
test_max_length_name_max_length_description()  # Both at limit
test_future_start_date_past_end_date()         # Date logic
test_optional_field_A_requires_field_B()       # Conditional requirements
```

### Negative Testing

Test what the system should NOT allow:

```python
# Access control
test_user_cannot_access_other_user_data()
test_user_cannot_escalate_permissions()
test_deleted_user_cannot_login()

# Data integrity
test_cannot_create_duplicate_email()
test_cannot_delete_in_use_resource()
test_cannot_exceed_quota()

# Business rules
test_cannot_book_past_date()
test_cannot_withdraw_more_than_balance()
test_cannot_submit_after_deadline()
```

## Test Quality Evaluation

### Three-Lens Validation (Expanded)

Every test should pass all three lenses:

#### Lens 1: Product/User Perspective

**Questions**:
- Does this test verify user-facing behavior?
- Would a user story acceptance criteria cover this?
- If this test fails, would users experience a problem?
- Are error messages in the test helpful to users?

**Example**:
```python
# ✓ PASS - Tests user-visible behavior
def test_user_cannot_create_project_with_duplicate_name():
    """Users should see clear error when project name already exists."""
    # User creates first project
    create_project("My Project")
    
    # User tries to create duplicate
    response = create_project("My Project")
    
    # User sees helpful error
    assert response.status_code == 422
    assert "already exists" in response.json()["detail"]

# ✗ FAIL - Tests internal implementation
def test_database_constraint_fires():
    """Database should raise IntegrityError."""
    # User doesn't care about database constraints
    # They care about getting a helpful error message
```

#### Lens 2: Developer/Code Perspective

**Questions**:
- Does this test cover a specific code path?
- Are edge cases and error conditions tested?
- Would this test catch regressions if code changes?
- Are all branches/conditions covered?

**Example**:
```python
# ✓ PASS - Covers specific code path
def test_expired_resource_returns_410():
    """Expired resources return 410 Gone status."""
    resource = create_resource(expires_at=past_date)
    response = get_resource(resource.id)
    assert response.status_code == 410  # Specific to expiry logic

# ✗ FAIL - Too generic, doesn't test specific path
def test_get_resource():
    """Get resource returns resource."""
    resource = create_resource()
    response = get_resource(resource.id)
    assert response.status_code == 200
    # Doesn't test expiry, permissions, not found, etc.
```

#### Lens 3: Tester/QA Perspective

**Questions**:
- Is this test independent (doesn't depend on test order)?
- Is this test repeatable (same result every run)?
- Are assertions specific and meaningful?
- Does test data represent realistic scenarios?
- Is the test name descriptive of what's being tested?
- Would a new developer understand this test?

**Example**:
```python
# ✓ PASS - Independent, repeatable, specific
def test_user_can_update_own_project_name():
    """User can update the name of their own project."""
    user = create_test_user()
    project = create_project(owner=user, name="Original")
    
    response = update_project(
        project.id,
        {"name": "Updated"},
        auth=user.token
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    
    # Verify persistence
    fetched = get_project(project.id)
    assert fetched.json()["name"] == "Updated"

# ✗ FAIL - Depends on external state
def test_update_project():
    """Update project."""
    # Assumes project with ID 123 exists
    response = update_project(123, {"name": "New"})
    assert response.status_code == 200
```

### Test Smells (Anti-Patterns)

**Smell 1: Magic Numbers/Strings**
```python
# ✗ BAD
assert len(results) == 3
assert response.json()["status"] == "active"

# ✓ GOOD
EXPECTED_RESULT_COUNT = 3  # User has 3 projects
assert len(results) == EXPECTED_RESULT_COUNT

from app.models import ProjectStatus
assert response.json()["status"] == ProjectStatus.ACTIVE
```

**Smell 2: Weak Assertions**
```python
# ✗ BAD
assert response is not None
assert len(results) > 0
assert "error" not in str(response)

# ✓ GOOD
assert response.status_code == 200
assert len(results) == expected_count
assert response.json()["name"] == "Expected Name"
```

**Smell 3: Testing Implementation, Not Behavior**
```python
# ✗ BAD - Tests implementation detail
def test_cache_is_cleared():
    """Cache should be cleared after update."""
    update_resource(id, data)
    assert cache.get(id) is None  # Internal detail

# ✓ GOOD - Tests observable behavior
def test_resource_update_returns_fresh_data():
    """Updated resource returns new data immediately."""
    update_resource(id, {"name": "New"})
    fetched = get_resource(id)
    assert fetched["name"] == "New"  # What users observe
```

**Smell 4: Multiple Assertions Testing Different Things**
```python
# ✗ BAD - Multiple unrelated assertions
def test_create_project():
    response = create_project(data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert get_project_count() == previous_count + 1
    assert user.project_quota_remaining() == previous_quota - 1
    # If any assertion fails, hard to know which scenario broke

# ✓ GOOD - Separate tests for separate concerns
def test_create_project_returns_201():
    response = create_project(data)
    assert response.status_code == 201

def test_create_project_returns_submitted_data():
    response = create_project(data)
    assert response.json()["name"] == data["name"]

def test_create_project_increments_count():
    before = get_project_count()
    create_project(data)
    assert get_project_count() == before + 1
```

**Smell 5: Ignoring Error Responses**
```python
# ✗ BAD - Happy path only
def test_create_project():
    response = create_project({"name": "Test"})
    assert response.status_code == 201

# ✓ GOOD - Test error cases too
def test_create_project_missing_name():
    response = create_project({})
    assert response.status_code == 422
    assert "name" in response.json()["detail"]
```

### Test Independence Checklist

- [ ] Test doesn't depend on other tests running first
- [ ] Test creates its own test data
- [ ] Test cleans up after itself (or uses fixtures that do)
- [ ] Test can run in any order
- [ ] Test can run in parallel with other tests
- [ ] Test doesn't modify global state
- [ ] Test doesn't depend on specific database records existing
- [ ] Test doesn't depend on current date/time (mocks time if needed)

## Test Patterns Library

### Pattern 1: Factory Pattern for Test Data

Create realistic, varied test data efficiently:

```python
# factories.py
from datetime import datetime, timedelta
from faker import Faker
import factory

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Faker('uuid4')
    email = factory.Faker('email')
    name = factory.Faker('name')
    created_at = factory.LazyFunction(datetime.utcnow)
    
class ProjectFactory(factory.Factory):
    class Meta:
        model = Project
    
    id = factory.Faker('uuid4')
    name = factory.Faker('bs')  # Business speak
    owner_id = factory.SubFactory(UserFactory)
    status = 'active'
    created_at = factory.LazyFunction(datetime.utcnow)

# Usage in tests
def test_user_can_list_own_projects():
    user = UserFactory()
    projects = ProjectFactory.create_batch(3, owner_id=user.id)
    
    response = list_projects(auth=user.token)
    assert len(response.json()) == 3
```

### Pattern 2: Fixture Hierarchy

Organize fixtures for reusability:

```python
# conftest.py
import pytest

@pytest.fixture
def db():
    """Database connection."""
    connection = create_db_connection()
    yield connection
    connection.close()

@pytest.fixture
def clean_db(db):
    """Database with clean slate."""
    db.execute("TRUNCATE TABLE users CASCADE")
    yield db

@pytest.fixture
def test_user(clean_db):
    """Authenticated test user."""
    user = create_user(email="test@example.com")
    yield user
    # Cleanup handled by clean_db CASCADE

@pytest.fixture
def admin_user(clean_db):
    """Admin user with elevated permissions."""
    user = create_user(email="admin@example.com", role="admin")
    yield user

@pytest.fixture
def auth_headers(test_user):
    """Authorization headers for test user."""
    return {"Authorization": f"Bearer {test_user.token}"}
```

### Pattern 3: Parameterized Tests

Test multiple inputs efficiently:

```python
import pytest

@pytest.mark.parametrize("status,expected_count", [
    ("active", 5),
    ("inactive", 2),
    ("archived", 1),
])
def test_filter_projects_by_status(status, expected_count, auth_headers):
    """Filter projects by status returns correct count."""
    # Setup data
    create_projects_with_statuses(
        active=5, inactive=2, archived=1, owner=current_user
    )
    
    response = list_projects(status=status, auth=auth_headers)
    assert len(response.json()) == expected_count

@pytest.mark.parametrize("invalid_email", [
    "",                    # Empty
    "notanemail",         # Missing @
    "@example.com",       # Missing local part
    "test@",              # Missing domain
    "test @example.com",  # Space in email
    "test@example",       # Missing TLD
])
def test_create_user_invalid_email(invalid_email):
    """Creating user with invalid email returns 422."""
    response = create_user(email=invalid_email)
    assert response.status_code == 422
    assert "email" in response.json()["detail"].lower()
```

### Pattern 4: Mocking External Dependencies

Mock external services for reliable tests:

```python
from unittest.mock import Mock, patch

def test_send_notification_email_success(test_user):
    """Successfully sending email returns True."""
    with patch('app.services.email.send_email') as mock_send:
        mock_send.return_value = True
        
        result = notify_user(test_user.id, "Welcome!")
        
        assert result is True
        mock_send.assert_called_once_with(
            to=test_user.email,
            subject="Welcome!",
            body=ANY  # Don't care about exact body
        )

def test_send_notification_email_failure_logs_error(test_user):
    """Failed email send logs error and returns False."""
    with patch('app.services.email.send_email') as mock_send, \
         patch('app.services.logger') as mock_logger:
        mock_send.side_effect = SMTPException("Connection failed")
        
        result = notify_user(test_user.id, "Welcome!")
        
        assert result is False
        mock_logger.error.assert_called_once()
```

### Pattern 5: Time-Based Testing

Test time-dependent behavior:

```python
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2025-01-14 10:00:00")
def test_expired_resource_cannot_be_accessed():
    """Expired resources return 410 Gone."""
    # Create resource that expires in 1 hour
    expires_at = datetime.utcnow() + timedelta(hours=1)
    resource = create_resource(expires_at=expires_at)
    
    # Access while valid
    response = get_resource(resource.id)
    assert response.status_code == 200
    
    # Fast forward 2 hours
    with freeze_time("2025-01-14 12:00:00"):
        response = get_resource(resource.id)
        assert response.status_code == 410
```

## Integration vs Unit Testing

### When to Write Unit Tests

**Use unit tests for**:
- Pure functions (no side effects)
- Business logic functions
- Utility functions
- Validators
- Transformers/parsers

**Characteristics**:
- Fast (milliseconds)
- No database, no network, no file I/O
- Mock all dependencies
- Test one function in isolation

```python
# Unit test - pure function
def test_calculate_discount():
    """Calculate discount returns correct percentage."""
    price = 100
    discount_rate = 0.2
    
    result = calculate_discount(price, discount_rate)
    
    assert result == 20.0
```

### When to Write Integration Tests

**Use integration tests for**:
- API endpoints (database + logic + HTTP)
- Database queries
- External service integrations
- Background jobs that touch multiple systems
- Multi-step workflows

**Characteristics**:
- Slower (seconds)
- Uses real database (test DB)
- May use mocked external services
- Tests multiple components together

```python
# Integration test - API endpoint with database
def test_create_project_persists_to_database(auth_headers, db):
    """Creating project via API persists to database."""
    project_data = {"name": "Test Project"}
    
    # API call
    response = client.post("/api/v1/projects", json=project_data, headers=auth_headers)
    assert response.status_code == 201
    project_id = response.json()["id"]
    
    # Verify in database
    project = db.exec(select(Project).where(Project.id == project_id)).first()
    assert project is not None
    assert project.name == "Test Project"
```

### When to Write E2E Tests

**Use E2E tests for**:
- Critical user journeys
- Multi-page workflows
- Complex state transitions
- Cross-service interactions

**Characteristics**:
- Slow (seconds to minutes)
- Full stack (UI + API + DB)
- Simulates real user behavior
- Fewer E2E tests, more unit/integration

**Example: Critical user journey**
```python
def test_complete_user_signup_flow():
    """User can complete full signup and create first project."""
    # 1. Sign up
    response = signup(email="new@example.com", password="secure123")
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # 2. Verify email (simulated)
    verify_email(user_id)
    
    # 3. Login
    response = login(email="new@example.com", password="secure123")
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # 4. Create first project
    response = create_project(
        {"name": "My First Project"},
        auth={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    
    # 5. Verify onboarding complete
    user = get_user(user_id)
    assert user["onboarding_completed"] is True
```

### Testing Pyramid

```
       /\
      /E2E\      <- Few (5-10% of tests)
     /------\
    / Integ  \   <- Some (20-30% of tests)
   /----------\
  /    Unit    \ <- Many (60-75% of tests)
 /--------------\
```

**Target distribution**:
- **60-75% Unit tests** - Fast, isolated, many scenarios
- **20-30% Integration tests** - Database + API, realistic scenarios
- **5-10% E2E tests** - Full stack, critical user journeys only

## LLM-Specific Test Generation Guidance

### Effective Prompts for Test Generation

**❌ Vague prompt**:
"Write tests for this function"

**✓ Specific prompt**:
```
Write comprehensive pytest tests for the create_project function.

Include tests for:
1. Happy path - valid project creation
2. Validation errors - missing name, invalid status, name too long
3. Authorization - unauthenticated user, user at quota limit
4. Edge cases - duplicate name, special characters in name, very long description
5. Database - verify persistence, verify owner_id set correctly

Use factories for test data. Each test should be independent.
Follow naming: test_create_project_<scenario>
```

**✓ With examples**:
```
Write tests for the update_project endpoint following this pattern:

def test_update_project_success(auth_headers):
    """User can update their own project."""
    project = create_project(owner=current_user)
    response = update_project(project.id, {"name": "New"}, auth=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "New"

Generate similar tests for:
- User cannot update other user's project (403)
- Update with invalid data returns 422
- Update non-existent project returns 404
- Partial update (only some fields)
```

### Common LLM Test Generation Blind Spots

LLMs often miss these scenarios - explicitly prompt for them:

**1. Concurrent operations**:
```
Also test concurrent scenarios:
- Two users creating projects with same name simultaneously
- User updating project while another reads it
- Race condition on quota checks
```

**2. Idempotency**:
```
Test idempotent operations:
- Deleting same resource twice
- Updating resource to same values
- Creating resource that already exists (if should be idempotent)
```

**3. Cascading effects**:
```
Test cascading behaviors:
- What happens to child resources when parent deleted?
- What happens to related resources?
- Verify soft-deleted resources don't appear in lists
```

**4. Edge cases with special characters**:
```
Test with special characters:
- Unicode: 名前, François, emoji 🎉
- SQL injection attempts: "Robert'); DROP TABLE--"
- XSS attempts: <script>alert('XSS')</script>
- Null bytes: "test\x00name"
```

**5. Timezone edge cases**:
```
Test timezone handling:
- UTC timestamps
- Daylight saving time transitions
- Different client timezones
- Leap seconds
```

**6. Quota and rate limits**:
```
Test limits:
- User at quota limit
- User exceeding rate limit
- Bulk operations near limits
```

### Prompt Template for Comprehensive Coverage

```
Generate comprehensive tests for [FUNCTION/ENDPOINT].

Context:
[Describe what the code does, dependencies, auth requirements]

Test Categories (generate at least one test for each):

1. HAPPY PATH:
   - Valid input with expected success

2. VALIDATION ERRORS (422):
   - Missing required fields: [list fields]
   - Invalid field values: [list validation rules]
   - Field length violations: [list length limits]
   - Type errors: [list expected types]

3. AUTHENTICATION (401):
   - Unauthenticated request

4. AUTHORIZATION (403):
   - User accessing other user's resource
   - [Any role-based restrictions]

5. NOT FOUND (404):
   - Resource doesn't exist
   - [Any other 404 scenarios]

6. EDGE CASES:
   - Boundary values: [list boundaries]
   - Empty/null values: [list optional fields]
   - Very large values: [list size limits]
   - Special characters: Unicode, SQL injection, XSS
   - Concurrent operations: [list race conditions]

7. DATABASE/STATE:
   - Verify persistence
   - Verify relationships
   - Verify soft delete behavior (if applicable)

Requirements:
- Use factories for test data
- Each test independent
- Descriptive test names: test_[operation]_[scenario]
- Specific assertions
- Follow three-lens validation (product, developer, tester)
```

### Review Checklist for LLM-Generated Tests

After LLM generates tests, verify:

**Coverage**:
- [ ] Happy path tested
- [ ] All validation rules tested
- [ ] Auth/authorization tested
- [ ] Not found scenarios tested
- [ ] Edge cases identified and tested
- [ ] Error messages validated

**Quality**:
- [ ] Tests are independent
- [ ] Tests use factories/fixtures (no hardcoded data)
- [ ] Test names are descriptive
- [ ] Assertions are specific
- [ ] Each test has one clear purpose
- [ ] Tests pass three-lens validation

**Realism**:
- [ ] Test data is realistic
- [ ] Error scenarios are plausible
- [ ] Edge cases are based on real risks
- [ ] No testing implementation details

**Completeness**:
- [ ] All code paths covered
- [ ] All error conditions tested
- [ ] All business rules validated
- [ ] Security scenarios tested

## Test Maintenance

### When to Refactor Tests

**Refactor when**:
- Tests are brittle (break with minor code changes)
- Tests are slow (taking minutes to run)
- Tests are flaky (sometimes pass, sometimes fail)
- Tests have duplicated setup code
- Tests are hard to understand

**How to refactor**:
```python
# Before - duplicated setup
def test_user_can_create_project():
    user = User(email="test@example.com")
    db.add(user)
    db.commit()
    token = generate_token(user)
    # Test code...

def test_user_can_update_project():
    user = User(email="test@example.com")
    db.add(user)
    db.commit()
    token = generate_token(user)
    # Test code...

# After - extracted fixture
@pytest.fixture
def authenticated_user(db):
    user = User(email="test@example.com")
    db.add(user)
    db.commit()
    user.token = generate_token(user)
    return user

def test_user_can_create_project(authenticated_user):
    # Test code...

def test_user_can_update_project(authenticated_user):
    # Test code...
```

### Dealing with Flaky Tests

**Common causes**:
1. Time-dependent assertions
2. Concurrent test execution conflicts
3. External service timeouts
4. Database state leakage
5. Random data causing inconsistent results

**Solutions**:
```python
# 1. Time-dependent - use freezegun
from freezegun import freeze_time

@freeze_time("2025-01-14 10:00:00")
def test_timestamp():
    resource = create_resource()
    assert resource.created_at == datetime(2025, 1, 14, 10, 0, 0)

# 2. Concurrent conflicts - use unique identifiers
def test_create_user():
    # Bad: email = "test@example.com"  # Conflicts if tests run parallel
    email = f"test-{uuid4()}@example.com"  # Unique per test
    user = create_user(email=email)

# 3. External service - mock it
with patch('external_api.call') as mock_call:
    mock_call.return_value = {"status": "success"}
    result = function_that_calls_api()

# 4. Database state - use transactions or truncate
@pytest.fixture
def clean_db(db):
    yield db
    db.execute("TRUNCATE TABLE users CASCADE")

# 5. Random data - seed randomness
import random
random.seed(42)  # Reproducible "random" data
```

## Documentation and Reporting

### Coverage Report Format

```markdown
# Test Coverage Report - [Feature Name]

## Summary
- Total Scenarios Identified: 28
- Scenarios Tested: 22
- Coverage: 78.6%
- Risk Level: Medium

## Tested Scenarios
### Happy Path (3/3 ✓)
- ✓ Create project with valid data
- ✓ List user's projects
- ✓ Update project name

### Validation Errors (8/10)
- ✓ Missing required field (name)
- ✓ Name exceeds max length
- ✓ Invalid status enum
- ✓ Description exceeds max length
- ✗ Name with SQL injection
- ✗ Name with XSS attempt
... 

### Auth/Authorization (6/8)
- ✓ Unauthenticated request rejected
- ✓ User cannot access other user's project
- ✗ Admin can access any project
- ✗ Deleted user's token rejected
...

## Gaps and Risks

### High Priority (MUST FIX)
1. **Security**: Missing SQL injection and XSS tests
   - Risk: Potential security vulnerability
   - Action: Add tests with malicious inputs

2. **Cascading Delete**: Not tested
   - Risk: Data orphaned when project deleted
   - Action: Add test for child resource cleanup

### Medium Priority (SHOULD FIX)
1. **Concurrent Operations**: Not tested
   - Risk: Race conditions on project creation
   - Action: Add concurrent test with threading

### Low Priority (NICE TO HAVE)
1. **Performance**: Large dataset handling
   - Risk: Slow queries on production data
   - Action: Add test with 1000+ projects

## Recommendations
1. Add security tests (SQL injection, XSS)
2. Test cascading delete behavior
3. Consider load testing for list endpoint
```

### Test Intent Documentation

For each test, document the intent:

```python
def test_user_cannot_exceed_project_quota():
    """
    INTENT: Prevent users from creating unlimited projects
    
    PRODUCT: Users with free plan limited to 3 projects
    DEVELOPER: ProjectService.create() checks quota before creating
    TESTER: Verify 403 returned when at quota, helpful error message
    
    RISK: High - financial impact if users bypass quota
    """
    user = create_user(plan="free", project_count=3)  # At quota
    
    response = create_project({"name": "Fourth"}, auth=user.token)
    
    assert response.status_code == 403
    assert "quota" in response.json()["detail"].lower()
    assert "upgrade" in response.json()["detail"].lower()  # Helpful message
```

## Quick Reference

### Coverage Analysis Workflow
1. Understand code → 2. Create scenario matrix → 3. Calculate coverage → 4. Prioritize gaps

### Edge Case Checklist
- [ ] Boundary values tested
- [ ] Empty/null inputs tested
- [ ] Maximum length inputs tested
- [ ] Invalid type inputs tested
- [ ] Special characters tested
- [ ] Concurrent operations tested
- [ ] State transitions tested

### Test Quality Checklist
- [ ] Passes product lens
- [ ] Passes developer lens
- [ ] Passes tester lens
- [ ] Independent and repeatable
- [ ] Specific assertions
- [ ] Realistic test data
- [ ] Descriptive name

### LLM Prompt Checklist
- [ ] Specify test categories (happy, validation, auth, edge)
- [ ] List expected scenarios
- [ ] Provide example test format
- [ ] Mention LLM blind spots explicitly
- [ ] Request specific assertion patterns

## Summary

Systematic test coverage analysis ensures:
- **Complete coverage** through scenario matrices
- **Quality tests** through three-lens validation
- **Edge case discovery** through systematic techniques
- **Effective LLM usage** through specific prompting
- **Maintainable tests** through patterns and best practices

For lean teams relying on LLM-generated tests, this framework provides the structure to ensure comprehensive, high-quality test coverage without a large QA team.
