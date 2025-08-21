

def test_register_and_login(client):
    resp = client.post(
        "/users",
        json={"username": "test", "email": "test@gmail.com", "password": "StrongPass1"},
    )
    assert resp.status_code == 201, f"Falha ao criar usuário: {resp.get_json()}"
    # Login
    resp2 = client.post(
        "/login", json={"email": "test@gmail.com", "password": "StrongPass1"}
    )
    assert resp2.status_code == 200, f"Falha ao logar: {resp2.get_json()}"
    assert "token" in resp2.get_json(), f"Token não retornado: {resp2.get_json()}"


def test_create_user_missing_fields(client):
    resp = client.post("/users", json={"email": "x@gmail.com"})
    assert (
        resp.status_code == 400
    ), f"Deveria retornar 400 para campos faltando, veio {resp.status_code}: {resp.get_json()}"


def test_create_user_duplicate_username(client):
    resp1 = client.post(
        "/users",
        json={"username": "dup", "email": "dup1@gmail.com", "password": "StrongPass1"},
    )
    assert resp1.status_code == 201, f"Não criou usuário inicial: {resp1.get_json()}"
    resp2 = client.post(
        "/users",
        json={"username": "dup", "email": "dup2@gmail.com", "password": "StrongPass1"},
    )
    assert (
        resp2.status_code == 400
    ), f"Deveria retornar 400 para username duplicado, veio {resp2.status_code}: {resp2.get_json()}"


def test_admin_can_delete_user(client, admin_token):
    # Cria normal user
    resp = client.post(
        "/users",
        json={
            "username": "worker",
            "email": "worker@gmail.com",
            "password": "StrongPass1",
        },
    )
    assert resp.status_code == 201, f"Erro ao criar worker: {resp.get_json()}"
    user_id = resp.get_json()["id"]
    resp_del = client.delete(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert (
        resp_del.status_code == 200
    ), f"Admin não conseguiu deletar user: {resp_del.get_json()}"


def test_delete_user_requires_admin(client, user_token):
    # Cria outro usuário
    resp = client.post(
        "/users",
        json={
            "username": "other",
            "email": "other@gmail.com",
            "password": "StrongPass1",
        },
    )
    assert resp.status_code == 201, f"Erro ao criar other: {resp.get_json()}"
    user_id = resp.get_json()["id"]
    resp_del = client.delete(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp_del.status_code in (
        403,
        404,
    ), f"User comum conseguiu deletar user: {resp_del.get_json()}"


def test_get_nonexistent_user(client, admin_token):
    resp = client.get(
        "/users/99999", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert (
        resp.status_code == 404
    ), f"Usuário inexistente retornou {resp.status_code}: {resp.get_json()}"
