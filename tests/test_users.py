
def test_register_and_login(client):
    resp = client.post("/users", json={
        "username": "test", "email": "test@gmail.com", "password": "StrongPass1"
    })
    assert resp.status_code == 201
    # Login
    resp2 = client.post("/login", json={"email": "test@gmail.com", "password": "StrongPass1"})
    assert resp2.status_code == 200
    assert "token" in resp2.get_json()


def test_create_user_missing_fields(client):
    resp = client.post("/users", json={"email": "x@gmail.com"})
    assert resp.status_code == 400


def test_create_user_duplicate_username(client):
    client.post("/users", json={"username": "dup", "email": "dup1@gmail.com", "password": "StrongPass1"})
    resp = client.post("/users", json={"username": "dup", "email": "dup2@gmail.com", "password": "StrongPass1"})
    assert resp.status_code == 400


def test_admin_can_delete_user(client, admin_token):
    # Cria normal user
    client.post("/users", json={"username": "worker", "email": "worker@gmail.com", "password": "StrongPass1"})
    users = client.get("/users").get_json()["users"]
    user = users[-1]
    resp = client.delete(f"/users/{user['id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200


def test_delete_user_requires_admin(client, user_token):
    # Cria outro usuário
    client.post("/users", json={"username": "other", "email": "other@gmail.com", "password": "StrongPass1"})
    users = client.get("/users").get_json()["users"]
    user_id = users[-1]["id"]
    resp = client.delete(f"/users/{user_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 403


def test_get_nonexistent_user(client, admin_token):
    resp = client.get("/users/99999", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 404
