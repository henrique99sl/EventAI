import time


def test_token_expiry_and_refresh(client):
    # Criação de usuário
    resp = client.post("/users", json={"username": "expuser", "email": "expuser@gmail.com", "password": "Senha1234@"})
    assert resp.status_code == 201

    # Login com expiração curta do token
    login_resp = client.post("/login", json={"email": "expuser@gmail.com", "password": "Senha1234@", "expires_in": 1})
    assert login_resp.status_code == 200
    token = login_resp.get_json()["token"]

    # Aguarda expirar
    time.sleep(2)
    resp = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401  # Token expirado

    # Testa refresh token (dummy)
    refresh_resp = client.post("/auth/refresh", json={"refresh_token": "dummy-refresh-token"})
    assert refresh_resp.status_code == 200
    new_token = refresh_resp.get_json()["token"]
    assert isinstance(new_token, str)
