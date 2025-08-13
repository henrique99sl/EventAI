![CI/CD](https://github.com/henrique99sl/EventAI/actions/workflows/ci-cd.yml/badge.svg)

# EventAI Backend

Este é o backend do **EventAI**, uma API RESTful em Flask para gerir utilizadores, eventos e locais (venues), com autenticação JWT, permissões de admin, documentação Swagger, testes automatizados, backup automatizado, pronto para Docker, CI/CD e **Kubernetes**.

---

## 🚀 Funcionalidades

- **Gestão de Utilizadores:** CRUD, autenticação JWT, roles, segurança de senha
- **Gestão de Eventos:** CRUD, filtros por nome/data/venue
- **Gestão de Locais (Venues):** CRUD completo
- **Permissões:** Apenas admin pode apagar utilizadores e criar outros admins
- **Documentação interativa Swagger/OpenAPI**
- **Testes automatizados (Pytest + Coverage)**
- **Backup automatizado do banco de dados**
- **Pronto para CI/CD (GitHub Actions + AWS)**
- **Docker e Docker Compose prontos para produção/dev**
- **Pronto para Kubernetes (manifests na pasta `k8s/` e exemplos abaixo)**

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

## ☸️ Deploy com Kubernetes

> **Pré-requesito:** Ter um cluster Kubernetes (ex: minikube, kind, GKE, EKS, etc) e `kubectl`.

- Os manifests de deployment e serviço estão na pasta `k8s/`

```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/adminer-deployment.yaml
```

- Exponha o backend e o Adminer com NodePort, LoadBalancer ou Ingress conforme o ambiente.
- Recomenda-se configurar o banco com PVC (PersistentVolumeClaim) para dados e backups.

> **Dica:** Adapte os manifests para apontar para os teus secrets e configurações.

---

## 🗄️ Backup e Restore do Banco de Dados

- **Backup manual:**  
  ```bash
  docker-compose exec backend bash scripts/backup_db.sh
  ```
  O backup `.sql` será salvo em `./backups` (pasta do host, mapeada no container).

- **Backup automático:**  
  Agende via cron fora do container, ou crie um Job/CronJob no Kubernetes para rodar `scripts/backup_db.sh`.

- **Restore manual:**  
  ```bash
  # copie o arquivo para o container do banco ou volume compartilhado
  docker-compose exec db bash
  psql -U eventos_user -d eventos_db -f /var/lib/postgresql/data/teubackup.sql
  ```
  *(Ajuste o caminho conforme onde o backup está disponível no container)*

- **Em produção/Kubernetes:**  
  Use Jobs/CronJobs para backups e restores, sempre garantindo que os arquivos estejam disponíveis nos volumes corretos.

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

## 🛠️ CI/CD (GitHub Actions + AWS)

- Os testes correm automaticamente a cada push/pull request.
- Deploy automatizado para AWS (EC2, ECS, EKS, etc).
- Workflow em `.github/workflows/ci-cd.yml`.
- Secrets e config protegidos via GitHub Secrets/AWS Secrets Manager.

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
  scripts/
    backup_db.sh
  requirements.txt
  README.md
  swagger.yaml
  docker-compose.yml
  Dockerfile
  .env.example
  backups/
k8s/
  postgres-deployment.yaml
  backend-deployment.yaml
  adminer-deployment.yaml
```

---

## 🗄️ Setup Base de Dados (SQLite e PostgreSQL)

O projeto suporta **SQLite** (para testes/desenvolvimento) e **PostgreSQL** (produção).  
A escolha é feita via variável `DATABASE_URL` no `.env`.

- **SQLite** (default para dev):  
  ```env
  DATABASE_URL=sqlite:///local.db
  ```
- **PostgreSQL** (produção ou integração):  
  ```env
  DATABASE_URL=postgresql://user:password@host:port/dbname
  ```

**Nota:**  
Em Docker Compose e Kubernetes, já vem pré-configurado para PostgreSQL.

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

## ✅ Checklist de Produção

- [x] CI/CD automatizado (GitHub Actions + AWS)
- [x] Backup automatizado do banco
- [x] Restore manual/documentado
- [ ] Restore testado regularmente
- [x] Rollback de deploy (imagem Docker anterior/backups)
- [ ] Monitoramento e alertas (containers, logs, saúde HTTP)
- [x] Variáveis de ambiente seguras (Secrets no GitHub/AWS)
- [x] Compatível com Kubernetes (manifests e exemplos)
- [ ] Documentação de restore e rollback no repositório

---

## 📄 Licença

[MIT](LICENSE)

---

Dúvidas? Sugestões? Abre uma issue ou PR!
