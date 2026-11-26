# NagrikSetu — Social Welfare Department (SWD) Microservice
## Integration Guide for Main NagrikSetu Platform

This guide is intended for team members and external developers integrating the Social Welfare Department (SWD) microservice into the unified NagrikSetu platform.

---

### 1. Architecture Overview
- **Service Name:** `swd-service`
- **Department:** Social Welfare Department (Government of Karnataka)
- **Role:** Dedicated Microservice for social security pensions, post-matric education scholarships, Divyangjan disability grants, and inter-caste marital incentives.
- **Backend Framework:** FastAPI (Python 3.10+)
- **Frontend Framework:** React 18 + TypeScript + Vite
- **Database:** Dedicated MySQL 8.0 schema `nagriksetu_swd` (User: `swd_app`)
- **Port Allocations:**
  - SWD Frontend: `http://127.0.0.1:5174/`
  - SWD Backend: `http://127.0.0.1:8004/`
  - Swagger Documentation: `http://127.0.0.1:8004/docs`
  - Database: MySQL port `3308` (completely isolated from `skill_db`)

---

### 2. Integration Contract & Endpoints
The SWD microservice exposes all capabilities under the standardized versioned prefix:

`/api/v1/swd/` (and backward-compatible `/api/swd/`)

| Domain | Method | Endpoint Path | Description | Access Role |
| :--- | :---: | :--- | :--- | :---: |
| **Auth** | POST | `/api/v1/swd/auth/register` | Register new citizen | Public |
| **Auth** | POST | `/api/v1/swd/auth/login` | Citizen / Officer / Admin Login | Public |
| **Schemes** | GET | `/api/v1/swd/schemes` | Published scheme catalogue | Public |
| **Schemes** | GET | `/api/v1/swd/schemes/{id}` | Detailed scheme metadata | Public |
| **Eligibility** | POST | `/api/v1/swd/schemes/{id}/eligibility-check` | Preliminary rule evaluation | Public / Citizen |
| **Applications** | POST | `/api/v1/swd/schemes/{id}/applications` | Submit scheme application | `CITIZEN` |
| **Applications** | GET | `/api/v1/swd/applications/{citizen_id}` | Track citizen dossiers | `CITIZEN` |
| **Public Track**| GET | `/api/v1/swd/public/track-status/{app_num}` | Non-login status lookup | Public |
| **Officer** | GET | `/api/v1/swd/admin/officer/assigned-applications` | Officer scrutiny list | `WELFARE_OFFICER` |
| **Officer** | POST | `/api/v1/swd/admin/applications/{id}/request-information`| Request supplementary docs | `WELFARE_OFFICER` |
| **Officer** | POST | `/api/v1/swd/admin/applications/{id}/decision` | Approve / Reject | `ADMINISTRATOR` |
| **DBT** | GET | `/api/v1/swd/dbt/dashboard-stats` | KPI summary & budget | `ADMINISTRATOR` |
| **DBT** | POST | `/api/v1/swd/dbt/batch-process` | Atomic simulated batch DBT | `ADMINISTRATOR` |
| **DBT** | GET | `/api/v1/swd/dbt/batch-report` | CSV transaction export | `ADMINISTRATOR` |
| **Grievance** | POST | `/api/v1/swd/grievances` | Submit citizen grievance | `CITIZEN` |
| **Grievance** | GET | `/api/v1/swd/grievances` | List & filter grievances | Role-based |

---

### 3. Authentication & SSO Integration Approach
The SWD microservice uses standard **JWT Bearer Tokens** (`Authorization: Bearer <token>`).

To integrate shared authentication with the Main Platform:
1. Ensure the Main Platform issues JWT tokens signed with the agreed `JWT_SECRET` (configured in `.env`).
2. Payload claims expected by SWD:
   - `sub`: Unique Citizen or Admin Identifier (e.g. `CIT-KA-9901`)
   - `role`: One of `CITIZEN`, `WELFARE_OFFICER`, or `ADMINISTRATOR`
   - `email`: User email address
   - `name`: Legal name as per Aadhaar Card
   - `state`: State of permanent domicile (default `Karnataka`)
   - `caste`: Social reservation category
3. The SWD backend validates signature, expiration, and role permissions automatically.

---

### 4. CORS & Routing Configuration
Configure the following in `NagrikSetu_SWD_FINAL/.env`:

```env
MAIN_WEBSITE_URL=http://localhost:5173
SWD_FRONTEND_URL=http://localhost:5174
SWD_API_BASE_URL=http://localhost:8004
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174
```

---

### 5. Docker Deployment via Windows CMD
To start the microservice:
```cmd
cd /d "C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final"
START_NAGRIKSETU.bat
```
To stop the microservice safely without losing database records:
```cmd
STOP_NAGRIKSETU.bat
```
