import uuid
from models.user import User


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def unique_username(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def unique_email(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex}@test.com"


def test_get_user_404(client, admin_token):
    resp = client.get("/users/99999", headers=auth_header(admin_token))
    assert resp.status_code in {401, 404}


def test_update_user_404(client, admin_token):
    resp = client.put("/users/99999",
                      headers=auth_header(admin_token),
                      json={"username": "newname"})
    assert resp.status_code == 404


def test_delete_user_404(client, admin_token):
    resp = client.delete("/users/99999", headers=auth_header(admin_token))
    assert resp.status_code == 404


def test_create_user_duplicate_email_username(client):
    # Cria usuário com dados únicos
    username = unique_username("userdup")
    email = unique_email("dup")
    client.post("/users",
                json={
                    "username": username,
                    "email": email,
                    "password": "Senha1234"
                })
    # Tenta criar com mesmo email
    resp1 = client.post(
        "/users",
        json={
            "username": "otheruser",
            "email": email,
            "password": "Senha1234"
        },
    )
    assert resp1.status_code == 400
    # Tenta criar com mesmo username
    resp2 = client.post(
        "/users",
        json={
            "username": username,
            "email": unique_email("otheremail"),
            "password": "Senha1234",
        },
    )
    assert resp2.status_code == 400


def test_create_admin_without_auth(client):
    resp = client.post(
        "/users",
        json={
            "username": unique_username("admin2"),
            "email": unique_email("admin2"),
            "password": "Admin1234",
            "role": "admin",
        },
    )
    assert resp.status_code == 403


def test_create_user_weak_password(client):
    resp = client.post(
        "/users",
        json={
            "username": unique_username("weakuser"),
            "email": unique_email("weak"),
            "password": "123",
        },
    )
    assert resp.status_code == 400


def test_login_wrong_password(client):
    username = unique_username("loginuser")
    email = unique_email("login")
    client.post("/users",
                json={
                    "username": username,
                    "email": email,
                    "password": "Senha1234"
                })
    resp = client.post("/login", json={"email": email, "password": "errada"})
    assert resp.status_code == 401


def test_get_me(client):
    username = unique_username("meuser")
    email = unique_email("me")
    # Cria usuário via API e faz login
    client.post("/users",
                json={
                    "username": username,
                    "email": email,
                    "password": "Senha1234"
                })
    login = client.post("/login",
                        json={
                            "email": email,
                            "password": "Senha1234"
                        })
    token = login.get_json()["token"]
    resp = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.get_json()["username"] == username


def test_get_venue_404(client):
    resp = client.get("/venues/99999")
    assert resp.status_code == 404


def test_update_venue_404(client, admin_token):
    resp = client.put(
        "/venues/99999",
        headers=auth_header(admin_token),
        json={
            "name": "n",
            "address": "a"
        },
    )
    assert resp.status_code == 404


def test_delete_venue_404(client, admin_token):
    resp = client.delete("/venues/99999", headers=auth_header(admin_token))
    assert resp.status_code == 404


def test_create_venue_missing_fields(client, admin_token):
    resp = client.post("/venues",
                       headers=auth_header(admin_token),
                       json={"address": "Rua A"})
    assert resp.status_code == 400


def test_events_invalid_date(client):
    resp = client.get("/events?date=12-31-2025")
    assert resp.status_code == 400


def test_get_event_404(client):
    resp = client.get("/events/99999")
    assert resp.status_code == 404


def test_update_event_404(client, admin_token):
    resp = client.put("/events/99999",
                      headers=auth_header(admin_token),
                      json={"name": "novo"})
    assert resp.status_code == 404


def test_delete_event_404(client, admin_token):
    resp = client.delete("/events/99999", headers=auth_header(admin_token))
    assert resp.status_code == 404


def test_create_event_invalid_venue(client, admin_token):
    resp = client.post(
        "/events",
        headers=auth_header(admin_token),
        json={
            "name": "Evento X",
            "date": "2025-12-12",
            "venue_id": 99999
        },
    )
    assert resp.status_code == 400


def test_update_event_invalid_venue(client, admin_token):
    # Cria um venue via API
    resp = client.post(
        "/venues",
        headers=auth_header(admin_token),
        json={
            "name": "v1",
            "address": "a1"
        },
    )
    venue_id = resp.get_json()["id"]
    # Cria evento via API
    resp2 = client.post(
        "/events",
        headers=auth_header(admin_token),
        json={
            "name": "Evento Y",
            "date": "2025-12-12",
            "venue_id": venue_id
        },
    )
    event_id = resp2.get_json()["id"]
    # Atualiza para venue inexistente
    resp3 = client.put(
        f"/events/{event_id}",
        headers=auth_header(admin_token),
        json={"venue_id": 99999},
    )
    assert resp3.status_code == 400


def test_update_event_forbidden(client):
    # Cria user1 via API
    username1 = unique_username("u1")
    email1 = unique_email("u1")
    client.post("/users",
                json={
                    "username": username1,
                    "email": email1,
                    "password": "Senha1234"
                })
    login1 = client.post("/login",
                         json={
                             "email": email1,
                             "password": "Senha1234"
                         })
    token1 = login1.get_json()["token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    # Cria user2 via API
    username2 = unique_username("u2")
    email2 = unique_email("u2")
    client.post("/users",
                json={
                    "username": username2,
                    "email": email2,
                    "password": "Senha1234"
                })
    login2 = client.post("/login",
                         json={
                             "email": email2,
                             "password": "Senha1234"
                         })
    token2 = login2.get_json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    # Cria venue via API
    resp = client.post("/venues",
                       headers=headers1,
                       json={
                           "name": "v1",
                           "address": "a1"
                       })
    venue_id = resp.get_json()["id"]
    # Cria evento com user1
    resp2 = client.post(
        "/events",
        headers=headers1,
        json={
            "name": "E",
            "date": "2025-12-12",
            "venue_id": venue_id
        },
    )
    event_id = resp2.get_json()["id"]
    # user2 tenta atualizar evento de user1
    resp3 = client.put(f"/events/{event_id}",
                       headers=headers2,
                       json={"name": "novo"})
    assert resp3.status_code == 403


def test_delete_event_forbidden(client):
    # Cria user1 via API
    username1 = unique_username("u3")
    email1 = unique_email("u3")
    client.post("/users",
                json={
                    "username": username1,
                    "email": email1,
                    "password": "Senha1234"
                })
    login1 = client.post("/login",
                         json={
                             "email": email1,
                             "password": "Senha1234"
                         })
    token1 = login1.get_json()["token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    # Cria user2 via API
    username2 = unique_username("u4")
    email2 = unique_email("u4")
    client.post("/users",
                json={
                    "username": username2,
                    "email": email2,
                    "password": "Senha1234"
                })
    login2 = client.post("/login",
                         json={
                             "email": email2,
                             "password": "Senha1234"
                         })
    token2 = login2.get_json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    # Cria venue via API
    resp = client.post("/venues",
                       headers=headers1,
                       json={
                           "name": "v1",
                           "address": "a1"
                       })
    venue_id = resp.get_json()["id"]
    # Cria evento com user1
    resp2 = client.post(
        "/events",
        headers=headers1,
        json={
            "name": "E",
            "date": "2025-12-12",
            "venue_id": venue_id
        },
    )
    event_id = resp2.get_json()["id"]
    # user2 tenta deletar evento de user1
    resp3 = client.delete(f"/events/{event_id}", headers=headers2)
    assert resp3.status_code == 403


# Testa métodos auxiliares de models/user.py


def test_user_repr_eq():
    u1 = User(username="a", email="a@a.com", password_hash="h", role="user")
    u2 = User(username="a", email="a@a.com", password_hash="h", role="user")
    u3 = User(username="b", email="b@b.com", password_hash="h", role="user")
    assert repr(u1)
    assert u1 == u2
    assert not (u1 == u3)
