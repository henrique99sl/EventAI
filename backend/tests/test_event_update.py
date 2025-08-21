

def test_update_event_by_owner(client, user_token, event):
    data = {"title": "Novo Título"}
    resp = client.put(f"/events/{event.id}", json=data, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Novo Título"


def test_update_event_by_non_owner(client, admin_token, event):
    data = {"title": "Título Não Permitido"}
    resp = client.put(f"/events/{event.id}", json=data, headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code in (403, 404)
