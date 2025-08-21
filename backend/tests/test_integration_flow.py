

def test_full_flow(client):
<<<<<<< HEAD
    # Criação de usuário
=======
    # Criação de usuário com email válido
>>>>>>> recuperar-anterior
    resp = client.post(
        "/users",
        json={
            "username": "flowuser",
<<<<<<< HEAD
            "email": "flowuser@gmail.com",
            "password": "SenhaF0rte!"})
    print("USER CREATE RESPONSE:", resp.get_json())
    assert resp.status_code == 201

    # Login
    resp = client.post("/login", json={"email": "flowuser@gmail.com", "password": "SenhaF0rte!"})
    print("LOGIN RESPONSE:", resp.get_json())
    assert resp.status_code == 200
    token = resp.get_json()["token"]

    # Criação de venue
    venue_resp = client.post(
        "/venues",
        json={
            "name": "Venue Flow",
            "address": "Rua Flow"},
        headers={
            "Authorization": f"Bearer {token}"})
    assert venue_resp.status_code == 201
    venue_id = venue_resp.get_json()["id"]

    # Criação de evento
    resp = client.post(
        "/events",
        json={
            "name": "Evento Flow",
            "date": "2025-08-13",
            "venue_id": venue_id},
        headers={
            "Authorization": f"Bearer {token}"})
    print("EVENT CREATE RESPONSE:", resp.get_json())
    assert resp.status_code == 201
    event_id = resp.get_json()["id"]

    # Participação
    resp = client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {token}"})
    print("PARTICIPATION RESPONSE:", resp.get_json())
    assert resp.status_code == 200

    # Listagem
    resp = client.get("/events", headers={"Authorization": f"Bearer {token}"})
    print("EVENT LIST RESPONSE:", resp.get_json())
    events = resp.get_json() if isinstance(resp.get_json(), list) else resp.get_json().get("events", [])
    assert any(ev["id"] == event_id for ev in events)
=======
            "email": "flowuser@test.com",
            "password": "SenhaF0rte!",
        },
    )
    assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
    resp.get_json().get("id")

    # Login por email
    resp_login = client.post(
        "/login", json={"email": "flowuser@test.com", "password": "SenhaF0rte!"}
    )
    assert resp_login.status_code == 200, f"Login failed: {resp_login.get_json()}"
    token = resp_login.get_json().get("token")
    assert token, f"Token não encontrado: {resp_login.get_json()}"

    # Criação de venue para usar venue_id, pois o evento exige venue_id
    resp_venue = client.post(
        "/venues",
        json={"name": "Venue Flow", "address": "Rua Teste, 123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert (
        resp_venue.status_code == 201
    ), f"Venue creation failed: {resp_venue.get_json()}"
    venue_id = resp_venue.get_json().get("id")
    assert venue_id, f"Venue ID não encontrado: {resp_venue.get_json()}"

    # Criação de evento com todos os campos obrigatórios (usa "name" ao invés de "title")
    resp = client.post(
        "/events",
        json={
            "name": "Evento Flow",  # <-- "name" é correto
            "date": "2025-08-13",
            "venue_id": venue_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201, f"Event creation failed: {resp.get_json()}"
    event_id = resp.get_json().get("id")
    assert event_id, f"ID do evento não encontrado: {resp.get_json()}"

    # Participação
    resp = client.post(
        f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200, f"Participate failed: {resp.get_json()}"

    # Listagem de eventos -- aceita tanto lista direta quanto dict com chave 'events'
    resp = client.get("/events", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    # Se a resposta for lista, usa direto. Se for dict, pega 'events'. Se for vazio, vira lista.
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict) and "events" in data:
        events = data["events"]
    else:
        events = []
    assert any(
        ev.get("id") == event_id for ev in events
    ), f"Evento {event_id} não encontrado: {events}"
>>>>>>> recuperar-anterior
