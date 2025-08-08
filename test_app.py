import json
from src.app import app, init_db

def setup_module(module):
    init_db()

def test_create_task():
    client = app.test_client()
    response = client.post("/tasks", json={"title": "Teste", "description": "Desc", "priority": "Alta"})
    assert response.status_code == 201

def test_get_tasks():
    client = app.test_client()
    response = client.get("/tasks")
    assert response.status_code == 200
