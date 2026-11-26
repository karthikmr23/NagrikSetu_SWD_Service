# Fix constant definition in schemes.py and admin.py

codes_block = """CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]
"""

# 1. schemes.py
schemes_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\schemes.py"
with open(schemes_path, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace(
    'router = APIRouter(prefix="/api/swd", tags=["SWD Schemes"])',
    'router = APIRouter(prefix="/api/swd", tags=["SWD Schemes"])\n\n' + codes_block
)

with open(schemes_path, "w", encoding="utf-8") as f:
    f.write(s)
print("Added CATALOGUE_HIDDEN_CODES to schemes.py")

# 2. admin.py
admin_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py"
with open(admin_path, "r", encoding="utf-8") as f:
    a = f.read()

a = a.replace(
    'router = APIRouter(prefix="/api/swd/admin", tags=["SWD Administration"])',
    'router = APIRouter(prefix="/api/swd/admin", tags=["SWD Administration"])\n\n' + codes_block
)

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(a)
print("Added CATALOGUE_HIDDEN_CODES to admin.py")
