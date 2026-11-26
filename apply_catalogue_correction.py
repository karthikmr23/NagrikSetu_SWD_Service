# Apply catalogue exclusion for Shakti and the 6 temporarily hidden schemes

import os

# Definition of excluded scheme codes:
# 1. Mandatory exclusion: Shakti Free Bus Travel Scheme
# 2. Six temporarily hidden schemes:
#    - Post-Matric Scholarship for SC/ST and Backward Classes Students (KAR-SSP-POSTMATRIC)
#    - Disability Maintenance & Assistive Aid Grant (KAR-DIVYANGJAN-PENSION)
#    - Farmer Irrigation Assistance Scheme (Micro-Irrigation) (KAR-AGR-MICRO-IRRIGATION)
#    - ELEVATE & ELEVATE NxT Startup Grants (KAR-EDU-ELEVATE)
#    - Rajiv Gandhi Entrepreneurship Program (KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR)
#    - Ambedkar Karmika Sahaya Hastha (KAR-LAB-AMBEDKAR-KARMIKA)

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]

# 1. Update schemes.py
schemes_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\schemes.py"
with open(schemes_path, "r", encoding="utf-8") as f:
    s_code = f.read()

# Define the constant near top or inside module
if "CATALOGUE_HIDDEN_CODES =" not in s_code:
    s_code = s_code.replace(
        "router = APIRouter(prefix=\"/api/swd\", tags=[\"SWD Welfare Schemes\"])",
        '''router = APIRouter(prefix="/api/swd", tags=["SWD Welfare Schemes"])

# Explicit catalogue exclusions:
# 1. Mandatory exclusion: Shakti Free Bus Travel Scheme
# 2. Six temporarily hidden schemes (preserved in database and history)
CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]'''
    )

old_filter = '''    # Non-destructive exclusion: Shakti Scheme (Transport Dept) is excluded from SWD catalogue
    query = query.filter(~Scheme.scheme_code.ilike("%SHAKTI%"), ~Scheme.name.ilike("%SHAKTI%"))'''

new_filter = '''    # Non-destructive catalogue exclusion for Shakti and temporarily hidden schemes
    query = query.filter(
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    )'''

assert old_filter in s_code, "old_filter not found in schemes.py"
s_code = s_code.replace(old_filter, new_filter)

# Form retrieval exclusion
old_form_check = '''    # Exclude Shakti Scheme from SWD application forms
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if scheme and ("shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower()):
        return None'''

new_form_check = '''    # Exclude Shakti and temporarily hidden schemes from active citizen application forms
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if scheme and (scheme.scheme_code in CATALOGUE_HIDDEN_CODES or "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower()):
        return None'''

assert old_form_check in s_code, "old_form_check not found in schemes.py"
s_code = s_code.replace(old_form_check, new_form_check)

with open(schemes_path, "w", encoding="utf-8") as f:
    f.write(s_code)
print("Updated schemes.py successfully")


# 2. Update finder.py
finder_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\finder.py"
with open(finder_path, "r", encoding="utf-8") as f:
    f_code = f.read()

# Add CATALOGUE_HIDDEN_CODES
if "CATALOGUE_HIDDEN_CODES =" not in f_code:
    f_code = f_code.replace(
        "router = APIRouter(prefix=\"/api/swd\", tags=[\"Smart Scheme Finder\"])",
        '''router = APIRouter(prefix="/api/swd", tags=["Smart Scheme Finder"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]'''
    )

old_finder_filter = '''    # Query all published schemes (excluding non-SWD Shakti scheme)
    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

new_finder_filter = '''    # Query all published schemes (excluding Shakti and temporarily hidden schemes)
    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

assert old_finder_filter in f_code, "old_finder_filter not found in finder.py"
f_code = f_code.replace(old_finder_filter, new_finder_filter)

with open(finder_path, "w", encoding="utf-8") as f:
    f.write(f_code)
print("Updated finder.py successfully")


