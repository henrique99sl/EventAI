def test_event_venue_creation_atomicity(client, user_token, mocker):
    # Mocka a função de criação de evento para simular falha
    mocker.patch("app.create_event_logic", side_effect=Exception("fail"))
    venue_resp = client.post(
        "/venues",
        json={"name": "VAtomic", "address": "Rua Atomic"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    venue_id = venue_resp.get_json()["id"]

    # Tenta criar evento (vai falhar)
    event_resp = client.post(
        "/events",
        json={"name": "EAtomic", "date": "2026-01-01", "venue_id": venue_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert event_resp.status_code == 500 or event_resp.status_code == 400

    # Verifica que o evento não foi criado (atomicidade)
    events_resp = client.get(
        "/events", headers={"Authorization": f"Bearer {user_token}"}
    )
    events = events_resp.get_json()
    assert all(ev["name"] != "EAtomic" for ev in events)
