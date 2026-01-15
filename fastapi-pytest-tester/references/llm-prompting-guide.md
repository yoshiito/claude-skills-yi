# LLM Test Generation Prompting Guide

Effective prompts for generating comprehensive tests with LLMs.

## Vague vs Specific Prompts

### Vague (Ineffective)
"Write tests for this function"

### Specific (Effective)
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

### With Examples
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

## Comprehensive Coverage Prompt Template

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

## Prompt for LLM Blind Spots

Add this to your prompts to catch commonly missed scenarios:

```
Also include tests for these often-missed scenarios:

CONCURRENT OPERATIONS:
- Two users creating with same unique field simultaneously
- Read while update in progress
- Race conditions on counters/quotas

IDEMPOTENCY:
- Same operation twice (delete, update)
- Retry behavior

CASCADING EFFECTS:
- Parent deleted, verify child behavior
- Related resources after deletion
- Soft-delete visibility

SPECIAL CHARACTERS:
- Unicode in text fields (Japanese, French accents, emoji)
- SQL injection attempts
- XSS attempts
- Null bytes

TIMEZONE/TIME:
- Different timezones
- DST transitions
- Far future/past dates

LIMITS:
- At quota/limit
- Exceeding rate limits
- Bulk operations near limits
```

## Review Checklist for LLM-Generated Tests

After LLM generates tests, verify:

### Coverage
- [ ] Happy path tested
- [ ] All validation rules tested
- [ ] Auth/authorization tested
- [ ] Not found scenarios tested
- [ ] Edge cases identified and tested
- [ ] Error messages validated

### Quality
- [ ] Tests are independent
- [ ] Tests use factories/fixtures (no hardcoded data)
- [ ] Test names are descriptive
- [ ] Assertions are specific
- [ ] Each test has one clear purpose
- [ ] Tests pass three-lens validation

### Realism
- [ ] Test data is realistic
- [ ] Error scenarios are plausible
- [ ] Edge cases are based on real risks
- [ ] No testing implementation details

### Completeness
- [ ] All code paths covered
- [ ] All error conditions tested
- [ ] All business rules validated
- [ ] Security scenarios tested

## Example: Full Prompt for API Endpoint

```
Generate comprehensive pytest tests for the POST /api/v1/projects endpoint.

Context:
- Creates a new project for authenticated user
- Requires: name (string, 1-255 chars), optional description (max 1000 chars)
- Returns 201 with project object on success
- User limited to 10 projects (free plan) or unlimited (pro plan)
- Project names must be unique per user

Test Categories:

1. HAPPY PATH:
   - Create with name only
   - Create with name and description

2. VALIDATION ERRORS (422):
   - Missing name
   - Empty name
   - Name > 255 chars
   - Description > 1000 chars
   - Invalid JSON body

3. AUTHENTICATION (401):
   - No auth header
   - Invalid token
   - Expired token

4. AUTHORIZATION (403):
   - User at quota limit (free plan)
   - Disabled user account

5. CONFLICT (409):
   - Duplicate project name for same user

6. EDGE CASES:
   - Name at exactly 255 chars
   - Description at exactly 1000 chars
   - Unicode in name (Japanese, emoji)
   - SQL injection in name
   - XSS in description
   - Very long valid input

7. DATABASE:
   - Verify project persisted
   - Verify owner_id matches authenticated user
   - Verify created_at timestamp

8. CONCURRENT:
   - Two requests with same name simultaneously

Requirements:
- Use UserFactory, ProjectFactory
- Fixtures: auth_headers, test_user, db
- Naming: test_create_project_[scenario]
- Assert specific status codes AND response body/errors
```
