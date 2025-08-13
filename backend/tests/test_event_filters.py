import pytest

def test_filter_events_by_date(client, user_token):
    resp = client.get("/events?date=2025-09-01", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    for event in resp.json()["events"]:
        assert event["date"].startswith("2025-09-01")

def test_filter_events_by_creator(client, admin_token, user):
    resp = client.get(f"/events?creator_id={user['id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    for event in resp.json()["events"]:
        assert event["creator_id"] == user["id"]