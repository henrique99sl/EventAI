import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db
from models.user import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_healthcheck(client):
    resp = client.get("/")
    print(resp.get_json())
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

def test_register_and_login(client):
    # Register user
    resp = client.post("/users", json={
        "username": "test",
        "email": "test@gmail.com",  # Usando domínio válido
        "password": "StrongPass1",
        "role": "user"
    })
    print(resp.get_json())
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "test"
    assert data["email"] == "test@gmail.com"

    # Register with same email
    resp2 = client.post("/users", json={
        "username": "test2",
        "email": "test@gmail.com",
        "password": "StrongPass1",
        "role": "user"
    })
    print(resp2.get_json())
    assert resp2.status_code == 400

    # Login
    resp3 = client.post("/login", json={
        "email": "test@gmail.com",
        "password": "StrongPass1"
    })
    print(resp3.get_json())
    assert resp3.status_code == 200
    assert "token" in resp3.get_json()

def test_weak_password(client):
    resp = client.post("/users", json={
        "username": "weakuser",
        "email": "weakuser@gmail.com",  # E-mail válido
        "password": "123"
    })
    print(resp.get_json())
    assert resp.status_code == 400
    assert "Senha fraca" in resp.get_json()["error"]

def test_invalid_email(client):
    resp = client.post("/users", json={
        "username": "bademail",
        "email": "bademail",  # E-mail inválido
        "password": "StrongPass1"
    })
    print(resp.get_json())
    assert resp.status_code == 400
    assert "E-mail inválido" in resp.get_json()["error"]