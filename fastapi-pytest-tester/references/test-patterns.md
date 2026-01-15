# Test Patterns Library

Complete code examples for pytest testing patterns with FastAPI.

## Pattern 1: Factory Pattern for Test Data

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

## Pattern 2: Fixture Hierarchy

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

## Pattern 3: Parameterized Tests

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

## Pattern 4: Mocking External Dependencies

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

## Pattern 5: Time-Based Testing

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

## Pattern 6: Three-Lens Validation Examples

### Lens 1: Product/User Perspective

```python
# PASS - Tests user-visible behavior
def test_user_cannot_create_project_with_duplicate_name():
    """Users should see clear error when project name already exists."""
    create_project("My Project")

    response = create_project("My Project")

    assert response.status_code == 422
    assert "already exists" in response.json()["detail"]

# FAIL - Tests internal implementation
def test_database_constraint_fires():
    """Database should raise IntegrityError."""
    # User doesn't care about database constraints
```

### Lens 2: Developer/Code Perspective

```python
# PASS - Covers specific code path
def test_expired_resource_returns_410():
    """Expired resources return 410 Gone status."""
    resource = create_resource(expires_at=past_date)
    response = get_resource(resource.id)
    assert response.status_code == 410

# FAIL - Too generic
def test_get_resource():
    """Get resource returns resource."""
    response = get_resource(resource.id)
    assert response.status_code == 200
    # Doesn't test expiry, permissions, not found, etc.
```

### Lens 3: Tester/QA Perspective

```python
# PASS - Independent, repeatable, specific
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

# FAIL - Depends on external state
def test_update_project():
    """Update project."""
    # Assumes project with ID 123 exists
    response = update_project(123, {"name": "New"})
    assert response.status_code == 200
```

## Test Smells (Anti-Patterns)

### Smell 1: Magic Numbers/Strings
```python
# BAD
assert len(results) == 3
assert response.json()["status"] == "active"

# GOOD
EXPECTED_RESULT_COUNT = 3  # User has 3 projects
assert len(results) == EXPECTED_RESULT_COUNT

from app.models import ProjectStatus
assert response.json()["status"] == ProjectStatus.ACTIVE
```

### Smell 2: Weak Assertions
```python
# BAD
assert response is not None
assert len(results) > 0

# GOOD
assert response.status_code == 200
assert len(results) == expected_count
```

### Smell 3: Testing Implementation, Not Behavior
```python
# BAD - Tests implementation detail
def test_cache_is_cleared():
    update_resource(id, data)
    assert cache.get(id) is None

# GOOD - Tests observable behavior
def test_resource_update_returns_fresh_data():
    update_resource(id, {"name": "New"})
    fetched = get_resource(id)
    assert fetched["name"] == "New"
```

### Smell 4: Multiple Unrelated Assertions
```python
# BAD - Multiple concerns in one test
def test_create_project():
    response = create_project(data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert get_project_count() == previous_count + 1
    assert user.project_quota_remaining() == previous_quota - 1

# GOOD - Separate tests for separate concerns
def test_create_project_returns_201():
    response = create_project(data)
    assert response.status_code == 201

def test_create_project_increments_count():
    before = get_project_count()
    create_project(data)
    assert get_project_count() == before + 1
```

## Dealing with Flaky Tests

**Common causes and solutions:**

```python
# 1. Time-dependent - use freezegun
from freezegun import freeze_time

@freeze_time("2025-01-14 10:00:00")
def test_timestamp():
    resource = create_resource()
    assert resource.created_at == datetime(2025, 1, 14, 10, 0, 0)

# 2. Concurrent conflicts - use unique identifiers
def test_create_user():
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

## Integration Test Example

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

## E2E Test Example

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

## Test Intent Documentation

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
    assert "upgrade" in response.json()["detail"].lower()
```
