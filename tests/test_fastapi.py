import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_create_todo(test_client):
    payload = {"title": "Test Todo"}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "id" in data and isinstance(data["id"], str)
    assert data["title"] == "Test Todo"
    assert data["completed"] is False

    # Save id for later tests
    test_create_todo.todo_id = data["id"]

def test_create_todo_malformed_payload(test_client):
    # Missing 'title' field
    payload = {"completed": False}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422

    # Title is not a string
    payload = {"title": 123}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422

def test_get_todos(test_client):
    response = test_client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        todo = data[0]
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo
        assert "created_at" in todo
        assert "updated_at" in todo

def test_update_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    payload = {"title": "Updated Todo", "completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True
    assert "updated_at" in data

def test_update_todo_partial_fields(test_client):
    # Create a new todo for this test
    payload = {"title": "Partial Update Todo"}
    response = test_client.post("/todos", json=payload)
    assert response.status_code in (200, 201)
    todo_id = response.json()["id"]

    # Update only the title
    payload = {"title": "Title Only Update"}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title Only Update"
    # Update only the completed field
    payload = {"completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    # Clean up
    test_client.delete(f"/todos/{todo_id}")

def test_delete_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Todo deleted successfully"}

def test_delete_unknown_todo(test_client):
    import uuid
    unknown_id = str(uuid.uuid4())
    response = test_client.delete(f"/todos/{unknown_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
