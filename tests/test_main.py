from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.json() == {"message": "Hello World"}

def test_create_and_list_tasks():
    client.post("/tasks", json={"title": "foo"})
    resp = client.get("/tasks")
    assert any(task["title"] == "foo" for task in resp.json())