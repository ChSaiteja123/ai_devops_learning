# AI-Powered DevOps & Cloud Architecture Learning Platform

A full-stack Django REST API platform for learning DevOps and Cloud Architecture through interactive courses, hands-on labs, AI-powered assistance, and real-world AIOps/monitoring tooling.

---

## Features

| Module | Description |
|---|---|
| **Courses & Lessons** | Categorised course catalog with video, text, interactive, and lab lesson types |
| **Hands-on Labs** | Step-by-step labs with commands, expected outputs, and submission tracking |
| **Projects** | Real-world capstone projects with GitHub submission and code review |
| **Quizzes** | MCQ, true/false, scenario, troubleshooting, and architecture question types |
| **Progress & Streaks** | Points system, learning streaks, certificates, and per-category skill percentages |
| **AI Assistant** | GPT-4o chat tutor with conversation history and DevOps-focused system prompt |
| **RAG Knowledge Base** | Upload PDF/TXT/MD docs → chunk → ChromaDB vector index → contextual Q&A |
| **Architecture Generator** | Natural-language → AI-generated cloud architecture diagram (JSON + Mermaid) |
| **AIOps** | Metric/log analysis with AI root-cause detection, human-approval gate, incident lifecycle |
| **Monitoring** | Metric snapshots, alert rules, fired alerts, health checks, observability dashboard |
| **Deployments** | Full deployment lifecycle tracking with rollback, notes, and CI/CD status webhooks |
| **Notifications** | In-app notification system with per-user preferences and mark-read/unread-count endpoints |
| **Audit Log** | Immutable write-once audit trail of every mutating API action (staff-readable) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **API** | Django 4.2 + Django REST Framework 3.15 |
| **Auth** | JWT via `djangorestframework-simplejwt` |
| **Database** | PostgreSQL 15 |
| **Cache / Broker** | Redis 7 |
| **Task Queue** | Celery 5 |
| **AI** | OpenAI GPT-4o + `text-embedding-3-small` |
| **Vector Store** | ChromaDB |
| **PDF Parsing** | pypdf |
| **Observability** | Prometheus client + OpenTelemetry SDK |
| **Containers** | Docker + Docker Compose |
| **Static Files** | WhiteNoise |

---

## Project Structure

```
devops_learning_platform/
├── config/
│   ├── settings/
│   │   ├── base.py          # Shared settings (all environments)
│   │   ├── development.py   # Local dev overrides (DEBUG, SQLite option, console email)
│   │   └── production.py    # Production (HTTPS, S3, Sentry, JSON logging)
│   ├── urls.py              # Root URL configuration
│   ├── celery.py            # Celery app + task autodiscovery
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/            # Custom User model, JWT auth, profiles
│   ├── courses/             # Category + Course catalog
│   ├── lessons/             # Lesson content (video/text/lab/interactive)
│   ├── labs/                # Hands-on labs with step-by-step instructions
│   ├── projects/            # Capstone projects + GitHub submission
│   ├── quizzes/             # Quiz engine with scoring and weak-area tracking
│   ├── progress/            # Enrollment, UserProgress, Certificates, Streaks
│   ├── ai_assistant/        # GPT-4o chat assistant with conversation history
│   ├── rag/                 # RAG: document ingestion + ChromaDB + Q&A
│   ├── architecture/        # AI architecture diagram generator (JSON + Mermaid)
│   ├── aiops/               # Incident management + AI root-cause analysis
│   ├── monitoring/          # Metric snapshots, alert rules, health checks
│   ├── deployments/         # Deployment tracking, rollback, CI/CD webhooks
│   ├── notifications/       # In-app notifications + user preferences
│   └── audit/               # Immutable audit log middleware + read API
├── requirements/
│   ├── base.txt             # All shared dependencies
│   ├── development.txt      # Adds debug-toolbar, pytest, black, etc.
│   └── production.txt       # Adds sentry-sdk, django-storages[s3], boto3
├── Dockerfile
├── docker-compose.yml       # Dev: app + postgres + redis + celery
├── docker-compose.prod.yml  # Production compose
├── Makefile                 # Common dev commands
└── .env.example             # Required environment variables
```

---

## API Endpoints

