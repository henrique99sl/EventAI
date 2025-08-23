import time
import pytest

def test_bulk_create_users_and_events(client):
    start = time.time()
    tokens = []
    for i in range(20):
        resp = client.post(
            "/users",
            json={
                "username": f"user{i}",
                "email": f"user{i}@mail.com",
                "password": "StrongPass1",
            },
        )
        assert resp.status_code == 201
        login = client.post("/login",
                            json={
                                "email": f"user{i}@mail.com",
                                "password": "StrongPass1"
                            })
        tokens.append(login.get_json()["token"])
    for token in tokens:
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.post("/venues",
                           json={
                               "name": "V",
                               "address": "A"
                           },
                           headers=headers)
        venue_id = resp.get_json()["id"]
        for j in range(5):
            resp2 = client.post(
                "/events",
                json={
                    "name": f"E{j}",
                    "date": "2025-12-12",
                    "venue_id": venue_id
                },
                headers=headers,
            )
            assert resp2.status_code == 201
    elapsed = time.time() - start
    # Ajuste para CI/CD: tolerância maior
    assert elapsed < 12  # Aceita até 12 segundos para performance

def test_events_pagination(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/venues",
                       json={
                           "name": "V",
                           "address": "A"
                       },
                       headers=headers)
    venue_id = resp.get_json()["id"]
    for i in range(30):
        client.post(
            "/events",
            json={
                "name": f"E{i}",
                "date": "2025-12-12",
                "venue_id": venue_id
            },
            headers=headers,
        )
    resp2 = client.get("/events?limit=10&offset=0", headers=headers)
    assert resp2.status_code == 200
    assert len(resp2.get_json()) == 10