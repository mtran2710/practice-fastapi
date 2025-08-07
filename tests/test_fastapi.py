import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

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

def test_delete_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Todo deleted successfully"}
