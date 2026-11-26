# NAGRIKSETU — SWD RABBITMQ EVENT CONTRACTS (FR-SWD-021)

### 1. Broker Configuration
* **Broker:** RabbitMQ 3.12+ (AMQP 0-9-1)
* **Topic Exchange:** `nagriksetu.events` (Durable)

### 2. Event Catalogue
* **`SCHEME_APPLICATION_CREATED`**
  * Routing key: `swd.scheme_application_created`
  * Purpose: Notifies downstream verification and recommendation workers.
* **`SCHEME_APPLICATION_UPDATED`**
  * Routing key: `swd.scheme_application_updated`
  * Purpose: Synchronizes application status and reviewer remarks.
