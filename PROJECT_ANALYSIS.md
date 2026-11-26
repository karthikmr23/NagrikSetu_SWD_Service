# NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
## COMPREHENSIVE PROJECT & REQUIREMENT ANALYSIS (PHASE 1 & 2)

**Author:** Member 2 (Social Welfare Department Microservice Owner)  
**Project:** NagrikSetu – AI-Powered Integrated Citizen Education, Employment, Skill Development & Welfare Intelligence Platform  
**Target Architecture:** Microservices Architecture (FastAPI + MySQL 8.0 + React/TypeScript + RabbitMQ + API Gateway)

---

## 1. PROJECT CONTEXT & TEAM RESPONSIBILITIES

NagrikSetu is an integrated citizen welfare and opportunities platform developed collaboratively by 3 members:
* **Member 1:** Education Service, Employment Service, Job/Education Recommendation contribution.
* **Member 2 (MY ROLE):** Social Welfare Department (SWD) Microservice, Frontend, Backend, MySQL Database (`swd_db`), Welfare Scheme Catalogue, Eligibility Assessment Engine, Application Workflow, Document Management, Beneficiary Management, RabbitMQ Event Integration, and SWD Recommendation Engine Provider.
* **Member 3 (Team Lead):** Citizen & Family/Household Management (Administrative Service), Central Agentic AI Service, API Gateway (NGINX), Platform Authentication & Identity contracts.

> **STRICT SCOPE BOUNDARY:**
> As Member 2, I develop ONLY the SWD microservice (`services/swd-service/`). The uploaded Skill Development repository is inspected strictly as a reference for coding conventions, folder layout, and design token integration. It is not part of this deliverable and will not be included in the final archive.

---

## 2. REFERENCE INSPECTION FINDINGS

### 2.1 Skill Development Reference Project
1. **Backend Structure:** Clean FastAPI application with modular SQLAlchemy ORM models, Pydantic schemas, isolated database configuration, secure JWT utilities, RabbitMQ publisher adapter, and Pytest test suites.
2. **Database:** Dedicated isolated MySQL schema (`skill_db`), parameterized queries, safe restore script, and Alembic migrations.
3. **Frontend:** React + TypeScript + Vite with custom styling tokens conforming to the national civic design system (DM Sans & Manrope fonts, Deep Navy `#0f2444`, Saffron `#ea580c`, Emerald Green `#23774b`, clean card hierarchy).

### 2.2 Authoritative Functional Specification (Docx Extraction)
* **FR-SWD-001 to FR-SWD-006 (Scheme Catalogue):**
  * Scheme creation with name, description, administering authority, benefit summary.
  * Application dates, required document references, public instructions, and criteria.
  * Status lifecycle: `DRAFT`, `PUBLISHED`, `CLOSED`, `INACTIVE`.
  * Scheme update with audit history.
  * Citizen discovery: filter by category, keyword, status.
  * Scheme detail views with eligibility, deadlines, and application steps.
