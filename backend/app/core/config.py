import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore", env_file=".env")

    SERVICE_NAME: str = "swd-service"
    ENVIRONMENT: str = "development"
    PORT: int = 8004
    LOG_LEVEL: str = "INFO"

    # MySQL Database Settings (nagriksetu_swd dedicated schema on Windows host port 3306)
    DB_HOST: str = "host.docker.internal"
    DB_PORT: int = 3306
    DB_NAME: str = "nagriksetu_swd"
    DB_USER: str = "swd_app"
    DB_PASSWORD: str = "swd-secure-pass-2026"
    DATABASE_URL: str = ""

    # Backward compatibility mappings
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 0
    MYSQL_DATABASE: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""

    # Security & JWT
    JWT_SECRET: str = "nagriksetu-swd-super-secret-key-2026-xyz-min32chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Default Pre-Seeded SWD Administrator
    ADMIN_EMAIL: str = "swd.admin@nagriksetu.local"
    ADMIN_PASSWORD: str = "SWDAdmin@2026!"

    # CORS & Integration
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:8004,http://localhost:8005,http://localhost:8000,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175,http://localhost:3000,http://127.0.0.1:3000"
    SWD_API_BASE_URL: str = "http://127.0.0.1:8004"
    SWD_FRONTEND_URL: str = "http://127.0.0.1:5174"
    MAIN_WEBSITE_URL: str = "http://127.0.0.1:5173"

    # RabbitMQ
    RABBITMQ_HOST: str = "host.docker.internal"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "nagriksetu"
    RABBITMQ_PASSWORD: str = "rabbitmq-pass-2026"
    RABBITMQ_EXCHANGE: str = "nagriksetu.events"
    RABBITMQ_ENABLED: bool = False

    # Documents
    UPLOAD_DIR: str = "./uploads/documents"
    MAX_UPLOAD_SIZE_MB: int = 5

    # Integration URLs
    ADMIN_SERVICE_URL: str = "http://localhost:8001"
    RECOMMENDATION_SERVICE_URL: str = "http://localhost:8005"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def effective_db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        host = self.DB_HOST or self.MYSQL_HOST or "host.docker.internal"
        port = self.DB_PORT or self.MYSQL_PORT or 3306
        name = self.DB_NAME or self.MYSQL_DATABASE or "nagriksetu_swd"
        user = self.DB_USER or self.MYSQL_USER or "swd_app"
        pw = self.DB_PASSWORD or self.MYSQL_PASSWORD or "swd-secure-pass-2026"
        return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{name}"

settings = Settings()
