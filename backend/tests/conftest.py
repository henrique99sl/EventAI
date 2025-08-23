import pytest
import uuid
from datetime import date
from app import create_app, db as _db
from models.user import User
from models.venue import Venue
from models.event import Event
from werkzeug.security import generate_password_hash

# --- App e DB ---


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
        _db.create_all()
        admin = User(
            username="seed_admin",
            email="seed_admin@test.com",
            password_hash=generate_password_hash("Admin1234"),
            role="admin",
        )
        _db.session.add(admin)
        _db.session.commit()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Sessão de banco para cada teste, sempre limpa."""
    with app.app_context():
        _db.session.rollback()
        _db.drop_all()
        _db.create_all()
        admin = User(
            username="seed_admin",
            email="seed_admin@test.com",
            password_hash=generate_password_hash("Admin1234"),
            role="admin",
        )
        _db.session.add(admin)
        _db.session.commit()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    """Retorna client Flask limpo para cada teste."""
    return app.test_client()


# --- Utilitários de geração única ---


@pytest.fixture
def unique_email():

    def _gen(prefix="user"):
        return f"{prefix}_{uuid.uuid4().hex}@test.com"

    return _gen


@pytest.fixture
def unique_username():

    def _gen(prefix="user"):
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    return _gen


# --- Usuário admin, normal, e função geradora de token ---


@pytest.fixture
def admin_token(client):
    """Retorna token do admin seed."""
    login = client.post(
        "/login",
        json={"email": "seed_admin@test.com", "password": "Admin1234"},
    )
    assert login.status_code == 200, f"Admin login failed: {login.get_json()}"
    return login.get_json()["token"]


@pytest.fixture
def user_token(client, unique_email, unique_username):
    """Cria usuário único e retorna token."""
    email = unique_email("user")
    username = unique_username("user")
    password = "User1234"
    resp = client.post(
        "/users",
        json={"username": username, "email": email, "password": password},
    )
    assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
    login = client.post("/login", json={"email": email, "password": password})
    assert login.status_code == 200, f"User login failed: {login.get_json()}"
    return login.get_json()["token"]


@pytest.fixture
def make_user_token(client, unique_email, unique_username):
    """Função para criar usuário e retornar token."""

    def _make(prefix="user"):
        email = unique_email(prefix)
        username = unique_username(prefix)
        password = "User1234"
        resp = client.post(
            "/users",
            json={"username": username, "email": email, "password": password},
        )
        assert (
            resp.status_code == 201
        ), f"User creation failed: {resp.get_json()}"
        login = client.post(
            "/login", json={"email": email, "password": password}
        )
        assert (
            login.status_code == 200
        ), f"User login failed: {login.get_json()}"
        return login.get_json()["token"]

    return _make


@pytest.fixture
def user(db, unique_email, unique_username):
    """Cria e retorna um usuário para testes."""
    u = User(
        username=unique_username("user"),
        email=unique_email("user"),
        password_hash=generate_password_hash("TestUser123!"),
        role="user",
    )
    db.session.add(u)
    db.session.commit()
    return u


# --- Venue, Event, e exemplos para extensão ---


@pytest.fixture
def venue(db):
    """Cria venue de exemplo."""
    v = Venue(name="Venue Teste", address="Rua 1")
    db.session.add(v)
    db.session.commit()
    return v


@pytest.fixture
def event(db, venue):
    """Cria evento de exemplo associado ao venue e admin."""
    admin = User.query.filter_by(email="seed_admin@test.com").first()
    e = Event(
        name="Evento Teste",
        date=date(2025, 9, 1),
        owner_id=admin.id,
        venue_id=venue.id,
    )
    db.session.add(e)
    db.session.commit()
    return e


# --- Tokens e outros utilitários ---


@pytest.fixture
def token_expiry():
    """Simula tempo de expiração (int, não str!)."""
    return 2  # segundos


@pytest.fixture
def refresh_token():
    """Simula valor para refresh token."""
    return "refresh_token"


# --- Exemplo de fixture para participação (adapte ao seu modelo) ---
# @pytest.fixture
# def participation(db, user, event):
#     p = Participation(user_id=user.id, event_id=event.id)
#     db.session.add(p)
#     db.session.commit()
#     return p

# --- Pronto para extensões futuras! ---