| Prefix | App | Notes |
|---|---|---|
| `/api/v1/accounts/` | accounts | Register, login, JWT refresh, profile, change-password |
| `/api/v1/courses/` | courses | Categories and course catalog (read-only, filterable) |
| `/api/v1/lessons/` | lessons | Lesson content + `complete` action (awards 10 pts) |
| `/api/v1/labs/` | labs | Labs + `submit` action (awards 25 pts) |
| `/api/v1/projects/` | projects | Projects + `submit` action (awards 50 pts) |
| `/api/v1/quizzes/` | quizzes | Quizzes, questions, `submit` scoring (awards 30 pts if passed) |
| `/api/v1/progress/` | progress | Enrollments, certificates, `dashboard/` aggregate view |
| `/api/v1/ai/` | ai_assistant | Conversations + `chat/` endpoint |
| `/api/v1/rag/` | rag | Document upload, `query/`, `history/` |
| `/api/v1/architecture/` | architecture | Diagrams CRUD + `generate/` action |
| `/api/v1/aiops/` | aiops | Incidents CRUD + `analyze/`, `approve/`, `resolve/` |
| `/api/v1/monitoring/` | monitoring | Metrics, alert rules, alerts, health checks, `dashboard/` |
| `/api/v1/deployments/` | deployments | Environments, services, deployments + `rollback/`, `update-status/` |
| `/api/v1/notifications/` | notifications | Notifications + `mark-read/`, `mark-all-read/`, `unread-count/`, `preferences/` |
| `/api/v1/audit/` | audit | Audit logs (staff read-only) |

---

## How to Learn & Start the Course

This platform is designed as a guided learning path. Start with the basics, complete each lesson, then move into labs and projects.

### Recommended learning path

1. Start at the home dashboard and browse the course catalog.
2. Pick a beginner-friendly course such as Docker, Linux, or CI/CD fundamentals.
3. Complete each lesson in order and earn points for progress.
4. Move to labs to apply what you learned in real commands and workflows.
5. Attempt quizzes to validate understanding.
6. Submit a project once you are comfortable with the topic.
7. Use the AI assistant to ask troubleshooting and architecture questions while learning.

### Quick start on Windows

```powershell
cd "c:\Users\chsai\Desktop\ai devops\devops_learning_platform"
.\start_dev.ps1
```

This script runs migrations and starts the local development server.

### Local manual start

```powershell
cd "c:\Users\chsai\Desktop\ai devops\devops_learning_platform"
.\sai\Scripts\python.exe manage.py migrate
.\sai\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

Then open:

- http://localhost:8000/
- http://localhost:8000/dashboard/
- http://localhost:8000/admin/

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL 15+
- Redis 7+
- An OpenAI API key (optional — all AI features degrade gracefully without one)

### Quick start with Docker

```bash
# 1. Copy and fill in environment variables
cp .env.example .env

# 2. Start all services (Django, PostgreSQL, Redis, Celery worker)
docker-compose up --build

# 3. Run migrations and create a superuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

The API will be available at `http://localhost:8000`.  
The browsable API is at `http://localhost:8000/api/v1/`.  
Django admin is at `http://localhost:8000/admin/`.

### Local development (no Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install development dependencies
pip install -r requirements/development.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — at minimum set DB_* and REDIS_URL

# 4. Apply migrations
python manage.py migrate

# 5. (Optional) Load sample data
python manage.py loaddata fixtures/sample_data.json

# 6. Start the dev server
python manage.py runserver

# 7. Start a Celery worker (separate terminal — needed for RAG indexing)
celery -A config worker -l info
```

---

## Environment Variables

Copy `.env.example` to `.env`. Key variables:

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure dev default |
| `DEBUG` | Enable debug mode | `False` |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | PostgreSQL connection | `devops_platform` / `postgres` / `postgres` / `localhost` / `5432` |
| `REDIS_URL` | Redis URL (cache) | `redis://localhost:6379/2` |
| `CELERY_BROKER_URL` | Redis URL (broker) | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | OpenAI key — all AI features work without this (fallback mode) | `""` |
| `OPENAI_MODEL` | Model name | `gpt-4o` |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `""` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins | `http://localhost:3000` |

---

## Points System

| Action | Points |
|---|---|
| Complete a lesson | 10 pts |
| Submit a lab | 25 pts |
| Pass a quiz | 30 pts |
| Submit a project | 50 pts |

A `Certificate` is issued automatically when a course is fully completed.

---

## AIOps — Human-in-the-Loop

The AIOps analyzer (`POST /api/v1/aiops/analyze/`) accepts metrics and logs, runs AI root-cause analysis (GPT-4o with rule-based fallback), and creates an `Incident` record. Every incident sets `requires_human_approval=True` — no automated remediation is ever taken. A human must `POST /api/v1/aiops/incidents/{id}/approve/` before any suggested action proceeds.

---

## Makefile Commands

```bash
make build          # Build Docker images
make up             # Start all services
make down           # Stop all services
make migrate        # Run database migrations
make superuser      # Create Django superuser
make test           # Run test suite
make lint           # Run flake8 + isort
make shell          # Open Django shell
make celery         # Start Celery worker
make logs           # Tail application logs
```

---

## License

MIT
