import time
import uuid
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.connection import engine, Base
from app.routers import (
    schemes, eligibility, applications, admin, beneficiaries, 
    recommendations, auth, grievances, reports, finder, offices, receipts
)

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("swd.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing NagrikSetu Social Welfare Department (SWD) Microservice...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")
    except Exception as e:
        logger.warning(f"Database auto-creation note: {e}")
    yield
    logger.info("Shutting down SWD Microservice.")

app = FastAPI(
    title="NagrikSetu - Social Welfare Department (SWD) Microservice",
    description="Official REST API for Social Welfare Department Schemes, Eligibility Rules Engine, Application Lifecycle, Officer Reviews, DBT Payments, Grievances, Office Locator, and PDF Receipts.",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID & Observability Middleware
@app.middleware("http")
async def correlation_id_and_audit_middleware(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    request.state.correlation_id = correlation_id

    response: Response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    logger.info(
        f"[{correlation_id}] {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)"
    )
    return response

# Standard Health Endpoint
@app.get("/health", tags=["Service Health"])
def health_check():
    return {
        "service": settings.SERVICE_NAME,
        "status": "healthy",
        "database": settings.MYSQL_DATABASE,
        "version": "2.1.0",
        "environment": settings.ENVIRONMENT
    }

# Register Routers (Both /api/swd and /api/v1/swd)
routers_list = [
    auth.router, schemes.router, eligibility.router, applications.router,
    admin.router, beneficiaries.router, grievances.router, reports.router,
    recommendations.router, finder.router, offices.router, receipts.router
]

for r in routers_list:
    app.include_router(r)

# Mirror under /api/v1/swd without breaking existing contracts
v1_app_router = FastAPI()
for r in routers_list:
    for route in r.routes:
        rel_path = route.path.replace("/api/swd", "/api/v1/swd")
        app.router.add_api_route(
            rel_path,
            route.endpoint,
            methods=route.methods,
            response_model=getattr(route, "response_model", None),
            status_code=getattr(route, "status_code", 200),
            tags=[f"v1 - {route.tags[0]}" if route.tags else "v1"],
            dependencies=getattr(route, "dependencies", None),
            summary=getattr(route, "summary", None),
            description=getattr(route, "description", None)
        )
