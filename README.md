# NagrikSetu – Social Welfare Department (SWD) Microservice
## Full-Stack Citizen Welfare Services, Rule Evaluation Engine & Beneficiary Management

**Platform:** NagrikSetu – Citizen Services Platform  
**Service:** Social Welfare Department (SWD)  
**Deliverable:** Independent Microservice (Member 2 Deliverable)  
**Architecture:** Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic v2, React 18, TypeScript, Vite, MySQL 8.0, RabbitMQ 3.x, Docker Compose  
**Environment:** Development & University Examination Rig  

---

## 1. Project Overview & Identity

NagrikSetu is an integrated citizen services platform. The **Social Welfare Department (SWD)** microservice operates as an independent service responsible for:
- Publishing and managing social welfare schemes, scholarships, disability pensions, and community empowerment grants.
- Configurable rule-based eligibility evaluation engine supporting preliminary citizen assessment.
- Citizen application submission, document management, and real-time status tracking.
- Administrative review workflow, duplicate applicant warning heuristics, and official beneficiary registers.
- Asynchronous event publication via RabbitMQ (`nagriksetu.events`).

> **Note on Project Identity:**  
> This is a student-developed academic microservice developed for the NagrikSetu platform. It is not an official government portal. It exclusively houses Social Welfare Department features and does not contain generic or unrelated department directories.

---

## 2. Architecture & Tech Stack

| Layer | Technology | Port / Container Name |
|---|---|---|
| **Frontend** | React 18, TypeScript, Vite, Lucide Icons, Vanilla CSS | `http://localhost:5173` (`nagriksetu-swd-frontend`) |
| **Backend API** | FastAPI, Python 3.11, Pydantic v2, PyJWT | `http://localhost:8004` (`nagriksetu-swd-backend`) |
| **API Docs (Swagger)** | OpenAPI 3.0 / Swagger UI | `http://localhost:8004/docs` |
| **Database** | MySQL 8.0 (Isolated database `swd_db`) | Host port `3307` -> Container port `3306` (`nagriksetu-swd-mysql`) |
| **Event Bus** | RabbitMQ 3.x with Management Plugin | Host `5672` (AMQP), `15672` (Web UI) (`nagriksetu-swd-rabbitmq`) |

---

## 3. Directory Structure

```
NagrikSetu_SWD_Final/
├── backend/
│   ├── app/
│   │   ├── core/           # Security, JWT, config settings
│   │   ├── database/       # SQLAlchemy engine & session manager
│   │   ├── events/         # RabbitMQ publisher & Outbox pattern
│   │   ├── models/         # SQLAlchemy 2.0 ORM database models
│   │   ├── routers/        # FastAPI endpoint routers (/api/swd/*)
│   │   ├── schemas/        # Pydantic v2 schemas and request validation
│   │   ├── services/       # Eligibility evaluation engine & documents
│   │   └── main.py         # Application entry point, CORS, startup events
│   ├── tests/              # 12 automated Pytest suites covering FRs
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── services/       # Type-safe API client (api.ts)
│   │   ├── App.tsx         # Dedicated SWD React Single Page Application
│   │   ├── style.css       # Clean, accessible styling matching UI reference
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── nginx.conf          # Nginx production reverse proxy configuration
│   └── package.json
├── database/
│   ├── swd_db_setup.sql    # Complete MySQL schema DDL & seed data
│   └── safe_restore.py     # Safe idempotent database restore tool
├── docker-compose.yml       # Production-ready 4-container stack
├── .env.example            # Environment configuration template
├── SWD_FR_TRACEABILITY_MATRIX.md # Complete requirement traceability matrix
├── SWD_INTEGRATION_SPEC.md # API contracts and RabbitMQ event specs
└── README.md
```

---

## 4. Quick Start & Docker Deployment

### 4.1 Prerequisites
- Docker Desktop with Docker Compose installed and running.
- Python 3.10+ (optional, for local development outside Docker).
- Node.js 18+ (optional, for local frontend development).

### 4.2 Starting the Microservice Stack
Run the following from the root directory:
```bash
docker compose up -d
```

This starts all four services with health checks:
1. `nagriksetu-swd-mysql` (Port 3307)
2. `nagriksetu-swd-rabbitmq` (Ports 5672, 15672)
3. `nagriksetu-swd-backend` (Port 8004)
4. `nagriksetu-swd-frontend` (Port 5173)

