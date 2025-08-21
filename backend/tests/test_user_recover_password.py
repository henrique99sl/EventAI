

<<<<<<< HEAD

@pytest.fixture
def user(client, unique_email, unique_username):
    """
    Cria e retorna um usuário persistido (email: user@email.com) para os testes de recuperação de senha.
    """
    email = "user@email.com"
    username = unique_username("user")
    password = "User1234"
    resp = client.post(
        "/users",
        json={"username": username, "email": email, "password": password},
    )
    assert resp.status_code == 201
    from models.user import User
    return User.query.filter_by(email=email).first()


def test_send_password_reset_email(client, user):
    resp = client.post("/users/recover-password", json={"email": user.email})
    assert resp.status_code == 200
=======
def test_send_password_reset_email(client):
    resp = client.post("/users/recover-password", json={"email": "user@email.com"})
    # O backend retorna 404 se o usuário não existe, 200 se existe.
    assert resp.status_code in (
        200,
        404,
    ), f"Status inesperado: {resp.status_code}, resposta: {resp.get_json()}"
    # Se existe um reset_token, valida formato:
    data = resp.get_json()
    if resp.status_code == 200:
        assert "reset_token" in data, f"reset_token não presente na resposta: {data}"
        assert isinstance(
            data["reset_token"], str
        ), f"reset_token não é string: {data['reset_token']}"

>>>>>>> recuperar-anterior


def test_recover_password_invalid_email(client):
    resp = client.post("/users/recover-password", json={"email": "naoexiste@email.com"})
    # O backend retorna 404 para email inexistente
    assert (
        resp.status_code == 404
    ), f"Status inesperado para email inválido: {resp.status_code}, resposta: {resp.get_json()}"


<<<<<<< HEAD
def test_reset_password_token_flow(client, user):
    # 1. Solicita token de recuperação
    resp = client.post("/users/recover-password", json={"email": user.email})
    assert resp.status_code == 200
    token = resp.get_json()["reset_token"]  # pega o token do endpoint
    # 2. Reseta senha
    resp2 = client.post("/users/reset-password", json={"token": token, "new_password": "SenhaNovaForte123"})
    assert resp2.status_code == 200
=======
def test_reset_password_token_flow(client):
    # Cria um usuário para testar
    email = "resetflow@teste.com"
    password = "SenhaF0rte123"
    resp_user = client.post(
        "/users",
        json={"username": "resetflowuser", "email": email, "password": password},
    )
    assert resp_user.status_code == 201, f"User creation failed: {resp_user.get_json()}"

    # Solicita token de recuperação
    resp = client.post("/users/recover-password", json={"email": email})
    assert resp.status_code == 200, f"Password reset request failed: {resp.get_json()}"
    data = resp.get_json()
    assert "reset_token" in data, f"reset_token não presente na resposta: {data}"
    token = data["reset_token"]

    # Reseta senha
    nova_senha = "SenhaNovaForte123"
    resp2 = client.post(
        "/users/reset-password", json={"token": token, "new_password": nova_senha}
    )
    assert resp2.status_code == 200, f"Password reset failed: {resp2.get_json()}"
    resp_login = client.post("/login", json={"email": email, "password": nova_senha})
    assert (
        resp_login.status_code == 200
    ), f"Login com senha nova falhou: {resp_login.get_json()}"
>>>>>>> recuperar-anterior
