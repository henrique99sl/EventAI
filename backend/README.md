![CI/CD](https://github.com/henrique99sl/EventAI/actions/workflows/ci-cd.yml/badge.svg)

# EventAI Backend

Este é o backend para o projeto **EventAI**, uma API RESTful desenvolvida em Flask para gerir utilizadores, eventos e locais (venues), com autenticação JWT, permissões de admin, documentação Swagger e testes automatizados.

---

## 🚀 Funcionalidades

- **Gestão de Utilizadores** (CRUD, admin, autenticação JWT, segurança de senha)
- **Gestão de Eventos** (CRUD, filtro por nome/data/venue)
- **Gestão de Locais (Venues)** (CRUD)
- **Permissões**: Apenas admin pode apagar utilizadores
- **Documentação Swagger**
- **Testes automatizados com Pytest**
- **Pronto para CI/CD (GitHub Actions)**

---

## 🛠️ Instalação e Setup

```bash
git clone https://github.com/henrique99sl/EventAI.git
cd EventAI/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Crie um ficheiro `.env` com as variáveis:

```env
DATABASE_URL=sqlite:///eventai.db
SECRET_KEY=minha_chave_ultra_secreta
```

Inicie a base de dados:

```bash
flask db upgrade
```

---

## ▶️ Como correr

```bash
flask run
```
A API ficará disponível em `http://localhost:5000/`

---

## 🧑‍💻 Testes

```bash
pytest
```

Todos os testes devem passar!  
Se quiser rodar localmente com coverage:

```bash
pytest --cov=.
```

---

## 🔐 Autenticação & Fluxo de Admin

- Para criar um utilizador **com role "admin"**, o request deve conter um token JWT de um admin autenticado.
- Apenas admins podem criar outros admins e apagar utilizadores.
- O primeiro admin pode ser criado manualmente na base de dados ou via script/teste.

---

## 📚 Endpoints Principais

### Utilizadores

| Método | Endpoint          | Descrição                           | Permissão      |
|--------|-------------------|-------------------------------------|----------------|
| GET    | /users            | Lista todos os utilizadores         | Livre          |
| POST   | /users            | Cria utilizador                     | Livre/admin    |
| GET    | /users/<id>       | Detalhe utilizador                  | JWT            |
| PUT    | /users/<id>       | Edita utilizador                    | JWT            |
| DELETE | /users/<id>       | Apaga utilizador                    | Admin/JWT      |

### Autenticação

| Método | Endpoint      | Descrição           |
|--------|---------------|---------------------|
| POST   | /login        | Login e token JWT   |
| GET    | /me           | Info do utilizador  |

### Eventos

| Método | Endpoint          | Descrição                                 | Permissão  |
|--------|-------------------|-------------------------------------------|------------|
| GET    | /events           | Lista/filtros de eventos                  | Livre      |
| POST   | /events           | Cria evento                               | JWT        |
| GET    | /events/<id>      | Detalhes evento                           | Livre      |
| PUT    | /events/<id>      | Edita evento                              | JWT        |
| DELETE | /events/<id>      | Apaga evento                              | JWT        |

### Venues

| Método | Endpoint          | Descrição                                 | Permissão  |
|--------|-------------------|-------------------------------------------|------------|
| GET    | /venues           | Lista/filtros de venues                   | Livre      |
| POST   | /venues           | Cria venue                                | JWT        |
| GET    | /venues/<id>      | Detalhes venue                            | Livre      |
| PUT    | /venues/<id>      | Edita venue                               | JWT        |
| DELETE | /venues/<id>      | Apaga venue                               | JWT        |

---

## 📃 Swagger

A documentação interativa está disponível em `/apidocs` quando o servidor está no ar.

---

## 🧪 Exemplo de Request com JWT

```bash
# Login
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" \
  -d '{"email":"user@gmail.com", "password":"StrongPass1"}'

# Criar evento autenticado
curl -X POST http://localhost:5000/events -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"name":"Concerto", "date":"2025-09-01", "venue_id":1}'
```

---

## 🛠️ CI/CD (GitHub Actions)

Já incluído: quando fazes push/pull request, os testes rodam automaticamente.  
Ver `.github/workflows/ci-cd.yml`.

---

## 📦 Estrutura

```
backend/
  app.py
  models/
    __init__.py
    user.py
    event.py
    venue.py
  tests/
    test_app.py
    test_auth.py
    test_events.py
    test_routes.py
    test_users.py
    test_venues.py
  requirements.txt
  README.md
  swagger.yaml
```

---

## 📄 Licença

[MIT](LICENSE)

---

Dúvidas? Abre uma issue!