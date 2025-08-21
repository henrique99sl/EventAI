

def test_send_password_reset_email(client):
    resp = client.post("/users/recover-password", json={"email": "user@email.com"})
    assert resp.status_code == 200


def test_recover_password_invalid_email(client):
    resp = client.post("/users/recover-password", json={"email": "naoexiste@email.com"})
    assert resp.status_code == 404


def test_reset_password_token_flow(client, db, user):
    # Supondo endpoint de reset de senha por token
    # 1. Solicita token
    resp = client.post("/users/recover-password", json={"email": user.email})
    assert resp.status_code == 200
    token = db.get_reset_token_for_email(user.email)  # função hipotética
    # 2. Reseta senha
    resp2 = client.post("/users/reset-password", json={"token": token, "new_password": "SenhaNovaForte123"})
    assert resp2.status_code == 200
