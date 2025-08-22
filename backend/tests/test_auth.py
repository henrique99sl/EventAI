def test_login_success(client, admin_token):
    # admin_token fixture ensures user exists and login works
    assert admin_token is not None


def test_login_invalid_password(client):
    client.post(
        "/users",
        json={
            "username": "test",
            "email": "test@gmail.com",
            "password": "StrongPass1"
        },
    )
    resp = client.post("/login",
                       json={
                           "email": "test@gmail.com",
                           "password": "errada"
                       })
    assert resp.status_code == 401
    assert "error" in resp.get_json()


def test_protected_route_without_token(client):
    resp = client.get("/users/1")
    assert resp.status_code == 401


def test_protected_route_with_invalid_token(client):
    resp = client.get("/users/1",
                      headers={"Authorization": "Bearer token_invalido"})
    assert resp.status_code == 401


# Testar token expirado depende de como está implementado o tempo no JWT