# 3. Update recommendations.py
rec_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\recommendations.py"
with open(rec_path, "r", encoding="utf-8") as f:
    r_code = f.read()

if "CATALOGUE_HIDDEN_CODES =" not in r_code:
    r_code = r_code.replace(
        "router = APIRouter(prefix=\"/api/swd\", tags=[\"SWD Recommendation Integration\"])",
        '''router = APIRouter(prefix="/api/swd", tags=["SWD Recommendation Integration"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]'''
    )

old_rec_filter = '''    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

new_rec_filter = '''    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

assert old_rec_filter in r_code, "old_rec_filter not found in recommendations.py"
r_code = r_code.replace(old_rec_filter, new_rec_filter)

with open(rec_path, "w", encoding="utf-8") as f:
    f.write(r_code)
print("Updated recommendations.py successfully")


# 4. Update applications.py
apps_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\applications.py"
with open(apps_path, "r", encoding="utf-8") as f:
    a_code = f.read()

if "CATALOGUE_HIDDEN_CODES =" not in a_code:
    a_code = a_code.replace(
        "router = APIRouter(prefix=\"/api/swd\", tags=[\"SWD Applications\"])",
        '''router = APIRouter(prefix="/api/swd", tags=["SWD Applications"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]'''
    )

old_app_guard = '''    if "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The Shakti Scheme is administered under the Transport Department and is not an SWD application scheme."
        )'''

new_app_guard = '''    if scheme.scheme_code in CATALOGUE_HIDDEN_CODES or "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower():
        detail_msg = "The Shakti Scheme is administered under the Transport Department and is not an SWD application scheme." if "shakti" in (scheme.scheme_code or "").lower() else "This scheme application window is currently inactive or under administrative review."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_msg
        )'''

assert old_app_guard in a_code, "old_app_guard not found in applications.py"
a_code = a_code.replace(old_app_guard, new_app_guard)

with open(apps_path, "w", encoding="utf-8") as f:
    f.write(a_code)
print("Updated applications.py successfully")


# 5. Update admin.py
admin_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py"
with open(admin_path, "r", encoding="utf-8") as f:
    adm_code = f.read()

if "CATALOGUE_HIDDEN_CODES =" not in adm_code:
    adm_code = adm_code.replace(
        "router = APIRouter(prefix=\"/api/swd/admin\", tags=[\"SWD Administrative Management\"])",
        '''router = APIRouter(prefix="/api/swd/admin", tags=["SWD Administrative Management"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]'''
    )

old_adm_dash = '''    # Exclude non-SWD Shakti scheme from dashboard SWD scheme metrics
    swd_schemes_q = db.query(Scheme).filter(~Scheme.scheme_code.ilike("%SHAKTI%"), ~Scheme.name.ilike("%SHAKTI%"))'''

new_adm_dash = '''    # Exclude Shakti and temporarily hidden schemes from active catalogue metrics
    swd_schemes_q = db.query(Scheme).filter(
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    )'''

assert old_adm_dash in adm_code, "old_adm_dash not found in admin.py"
adm_code = adm_code.replace(old_adm_dash, new_adm_dash)

# Also category breakdown
old_adm_cat = '''        # Scheme-wise breakdown in this category (excluding non-SWD Shakti)
        schemes_in_cat = db.query(Scheme).filter(
            Scheme.category_id == cat.id,
            ~Scheme.scheme_code.ilike("%SHAKTI%"),
            ~Scheme.name.ilike("%SHAKTI%")
        ).all()'''

new_adm_cat = '''        # Scheme-wise breakdown in this category (excluding Shakti and hidden schemes)
        schemes_in_cat = db.query(Scheme).filter(
            Scheme.category_id == cat.id,
            ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
            ~Scheme.scheme_code.ilike("%SHAKTI%"),
            ~Scheme.name.ilike("%SHAKTI%")
        ).all()'''

assert old_adm_cat in adm_code, "old_adm_cat not found in admin.py"
adm_code = adm_code.replace(old_adm_cat, new_adm_cat)

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(adm_code)
print("Updated admin.py successfully")
