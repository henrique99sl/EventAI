def test_send_event_created_email(monkeypatch):
    # Mock do envio de email
    def fake_send_email(event):
        return True

    mock_send_email = fake_send_email
    assert mock_send_email("evento") is True


def test_event_creation_sends_email(client, user_token, mocker):
    mock_send_email = mocker.patch("app.send_event_created_email")
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/venues", json={"name": "V", "address": "A"}, headers=headers)
    venue_id = resp.get_json()["id"]
    event_resp = client.post("/events", json={"name": "E", "date": "2025-12-12", "venue_id": venue_id}, headers=headers)
    assert event_resp.status_code == 201
    mock_send_email.assert_called_once()


def test_notification_failure_does_not_block_event_creation(client, user_token, mocker):
    mock_send_email = mocker.patch("app.send_event_created_email", side_effect=Exception("Falhou"))
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/venues", json={"name": "V", "address": "A"}, headers=headers)
    venue_id = resp.get_json()["id"]
    event_resp = client.post("/events", json={"name": "E", "date": "2025-12-12", "venue_id": venue_id}, headers=headers)
    assert event_resp.status_code == 201
    mock_send_email.assert_called_once()
