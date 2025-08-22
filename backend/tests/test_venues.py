def register_and_login(client,
                       username="venueuser",
                       email="venueuser@gmail.com",
                       password="StrongPass1"):
    """Registra e faz login, retornando o token JWT."""
    client.post(
        "/users",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": "user",
        },
    )
    resp = client.post("/login", json={"email": email, "password": password})
    return resp.get_json()["token"]


def test_create_venue(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "Auditório Central",
            "address": "Rua do Parque"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Auditório Central"
    assert data["address"] == "Rua do Parque"


def test_create_venue_missing_fields(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={"name": "Sem endereço"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400
    assert "obrigatório" in resp.get_json()["error"].lower()


def test_get_venues(client):
    token = register_and_login(client)
    # Cria 2 venues
    client.post(
        "/venues",
        json={
            "name": "A",
            "address": "Rua A"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/venues",
        json={
            "name": "B",
            "address": "Rua B"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = client.get("/venues")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_venue_by_id(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "Centro 1",
            "address": "Rua 1"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.get(f"/venues/{venue_id}")
    assert resp2.status_code == 200
    assert resp2.get_json()["name"] == "Centro 1"


def test_update_venue(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "Velho",
            "address": "Endereço antigo"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp.get_json()["id"]

    # Atualiza
    resp2 = client.put(
        f"/venues/{venue_id}",
        json={
            "name": "Novo Nome",
            "address": "Novo Endereço"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data["name"] == "Novo Nome"
    assert data["address"] == "Novo Endereço"


def test_delete_venue(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "A Deletar",
            "address": "Rua"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.delete(f"/venues/{venue_id}",
                          headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    # Não encontra mais
    resp3 = client.get(f"/venues/{venue_id}")
    assert resp3.status_code == 404


def test_update_venue_invalid_id(client):
    token = register_and_login(client)
    resp = client.put(
        "/venues/9999",
        json={
            "name": "Nao existe",
            "address": "Algum endereço"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_delete_venue_invalid_id(client):
    token = register_and_login(client)
    resp = client.delete("/venues/9999",
                         headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404


def test_create_venue_unauthenticated(client):
    resp = client.post("/venues", json={"name": "Sem Auth", "address": "Rua"})
    assert resp.status_code == 401


def test_get_venue_nonexistent(client):
    resp = client.get("/venues/99999")
    assert resp.status_code == 404


def test_update_venue_missing_fields(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "Teste",
            "address": "Rua"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.put(f"/venues/{venue_id}",
                       json={},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 400


def test_delete_venue_unauthenticated(client):
    token = register_and_login(client)
    resp = client.post(
        "/venues",
        json={
            "name": "Para deletar",
            "address": "Rua"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = resp.get_json()["id"]
    resp2 = client.delete(f"/venues/{venue_id}")
    assert resp2.status_code == 401
