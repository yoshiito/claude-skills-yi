# FastAPI + SQLModel Code Patterns

Standard patterns for implementing CRUD APIs.

## SQLModel Pattern

```python
class ResourceBase(SQLModel):
    """Shared fields for all operations"""
    name: str
    description: Optional[str] = None

class Resource(ResourceBase, table=True):
    """Database model - includes ID, timestamps, ownership"""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(foreign_key="profiles.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None  # Soft delete

class ResourceCreate(ResourceBase):
    """Create request - only user-settable fields"""
    pass

class ResourceUpdate(SQLModel):
    """Update request - all fields optional"""
    name: Optional[str] = None
    description: Optional[str] = None

class ResourceResponse(ResourceBase):
    """API response - includes ID and timestamps"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
```

## Route Patterns

### Create
```python
@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource(
    data: ResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new resource."""
    resource = Resource(
        **data.model_dump(),
        owner_id=current_user.profile_id
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource
```

### List
```python
@router.get("", response_model=List[ResourceResponse])
async def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List resources for current user."""
    statement = (
        select(Resource)
        .where(Resource.owner_id == current_user.profile_id)
        .where(Resource.deleted_at.is_(None))
        .order_by(Resource.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.exec(statement).all()
```

### Get by ID
```python
@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resource by ID."""
    resource = db.exec(
        select(Resource)
        .where(Resource.id == resource_id)
        .where(Resource.deleted_at.is_(None))
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.owner_id != current_user.profile_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return resource
```

### Update
```python
@router.patch("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: UUID,
    data: ResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update resource."""
    resource = db.exec(
        select(Resource)
        .where(Resource.id == resource_id)
        .where(Resource.deleted_at.is_(None))
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.owner_id != current_user.profile_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update only provided fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resource, key, value)

    resource.updated_at = datetime.utcnow()
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource
```

### Delete (Soft)
```python
@router.delete("/{resource_id}", status_code=204)
async def delete_resource(
    resource_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete resource."""
    resource = db.exec(
        select(Resource)
        .where(Resource.id == resource_id)
        .where(Resource.deleted_at.is_(None))
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.owner_id != current_user.profile_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    resource.deleted_at = datetime.utcnow()
    db.add(resource)
    db.commit()
```

## DDL Pattern

```sql
CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    deleted_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT resources_name_not_empty CHECK (LENGTH(TRIM(name)) > 0)
);

-- Indexes
CREATE INDEX idx_resources_owner_id ON resources(owner_id);
CREATE INDEX idx_resources_deleted_at ON resources(deleted_at) WHERE deleted_at IS NULL;
```

## Test Pattern

```python
import pytest
from fastapi.testclient import TestClient

class TestCreateResource:
    """Tests for POST /api/v1/resources"""

    def test_create_success(self, auth_headers, resource_data):
        """Test successful resource creation."""
        response = client.post(
            "/api/v1/resources",
            json=resource_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == resource_data["name"]
        assert "id" in data
        assert "created_at" in data

    def test_create_missing_name(self, auth_headers):
        """Test 422 when name is missing."""
        response = client.post(
            "/api/v1/resources",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_unauthenticated(self, resource_data):
        """Test 401 without auth."""
        response = client.post(
            "/api/v1/resources",
            json=resource_data
        )
        assert response.status_code == 401


class TestGetResource:
    """Tests for GET /api/v1/resources/{id}"""

    def test_get_success(self, auth_headers, created_resource):
        """Test getting own resource."""
        response = client.get(
            f"/api/v1/resources/{created_resource['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == created_resource["id"]

    def test_get_not_found(self, auth_headers):
        """Test 404 for non-existent resource."""
        response = client.get(
            f"/api/v1/resources/{uuid4()}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_other_user_resource(self, auth_headers, other_user_resource):
        """Test 403 accessing other user's resource."""
        response = client.get(
            f"/api/v1/resources/{other_user_resource['id']}",
            headers=auth_headers
        )
        assert response.status_code == 403
```

## Fixtures Pattern

```python
# conftest.py
import pytest
from uuid import uuid4

@pytest.fixture
def resource_data():
    """Sample resource creation data."""
    return {
        "name": f"Test Resource {uuid4().hex[:8]}",
        "description": "Test description"
    }

@pytest.fixture
def created_resource(auth_headers, resource_data, db):
    """Create a resource for testing."""
    response = client.post(
        "/api/v1/resources",
        json=resource_data,
        headers=auth_headers
    )
    yield response.json()
    # Cleanup handled by test database reset

@pytest.fixture
def other_user_resource(db):
    """Resource owned by a different user."""
    other_user = create_test_user(db)
    resource = Resource(
        name="Other User Resource",
        owner_id=other_user.profile_id
    )
    db.add(resource)
    db.commit()
    return {"id": str(resource.id)}
```

## Service Layer Pattern (Optional)

For complex business logic:

```python
# app/services/resource_service.py
class ResourceService:
    @staticmethod
    def create(
        data: ResourceCreate,
        owner_id: UUID,
        db: Session
    ) -> Resource:
        """Create resource with business logic."""
        # Validate business rules
        if ResourceService.name_exists(data.name, owner_id, db):
            raise ValueError("Resource name already exists")

        resource = Resource(
            **data.model_dump(),
            owner_id=owner_id
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource

    @staticmethod
    def name_exists(name: str, owner_id: UUID, db: Session) -> bool:
        """Check if resource name exists for owner."""
        existing = db.exec(
            select(Resource)
            .where(Resource.name == name)
            .where(Resource.owner_id == owner_id)
            .where(Resource.deleted_at.is_(None))
        ).first()
        return existing is not None
```
