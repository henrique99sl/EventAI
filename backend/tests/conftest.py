import pytest
import uuid
from app import create_app, db
from models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():
    """Cria app Flask para testes com banco em memória e seed de admin."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": "test",
            "JWT_SECRET_KEY": "jwt-secret",
        }
    )
    with app.app_context():
        db.create_all()
        admin = User(
            username="seed_admin",
            email="seed_admin@test.com",
            password_hash=generate_password_hash("Admin1234"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria client Flask limpo para cada teste e reseed do admin."""
    with app.app_context():
        db.session.rollback()
        db.drop_all()
        db.create_all()
        admin = User(
            username="seed_admin",
            email="seed_admin@test.com",
            password_hash=generate_password_hash("Admin1234"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
    return app.test_client()


@pytest.fixture
def unique_email():
    """Retorna função para gerar email único."""
    def _gen(prefix="user"):
        return f"{prefix}_{uuid.uuid4().hex}@test.com"
    return _gen


@pytest.fixture
def unique_username():
    """Retorna função para gerar username único."""
    def _gen(prefix="user"):
        return f"{prefix}_{uuid.uuid4().hex[:8]}"
    return _gen


@pytest.fixture
def admin_token(client):
    """Retorna token de admin seed."""
    login = client.post(
        "/login", json={"email": "seed_admin@test.com", "password": "Admin1234"}
    )
    assert login.status_code == 200, f"Admin login failed: {login.get_json()}"
    return login.get_json()["token"]


@pytest.fixture
def user_token(client, unique_email, unique_username):
    """Cria usuário único e retorna seu token."""
    email = unique_email("user")
    username = unique_username("user")
    password = "User1234"
    resp = client.post(
        "/users",
        json={"username": username, "email": email, "password": password},
    )
    assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
    login = client.post(
        "/login", json={"email": email, "password": password}
    )
    assert login.status_code == 200, f"User login failed: {login.get_json()}"
    return login.get_json()["token"]


@pytest.fixture
def make_user_token(client, unique_email, unique_username):
    """Retorna função que cria usuário com username/email únicos e retorna seu token."""
    def _make(prefix="user"):
        email = unique_email(prefix)
        username = unique_username(prefix)
        password = "User1234"
        resp = client.post(
            "/users",
            json={"username": username, "email": email, "password": password},
        )
        assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
        login = client.post(
            "/login", json={"email": email, "password": password}
        )
        assert login.status_code == 200, f"User login failed: {login.get_json()}"
        return login.get_json()["token"]
    return _make
