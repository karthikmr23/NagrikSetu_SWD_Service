import zipfile
import os

zip_path = r'C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD.zip'
print(f'Checking {zip_path} ({os.path.getsize(zip_path)} bytes)...')

with zipfile.ZipFile(zip_path, 'r') as z:
    names = z.namelist()
    print(f'Total files in archive: {len(names)}')
    
    checks = [
        'SWD_FINAL/docker-compose.yml',
        'SWD_FINAL/README.md',
        'SWD_FINAL/.env.example',
        'SWD_FINAL/START_NAGRIKSETU.bat',
        'SWD_FINAL/STOP_NAGRIKSETU.bat',
        'SWD_FINAL/CHECK_NAGRIKSETU.bat',
        'SWD_FINAL/VIEW_LOGS.bat',
        'SWD_FINAL/database/swd_migration_backup_20261124.sql',
        'SWD_FINAL/frontend/package.json',
        'SWD_FINAL/backend/requirements.txt',
        'SWD_FINAL/backend/app/main.py',
        'SWD_FINAL/backend/Dockerfile',
        'SWD_FINAL/frontend/Dockerfile'
    ]
    for c in checks:
        found = c in names
        print(f'  {c}: {"PRESENT" if found else "MISSING"}')
        
    exclusions = [
        'SWD_FINAL/PRIVATE_DEMO_CREDENTIALS.txt',
        'SWD_FINAL/verified_pre_audit_backup.sql',
        'SWD_FINAL/.env'
    ]
    for e in exclusions:
        leak = e in names
        print(f'  Sensitive check {e}: {"SAFE_EXCLUDED" if not leak else "LEAKED"}')
