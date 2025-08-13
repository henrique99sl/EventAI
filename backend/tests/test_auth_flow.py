import pytest
import time

def test_login_with_expired_token(client, user_token, token_expiry):
    # Token expirado propositalmente
    time.sleep(token_expiry + 1)
    resp = client.get("/users/me", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 401

def test_login_with_malformed_token(client):
    resp = client.get("/users/me", headers={"Authorization": "Bearer abc.def.ghi"})
    assert resp.status_code == 401

def test_refresh_token_flow(client, user_token, refresh_token):
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()