def test_list_users_with_pagination(client, admin_token):
    resp = client.get(
        "/users?limit=5&offset=0",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "users" in data, f"Resposta inesperada: {data}"
    users = data["users"]
    assert isinstance(users, list), f"Campo 'users' não é lista: {users}"
    assert (
        len(users) <= 5
    ), f"Foram retornados mais de 5 usuários: {len(users)}"


def test_filter_users_by_name(client, admin_token):
    resp = client.get(
        "/users?name=admin", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "users" in data, f"Resposta inesperada: {data}"
    users = data["users"]
    assert isinstance(users, list), f"Campo 'users' não é lista: {users}"
    assert any(
        "admin" in user["username"] for user in users
    ), f"Nenhum usuário com 'admin' no username: {users}"
