import pytest

def test_list_users_with_pagination(client, admin_token):
    resp = client.get("/users?limit=5&offset=0", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert "users" in resp.json()
    assert len(resp.json()["users"]) <= 5

def test_filter_users_by_name(client, admin_token):
    resp = client.get("/users?name=admin", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    users = resp.json()["users"]
    assert any("admin" in user["username"] for user in users)