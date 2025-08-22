import pytest


@pytest.fixture
def user(client, unique_email, unique_username):
    """
    Cria e retorna um usuário persistido (email: user@email.com)
    para os testes de recuperação de senha.
    """
    email = "user@email.com"
    username = unique_username("user")
    password = "User1234"
    resp = client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": password
        },
    )
    assert resp.status_code == 201
    from models.user import User
    return User.query.filter_by(email=email).first()


def test_send_password_reset_email(client, user):
    resp = client.post("/users/recover-password", json={"email": user.email})
    assert resp.status_code == 200


def test_recover_password_invalid_email(client):
    resp = client.post(
        "/users/recover-password",
        json={"email": "naoexiste@email.com"}
    )
    assert resp.status_code == 404


def test_reset_password_token_flow(client, user):
    # 1. Solicita token de recuperação
    resp = client.post("/users/recover-password", json={"email": user.email})
    assert resp.status_code == 200
    assert "reset_token" in resp.get_json(), (
        "Deve retornar reset_token"
    )
    token = resp.get_json()["reset_token"]  # pega o token do endpoint
    # 2. Reseta senha
    resp2 = client.post(
        "/users/reset-password",
        json={
            "token": token,
            "new_password": "SenhaNovaForte123"
        }
    )
    assert resp2.status_code == 200
