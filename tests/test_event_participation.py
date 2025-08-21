import pytest

def create_event_for_user(client, user_token):
    # Cria venue
    venue_resp = client.post("/venues", json={"name": "V", "address": "A"}, headers={"Authorization": f"Bearer {user_token}"})
    venue_id = venue_resp.get_json()["id"]
    # Cria evento
    event_resp = client.post("/events", json={"name": "E", "date": "2025-12-12", "venue_id": venue_id}, headers={"Authorization": f"Bearer {user_token}"})
    event_id = event_resp.get_json()["id"]
    return event_id

def test_user_can_participate_event(client, user_token):
    event_id = create_event_for_user(client, user_token)
    resp = client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200

def test_user_cannot_participate_twice(client, user_token):
    event_id = create_event_for_user(client, user_token)
    client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    resp = client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 400

def test_cancel_participation(client, user_token):
    event_id = create_event_for_user(client, user_token)
    client.post(f"/events/{event_id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    resp = client.post(f"/events/{event_id}/cancel", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200