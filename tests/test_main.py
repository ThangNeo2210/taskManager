from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.json() == {"message": "Hello, world!"}

def test_create_and_list():
    client.post("/tasks", json={"title": "foo"})
    resp = client.get("/tasks")
    assert any(t["title"] == "foo" for t in resp.json())