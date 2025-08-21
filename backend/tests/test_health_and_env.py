import os


def test_healthcheck_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "status" in data
    assert data["status"] == "ok"


def test_readiness_probe(client):
    resp = client.get("/readiness")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("ready") is True


def test_liveness_probe(client):
    resp = client.get("/liveness")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("alive") is True


def test_environment_variables_present():
    # Testa se variáveis essenciais estão setadas (ajuste nomes conforme sua app)
    assert os.getenv("DATABASE_URL") is not None
    assert os.getenv("SECRET_KEY") is not None
    assert os.getenv("JWT_SECRET_KEY") is not None
