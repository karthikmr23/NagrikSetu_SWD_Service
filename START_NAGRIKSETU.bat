@echo off
REM ==============================================================================
REM NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
REM START_NAGRIKSETU.bat — Windows CMD Startup Script
REM ==============================================================================

echo [1/3] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in your system PATH.
    echo Please install Docker Desktop for Windows.
    pause
    exit /b 1
)

echo [2/3] Checking if Docker Engine / Desktop is running...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Desktop is not currently running.
    echo Please start Docker Desktop and wait until the engine is ready.
    pause
    exit /b 1
)

echo [3/3] Starting NagrikSetu SWD Microservice via Docker Compose...
echo Building and starting containers in detached mode...
docker compose up -d --build

if %errorlevel% equ 0 (
    echo ==============================================================================
    echo NAGRIKSETU SWD MICROSERVICE STARTED SUCCESSFULLY!
    echo ==============================================================================
    echo.
    echo  Frontend Portal:    http://127.0.0.1:5174/
    echo  Backend Swagger:    http://127.0.0.1:8004/docs
    echo  Health Check:       http://127.0.0.1:8004/health
    echo.
    echo Port 5173 remains untouched for your Skill Development application.
    echo Database: nagriksetu_swd on host port 3308 (skill_db is preserved).
    echo ==============================================================================
) else (
    echo [ERROR] Failed to start containers. Check output above.
)
pause
