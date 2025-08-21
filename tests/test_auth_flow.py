import pytest

def test_login_with_expired_token(client, token_expiry):
    # Testa que o token expirado retorna 401 sem sleep
    resp = client.get("/users/me", headers={"Authorization": f"Bearer {token_expiry}"})
    assert resp.status_code == 401

def test_login_with_malformed_token(client):
    resp = client.get("/users/me", headers={"Authorization": "Bearer abc.def.ghi"})
    assert resp.status_code == 401

def test_refresh_token_flow(client, user_token, refresh_token):
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "token" in resp.get_json()