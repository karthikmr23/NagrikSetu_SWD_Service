# NAGRIKSETU — SWD DOCKER DEPLOYMENT SPECIFICATION

### 1. Services in Docker Compose
* `nagriksetu-swd-mysql`: MySQL 8.0 on port 3306 with health check and initialization DDL mount.
* `nagriksetu-swd-rabbitmq`: RabbitMQ 3-management on ports 5672 (AMQP) & 15672 (Management).
* `nagriksetu-swd-backend`: Python 3.11 / FastAPI on port 8004.
* `nagriksetu-swd-frontend`: Multi-stage Node/NGINX container on port 5173.

### 2. Startup Command
```bash
docker compose up -d --build
```
