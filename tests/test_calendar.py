from datetime import date, timedelta


def test_calendar_returns_events_in_interval(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Cria venue
    resp_venue = client.post("/venues", json={"name": "Test Venue", "address": "Test Address"}, headers=headers)
    venue_id = resp_venue.get_json()["id"]

    # Cria eventos em datas diferentes
    today = date.today()
    event_dates = [today, today + timedelta(days=1), today + timedelta(days=2)]
    event_ids = []
    for i, d in enumerate(event_dates):
        _resp_event = client.post(
            "/events",
            json={"name": f"Event {i}", "date": d.isoformat(), "venue_id": venue_id},
            headers=headers
        )
        event_ids.append(_resp_event.get_json()["id"])

    # Consulta calendário para o intervalo
    start = today.isoformat()
    end = (today + timedelta(days=2)).isoformat()
    resp = client.get(f"/events/calendar?start={start}&end={end}", headers=headers)
    assert resp.status_code == 200
    events = resp.get_json()
    names = [ev["name"] for ev in events]
    assert set(names) == {"Event 0", "Event 1", "Event 2"}


def test_calendar_excludes_events_outside_interval(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Cria venue e evento fora do intervalo
    resp_venue = client.post("/venues", json={"name": "Another Venue", "address": "Another Address"}, headers=headers)
    venue_id = resp_venue.get_json()["id"]
    client.post(
        "/events",
        json={"name": "Out of Interval Event", "date": "2100-01-01", "venue_id": venue_id},
        headers=headers
    )
    # Consulta intervalo que não inclui este evento
    today = date.today()
    resp = client.get(
        f"/events/calendar?start={today.isoformat()}&end={(today + timedelta(days=7)).isoformat()}",
        headers=headers
    )
    assert resp.status_code == 200
    events = resp.get_json()
    assert all(ev["name"] != "Out of Interval Event" for ev in events)


def test_calendar_event_structure(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Cria venue e evento
    resp_venue = client.post("/venues", json={"name": "Struct Venue", "address": "Struct Address"}, headers=headers)
    venue_id = resp_venue.get_json()["id"]
    client.post(
        "/events",
        json={"name": "Structure Test", "date": date.today().isoformat(), "venue_id": venue_id},
        headers=headers
    )
    resp = client.get(
        f"/events/calendar?start={date.today().isoformat()}&end={date.today().isoformat()}",
        headers=headers
    )
    assert resp.status_code == 200
    events = resp.get_json()
    for ev in events:
        assert "id" in ev
        assert "name" in ev
        assert "date" in ev or "start" in ev
        assert "venue" in ev or "venue_id" in ev
