import uuid


def test_filter_events_by_creator(client, admin_token):
    unique_str = str(uuid.uuid4())
    username = f"creator_{unique_str}"
    email = f"{unique_str}@gmail.com"  # Domínio válido!

    user_resp = client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": "Senha1234@",
        },
    )
    assert user_resp.status_code == 201
    user_id = user_resp.get_json()["id"]

    login_resp = client.post(
        "/login",
        json={
            "email": email,
            "password": "Senha1234@",
        },
    )
    creator_token = login_resp.get_json()["token"]

    venue_resp = client.post(
        "/venues",
        json={"name": "V", "address": "A"},
        headers={"Authorization": f"Bearer {creator_token}"},
    )
    venue_id = venue_resp.get_json()["id"]
    client.post(
        "/events",
        json={"name": "E", "date": "2025-12-12", "venue_id": venue_id},
        headers={"Authorization": f"Bearer {creator_token}"},
    )

    resp = client.get(
        f"/events?creator_id={user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    for event in resp.get_json():
        assert event.get("creator_id", event.get("owner_id")) == user_id
