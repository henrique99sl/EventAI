![CI/CD](https://github.com/henrique99sl/EventAI/actions/workflows/ci-cd.yml/badge.svg)

# EventAI Backend

Este é o backend do **EventAI**, uma API RESTful em Flask para gerir utilizadores, eventos e locais (venues), com autenticação JWT, permissões de admin, documentação Swagger, testes automatizados e pronto para Docker/CI/CD.

---

## 🚀 Funcionalidades

- **Gestão de Utilizadores:** CRUD, autenticação JWT, roles, segurança de senha
- **Gestão de Eventos:** CRUD, filtros por nome/data/venue
- **Gestão de Locais (Venues):** CRUD completo
- **Permissões:** Apenas admin pode apagar utilizadores e criar outros admins
- **Documentação interativa Swagger/OpenAPI**
- **Testes automatizados (Pytest + Coverage)**
- **Pronto para CI/CD (GitHub Actions)**
- **Docker e Docker Compose prontos para produção/dev**

---

## ⚡ Setup rápido (Docker recomendado)

```bash
git clone https://github.com/henrique99sl/EventAI.git
cd EventAI/backend
cp .env.example .env
docker-compose up --build
```

- O backend estará em [http://localhost:8000](http://localhost:8000)
- O Adminer (gestor de base de dados) em [http://localhost:8080](http://localhost:8080)
- A documentação Swagger em [http://localhost:8000/apidocs](http://localhost:8000/apidocs)

### Variáveis de ambiente `.env` (exemplo)

```env
DATABASE_URL=postgresql://eventos_user:eventos_pass@db:5432/eventos_db
SECRET_KEY=minha_chave_ultra_secreta
```

---

## 🧑‍💻 Setup manual (sem Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
flask run
```
API disponível em `http://localhost:5000/`

---

## 🧪 Testes

```bash
pytest
# ou com coverage
pytest --cov=.
```

---

## 🔐 Autenticação & Fluxo de Admin

- Para criar utilizador/admin, enviar role no JSON. Criar admin exige token JWT de admin.
- Apenas admins podem criar outros admins e apagar utilizadores.
- O primeiro admin pode ser criado manualmente na base de dados, via migration ou script.

---

## 📚 Endpoints Principais

### Utilizadores

| Método | Endpoint         | Descrição               | Permissão      |
|--------|------------------|-------------------------|----------------|
| GET    | /users           | Listar utilizadores     | Livre          |
| POST   | /users           | Criar utilizador        | Livre/Admin    |
| GET    | /users/&lt;id&gt;| Ver detalhes            | JWT            |
| PUT    | /users/&lt;id&gt;| Editar utilizador       | JWT            |
| DELETE | /users/&lt;id&gt;| Apagar utilizador       | Admin/JWT      |

### Autenticação

| Método | Endpoint  | Descrição           |
|--------|-----------|---------------------|
| POST   | /login    | Login & token JWT   |
| GET    | /me       | Info do utilizador  |

### Eventos

| Método | Endpoint         | Descrição             | Permissão  |
|--------|------------------|-----------------------|------------|
| GET    | /events          | Listar/filtros        | Livre      |
| POST   | /events          | Criar evento          | JWT        |
| GET    | /events/&lt;id&gt;| Ver detalhes         | Livre      |
| PUT    | /events/&lt;id&gt;| Editar evento        | JWT        |
| DELETE | /events/&lt;id&gt;| Apagar evento        | JWT        |

### Venues

| Método | Endpoint         | Descrição             | Permissão  |
|--------|------------------|-----------------------|------------|
| GET    | /venues          | Listar/filtros        | Livre      |
| POST   | /venues          | Criar venue           | JWT        |
| GET    | /venues/&lt;id&gt;| Ver detalhes        | Livre      |
| PUT    | /venues/&lt;id&gt;| Editar venue         | JWT        |
| DELETE | /venues/&lt;id&gt;| Apagar venue         | JWT        |

---

## 📃 Documentação Swagger

Acede a `/apidocs` com o servidor a correr para usar a documentação interativa.

---

## 🧪 Exemplos de Requests

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@gmail.com", "password":"StrongPass1"}'
```

### Criar evento autenticado

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"name":"Concerto", "date":"2025-09-01", "venue_id":1}'
```

### Criar utilizador

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"joao", "email":"joao@exemplo.com", "password":"forte123", "role":"user"}'
```

---

## 🛠️ CI/CD (GitHub Actions)

- Os testes correm automaticamente a cada push/pull request.
- Workflow em `.github/workflows/ci-cd.yml`.

---

## 🗂️ Estrutura do projeto

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
  docker-compose.yml
  Dockerfile
  .env.example
```

---

## 🗄️ Setup Base de Dados (SQLite e PostgreSQL)

O projeto suporta **SQLite** (para testes/desenvolvimento) e **PostgreSQL** (produção).  
A escolha é feita através da variável `DATABASE_URL` no `.env`.

- **SQLite** (default para dev):  
  ```env
  DATABASE_URL=sqlite:///local.db
  ```
- **PostgreSQL** (produção ou integração):  
  ```env
  DATABASE_URL=postgresql://user:password@host:port/dbname
  ```

**Nota:**  
Em Docker Compose, já vem pré-configurado para PostgreSQL.

---

## 🧩 Migrações de Base de Dados

Usamos Alembic/Flask-Migrate:

- **Criar nova migração:**
  ```bash
  flask db migrate -m "Descrição da alteração"
  ```
- **Aplicar migrações:**
  ```bash
  flask db upgrade
  ```

---

## 📄 Licença

[MIT](LICENSE)

---

Dúvidas? Sugestões? Abre uma issue ou PR!
Teste de CI/CD em 11/08/2025
Atualização para testar CI/CD em 11/08/2025
