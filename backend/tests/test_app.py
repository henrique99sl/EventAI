import pytest
from app import create_app, db


@pytest.fixture
def client():
    # Cria a app com configuração de testing e banco SQLite em memória
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test",  # define uma secret para JWT nos testes
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_healthcheck(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_register_and_login(client):
    # Registra novo usuário
    resp = client.post(
        "/users",
        json={
            "username": "test",
            "email": "test@gmail.com",
            "password": "StrongPass1",
            "role": "user",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "test"
    assert data["email"] == "test@gmail.com"

    # Tenta registrar com o mesmo email
    resp2 = client.post(
        "/users",
        json={
            "username": "test2",
            "email": "test@gmail.com",
            "password": "StrongPass1",
            "role": "user",
        },
    )
    assert resp2.status_code == 400

    # Login com o usuário criado
    resp3 = client.post("/login",
                        json={
                            "email": "test@gmail.com",
                            "password": "StrongPass1"
                        })
    assert resp3.status_code == 200
    assert "token" in resp3.get_json()


def test_weak_password(client):
    resp = client.post(
        "/users",
        json={
            "username": "weakuser",
            "email": "weakuser@gmail.com",
            "password": "123"
        },
    )
    assert resp.status_code == 400
    assert "Senha fraca" in resp.get_json()["error"]


def test_invalid_email(client):
    resp = client.post(
        "/users",
        json={
            "username": "bademail",
            "email": "bademail",
            "password": "StrongPass1"
        },
    )
    assert resp.status_code == 400
    assert "E-mail inválido" in resp.get_json()["error"]
