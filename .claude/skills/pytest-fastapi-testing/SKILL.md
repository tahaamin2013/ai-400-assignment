---
name: pytest-fastapi-testing
description: Generates pytest test cases for FastAPI endpoints including fixtures, test database setup, and CRUD operation tests. Use when writing tests for FastAPI applications.
---

# Pytest FastAPI Testing

Generate comprehensive pytest test cases for FastAPI endpoints.

## Core Principles

- Use TestClient from fastapi.testclient
- Create database fixtures for test isolation
- Test all CRUD operations (create, read, update, delete)
- Test error cases (404, 422, 400)
- Use dependency overrides for test database

## Test File Template

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from myapp.main import app, get_session
from myapp.models import Item

# Test database fixture
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Test client with dependency override
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# CREATE tests
def test_create_item(client: TestClient):
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "A test item"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

def test_create_item_invalid(client: TestClient):
    response = client.post("/items/", json={"invalid": "data"})
    assert response.status_code == 422

# READ ALL tests
def test_read_items(client: TestClient):
    # First create items
    client.post("/items/", json={"name": "Item 1"})
    client.post("/items/", json={"name": "Item 2"})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

# READ ONE tests
def test_read_item(client: TestClient):
    create_response = client.post("/items/", json={"name": "Test"})
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"

def test_read_item_not_found(client: TestClient):
    response = client.get("/items/99999")
    assert response.status_code == 404

# UPDATE tests
def test_update_item(client: TestClient):
    create_response = client.post("/items/", json={"name": "Original"})
    item_id = create_response.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"name": "Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"

def test_update_item_not_found(client: TestClient):
    response = client.patch("/items/99999", json={"name": "Updated"})
    assert response.status_code == 404

# DELETE tests
def test_delete_item(client: TestClient):
    create_response = client.post("/items/", json={"name": "To Delete"})
    item_id = create_response.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    # Verify deletion
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_item_not_found(client: TestClient):
    response = client.delete("/items/99999")
    assert response.status_code == 404
```

## Test Organization

1. **Fixtures first**: Define session and client fixtures at the top
2. **CRUD order**: Test create, read, update, delete in order
3. **Error cases**: Test 404, 422 responses after happy path
4. **Test isolation**: Each test should be independent
