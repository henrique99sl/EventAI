def test_full_flow(client):
    # Criação de usuário
    resp = client.post("/users",
                       json={
                           "username": "flowuser",
                           "email": "flowuser@gmail.com",
                           "password": "SenhaF0rte!"
                       })
    print("USER CREATE RESPONSE:", resp.get_json())
    assert resp.status_code == 201

    # Login
    resp = client.post("/login",
                       json={
                           "email": "flowuser@gmail.com",
                           "password": "SenhaF0rte!"
                       })
    print("LOGIN RESPONSE:", resp.get_json())
    assert resp.status_code == 200
    token = resp.get_json()["token"]

    # Criação de venue
    venue_resp = client.post("/venues",
                             json={
                                 "name": "Venue Flow",
                                 "address": "Rua Flow"
                             },
                             headers={"Authorization": f"Bearer {token}"})
    assert venue_resp.status_code == 201
    venue_id = venue_resp.get_json()["id"]

    # Criação de evento
    resp = client.post("/events",
                       json={
                           "name": "Evento Flow",
                           "date": "2025-08-13",
                           "venue_id": venue_id
                       },
                       headers={"Authorization": f"Bearer {token}"})
    print("EVENT CREATE RESPONSE:", resp.get_json())
    assert resp.status_code == 201
    event_id = resp.get_json()["id"]

    # Participação
    resp = client.post(f"/events/{event_id}/participate",
                       headers={"Authorization": f"Bearer {token}"})
    print("PARTICIPATION RESPONSE:", resp.get_json())
    assert resp.status_code == 200

    # Listagem
    resp = client.get("/events", headers={"Authorization": f"Bearer {token}"})
    print("EVENT LIST RESPONSE:", resp.get_json())
    events = resp.get_json() if isinstance(
        resp.get_json(), list) else resp.get_json().get("events", [])
    assert any(ev["id"] == event_id for ev in events)
