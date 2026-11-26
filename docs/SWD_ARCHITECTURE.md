# NAGRIKSETU — SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
## TECHNICAL ARCHITECTURE SPECIFICATION (MEMBER 2 DELIVERABLE)

### 1. High-Level System Architecture

```
+--------------------------------------------------------------------------+
|                             CITIZEN BROWSER                              |
|           React 18 + TypeScript + Vite (Port 5173 / Container: 80)       |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                        NGINX API GATEWAY (Member 3)                      |
|                  Route Prefix: /api/swd/*  --> Port 8004                 |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                     SWD FASTAPI MICROSERVICE (Port 8004)                 |
|                                                                          |
|  +--------------------+  +--------------------+  +--------------------+  |
|  |  Scheme Catalogue  |  | Eligibility Engine |  | Application Flow   |  |
|  |  - CRUD & Search   |  | - Rules Evaluator  |  | - State Machine    |  |
|  |  - Active/Closed   |  | - Missing Fields   |  | - Duplicate Warning|  |
|  +--------------------+  +--------------------+  +--------------------+  |
|                                                                          |
|  +--------------------+  +--------------------+  +--------------------+  |
|  | Document Manager   |  | Admin Command Ctr  |  | Event Publisher    |  |
|  | - MIME Validation  |  | - Review & Audit   |  | - Transactional    |  |
|  | - Secure Storage   |  | - Beneficiaries    |  | - RabbitMQ Outbox  |  |
|  +--------------------+  +--------------------+  +--------------------+  |
+--------------------------------------------------------------------------+
              |                                            |
              v                                            v
+---------------------------+                +---------------------------+
|    MySQL 8.0 (swd_db)     |                |   RabbitMQ Event Broker   |
|   10 Relational Tables    |                |   Exchange:               |
|   Strict Schema Isolation |                |     nagriksetu.events     |
+---------------------------+                +---------------------------+
```

### 2. Microservice Boundaries & Responsibilities

1. **Owns Database `swd_db`:** Schemes, Categories, Eligibility Rules, Scheme Documents, Applications, Application Documents, Application History, Beneficiaries, Audit Logs, Outbox Events.
2. **Citizen Identity Decoupling:** Citizen and family records remain owned by Member 3 (Administrative Service). SWD references `citizen_id` and verifies identity and roles via standards-compliant JWT claims.
3. **Event Contract Compliance:**
   * Topic Exchange: `nagriksetu.events`
   * Outbox pattern guarantees message publishing after database commit.
   * Minimal payload schema without personal or sensitive citizen information.
