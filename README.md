# EventAI — Intelligent Event Management Platform

This repository contains **EventAI**, a full-stack solution for modern event management, recommendation, and interaction.  
It is comprised of two main projects:

- **Frontend**: A modern Angular Single Page Application (SPA) featuring modular architecture, responsive design, Material UI, and integration with the backend via REST API.
- **Backend**: A robust Flask RESTful API, production-ready with Docker/Kubernetes, CI/CD, ML/AI-powered recommendations, and advanced user/event management.

---

![CI/CD](https://github.com/henrique99sl/EventAI/actions/workflows/ci-cd.yml/badge.svg)

---

## 🚀 Quick Start: Deploy Everything

To launch **both frontend and backend** together, simply run:

```bash
./start-all.sh
```

This script boots both applications (via Docker Compose, scripts, or as defined in each project):

- **Frontend**: [http://localhost:4200](http://localhost:4200)
- **Backend**: [http://localhost:8000](http://localhost:8000)
- **Swagger API Docs**: [http://localhost:8000/apidocs](http://localhost:8000/apidocs)
- **Adminer (DB GUI)**: [http://localhost:8080](http://localhost:8080)

---

## 🗂️ Project Structure

```
EventAI/
│
├── backend/           # Flask API, ML/AI, DB, Docker, K8s, CI/CD
│   ├── app.py
│   ├── assistant/
│   ├── models/
│   ├── tests/
│   ├── scripts/
│   ├── requirements.txt
│   ├── README.md
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── .env.example
│   └── kubernetes/
│
├── frontend/          # Angular SPA, Material, SCSS, i18n
│   ├── src/
│   ├── angular.json
│   ├── package.json
│   ├── README.md
│   └── ...
│
├── start-all.sh       # Script to deploy both frontend & backend
├── LICENSE
└── README.md          # This file!
```

---

## ✨ Key Features

### Backend (Flask)

- **User, Event, and Venue Management**
  - Full CRUD for users, events, venues
  - Advanced permissions: JWT authentication, role-based access, admin controls
  - Secure password hashing & validation
- **Feedback & Recommendation System (AI/ML)**
  - Personalized recommendations via embeddings (ChromaDB, LangChain, OpenAI, transformers)
  - Semantic search, custom pipelines, user feedback analysis
  - Built-in assistant endpoint (`/assistant`) for conversational AI
- **API Documentation**
  - Swagger/OpenAPI interactive docs at `/apidocs`
- **Testing & Coverage**
  - Automated tests (Pytest), coverage reports
- **Backup & Restore**
  - Manual and automated database backup/restore (scripts, cron, K8s jobs)
- **Production-Readiness**
  - Docker & Docker Compose for containerization
  - Kubernetes manifests for scalable deployment
  - CI/CD via GitHub Actions (AWS ready)
- **Monitoring**
  - Prometheus, Loki, ready-to-use dashboards and alerts

### Frontend (Angular)

- **Modern SPA Architecture**
  - Angular 16+ with standalone components and modules
  - Responsive, mobile-first design with Angular Material
- **Feature-Rich UI**
  - Event agenda, dashboard, live chat, speaker profiles, organizer tools
  - Authentication, onboarding, feedback forms, recommendation widgets
  - Integrated AI assistant (chat, semantic search, recommendations)
- **Internationalization (i18n)**
  - Multi-language support (JSON-based translations)
- **Styling & Theming**
  - Modular SCSS, custom themes, Material customization
- **Testing**
  - Full unit test coverage (Jasmine/Karma)
- **Easy Integration**
  - RESTful communication with backend services

---

## 🔧 Individual Setup & Usage

### Backend

**Dockerized Setup**

```bash
cd backend
cp .env.example .env
docker-compose up --build
```

**Manual Setup (for local development)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
flask run
```

**Kubernetes Deployment**

```bash
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-ingress.yaml
```

- See backend/README.md for full details, environment variables, and advanced options.

---

### Frontend

**Setup & Development**

```bash
cd frontend
npm install
npm start
```

**Production Build**

```bash
ng build --configuration production
```

**Testing**

```bash
ng test
```

- See frontend/README.md for more on Angular configuration, theming, i18n, and module development.

---

## 🧪 Testing

- **Backend**
  - Run tests: `pytest`
  - Coverage: `pytest --cov=.`
- **Frontend**
  - Run tests: `ng test`
  - Coverage available via Karma/Jasmine reports

---

## 📚 API & Documentation

- **Backend**
  - Interactive docs: [http://localhost:8000/apidocs](http://localhost:8000/apidocs)
  - Endpoints for users, events, venues, recommendations, assistant, feedback (see backend README for details)
- **Frontend**
  - Developer documentation in `frontend/README.md`, including architecture, module structure, and usage instructions

---

## 🌐 Internationalization (i18n)

- **Frontend**
  - Translation files in `src/assets/i18n/` (English, Portuguese, easily extendable)
  - Language selection via Angular service or configuration
- **Backend**
  - API responses and assistant support adaptable for future localization

---

## ☸️ Production & CI/CD

- **CI/CD Pipeline**
  - Automated testing, build, and deployment via GitHub Actions
  - Ready for AWS (EC2, ECS, EKS), Docker Hub, etc.
- **Docker/Kubernetes**
  - Both projects are containerized, manifests provided for scalable cloud deployment
- **Secrets & Security**
  - Sensitive configs managed via `.env`, GitHub/AWS secrets, environment variables

---

## 🗄️ Database & Backup

- **Database Options**
  - SQLite (local/dev), PostgreSQL (production, Docker, K8s)
  - Connection string set via `.env`
- **Backup & Restore**
  - Scripts and cron jobs for manual/automatic DB backup/restoration
  - Kubernetes jobs and PersistentVolumeClaim (PVC) support

---

## 🔒 Security & Best Practices

- JWT authentication, password hashing, RBAC (role-based access control)
- CORS configuration, optional Sentry monitoring
- Secure secrets management
- Automated database backup & restore tested regularly
- Rollback strategies: previous Docker images, database backups

---

## ✅ Production Readiness Checklist

- [x] Automated CI/CD (GitHub Actions + AWS)
- [x] Database backup/restore (manual & automated)
- [x] Rollback procedures documented and tested
- [x] Monitoring & alerting (Prometheus, Loki)
- [x] Secure secrets management
- [x] Kubernetes manifests for backend/db
- [x] API documentation (Swagger)
- [x] Comprehensive unit and integration tests

---

## 📄 License

This project is open-source under the MIT license.  
See the [LICENSE](LICENSE) file for details.

---

## 🤝 Questions, Support & Contributions

- Open an **issue** or submit a **pull request** on GitHub!
- Consult the individual `README.md` files in `backend/` and `frontend/` for more details.
- For bug reports, feature requests, or deployment help, please use the issue tracker.

---

**EventAI** — Next-generation event management powered by AI, built for scalability, usability, and innovation.