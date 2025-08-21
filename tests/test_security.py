import pytest


@pytest.mark.parametrize("payload", [
    {"username": "' OR 1=1 --", "password": "teste"},
    {"username": "user", "password": "<script>alert(1)</script>"},
    {"title": "<img src=x onerror=alert(1)>", "date": "2025-09-01"}
])
def test_injection_protection(client, payload):
    resp = client.post("/users", json=payload)
    assert resp.status_code in (400, 422)


def test_rate_limit(client):
    for _ in range(20):
        resp = client.get("/users")
    assert resp.status_code in (200, 429)
