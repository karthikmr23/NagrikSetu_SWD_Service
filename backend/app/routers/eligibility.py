from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Scheme, EligibilityRule
from app.schemas import (
    EligibilityCheckRequest, EligibilityCheckResponse, 
    EligibilityRuleResponse, EligibilityRuleCreate,
    DraftRuleTestRequest, DraftRuleTestResponse, DraftRuleTestProfileResult
)
from app.services.eligibility_engine import assess_scheme_eligibility, assess_draft_rules
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/swd", tags=["SWD Eligibility Engine"])

@router.post("/schemes/{scheme_id}/eligibility-check", response_model=EligibilityCheckResponse)
def check_scheme_eligibility(
    scheme_id: int,
    request: EligibilityCheckRequest,
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return assess_scheme_eligibility(scheme, request.citizen_attributes)

@router.get("/citizens/{citizen_id}/eligibility", response_model=List[EligibilityCheckResponse])
def batch_check_citizen_eligibility(
    citizen_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verify ownership or admin role
    user_role = current_user.get("role", "CITIZEN")
    if user_role not in ["SWD_ADMIN", "PLATFORM_ADMIN"]:
        if current_user.get("citizen_id") != citizen_id:
            raise HTTPException(status_code=403, detail="Forbidden: You cannot query eligibility for another citizen.")

    # Retrieve published schemes
    schemes = db.query(Scheme).filter(Scheme.status == "PUBLISHED").all()

    # Synthetic demo profile attributes from token or defaults
    citizen_attrs = {
        "residence_state": current_user.get("state", "Karnataka"),
        "annual_income": current_user.get("income", 150000),
        "caste_category": current_user.get("caste", "SC"),
        "education_level": current_user.get("education", "Undergraduate"),
        "age": current_user.get("age", 21)
    }

    results = []
    for s in schemes:
        res = assess_scheme_eligibility(s, citizen_attrs)
        results.append(res)

    return results

# ------------------------------------------------------------------------------
# Rule Management Endpoints (FR-SWD-007 to FR-SWD-008)
# ------------------------------------------------------------------------------
@router.get("/schemes/{scheme_id}/rules", response_model=List[EligibilityRuleResponse])
def list_scheme_rules(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme.rules

@router.post("/schemes/{scheme_id}/rules", response_model=EligibilityRuleResponse)
def add_scheme_rule(
    scheme_id: int,
    rule_in: EligibilityRuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR"]))
):
    if current_user.get("role") in ["PLATFORM_ADMIN", "SWD_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform Admin is strictly view-only for SWD monitoring. Rule creation is disabled."
        )
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    new_rule = EligibilityRule(scheme_id=scheme_id, **rule_in.model_dump())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

# ------------------------------------------------------------------------------
# Draft Rule Testing (FR-SWD-013)
# ------------------------------------------------------------------------------
@router.post("/admin/rules/test-draft", response_model=DraftRuleTestResponse)
def test_draft_rules(
    request: DraftRuleTestRequest,
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN"]))
):
    # Convert draft rule schemas to ephemeral EligibilityRule model instances (in-memory only)
    temp_rules = []
    for r in request.draft_rules:
        temp_rules.append(EligibilityRule(
            scheme_id=0,
            field_name=r.field_name,
            operator=r.operator,
            expected_value=r.expected_value,
            value_type=r.value_type,
            is_mandatory=r.is_mandatory,
            description=r.description,
            rule_version=r.rule_version,
            is_active=r.is_active
        ))

    profiles_to_test = request.synthetic_profiles or request.test_profiles or []
    results = []
    eligible_count = 0
    ineligible_count = 0
    insufficient_count = 0

    for idx, profile in enumerate(profiles_to_test):
        eval_res = assess_draft_rules(temp_rules, profile)
        status_val = eval_res["preliminary_status"]
        if status_val == "LIKELY_ELIGIBLE":
            eligible_count += 1
        elif status_val == "NOT_ELIGIBLE":
            ineligible_count += 1
        else:
            insufficient_count += 1

        results.append(DraftRuleTestProfileResult(
            profile_index=idx,
            profile_id=str(profile.get("citizen_id", f"profile_{idx}")),
            profile=profile,
            preliminary_status=status_val,
            satisfied_count=len(eval_res["satisfied_criteria"]),
            unmet_count=len(eval_res["unmet_criteria"]),
            unknown_count=len(eval_res["unknown_criteria"]),
            satisfied_criteria=eval_res["satisfied_criteria"],
            unmet_criteria=eval_res["unmet_criteria"],
            unknown_criteria=eval_res["unknown_criteria"],
            missing_fields=eval_res["missing_fields"]
        ))

    return DraftRuleTestResponse(
        scheme_id=request.scheme_id,
        total_profiles_tested=len(results),
        eligible_count=eligible_count,
        ineligible_count=ineligible_count,
        insufficient_info_count=insufficient_count,
        results=results
    )
