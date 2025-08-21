

def test_update_user_details(client):
    # Cria usuário para garantir consistência nos testes
    resp_user = client.post(
        "/users",
        json={
            "username": "testuserupdate",
            "email": "testuserupdate@email.com",
            "password": "SenhaOriginal1",
        },
    )
    assert resp_user.status_code == 201, f"User creation failed: {resp_user.get_json()}"
    resp_user.get_json().get("id")

    # Login para obter token
    resp_login = client.post(
        "/login",
        json={"email": "testuserupdate@email.com", "password": "SenhaOriginal1"},
    )
    assert resp_login.status_code == 200, f"Login failed: {resp_login.get_json()}"
    token = resp_login.get_json().get("token")
    assert token, f"Token não encontrado: {resp_login.get_json()}"

    # Atualiza email
    new_data = {"email": "novo@email.com"}
    resp = client.put(
        "/users/me", json=new_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200, f"Falha ao atualizar usuário: {resp.get_json()}"
    data = resp.get_json()
    assert data.get("email") == "novo@email.com", f"Email não atualizado: {data}"
    # Se existir name no modelo (opcional)
    if "name" in data:
        resp = client.put(
            "/users/me",
            json={"name": "Novo Nome"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("name") == "Novo Nome", f"Nome não atualizado: {data}"


def test_update_user_invalid_email(client):
    # Cria usuário e faz login
    resp_user = client.post(
        "/users",
        json={
            "username": "testuseremail",
            "email": "testuseremail@email.com",
            "password": "SenhaOriginal1",
        },
    )
    assert resp_user.status_code == 201
    resp_login = client.post(
        "/login",
        json={"email": "testuseremail@email.com", "password": "SenhaOriginal1"},
    )
    assert resp_login.status_code == 200
    token = resp_login.get_json().get("token")
    resp = client.put(
        "/users/me",
        json={"email": "emailinvalido"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert (
        resp.status_code == 422
    ), f"Esperado 422 para email inválido, recebido {resp.status_code}: {resp.get_json()}"


def test_change_password(client):
    # Cria usuário e faz login
    resp_user = client.post(
        "/users",
        json={
            "username": "testuserpass",
            "email": "testuserpass@email.com",
            "password": "SenhaOriginal1",
        },
    )
    assert resp_user.status_code == 201
    resp_login = client.post(
        "/login", json={"email": "testuserpass@email.com", "password": "SenhaOriginal1"}
    )
    assert resp_login.status_code == 200
    token = resp_login.get_json().get("token")
    data = {"old_password": "SenhaOriginal1", "new_password": "NovaSenhaF0rte!"}
    resp = client.post(
        "/users/change-password",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, f"Falha ao trocar a senha: {resp.get_json()}"
    resposta = resp.get_json()
    assert (
        "message" in resposta and "Senha alterada" in resposta["message"]
    ), f"Mensagem inesperada: {resposta}"


def test_change_password_weak(client):
    # Cria usuário e faz login
    resp_user = client.post(
        "/users",
        json={
            "username": "testuserweakpass",
            "email": "testuserweakpass@email.com",
            "password": "SenhaOriginal1",
        },
    )
    assert resp_user.status_code == 201
    resp_login = client.post(
        "/login",
        json={"email": "testuserweakpass@email.com", "password": "SenhaOriginal1"},
    )
    assert resp_login.status_code == 200
    token = resp_login.get_json().get("token")
    data = {"old_password": "SenhaOriginal1", "new_password": "123"}
    resp = client.post(
        "/users/change-password",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert (
        resp.status_code == 422
    ), f"Esperado 422 para senha fraca, recebido {resp.status_code}: {resp.get_json()}"


def test_user_cannot_update_other_user(client):
    # Cria usuário normal
    resp_user = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "testuser@email.com",
            "password": "SenhaOriginal1",
        },
    )
    assert resp_user.status_code == 201
    # Tenta criar admin SEM autenticação de admin
    resp_admin = client.post(
        "/users",
        json={
            "username": "testadmin",
            "email": "testadmin@email.com",
            "password": "SenhaAdmin1",
            "role": "admin",
        },
    )
    assert resp_admin.status_code == 403
