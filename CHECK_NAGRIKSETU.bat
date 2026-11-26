@echo off
REM ==============================================================================
REM NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
REM CHECK_NAGRIKSETU.bat — Container Status & Health Check Script
REM ==============================================================================

echo Inspecting NagrikSetu SWD container status...
docker compose ps

echo.
echo Checking backend health endpoint directly...
curl -s http://127.0.0.1:8004/health
echo.
pause
