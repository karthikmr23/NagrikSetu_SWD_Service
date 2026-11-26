@echo off
REM ==============================================================================
REM NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
REM VIEW_LOGS.bat — View Real-Time Service Logs
REM ==============================================================================

echo Streaming logs from NagrikSetu SWD backend and frontend...
echo Press Ctrl + C to exit log stream.
docker compose logs -f --tail 100
pause
