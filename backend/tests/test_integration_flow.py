

def test_full_flow(client):
    # Criação de usuário
    resp = client.post("/users", json={"username": "flowuser", "email": "flow@a.com", "password": "SenhaF0rte!"})
    assert resp.status_code == 201
    # Login
    resp = client.post("/auth/login", data={"username": "flowuser", "password": "SenhaF0rte!"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    # Criação de evento
    resp = client.post("/events", json={"title": "Evento Flow", "date": "2025-08-13"},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    event_id = resp.json()["id"]
    # Participação
    resp = client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    # Listagem
    resp = client.get("/events", headers={"Authorization": f"Bearer {token}"})
    assert any(ev["id"] == event_id for ev in resp.json()["events"])
