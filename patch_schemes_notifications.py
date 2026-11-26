import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\schemes.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update imports
old_import = "from app.models import (\n    Scheme, SchemeCategory, EligibilityRule, SchemeDocument, \n    AuditLog, DynamicFormDefinition, DynamicFormField\n)"
new_import = "from app.models import (\n    Scheme, SchemeCategory, EligibilityRule, SchemeDocument, \n    AuditLog, DynamicFormDefinition, DynamicFormField, Notification, User\n)"

assert old_import in code, "old_import not found in schemes.py"
code = code.replace(old_import, new_import)

# 2. Update create_scheme to notify citizens
target_create = """    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "SWD_ADMIN"),
        action="CREATE_SCHEME",
        entity_type="SCHEME",
        entity_id=str(new_scheme.id),
        details={"scheme_code": new_scheme.scheme_code, "name": new_scheme.name}
    )
    db.add(audit)

    db.commit()"""

replacement_create = """    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "SWD_ADMIN"),
        action="CREATE_SCHEME",
        entity_type="SCHEME",
        entity_id=str(new_scheme.id),
        details={"scheme_code": new_scheme.scheme_code, "name": new_scheme.name}
    )
    db.add(audit)

    # Dispatch Notification to Citizens about New Scheme
    active_citizens = db.query(User).filter(User.role == "CITIZEN", User.is_active == True).all()
    for cit in active_citizens:
        notif = Notification(
            user_id=cit.citizen_id,
            title=f"New Welfare Scheme Published: {new_scheme.name}",
            message=f"Department of Social Welfare has launched '{new_scheme.name}'. Check your eligibility and apply online.",
            notification_type="SUCCESS"
        )
        db.add(notif)

    db.commit()"""

assert target_create in code, "target_create not found in schemes.py"
code = code.replace(target_create, replacement_create)

# 3. Update update_scheme to notify citizens about scheme/guidelines updates
target_update = """    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "SWD_ADMIN"),
        action="UPDATE_SCHEME",
        entity_type="SCHEME",
        entity_id=str(scheme.id),
        details=update_data
    )
    db.add(audit)

    db.commit()"""

replacement_update = """    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "SWD_ADMIN"),
        action="UPDATE_SCHEME",
        entity_type="SCHEME",
        entity_id=str(scheme.id),
        details=update_data
    )
    db.add(audit)

    # Dispatch Notification to Citizens about Scheme Update
    active_citizens = db.query(User).filter(User.role == "CITIZEN", User.is_active == True).all()
    for cit in active_citizens:
        notif = Notification(
            user_id=cit.citizen_id,
            title=f"Welfare Scheme Updated: {scheme.name}",
            message=f"Guidelines, eligibility criteria, or details for '{scheme.name}' have been updated by the Welfare Department.",
            notification_type="INFO"
        )
        db.add(notif)

    db.commit()"""

assert target_update in code, "target_update not found in schemes.py"
code = code.replace(target_update, replacement_update)

# 4. Update save_scheme_dynamic_form to notify citizens when form guidelines/version updated
target_form = """    for idx, f in enumerate(form_in.fields):
        new_field = DynamicFormField(
            form_id=new_form.id,
            field_name=f.field_name,
            field_label=f.field_label,
            field_type=f.field_type,
            placeholder=f.placeholder,
            help_text=f.help_text,
            is_required=f.is_required,
            display_order=f.display_order or (idx + 1),
            options_json=f.options_json,
            validation_rules_json=f.validation_rules_json,
            conditional_visibility_json=f.conditional_visibility_json
        )
        db.add(new_field)

    db.commit()"""

replacement_form = """    for idx, f in enumerate(form_in.fields):
        new_field = DynamicFormField(
            form_id=new_form.id,
            field_name=f.field_name,
            field_label=f.field_label,
            field_type=f.field_type,
            placeholder=f.placeholder,
            help_text=f.help_text,
            is_required=f.is_required,
            display_order=f.display_order or (idx + 1),
            options_json=f.options_json,
            validation_rules_json=f.validation_rules_json,
            conditional_visibility_json=f.conditional_visibility_json
        )
        db.add(new_field)

    # Notify Citizens of updated application form guidelines
    active_citizens = db.query(User).filter(User.role == "CITIZEN", User.is_active == True).all()
    for cit in active_citizens:
        notif = Notification(
            user_id=cit.citizen_id,
            title=f"Application Guidelines Updated: {scheme.name}",
            message=f"Application form version {next_ver} for '{scheme.name}' has been released with updated questions and documentation requirements.",
            notification_type="INFO"
        )
        db.add(notif)

    db.commit()"""

assert target_form in code, "target_form not found in schemes.py"
code = code.replace(target_form, replacement_form)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("schemes.py updated with notification dispatchers!")
