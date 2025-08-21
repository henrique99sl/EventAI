import pytest

def test_update_user_details(client, user_token):
    new_data = {"name": "Novo Nome", "email": "novo@email.com"}
    resp = client.put("/users/me", json=new_data, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Novo Nome"
    assert resp.get_json()["email"] == "novo@email.com"

def test_update_user_invalid_email(client, user_token):
    resp = client.put("/users/me", json={"email": "emailinvalido"}, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 422

def test_change_password(client, user_token):
    # Corrige o old_password para o correto conforme user fixture
    data = {"old_password": "User1234", "new_password": "NovaSenhaF0rte!"}
    resp = client.post("/users/change-password", json=data, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200

def test_change_password_weak(client, user_token):
    data = {"old_password": "User1234", "new_password": "123"}
    resp = client.post("/users/change-password", json=data, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 422

def test_user_cannot_update_other_user(client, admin_token):
    # Tenta atualizar outro usuário sem permissão
    resp = client.put("/users/999", json={"name": "Hacker"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code in (403, 404)