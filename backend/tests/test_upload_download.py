import io
import os


def test_upload_image_to_event(client, user_token):
    # Garante que a pasta 'uploads' existe
    os.makedirs("uploads", exist_ok=True)

    # Cria venue e evento
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post(
        "/venues", json={"name": "V", "address": "A"}, headers=headers
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.post(
        "/events",
        json={"name": "E", "date": "2025-12-12", "venue_id": venue_id},
        headers=headers,
    )
    event_id = resp2.get_json()["id"]
    # Faz upload de imagem
    img = (io.BytesIO(b"fakeimagedata"), "event.png")
    data = {"file": img}
    resp3 = client.post(
        f"/events/{event_id}/upload",
        data=data,
        content_type="multipart/form-data",
        headers=headers,
    )
    assert resp3.status_code == 201
    # Faz download
    resp4 = client.get(f"/events/{event_id}/image", headers=headers)
    assert resp4.status_code == 200
    assert resp4.content_type.startswith("image/")

    # Limpa o arquivo após o teste para evitar interferência em outros testes
    file_path = f"uploads/event_{event_id}_event.png"
    if os.path.exists(file_path):
        os.remove(file_path)


def test_upload_invalid_file_type(client, user_token):
    # Garante que a pasta 'uploads' existe
    os.makedirs("uploads", exist_ok=True)

    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post(
        "/venues", json={"name": "V", "address": "A"}, headers=headers
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.post(
        "/events",
        json={"name": "E", "date": "2025-12-12", "venue_id": venue_id},
        headers=headers,
    )
    event_id = resp2.get_json()["id"]
    # Upload de arquivo texto
    txt = (io.BytesIO(b"not an image"), "file.txt")
    data = {"file": txt}
    resp3 = client.post(
        f"/events/{event_id}/upload",
        data=data,
        content_type="multipart/form-data",
        headers=headers,
    )
    assert resp3.status_code == 400
