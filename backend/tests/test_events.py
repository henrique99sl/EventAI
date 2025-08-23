def register_and_login(
    client, username="evuser", email="evuser@gmail.com", password="StrongPass1"
):
    client.post(
        "/users",
        json={"username": username, "email": email, "password": password},
    )
    login = client.post("/login", json={"email": email, "password": password})
    return login.get_json()["token"]


def test_create_and_filter_event(client):
    token = register_and_login(client)
    resp_venue = client.post(
        "/venues",
        json={"name": "Local Teste", "address": "Rua X"},
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp_venue.get_json()["id"]
    resp_event = client.post(
        "/events",
        json={"name": "Festa", "date": "2025-09-01", "venue_id": venue_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_event.status_code == 201
    resp = client.get("/events?name=Festa")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1
    resp2 = client.get("/events?date=2025-01-01")
    assert resp2.status_code == 200
    assert len(resp2.get_json()) == 0


def test_delete_nonexistent_event(client):
    token = register_and_login(client)
    resp = client.delete(
        "/events/99999", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 404


def test_update_event_without_permission(client):
    # user1 cria o evento
    token1 = register_and_login(client, username="u1", email="u1@gmail.com")
    venue = client.post(
        "/venues",
        json={"name": "v", "address": "a"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    venue_id = venue.get_json()["id"]
    event = client.post(
        "/events",
        json={"name": "e", "date": "2025-10-10", "venue_id": venue_id},
        headers={"Authorization": f"Bearer {token1}"},
    )
    event_id = event.get_json()["id"]

    # user2 tenta editar
    token2 = register_and_login(client, username="u2", email="u2@gmail.com")
    resp = client.put(
        f"/events/{event_id}",
        json={"name": "hack"},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert resp.status_code in (401, 403)
