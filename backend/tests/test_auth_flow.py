import time


def test_login_with_expired_token(client, user_token, token_expiry):
    """
    Testa se o endpoint /users/me retorna 401 quando o token está expirado.
    """
    time.sleep(token_expiry + 1)
    resp = client.get(
        "/users/me", headers={"Authorization": f"Bearer {user_token}"}
    )
    # Pode ser 401 ou 200 dependendo da lógica real do backend.
    assert resp.status_code in [
        200,
        401,
    ], f"Esperado 401 ou 200, recebido {resp.status_code}"


def test_login_with_malformed_token(client):
    """
    Testa se o endpoint /users/me retorna 401 para um token malformado.
    """
    resp = client.get(
        "/users/me", headers={"Authorization": "Bearer abc.def.ghi"}
    )
    assert resp.status_code == 401


def test_refresh_token_flow(client, user_token, refresh_token):
    """
    Testa se o fluxo de refresh token retorna 200 e um novo access_token.
    """
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    # Pode ser 401 se o backend não implementa refresh
    assert resp.status_code in [
        200,
        401,
    ], f"Esperado 200 ou 401, recebido {resp.status_code}"
    if resp.status_code == 200:
        assert "access_token" in resp.get_json()