* **FR-SWD-007 to FR-SWD-013 (Eligibility Engine):**
  * Configurable criteria using defined fields (age, income, education, caste category, residence, disability status), operators (`EQUALS`, `NOT_EQUALS`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`, `IN`, `NOT_IN`), and value types.
  * Strict validation rejecting malformed rules.
  * Rule evaluation returning `SATISFIED`, `UNMET`, or `UNKNOWN`.
  * Missing information tracking: unknown values are NEVER treated as satisfied.
  * Criterion-level explanations and rule version tracking.
  * Mandatory disclaimer: "You appear to meet the preliminary criteria based on the information available. Final eligibility is determined by the authorized department."
  * Human-in-the-loop decision boundary: system never issues official approval or rejection.
* **FR-SWD-014 to FR-SWD-021 (Application & Beneficiary Workflow):**
  * Submission to published schemes within valid date windows.
  * Validation of required fields and document references.
  * Lifecycle tracking: `SUBMITTED`, `UNDER_REVIEW`, `MORE_INFORMATION_REQUIRED`, `APPROVED`, `REJECTED`.
  * Citizen application tracking and immutable history timeline.
  * Administrative review: information requests, decision recording with reasons.
  * Beneficiary record creation strictly upon authorized approval.
  * Duplicate application detection flagging items for human review without automatic rejection.
  * Event publishing: `SCHEME_APPLICATION_CREATED`, `SCHEME_APPLICATION_UPDATED`.
* **FR-REC-015 to FR-REC-018 (Recommendation Engine Contribution):**
  * Pre-filtering published schemes.
  * Categorization: `LIKELY_MATCH`, `POSSIBLE_MATCH`, `UNMET_CRITERIA`, `INSUFFICIENT_INFORMATION`.
  * Match explanations and missing criteria identification.
* **FR-COM-001 to FR-COM-014 (Shared Microservice Requirements):**
  * Health check (`GET /health`), request validation, structured error codes, schema isolation, OpenAPI docs, RBAC & citizen ownership enforcement, audit logging, correlation IDs, environment-based configuration, container readiness.

### 2.3 Exact Visual Identity (WhatsApp Reference Image)
The WhatsApp screenshot (`media_1794456225900_a164bcfb.jpg`) defines the exact NagrikSetu visual standard:
1. **Top Header:** Clean white header with National Emblazonment, "NagrikSetu (नागरिक सेतु) — Unified Public Administration & Citizen Services Platform", quick links (WhatsApp Bot & QR, Citizen Sign In, Citizen Registration, Admin Portal).
2. **Hero Section:** Deep Blue/Navy gradient (`#0f2444` to `#132d4a`), official emblem header ("राष्ट्रीय डिजिटल शासन पहल | NATIONAL DIGITAL GOVERNANCE INITIATIVE"), bilingual typography ("नागरिक सेतु — NagrikSetu"), and call-to-action buttons (Saffron Orange "Citizen Registration", Emerald Green "WhatsApp Bot & QR Code", Dark Navy "Citizen Sign In").
3. **Services Grid:** "Essential Public & Welfare Services (नागरिक कल्याणकारी सेवाएं)" showing 4 core streams:
   * Education Service
   * Employment Service
   * Skill Development Service
   * **SWD (Social Welfare Development) Service** (Highlighted with peach/amber border, heart-handshake icon, tags for National Social Assistance, Divyangjan Disability Aid, DBT, Senior Citizen Welfare).
4. **Civic Modules Grid:** Official Citizen Registry, Household & Dwelling Management, Landbot WhatsApp Services.
5. **Accessibility Banner:** Government Inclusivity & WCAG 2.2 AA Standards badge.
6. **Pre-Seeded Demonstration Credentials:** Quick login badges for seamless presentation and testing.

---

## 3. SWD MICROSERVICE ARCHITECTURE PLAN

```
+-----------------------------------------------------------------------+
|                         NAGRIKSETU FRONTEND                           |
|       (React 18 + TypeScript + Vite + NagrikSetu Design System)       |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                    NGINX API GATEWAY / REVERSE PROXY                  |
|                 Prefix: /api/swd/*  -->  Port 8004                    |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                    SWD MICROSERVICE (FastAPI :8004)                   |
|  - Scheme Catalogue Router       - Preliminary Eligibility Engine     |
|  - Application Lifecycle Router   - Document Upload & Storage Handler  |
|  - Admin Dashboard & Review Router- Beneficiary Registry Router       |
|  - Recommendation Query Router   - JWT & RBAC Auth Middleware         |
|  - Outbox & RabbitMQ Publisher   - Structured Audit Logger            |
+-----------------------------------------------------------------------+
          |                                            |
          v                                            v
+-----------------------------+           +-----------------------------+
|    MySQL 8.0 (swd_db)       |           |   RabbitMQ Event Broker     |
|  10 Core Relational Tables  |           |   Exchange: nagriksetu.events|
|  Strict Schema Isolation    |           |   Key: swd.application.*    |
+-----------------------------+           +-----------------------------+
```

---

## 4. DETAILED IMPLEMENTATION PHASES

* **Phase 1-3:** Analysis & Architecture (Complete).
* **Phase 4:** MySQL 8.0 `swd_db` Schema & Setup Scripts (`swd_db_setup.sql` + Python safe migration/restore).
* **Phase 5-7:** Backend Implementation (FastAPI, SQLAlchemy, Pydantic, Rule Engine, Workflow, Beneficiaries, Documents, Audit).
* **Phase 8-9:** Frontend Implementation (12 distinct pages matching the WhatsApp screenshot).
* **Phase 10-13:** Security, RabbitMQ Events, API Gateway config & Recommendation Engine integration.
* **Phase 14-16:** Dockerization, Automated Testing (Backend & Frontend), Visual Verification.
* **Phase 17-19:** Technical Documentation & `NagrikSetu_SWD_Final.zip` creation.
