from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.connection import get_db
from app.models import (
    Scheme, SchemeCategory, EligibilityRule, SchemeDocument, 
    AuditLog, DynamicFormDefinition, DynamicFormField, Notification, User
)
from app.schemas import (
    SchemeResponse, SchemeCreate, SchemeUpdate, 
    SchemeCategoryResponse, SchemeCategoryCreate,
    EligibilityRuleResponse, EligibilityRuleCreate,
    DynamicFormDefinitionResponse, DynamicFormCreate
)
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/swd", tags=["SWD Schemes"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]


# ------------------------------------------------------------------------------
# Categories (FR-SWD-005)
# ------------------------------------------------------------------------------
@router.get("/categories", response_model=List[SchemeCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(SchemeCategory).filter(SchemeCategory.is_active == True).all()

@router.post("/categories", response_model=SchemeCategoryResponse)
def create_category(
    cat_in: SchemeCategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR"]))
):
    # Platform Admin is view-only
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Category creation is disabled."
        )
    existing = db.query(SchemeCategory).filter(SchemeCategory.code == cat_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Category code '{cat_in.code}' already exists")
    cat = SchemeCategory(**cat_in.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

# ------------------------------------------------------------------------------
# Schemes (FR-SWD-001 to FR-SWD-006)
# ------------------------------------------------------------------------------
@router.get("/schemes", response_model=List[SchemeResponse])
def get_schemes(
    category_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    beneficiary_category: Optional[str] = None,
    department: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Scheme)

    # For public citizen catalogue, default to PUBLISHED unless admin requests otherwise
    if status_filter:
        query = query.filter(Scheme.status == status_filter.upper())
    else:
        query = query.filter(Scheme.status == "PUBLISHED")

    if category_id:
        query = query.filter(Scheme.category_id == category_id)

    if department:
        query = query.filter(Scheme.department.ilike(f"%{department}%"))

    if beneficiary_category:
        query = query.filter(Scheme.beneficiary_categories.ilike(f"%{beneficiary_category}%"))

    # Non-destructive catalogue exclusion for Shakti and temporarily hidden schemes
    query = query.filter(
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    )

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

    return query.order_by(Scheme.id.asc()).offset(skip).limit(limit).all()

@router.get("/schemes/beneficiaries")
def get_beneficiary_categories(db: Session = Depends(get_db)):
    schemes = db.query(Scheme.beneficiary_categories).filter(Scheme.status == "PUBLISHED").all()
    categories_set = set()
    for (cats,) in schemes:
        if cats:
            for c in cats.split(","):
                c_clean = c.strip()
                if c_clean:
                    categories_set.add(c_clean)
    return sorted(list(categories_set))

@router.get("/schemes/{scheme_id}", response_model=SchemeResponse)
def get_scheme_by_id(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.post("/schemes", response_model=SchemeResponse)
def create_scheme(
    scheme_in: SchemeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR"]))
):
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Scheme creation is disabled."
        )
    existing = db.query(Scheme).filter(Scheme.scheme_code == scheme_in.scheme_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Scheme code '{scheme_in.scheme_code}' already exists")

    # Extract nested rules and documents
    rules_data = scheme_in.rules or []
    docs_data = scheme_in.documents or []
    scheme_dict = scheme_in.model_dump(exclude={"rules", "documents"})
    scheme_dict["created_by"] = current_user.get("sub", "SWD_ADMIN")

    new_scheme = Scheme(**scheme_dict)
    db.add(new_scheme)
    db.flush()

    for r in rules_data:
        rule_obj = EligibilityRule(scheme_id=new_scheme.id, **r.model_dump())
        db.add(rule_obj)

    for d in docs_data:
        doc_obj = SchemeDocument(scheme_id=new_scheme.id, **d.model_dump())
        db.add(doc_obj)

    # Record Audit
    audit = AuditLog(
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

    db.commit()
    db.refresh(new_scheme)
    return new_scheme

@router.put("/schemes/{scheme_id}", response_model=SchemeResponse)
def update_scheme(
    scheme_id: int,
    scheme_update: SchemeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR"]))
):
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Scheme modification is disabled."
        )
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    update_data = scheme_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scheme, field, value)

    # Audit log
    audit = AuditLog(
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

    db.commit()
    db.refresh(scheme)
    return scheme

@router.delete("/schemes/{scheme_id}")
def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR"]))
):
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Scheme deletion is disabled."
        )
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    # Soft-delete by setting status to INACTIVE
    scheme.status = "INACTIVE"
    audit = AuditLog(
        actor_id=current_user.get("sub", "SWD_ADMIN"),
        actor_role=current_user.get("role", "SWD_ADMIN"),
        action="DEACTIVATE_SCHEME",
        entity_type="SCHEME",
        entity_id=str(scheme.id),
        details={"status": "INACTIVE"}
    )
    db.add(audit)
    db.commit()
    return {"message": f"Scheme '{scheme.scheme_code}' has been deactivated (status set to INACTIVE)."}


# ------------------------------------------------------------------------------
# Dynamic Form Definitions for Schemes
# ------------------------------------------------------------------------------
@router.get("/schemes/{scheme_id}/form", response_model=Optional[DynamicFormDefinitionResponse])
def get_scheme_dynamic_form(scheme_id: int, db: Session = Depends(get_db)):
    """Retrieve active dynamic form definition and fields for a specific welfare scheme."""
    # Exclude Shakti and temporarily hidden schemes from active citizen application forms
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if scheme and (scheme.scheme_code in CATALOGUE_HIDDEN_CODES or "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower()):
        return None
    form = db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id,
        DynamicFormDefinition.is_active == True
    ).first()
    return form

@router.post("/schemes/{scheme_id}/form", response_model=DynamicFormDefinitionResponse)
def save_scheme_dynamic_form(
    scheme_id: int,
    form_in: DynamicFormCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["GOVERNMENT_WELFARE_ADMIN", "WELFARE_OFFICER", "ADMINISTRATOR"]))
):
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Scheme form modification is disabled."
        )
    """Welfare Admin: Create a new dynamic form version for a scheme."""
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    # Get max version
    max_ver = db.query(DynamicFormDefinition.version).filter(
        DynamicFormDefinition.scheme_id == scheme_id
    ).order_by(DynamicFormDefinition.version.desc()).first()
    next_ver = (max_ver[0] + 1) if max_ver else 1

    # Deactivate older forms
    db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id
    ).update({"is_active": False})

    new_form = DynamicFormDefinition(
        scheme_id=scheme_id,
        version=next_ver,
        title=form_in.title,
        description=form_in.description,
        is_active=True
    )
    db.add(new_form)
    db.flush()

    for idx, f in enumerate(form_in.fields):
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

    db.commit()
    db.refresh(new_form)
    return new_form

