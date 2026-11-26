# Script to patch backend routers to exclude Shakti Scheme from SWD catalogue, recommendations, and options

import os

# 1. Patch app/routers/schemes.py
schemes_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\schemes.py"
with open(schemes_path, "r", encoding="utf-8") as f:
    schemes_code = f.read()

# Filter out Shakti in get_schemes
old_get_schemes = '''    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            or_(
                Scheme.name.ilike(search_fmt),
                Scheme.description.ilike(search_fmt),
                Scheme.scheme_code.ilike(search_fmt),
                Scheme.department.ilike(search_fmt),
                Scheme.beneficiary_categories.ilike(search_fmt)
            )
        )

    return query.order_by(Scheme.id.asc()).offset(skip).limit(limit).all()'''

new_get_schemes = '''    # Non-destructive exclusion: Shakti Scheme (Transport Dept) is excluded from SWD catalogue
    query = query.filter(~Scheme.scheme_code.ilike("%SHAKTI%"), ~Scheme.name.ilike("%SHAKTI%"))

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            or_(
                Scheme.name.ilike(search_fmt),
                Scheme.description.ilike(search_fmt),
                Scheme.scheme_code.ilike(search_fmt),
                Scheme.department.ilike(search_fmt),
                Scheme.beneficiary_categories.ilike(search_fmt)
            )
        )

    return query.order_by(Scheme.id.asc()).offset(skip).limit(limit).all()'''

assert old_get_schemes in schemes_code, "old_get_schemes not found in schemes.py"
schemes_code = schemes_code.replace(old_get_schemes, new_get_schemes)

# Also block Shakti from dynamic form retrieval and direct apply options if queried
old_get_form = '''    form = db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id,
        DynamicFormDefinition.is_active == True
    ).first()
    return form'''

new_get_form = '''    # Exclude Shakti Scheme from SWD application forms
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if scheme and ("shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower()):
        return None
    form = db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id,
        DynamicFormDefinition.is_active == True
    ).first()
    return form'''

assert old_get_form in schemes_code, "old_get_form not found in schemes.py"
schemes_code = schemes_code.replace(old_get_form, new_get_form)

with open(schemes_path, "w", encoding="utf-8") as f:
    f.write(schemes_code)
print("Successfully patched schemes.py")


# 2. Patch app/routers/finder.py
finder_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\finder.py"
with open(finder_path, "r", encoding="utf-8") as f:
    finder_code = f.read()

# Remove KAR-FLAG-SHAKTI from ACTIVE_APPLICATION_SCHEMES
finder_code = finder_code.replace('"KAR-FLAG-SHAKTI",\n', '')

# Exclude Shakti from published_schemes query in match_smart_schemes
old_finder_query = '''    # Query all published schemes
    published_schemes = db.query(Scheme).filter(Scheme.status == "PUBLISHED").all()'''

new_finder_query = '''    # Query all published schemes (excluding non-SWD Shakti scheme)
    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

assert old_finder_query in finder_code, "old_finder_query not found in finder.py"
finder_code = finder_code.replace(old_finder_query, new_finder_query)

with open(finder_path, "w", encoding="utf-8") as f:
    f.write(finder_code)
print("Successfully patched finder.py")


# 3. Patch app/routers/recommendations.py
rec_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\recommendations.py"
with open(rec_path, "r", encoding="utf-8") as f:
    rec_code = f.read()

old_rec_query = '''    published_schemes = db.query(Scheme).filter(Scheme.status == "PUBLISHED").all()'''
new_rec_query = '''    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()'''

assert old_rec_query in rec_code, "old_rec_query not found in recommendations.py"
rec_code = rec_code.replace(old_rec_query, new_rec_query)

with open(rec_path, "w", encoding="utf-8") as f:
    f.write(rec_code)
print("Successfully patched recommendations.py")


# 4. Patch app/routers/applications.py to block application submission for Shakti
apps_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\applications.py"
with open(apps_path, "r", encoding="utf-8") as f:
    apps_code = f.read()

old_apps_check = '''    # 1. Verify scheme is open and active (FR-SWD-014)
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")'''

new_apps_check = '''    # 1. Verify scheme is open and active (FR-SWD-014)
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    if "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The Shakti Scheme is administered under the Transport Department and is not an SWD application scheme."
        )'''

assert old_apps_check in apps_code, "old_apps_check not found in applications.py"
apps_code = apps_code.replace(old_apps_check, new_apps_check)

with open(apps_path, "w", encoding="utf-8") as f:
    f.write(apps_code)
print("Successfully patched applications.py")


# 5. Patch app/routers/admin.py:
# Ensure category stats and dashboard exclude Shakti from SWD scheme totals / breakdowns
admin_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\admin.py"
with open(admin_path, "r", encoding="utf-8") as f:
    admin_code = f.read()

old_dash_schemes = '''    total_schemes = db.query(Scheme).count()
    published_schemes = db.query(Scheme).filter(Scheme.status == "PUBLISHED").count()
    draft_schemes = db.query(Scheme).filter(Scheme.status == "DRAFT").count()
    closed_schemes = db.query(Scheme).filter(Scheme.status == "CLOSED").count()'''

new_dash_schemes = '''    # Exclude non-SWD Shakti scheme from dashboard SWD scheme metrics
    swd_schemes_q = db.query(Scheme).filter(~Scheme.scheme_code.ilike("%SHAKTI%"), ~Scheme.name.ilike("%SHAKTI%"))
    total_schemes = swd_schemes_q.count()
    published_schemes = swd_schemes_q.filter(Scheme.status == "PUBLISHED").count()
    draft_schemes = swd_schemes_q.filter(Scheme.status == "DRAFT").count()
    closed_schemes = swd_schemes_q.filter(Scheme.status == "CLOSED").count()'''

assert old_dash_schemes in admin_code, "old_dash_schemes not found in admin.py"
admin_code = admin_code.replace(old_dash_schemes, new_dash_schemes)

# Also in category breakdown
old_cat_breakdown = '''        # Scheme-wise breakdown in this category
        schemes_in_cat = db.query(Scheme).filter(Scheme.category_id == cat.id).all()'''

new_cat_breakdown = '''        # Scheme-wise breakdown in this category (excluding non-SWD Shakti)
        schemes_in_cat = db.query(Scheme).filter(
            Scheme.category_id == cat.id,
            ~Scheme.scheme_code.ilike("%SHAKTI%"),
            ~Scheme.name.ilike("%SHAKTI%")
        ).all()'''

assert old_cat_breakdown in admin_code, "old_cat_breakdown not found in admin.py"
admin_code = admin_code.replace(old_cat_breakdown, new_cat_breakdown)

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(admin_code)
print("Successfully patched admin.py")


# 6. Patch frontend App.tsx static references
app_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Replace mentions of Shakti in category 5 featured schemes
app_code = app_code.replace(
    "Gruha Lakshmi, Gruha Jyothi, Shakti Free Travel, Anna Bhagya, and Yuva Nidhi universal citizen guarantees.",
    "Gruha Lakshmi, Gruha Jyothi, Anna Bhagya, and Yuva Nidhi flagship citizen welfare guarantees."
)
app_code = app_code.replace(
    "<li><Check size={12} color=\"#16a34a\" /> Shakti & Yuva Nidhi</li>",
    "<li><Check size={12} color=\"#16a34a\" /> Anna Bhagya & Yuva Nidhi</li>"
)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)
print("Successfully patched App.tsx")
