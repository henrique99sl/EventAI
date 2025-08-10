import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Hello" in resp.data  # Ajusta conforme o que a tua home retorna!