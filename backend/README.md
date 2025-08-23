![CI/CD](https://github.com/henrique99sl/EventAI/actions/workflows/ci-cd.yml/badge.svg)

# EventAI Backend

Este é o backend do **EventAI**, uma API RESTful construída em Flask para gestão de utilizadores, eventos, recomendações, feedbacks e integração com IA e ML (LangChain, ChromaDB, OpenAI, transformers). Pronto para produção (Docker, CI/CD, AWS, Kubernetes) e com documentação interativa.

---

## 🚀 Funcionalidades Principais

- **Gestão de Utilizadores:** CRUD, autenticação JWT, roles, segurança de senha
- **Gestão de Eventos e Locais (Venues):** CRUD completo, filtros avançados
- **Permissões avançadas:** Apenas admin pode apagar utilizadores e criar outros admins
- **Documentação Swagger/OpenAPI**
- **Testes automatizados (Pytest + Coverage)**
- **Backup automatizado do banco de dados**
- **Pronto para CI/CD (GitHub Actions + AWS)**
- **Docker e Docker Compose para produção/dev**
- **Kubernetes (manifests na pasta `kubernetes/`)**
- **Monitoramento e alertas (Prometheus, YAML de alertas, Loki, dashboards)**
- **Integração ML/AI:** LangChain, ChromaDB, OpenAI, transformers, sentence-transformers
- **Assistente IA embutido:** Responde perguntas, faz busca semântica, recomenda eventos
- **Sistema de Recomendações Personalizadas:** Embeddings, histórico, feedback
- **Feedback dos usuários:** CRUD de feedback, análise de satisfação

---

## 🧠 Funcionalidades Avançadas: Assistant, Recomendações e Feedback

### Assistant (IA)

- **Interação via endpoint:** `/assistant`
- **Funcionalidades:**  
  - Responde dúvidas sobre eventos, locais, usuários e funcionamento da plataforma
  - Busca semântica via embeddings e ChromaDB
  - Gera recomendações de eventos personalizadas
  - Integração com modelos OpenAI, LangChain, transformers, sentence-transformers
- **Exemplo de request:**
  ```bash
  curl -X POST http://localhost:8000/assistant \
    -H "Content-Type: application/json" \
    -d '{"question":"Quais eventos recomendados para mim esta semana?"}'
  ```
- **Configuração de persistência:**  
  - Diretório: `CHROMA_PERSIST_DIR`
  - Coleção: `CHROMA_COLLECTION`
  - Modelo: `EMBEDDING_MODEL`

---

### Recomendações

- **Endpoint principal:** `/recommendations`
- **Funcionalidades:**  
  - Sugere eventos com base no perfil, histórico e feedback do usuário
  - Utiliza embeddings, ChromaDB e ML para personalizar sugestões
  - Pode ser integrado a workflows de onboarding ou notificações
- **Exemplo de request:**
  ```bash
  curl -X GET http://localhost:8000/recommendations \
    -H "Authorization: Bearer SEU_TOKEN_JWT"
  ```
- **Scripts e pipelines:**  
  - `assistant/embedding_pipeline.py`
  - `assistant/chroma_service.py`
  - `update_recommendations.py`

---

### Feedback

- **Endpoint:** `/feedback`
- **Funcionalidades:**  
  - Usuários podem enviar feedback sobre eventos, recomendações, assistente e plataforma
  - Feedback é associado ao usuário e pode ser analisado para melhorias
  - Admin pode visualizar, filtrar e exportar feedbacks
- **Exemplo de request:**
  ```bash
  curl -X POST http://localhost:8000/feedback \
    -H "Authorization: Bearer SEU_TOKEN_JWT" \
    -H "Content-Type: application/json" \
    -d '{"event_id":1, "rating":5, "comment":"Evento excelente!"}'
  ```

---

## ⚡ Setup rápido (Docker recomendado)

```bash
git clone https://github.com/henrique99sl/EventAI.git
cd EventAI/backend
cp .env.example .env
docker-compose up --build
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Adminer (DB GUI): [http://localhost:8080](http://localhost:8080)
- Swagger: [http://localhost:8000/apidocs](http://localhost:8000/apidocs)

---

## 🧬 Integração ML/AI

Dependências instaladas para IA/ML:
- `langchain`
- `chromadb`
- `openai`
- `sentence-transformers`
- `transformers`

Exemplo de variáveis no `.env`:
```env
CHROMA_PERSIST_DIR=chroma_db
CHROMA_COLLECTION=eventai_docs
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_API_KEY=sua_openai_api_key_aqui
```

Utilize scripts como `populate_chroma.py` para inicializar embeddings e persistência.

---

## ☸️ Deploy com Kubernetes

Manifests na pasta `kubernetes/`:
```bash
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-ingress.yaml
```

- Recomenda-se PVC para dados e backups.
- Adapte configs para seus secrets e ambiente.

---

## 🗄️ Backup e Restore do Banco de Dados

### Backup manual (docker):
```bash
docker-compose exec backend bash scripts/backup_db.sh
```
Backup `.sql` salvo em `./backups`.

### Restore manual:
```bash
docker-compose exec db bash
psql -U eventos_user -d eventos_db -f /var/lib/postgresql/data/seubackup.sql
```

### Backup/restore automático:
Agende via cron, ou use Job/CronJob no Kubernetes.

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
API: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Testes

```bash
pytest
pytest --cov=.
```
Cobertura para rotas, autenticação, IA, feedback, recomendações, backup/restore.

---

## 📚 Endpoints Principais

### Utilizadores

| Método | Endpoint         | Descrição               | Permissão      |
|--------|------------------|-------------------------|----------------|
| GET    | /users           | Listar utilizadores     | Livre          |
| POST   | /users           | Criar utilizador        | Livre/Admin    |
| GET    | /users/&lt;id&gt;| Detalhes do usuário     | JWT            |
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
| GET    | /events/&lt;id&gt;| Detalhes do evento   | Livre      |
| PUT    | /events/&lt;id&gt;| Editar evento        | JWT        |
| DELETE | /events/&lt;id&gt;| Apagar evento        | JWT        |

### Venues

| Método | Endpoint         | Descrição             | Permissão  |
|--------|------------------|-----------------------|------------|
| GET    | /venues          | Listar/filtros        | Livre      |
| POST   | /venues          | Criar venue           | JWT        |
| GET    | /venues/&lt;id&gt;| Detalhes do venue    | Livre      |
| PUT    | /venues/&lt;id&gt;| Editar venue         | JWT        |
| DELETE | /venues/&lt;id&gt;| Apagar venue         | JWT        |

### Assistant (IA)

| Método | Endpoint      | Descrição                              | Permissão  |
|--------|---------------|----------------------------------------|------------|
| POST   | /assistant    | Perguntas e respostas IA, recomendações| Livre/JWT  |

### Recomendações

| Método | Endpoint           | Descrição                           | Permissão  |
|--------|--------------------|-------------------------------------|------------|
| GET    | /recommendations   | Sugestão de eventos por IA/ML       | JWT        |

### Feedback

| Método | Endpoint     | Descrição                       | Permissão  |
|--------|--------------|----------------------------------|------------|
| POST   | /feedback    | Enviar feedback                  | JWT        |
| GET    | /feedback    | Listar feedbacks                 | Admin/JWT  |

---

## 📃 Documentação Swagger

Acede a `/apidocs` para documentação interativa.

---

## 🧪 Exemplos de Requests

### Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@gmail.com", "password":"StrongPass1"}'
```

### Assistant (IA)
```bash
curl -X POST http://localhost:8000/assistant \
  -H "Content-Type: application/json" \
  -d '{"question":"Quais eventos recomendados para mim esta semana?"}'
```

### Recomendações
```bash
curl -X GET http://localhost:8000/recommendations \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

### Feedback
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"event_id":1, "rating":5, "comment":"Evento excelente!"}'
```

---

## 🛠️ CI/CD (GitHub Actions + AWS)

- Testes automatizados por push/pr
- Deploy automático para AWS (EC2/ECS/EKS)
- Workflow: `.github/workflows/ci-cd.yml`
- Secrets/configs protegidos via GitHub/AWS Secrets Manager

---

## 🗂️ Estrutura do Projeto

```
backend/
  app.py
  assistant/
    chroma_service.py
    embedding_pipeline.py
    routes.py
  models/
    __init__.py
    user.py
    event.py
    feedback.py
    recommendation.py
    venue.py
    chat_log.py
    event_participation.py
  tests/
    test_app.py
    test_auth.py
    test_events.py
    test_users.py
    test_venues.py
    test_feedback.py
    test_recommendations.py
  scripts/
    backup_db.sh
    restore_db.sh
    populate_chroma.py
  requirements.txt
  README.md
  swagger.yaml
  docker-compose.yml
  Dockerfile
  .env.example
  backups/
kubernetes/
  backend-deployment.yaml
  backend-ingress.yaml
  backend-service.yaml
  postgres-deployment.yaml
```

---

## 🗄️ Setup Banco de Dados (SQLite/PostgreSQL)

Configuração via `.env`, exemplo:
```env
DATABASE_URL=sqlite:///local.db          # Dev
DATABASE_URL=postgresql://user:pass@db:5432/eventos_db  # Prod/Docker/K8s
```

---

## 🧩 Migrações de Banco de Dados

```bash
flask db migrate -m "Descrição da alteração"
flask db upgrade
```

---

## 🔒 Segurança

- Variáveis sensíveis via secrets (GitHub/AWS)
- Senhas com hash seguro, validação de força
- JWT com expiração, permissões e revogação
- CORS configurado
- Sentry (opcional)

---

## ✅ Checklist de Produção

- [x] CI/CD automatizado (GitHub Actions + AWS)
- [x] Backup automatizado do banco
- [x] Restore manual/documentado
- [x] Restore testado regularmente
- [x] Rollback de deploy (imagem Docker anterior/backups)
- [x] Monitoramento e alertas (Prometheus, Loki, dashboards)
- [x] Variáveis de ambiente seguras (Secrets no GitHub/AWS)
- [x] Compatível com Kubernetes (manifests e exemplos)
- [x] Documentação de restore e rollback no repositório

---

## 📄 Licença

[MIT](LICENSE)

---

**Dúvidas ou sugestões?**  
Abra uma [issue](https://github.com/henrique99sl/EventAI/issues) ou envie um PR!
