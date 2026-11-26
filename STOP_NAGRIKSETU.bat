@echo off
REM ==============================================================================
REM NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
REM STOP_NAGRIKSETU.bat — Windows CMD Safe Shutdown Script
REM ==============================================================================

echo Stopping NagrikSetu SWD Microservice containers safely...
echo Note: Database records and volumes are strictly preserved.
docker compose down

echo ==============================================================================
echo NagrikSetu SWD containers stopped cleanly.
echo All database tables and records in nagriksetu_swd remain intact.
echo ==============================================================================
pause
