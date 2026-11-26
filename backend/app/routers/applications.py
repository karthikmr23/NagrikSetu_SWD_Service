import os
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.connection import get_db
from app.models import (
    Scheme, SchemeApplication, ApplicationDocument, 
    ApplicationHistory, Beneficiary, AuditLog, DynamicFormDefinition
)
from app.schemas import (
    ApplicationResponse, ApplicationSubmissionRequest,
    ApplicationDocumentResponse
)
from app.core.security import get_current_user, require_role, verify_citizen_ownership
from app.services.document_service import save_uploaded_document
from app.events.rabbitmq_publisher import publish_event_to_broker, create_outbox_event

router = APIRouter(prefix="/api/swd", tags=["SWD Applications"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]

@router.post("/schemes/{scheme_id}/applications", response_model=ApplicationResponse)
def submit_scheme_application(
    scheme_id: int,
    app_in: ApplicationSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Enforce role restriction: Only CITIZEN users can apply for welfare schemes
    user_role = (current_user.get("role") or "").upper()
    if user_role != "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Administrative accounts (Welfare Officers and Platform Admins) cannot submit citizen welfare scheme applications."
        )

    # Verify citizen ID ownership
    verify_citizen_ownership(app_in.citizen_id, current_user)

    # 1. Verify scheme is open and active (FR-SWD-014)
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    if scheme.scheme_code in CATALOGUE_HIDDEN_CODES or "shakti" in (scheme.scheme_code or "").lower() or "shakti" in (scheme.name or "").lower():
        detail_msg = "The Shakti Scheme is administered under the Transport Department and is not an SWD application scheme." if "shakti" in (scheme.scheme_code or "").lower() else "This scheme application window is currently inactive or under administrative review."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_msg
        )

    if scheme.status != "PUBLISHED":
        raise HTTPException(
            status_code=400,
            detail=f"Applications are not currently accepted. Scheme status is '{scheme.status}'."
        )

    today = date.today()
    if today < scheme.application_start_date or today > scheme.application_end_date:
        raise HTTPException(
            status_code=400,
            detail=f"Application window is closed. Open dates: {scheme.application_start_date} to {scheme.application_end_date}."
        )

    # 2. Duplicate detection (FR-SWD-020: Flag possible duplicates for human review; do NOT automatically reject)
    is_duplicate = False
    dup_reason = None
    existing_app = db.query(SchemeApplication).filter(
        SchemeApplication.scheme_id == scheme_id,
        SchemeApplication.citizen_id == app_in.citizen_id
    ).first()

    if existing_app:
        is_duplicate = True
        dup_reason = f"Previous application {existing_app.application_number} found for this citizen on this scheme."

    # Find active form definition version if available
    active_form = db.query(DynamicFormDefinition).filter(
        DynamicFormDefinition.scheme_id == scheme_id,
        DynamicFormDefinition.is_active == True
    ).first()
    active_version_id = active_form.version if active_form else 1

    # Generate unique application number
    app_num = f"SWD-APP-{datetime.utcnow().year}-{os.urandom(3).hex().upper()}"

    new_app = SchemeApplication(
        application_number=app_num,
        scheme_id=scheme_id,
        category_id=scheme.category_id,
        form_version_id=active_version_id,
        citizen_id=app_in.citizen_id,
        citizen_name=app_in.citizen_name,
        citizen_email=app_in.citizen_email,
        citizen_phone=app_in.citizen_phone,
        annual_income=app_in.annual_income,
        caste_category=app_in.caste_category,
        residence_district=app_in.residence_district,
        disability_percentage=app_in.disability_percentage or 0.00,
        bank_account_number=app_in.bank_account_number,
        bank_ifsc=app_in.bank_ifsc,
        application_data_json=app_in.application_data_json,
        status="SUBMITTED",
        is_duplicate_suspect=is_duplicate,
        duplicate_reason=dup_reason
    )
    db.add(new_app)
    db.flush()

    # Create Initial History entry
    history = ApplicationHistory(
        application_id=new_app.id,
        from_status=None,
        to_status="SUBMITTED",
        changed_by=app_in.citizen_id,
        action_type="SUBMISSION",
        remarks="Citizen submitted online scheme application dossier."
    )
    db.add(history)

    # Create Audit log
    audit = AuditLog(
        actor_id=app_in.citizen_id,
        actor_role="CITIZEN",
        action="SUBMIT_APPLICATION",
        entity_type="APPLICATION",
        entity_id=str(new_app.id),
        details={"application_number": app_num, "is_duplicate_suspect": is_duplicate}
    )
    db.add(audit)

    # FR-SWD-021 & FR-MQ-012: Create Outbox Event in the same atomic database transaction
    event_payload = {
        "application_id": new_app.id,
        "application_number": new_app.application_number,
        "scheme_id": scheme.id,
        "scheme_code": scheme.scheme_code,
        "citizen_id": new_app.citizen_id,
        "status": new_app.status,
        "is_duplicate_suspect": new_app.is_duplicate_suspect
    }
    outbox_entry = create_outbox_event(
        db=db,
        event_type="SCHEME_APPLICATION_CREATED",
        correlation_id=app_num,
        payload=event_payload
    )

    db.commit()
    db.refresh(new_app)

    # Publish RabbitMQ Event after committed transaction (FR-SWD-021)
    published = publish_event_to_broker(
        event_type="SCHEME_APPLICATION_CREATED",
        correlation_id=app_num,
        payload=event_payload,
        event_id=outbox_entry.event_id
    )
    if published:
        outbox_entry.status = "PUBLISHED"
        outbox_entry.published_at = datetime.utcnow()
        db.commit()

    return new_app

