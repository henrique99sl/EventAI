

def test_filter_events_by_date(client, user_token):
    resp = client.get(
        "/events?date=2025-09-01", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    # Aceita tanto lista direta quanto dict com chave 'events'
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict) and "events" in data:
        events = data["events"]
    else:
        events = []
    # Testa cada evento retornado
    for event in events:
        assert str(event.get("date", ""))[:10] == "2025-09-01"


def test_filter_events_by_creator(client, admin_token, user):
    resp = client.get(
        f"/events?creator_id={user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict) and "events" in data:
        events = data["events"]
    else:
        events = []
    for event in events:
        cid = event.get("creator_id", event.get("owner_id"))
        assert cid == user.id, f"Criador inesperado: {cid}, esperado: {user.id}"