### 4.3 Verifying Service Health
Check the container status:
```bash
docker compose ps
```
Or check the backend health endpoint:
```bash
curl http://localhost:8004/health
```
Expected output:
```json
{"service":"swd-service","status":"healthy","database":"mysql_8.0","version":"2.0.0","environment":"development"}
```

---

## 5. Portal Access & Demo Credentials

Open your browser to `http://localhost:5173`:

- **Pre-Seeded Administrator:**
  - Email: `swd.admin@nagriksetu.local`
  - Password: `SWDAdmin@2026!`
  - Role: `SWD_ADMIN` (Access to Scheme Management, Decision Drawer, Beneficiary Registry)
- **Pre-Seeded Citizen:**
  - Email: `citizen@example.com`
  - Password: `CitizenPass@2026`
  - Role: `CITIZEN` (Access to Scheme Discovery, Eligibility Checker, Application Tracking)

---

## 6. Running Automated Tests

The backend includes a comprehensive pytest suite testing all functional requirements (FR-SWD-001 through FR-SWD-021, FR-COM, FR-MQ, and FR-REC):

Run tests inside the backend container:
```bash
docker exec -e PYTHONPATH=/app nagriksetu-swd-backend pytest -v
```

Expected output:
```
tests/test_swd_service.py::test_health_endpoint PASSED                   [  8%]
tests/test_swd_service.py::test_get_categories PASSED                    [ 16%]
tests/test_swd_service.py::test_get_published_schemes PASSED             [ 25%]
tests/test_swd_service.py::test_eligibility_engine_satisfied PASSED      [ 33%]
tests/test_swd_service.py::test_eligibility_engine_unmet PASSED          [ 41%]
tests/test_swd_service.py::test_eligibility_engine_missing_data_insufficient PASSED [ 50%]
tests/test_swd_service.py::test_submit_application_workflow PASSED       [ 58%]
tests/test_swd_service.py::test_admin_dashboard_and_decision PASSED      [ 66%]
tests/test_swd_service.py::test_scheme_creation_and_update PASSED        [ 75%]
tests/test_swd_service.py::test_duplicate_application_detection PASSED   [ 83%]
tests/test_swd_service.py::test_recommendation_match_endpoint PASSED     [ 91%]
tests/test_swd_service.py::test_unauthorized_and_ownership_restrictions PASSED [100%]

======================= 12 passed in 2.99s =======================
```

---

## 7. Safe Docker Operations

To safely stop the containers without destroying data:
```bash
docker compose stop
```

To restart the containers:
```bash
docker compose start
```

> **CRITICAL SAFETY NOTICE:**  
> Never run `docker compose down -v` as it deletes database volumes.


## Smart Scheme Finder (Intelligent Scheme Matching)

The Smart Scheme Finder enables citizens and visitors to discover welfare programs matching their socioeconomic and demographic profile through an explainable, deterministic matching engine.

### Key Capabilities:
- Citizen Questionnaire: Gathers non-invasive parameters (Age, District, Taluk, Gender, Social Category, Annual Family Income, Occupation, Education, Farmer status, Student status, Woman/Girl child status, Disability percentage).
- Profile Independence: When logged in as a citizen, profile attributes prefill automatically. Changes made within the Smart Scheme Finder questionnaire are isolated to the active search and never overwrite the citizen permanent registry profile.
- Explainable Match Engine: Rules are evaluated in real-time on the FastAPI backend against 83 structured eligibility rules across 35 Karnataka welfare schemes.
- Honest Indicators: Results are categorized strictly as Potential Match, Check Requirements, or Not Matched. Absolute claims ("Government Approved", "Guaranteed Benefit") are barred.
- Direct Application Handoff: Eligible schemes with active online workflows navigate directly to the scheme application form with prefilled credentials, editable category selection, and single "Confirm & Submit" verification.

### Running the Smart Scheme Finder:
1. Open the portal at http://localhost:5175/ (or port 5174).
2. Click Smart Scheme Finder in the top navigation or hero section.
3. Review or customize your questionnaire answers.
4. Click Find Matching Schemes.
5. Explore matching schemes, filter by domain categories (Education, Women & Children, Agriculture, etc.), or search by keyword.
6. Click View Details for comprehensive official summaries, or click Apply Now to submit an official application.