@router.get("/applications/{citizen_id}", response_model=List[ApplicationResponse])
def get_citizen_applications(
    citizen_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    verify_citizen_ownership(citizen_id, current_user)
    return db.query(SchemeApplication).filter(SchemeApplication.citizen_id == citizen_id).order_by(SchemeApplication.id.desc()).all()

@router.get("/applications/{application_id}/details", response_model=ApplicationResponse)
def get_application_details(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    verify_citizen_ownership(app_record.citizen_id, current_user)
    return app_record

@router.post("/applications/{application_id}/documents", response_model=ApplicationDocumentResponse)
def upload_application_document(
    application_id: int,
    document_code: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    verify_citizen_ownership(app_record.citizen_id, current_user)

    upload_meta = save_uploaded_document(file, app_record.citizen_id, document_code)

    doc_record = ApplicationDocument(
        application_id=app_record.id,
        document_code=document_code,
        file_name=upload_meta["file_name"],
        file_path=upload_meta["file_path"],
        file_type=upload_meta["file_type"],
        file_size_bytes=upload_meta["file_size_bytes"],
        uploaded_by=current_user.get("sub", app_record.citizen_id)
    )
    db.add(doc_record)

    # If application was awaiting info/documents, transition back to UNDER_REVIEW and append history
    if app_record.status in ["MORE_INFORMATION_REQUIRED", "DOCUMENTS_REQUIRED", "AWAITING_DOCUMENTS"]:
        old_st = app_record.status
        hist = ApplicationHistory(
            application_id=app_record.id,
            from_status=old_st,
            to_status="UNDER_REVIEW",
            changed_by=app_record.citizen_id,
            action_type="DOCUMENT_UPLOAD",
            remarks=f"Citizen uploaded requested supplementary document: {doc_record.file_name}"
        )
        app_record.status = "UNDER_REVIEW"
        db.add(hist)

    db.commit()
    db.refresh(doc_record)
    return doc_record

@router.get("/applications/{application_id}/documents/{document_id}/download")
def download_application_document(
    application_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Secure download of uploaded application document with role authorization check.
    """
    app_record = db.query(SchemeApplication).filter(SchemeApplication.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    user_role = current_user.get("role", "")
    user_citizen_id = current_user.get("citizen_id")

    # Access control: Citizen can only download their own docs; Welfare Officer/Admin can download
    if user_role == "CITIZEN":
        if not user_citizen_id or user_citizen_id != app_record.citizen_id:
            raise HTTPException(status_code=403, detail="Access denied: Cannot access documents belonging to another citizen.")
    elif user_role not in ["GOVERNMENT_WELFARE_ADMIN", "WELFARE_OFFICER", "ADMINISTRATOR", "PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(status_code=403, detail="Access restricted to authorized personnel.")

    doc_record = db.query(ApplicationDocument).filter(
        ApplicationDocument.id == document_id,
        ApplicationDocument.application_id == application_id
    ).first()

    if not doc_record:
        raise HTTPException(status_code=404, detail="Document not found")

    import os
    if not os.path.exists(doc_record.file_path):
        raise HTTPException(status_code=404, detail="Physical document file not found on server")

    from fastapi.responses import FileResponse
    return FileResponse(
        path=doc_record.file_path,
        media_type=doc_record.file_type or "application/octet-stream",
        filename=doc_record.file_name
    )

@router.get("/public/track-status/{application_number}")
def public_track_status(application_number: str, db: Session = Depends(get_db)):
    """
    Public minimal status lookup without login.
    Masks personal identifiers for privacy.
    """
    clean_num = application_number.strip().upper()
    app_record = db.query(SchemeApplication).filter(SchemeApplication.application_number == clean_num).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="No application found matching this reference number.")

    # Mask name: Ramesh Kumar Nayak -> R***** K**** N****
    name_parts = app_record.citizen_name.split()
    masked_name = " ".join([p[0] + "*" * (len(p) - 1) if len(p) > 1 else p for p in name_parts])

    # Check DBT status if sanctioned
    dbt_status = None
    if app_record.status == "BENEFIT_PROCESSED" or (app_record.beneficiary and app_record.beneficiary.dbt_transactions):
        dbt_status = "Simulated DBT Credited via APB"

    return {
        "application_number": app_record.application_number,
        "scheme_name": app_record.scheme.name if app_record.scheme else "Welfare Scheme",
        "masked_citizen_name": masked_name,
        "district": app_record.residence_district,
        "current_status": app_record.status,
        "submission_date": app_record.created_at.strftime("%Y-%m-%d"),
        "dbt_status": dbt_status,
        "notice": "DEMO MODE — Preliminary Public Status Lookup"
    }
