import pytest

def test_user_can_participate_event(client, user_token, event):
    resp = client.post(f"/events/{event.id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200

def test_user_cannot_participate_twice(client, user_token, event):
    client.post(f"/events/{event.id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    resp = client.post(f"/events/{event.id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 400

def test_cancel_participation(client, user_token, event):
    client.post(f"/events/{event.id}/participate", headers={"Authorization": f"Bearer {user_token}"})
    resp = client.post(f"/events/{event.id}/cancel", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200