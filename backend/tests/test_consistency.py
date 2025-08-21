

def test_delete_user_removes_events_and_participations(client, admin_token, make_user_token):
    # Cria usuário e eventos/participações
    user_token = make_user_token("cascadetest")
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/venues", json={"name": "V", "address": "A"}, headers=headers)
    venue_id = resp.get_json()["id"]
    resp2 = client.post("/events", json={"name": "E", "date": "2025-12-12", "venue_id": venue_id}, headers=headers)
    event_id = resp2.get_json()["id"]
    # Participa do evento
    client.post(f"/events/{event_id}/participate", headers=headers)
    # Deleta usuário via admin
    users_list = client.get("/users", headers={"Authorization": f"Bearer {admin_token}"}).get_json()["users"]
    user_id = users_list[-1]["id"]
    resp3 = client.delete(f"/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp3.status_code == 200
    # Tenta acessar evento/participação do usuário deletado
    resp4 = client.get(f"/events/{event_id}")
    assert resp4.status_code in (404, 410)  # Pode ser 410 Gone se removido em cascata


def test_delete_event_removes_participations(client, user_token):
    # Cria venue e evento
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/venues", json={"name": "V", "address": "A"}, headers=headers)
    venue_id = resp.get_json()["id"]
    resp2 = client.post("/events", json={"name": "E", "date": "2025-12-12", "venue_id": venue_id}, headers=headers)
    event_id = resp2.get_json()["id"]
    # Participa do evento
    client.post(f"/events/{event_id}/participate", headers=headers)
    # Deleta evento
    resp3 = client.delete(f"/events/{event_id}", headers=headers)
    assert resp3.status_code == 200
    # Tenta acessar participação
    resp4 = client.get(f"/events/{event_id}/participants", headers=headers)
    assert resp4.status_code in (404, 410)
