# NAGRIKSETU — SWD PLATFORM INTEGRATION
## RabbitMQ Events, Recommendation Engine & API Gateway

### 1. RabbitMQ Event Contracts (FR-SWD-021 & Section 15)

* **Exchange:** `nagriksetu.events` (Topic, Durable)
* **Routing Keys:**
  * `swd.scheme_application_created`
  * `swd.scheme_application_updated`

#### Event Envelope (FR-MQ-002 & FR-MQ-004):
```json
{
  "event_id": "evt_swd_1731384000000",
  "event_type": "SCHEME_APPLICATION_CREATED",
  "schema_version": "1.0",
  "timestamp": "2026-11-12T09:30:00Z",
  "correlation_id": "SWD-APP-2026-000101",
  "publisher": "swd-service",
  "payload": {
    "application_id": 1,
    "application_number": "SWD-APP-2026-000101",
    "scheme_id": 1,
    "scheme_code": "KAR-SSP-POSTMATRIC",
    "citizen_id": "CIT-KA-9901",
    "status": "SUBMITTED",
    "is_duplicate_suspect": false
  }
}
```
* **Privacy Minimization:** Full bank account numbers, passwords, and private citizen profiles are **excluded** from event payloads.

---

### 2. Recommendation Engine Integration (FR-REC-015 to FR-REC-018)

* **Endpoint:** `POST /api/swd/recommendations/match`
* **Consumer:** Member 3's Recommendation Engine / Central Agentic AI.
* **Response Categories:**
  * `LIKELY_MATCH`: High score (0.95), all preliminary criteria met.
  * `POSSIBLE_MATCH`: Moderate score (0.50), partially satisfied with missing non-mandatory criteria.
  * `INSUFFICIENT_INFORMATION`: Missing essential attributes.
  * `UNMET_CRITERIA`: Mandatory criteria not satisfied.
* **Explanation:** Clear human-readable justification provided for every surfaced scheme.

---

### 3. API Gateway (NGINX) Routing Snippet (Member 3 Gateway Integration)

```nginx
# NagrikSetu Central Gateway Integration Snippet for SWD
upstream swd_microservice {
    server swd-backend:8004;
}

server {
    listen 80;

    # SWD Microservice API Prefix
    location /api/swd/ {
        proxy_pass http://swd_microservice;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Correlation-ID $request_id;
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
    }

    # SWD Health Endpoint
    location /health/swd {
        proxy_pass http://swd_microservice/health;
    }
}
```
