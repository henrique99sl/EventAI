import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test"
    })
    with app.test_client() as client:
        yield client

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}