import pytest
import uuid
from app import create_app, db
from models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():
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
        # Seed admin for all tests
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
    """Returns a Flask test client and resets DB after each test for
    isolation."""
    with app.app_context():
        db.session.rollback()
        db.drop_all()
        db.create_all()
        # Reseed admin for each test so admin_token works
        admin = User(
            username="seed_admin",
            email="seed_admin@test.com",
            password_hash=generate_password_hash("Admin1234"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
    return app.test_client()


def _unique_email(prefix="user"):
    """Helper to generate a unique email every time."""
    return f"{prefix}_{uuid.uuid4().hex}@test.com"


def _unique_username(prefix="user"):
    """Helper to generate a unique username every time."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def admin_token(client):
    """Logs in with the seeded admin user and returns a valid token."""
    login = client.post(
        "/login", json={"email": "seed_admin@test.com", "password": "Admin1234"}
    )
    assert login.status_code == 200, f"Admin login failed: {login.get_json()}"
    return login.get_json()["token"]


@pytest.fixture
def user_token(client):
    """Creates a unique user and returns a valid token."""
    unique_email = _unique_email("user")
    username = _unique_username("user")
    strong_password = "User1234"  # Must be >=8 chars, upper, lower, and number
    resp = client.post(
        "/users",
        json={"username": username, "email": unique_email, "password": strong_password},
    )
    assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
    login = client.post(
        "/login", json={"email": unique_email, "password": strong_password}
    )
    assert login.status_code == 200, f"User login failed: {login.get_json()}"
    return login.get_json()["token"]
