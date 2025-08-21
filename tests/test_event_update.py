import pytest


@pytest.fixture
def event(client, user_token):
    resp = client.post("/events", json={
        "title": "Evento Teste",
        "description": "Descrição",
        "date": "2025-08-21T10:00:00",
        "venue_id": 1,
        "owner_id": 1
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 201
    return resp.get_json()
