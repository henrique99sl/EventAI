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
- **Restauração do banco testada e automatizada via script** <!-- ADICIONADO -->
- **Pronto para CI/CD (GitHub Actions + AWS)**
- **Docker e Docker Compose prontos para produção/dev**
- **Pronto para Kubernetes (manifests na pasta `k8s/` e exemplos abaixo)**
- **Cache Redis com Flask-Caching e rate limiting**
- **Métricas Prometheus e monitoramento com Sentry**
- **Tuning de performance com Gunicorn (workers configuráveis)**
- **Endpoints de health, readiness e liveness**
- **Documentação de operação e recuperação incluída**

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
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=minha_chave_jwt
CORS_ORIGINS=*
SENTRY_DSN=
FLASK_ENV=production
```
> **Nota:** O Redis é usado para cache e para rate limiting.  
> Recomenda-se usar um serviço externo para produção.

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
  bash scripts/restore_db.sh caminho/do/backup.sql
  ```
  > Este comando apaga e recria o banco antes de restaurar o backup  
  *(Ajuste o caminho conforme onde o backup está disponível no container)*

- **Teste de restauração automatizado:**  
  ```bash
  bash scripts/test_restore_db.sh caminho/do/backup.sql
  ```
  > O script executa o restore em um banco limpo e valida se a restauração foi bem sucedida (ex: conta registros na tabela de usuários).

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
| GET    | /events/cached   | Listar eventos cacheados | Livre   |
| POST   | /events          | Criar evento          | JWT        |
| GET    | /events/&lt;id&gt;| Ver detalhes         | Livre      |
| PUT    | /events/&lt;id&gt;| Editar evento        | JWT        |
| DELETE | /events/&lt;id&gt;| Apagar evento        | JWT        |
| GET    | /events/calendar | Listar por calendário | Livre      |

### Venues

| Método | Endpoint         | Descrição             | Permissão  |
|--------|------------------|-----------------------|------------|
| GET    | /venues          | Listar/filtros        | Livre      |
| POST   | /venues          | Criar venue           | JWT        |
| GET    | /venues/&lt;id&gt;| Ver detalhes        | Livre      |
| PUT    | /venues/&lt;id&gt;| Editar venue         | JWT        |
| DELETE | /venues/&lt;id&gt;| Apagar venue         | JWT        |

### Infraestrutura

| Método | Endpoint    | Descrição             |
|--------|-------------|-----------------------|
| GET    | /health     | Health check          |
| GET    | /readiness  | Pronto para requests  |
| GET    | /liveness   | Está vivo             |

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
    restore_db.sh
    test_restore_db.sh
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

## ⚡ Performance, Cache e Workers

- **Cache Redis:**  
  O backend usa Flask-Caching com Redis para acelerar consultas, especialmente o endpoint `/events/cached` (cache de 60 segundos por padrão).
- **Rate Limiting:**  
  Proteção contra abuso via Flask-Limiter, usando Redis para controle distribuído.
- **Gunicorn:**  
  Recomenda-se rodar o backend com Gunicorn e múltiplos workers para máximo desempenho:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:8000 backend.app:create_app()
  ```
  Ajuste `-w` conforme CPU/RAM do servidor.
- **Monitoramento:**  
  Sentry integrado para erros, Prometheus para métricas de saúde.

---

## 💡 Operação

### Subir em produção

1. Configure variáveis de ambiente no `.env`.
2. Gere/migre o banco com `flask db upgrade`.
3. Suba Redis e Postgres (via Docker/K8s ou serviços gerenciados).
4. Rode com Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 backend.app:create_app()
   ```
5. Monitore os endpoints:
   - `/health` para status geral
   - `/readiness` para saber se está pronto para receber requests
   - `/liveness` para saber se está vivo no K8s

### Backup e restore

- **Backup:**  
  Execute `scripts/backup_db.sh` via cron, Job ou manualmente.
- **Restore:**  
  Use o comando do Postgres dentro do container e garanta que o arquivo `.sql` está acessível.
  Ou utilize `scripts/restore_db.sh caminho/do/backup.sql` para restaurar e re-criar o banco automaticamente.

- **Teste de restauração:**  
  Execute `scripts/test_restore_db.sh caminho/do/backup.sql` para validar se o backup pode ser restaurado com sucesso.

### Cache

- O Redis deve estar ativo e acessível pelo backend.
- Se precisar limpar cache, execute:
  ```bash
  redis-cli -h <host> -p <porta> FLUSHALL
  ```
  (Atenção: isso remove todo o cache e dados do Redis configurado.)

### Tuning de workers

- Ajuste o parâmetro `-w` do Gunicorn conforme a carga e recursos disponíveis.
- Para alta concorrência, use um proxy reverso (nginx, traefik) e configure health checks.

---

## 🛠️ Recuperação e Diagnóstico

### Falha do backend

- Verifique os logs do Gunicorn e do Flask (`docker-compose logs`, `kubectl logs` ou logs em `/var/log`).
- Cheque o estado do Redis e do Postgres.
- Use `/health`, `/readiness` e `/liveness` para diagnóstico rápido.

### Falha no cache/Redis

- Reinicie o serviço Redis (`docker restart redis` ou `systemctl restart redis`).
- Limpe o cache se necessário (`FLUSHALL` via redis-cli).
- Cheque as variáveis de ambiente (`REDIS_URL`).

### Falha no banco de dados

- Restaure o banco usando o backup `.sql` mais recente.
- Use o script de restauração e teste para garantir integridade.
- Verifique o volume/PVC no Kubernetes para persistência dos dados.

### Workers não respondendo

- Reinicie o Gunicorn:
  ```bash
  pkill gunicorn
  gunicorn -w 4 -b 0.0.0.0:8000 backend.app:create_app()
  ```
- Monitore a saúde dos pods no Kubernetes e faça rollout se necessário.

### Rollback de deploy

- Use imagens Docker anteriores ou restaure backup do banco.
- Refaça o deploy dos manifests K8s ou Docker Compose.

---

## ✅ Checklist de Produção

- [x] CI/CD automatizado (GitHub Actions + AWS)
- [x] Cache Redis configurado e testado
- [x] Rate limiting via Redis
- [x] Backup automatizado do banco
- [x] Restore manual/documentado
- [x] Teste de restauração de banco automatizado/documentado <!-- ADICIONADO -->
- [x] Rollback de deploy (imagem Docker anterior/backups)
- [x] Monitoramento e alertas (containers, logs, saúde HTTP)
- [x] Variáveis de ambiente seguras (Secrets no GitHub/AWS)
- [x] Compatível com Kubernetes (manifests e exemplos)
- [x] Documentação de operação e recuperação incluída!

---

## 📄 Licença

[MIT](LICENSE)

---

Dúvidas? Sugestões? Abre uma issue ou PR!