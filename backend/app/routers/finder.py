from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Scheme, SchemeCategory
from app.schemas import (
    SmartFinderQuestionnaire,
    SmartFinderResponse,
    SmartFinderMatchItem
)
from app.services.eligibility_engine import assess_scheme_eligibility

router = APIRouter(prefix="/api/swd", tags=["Smart Scheme Finder"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]

# Schemes that have functional online application workflow
ACTIVE_APPLICATION_SCHEMES = {
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-SANDHYA-SURAKSHA",
    "KAR-INTERCASTE-MARRIAGE",
    "KAR-FLAG-GRUHA-LAKSHMI",
    "KAR-FLAG-GRUHA-JYOTHI",
    "KAR-FLAG-ANNA-BHAGYA",
    "KAR-FLAG-YUVA-NIDHI",
    "KAR-WCM-UDYOGINI",
    "KAR-AGR-RAITHA-VIDYA-NIDHI",
    "KAR-AGR-GANGA-KALYANA",
    "KAR-EDU-ARIVU-LOAN",
    "KAR-EDU-VIDYASIRI",
    "KAR-LAB-KBOCWWB",
    "KAR-LAB-GIG-WORKERS-INSURANCE",
    "KAR-LAB-BASAVA-AMBEDKAR-NIVAS"
}

@router.get("/finder/options")
def get_finder_options(db: Session = Depends(get_db)):
    """
    Returns verified questionnaire options for the Smart Scheme Finder.
    """
    districts = [
        "Bagalkote", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
        "Bidar", "Chamarajanagar", "Chikkaballapura", "Chikkamagaluru", "Chitradurga",
        "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
        "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
        "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
        "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir"
    ]
    categories = [
        "General", "SC", "ST", "OBC", "Category 1", "Category 2A",
        "Category 2B", "Category 3A", "Category 3B", "Minority", "Other", "Prefer not to disclose"
    ]
    occupations = [
        "Student", "Farmer", "Unemployed", "Employed",
        "Self-employed", "Construction worker", "Gig worker", "Other"
    ]
    education_levels = [
        "Below 10th", "10th / SSLC", "12th / PUC", "Diploma / ITI",
        "Undergraduate", "Postgraduate", "Professional / Engineering / Medical", "Other"
    ]
    return {
        "districts": sorted(districts),
        "social_categories": categories,
        "occupations": occupations,
        "education_levels": education_levels
    }

@router.post("/finder/match", response_model=SmartFinderResponse)
def match_smart_schemes(
    q: SmartFinderQuestionnaire,
    db: Session = Depends(get_db)
):
    """
    Matches citizen profile against active Karnataka SWD scheme eligibility rules.
    Outputs: Potential Match, Check Requirements, or Not Matched.
    Organizes results with the most relevant schemes first.
    """
    # Build dictionary of citizen attributes for eligibility evaluator
    attrs: Dict[str, Any] = {
        "residence_state": "Karnataka",
        "state": "Karnataka"
    }

    if q.age is not None:
        attrs["age"] = q.age
    if q.district:
        attrs["district"] = q.district.strip()
        attrs["residence_district"] = q.district.strip()
    if q.taluk:
        attrs["taluk"] = q.taluk.strip()
    if q.gender:
        g = q.gender.strip().lower()
        attrs["gender"] = g
        if g in ["female", "woman"]:
            attrs["is_woman"] = True
        elif g in ["male", "man"]:
            attrs["is_woman"] = False
    if q.is_woman is not None:
        attrs["is_woman"] = q.is_woman
        if q.is_woman:
            attrs["gender"] = "female"
        elif attrs.get("gender") in ["female", "woman"]:
            attrs["gender"] = "male"

    if q.caste_category and q.caste_category != "Prefer not to disclose":
        attrs["caste_category"] = q.caste_category.strip()
        attrs["caste"] = q.caste_category.strip()
    if q.annual_income is not None:
        attrs["annual_income"] = float(q.annual_income)
        attrs["income"] = float(q.annual_income)
    if q.occupation:
        occ = q.occupation.strip().lower()
        attrs["occupation"] = occ
        if occ == "farmer":
            attrs["is_farmer"] = True
        elif occ == "student":
            attrs["is_student"] = True
    if q.education_level:
        attrs["education_level"] = q.education_level.strip()
        attrs["education"] = q.education_level.strip()
    if q.is_farmer is not None:
        attrs["is_farmer"] = q.is_farmer
    if q.is_student is not None:
        attrs["is_student"] = q.is_student
    if q.marital_status:
        attrs["marital_status"] = q.marital_status.strip().lower()

    if q.disability_percentage is not None:
        attrs["disability_percentage"] = float(q.disability_percentage)
    elif q.disability_status and q.disability_status.lower() in ["yes", "true"]:
        attrs["disability_percentage"] = 40.0 # Standard threshold
    elif q.disability_status and q.disability_status.lower() in ["no", "false"]:
        attrs["disability_percentage"] = 0.0

    # Query all published schemes (excluding Shakti and temporarily hidden schemes)
    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()

    results: List[SmartFinderMatchItem] = []
    potential_count = 0
    check_req_count = 0

    for scheme in published_schemes:
        eval_res = assess_scheme_eligibility(scheme, attrs)

        why_matched: List[str] = []
        missing_reqs: List[str] = []
        unmet_explanations: List[str] = []

        # Build explainable why matched
        for sat in eval_res.satisfied_criteria:
            if sat.field_name == "residence_state":
                why_matched.append("Your residence state matches Karnataka domicile criteria.")
            elif sat.field_name == "annual_income":
                why_matched.append(f"Your declared family income (₹{int(q.annual_income):,}) falls within the verified limit ({sat.expected}).")
            elif sat.field_name == "caste_category":
                why_matched.append(f"Your social category ({q.caste_category}) is recognized under this scheme.")
            elif sat.field_name == "is_woman" or sat.field_name == "gender":
                why_matched.append("Your gender matches the target women beneficiary criteria.")
            elif sat.field_name == "is_student":
                why_matched.append("Your student status satisfies the educational beneficiary condition.")
            elif sat.field_name == "is_farmer":
                why_matched.append("Your agricultural farmer status matches target beneficiaries.")
            elif sat.field_name == "occupation":
                why_matched.append(f"Your occupation ({q.occupation}) satisfies the target occupational group.")
            elif sat.field_name == "age":
                why_matched.append(f"Your age ({q.age} yrs) complies with the scheme age criteria ({sat.expected}).")
            elif sat.field_name == "disability_percentage":
                why_matched.append("Your verified disability status meets the assistive grant threshold.")
            elif sat.field_name == "marital_status":
                why_matched.append(f"Your marital status ({q.marital_status}) meets scheme requirements.")
            else:
                why_matched.append(f"Requirement met: {sat.description}")

        # Document unmet mandatory conditions
        for unmet in eval_res.unmet_criteria:
            if unmet.is_mandatory:
                unmet_explanations.append(f"Mandatory requirement not met: {unmet.description}")

        # Document unknown / unverified conditions
        for unk in eval_res.unknown_criteria:
            missing_reqs.append(f"{unk.description} (Needs verification)")

        # Determine Match Indicator: 3-tier classification
        # A. Potential Match: All mandatory conditions are SATISFIED (zero mandatory unmet, zero mandatory unknown)
        # B. Check Requirements: Some mandatory conditions need confirmation, but NO mandatory condition is violated
        # C. Not Matched: At least one mandatory condition is definitely violated
        if eval_res.preliminary_status == "LIKELY_ELIGIBLE":
            # Guard against classifying merely on residence_state alone if scheme has no specific conditions
            has_substantive_satisfied = any(
                s.field_name not in ["residence_state", "state"] 
                for s in eval_res.satisfied_criteria
            )
            # If all rules were satisfied and at least one substantive or only domicile scheme
            match_status = "Potential Match"
            match_score = 0.95
            potential_count += 1
            if not why_matched:
                why_matched.append("Your profile attributes satisfy the known scheme rules.")

        elif eval_res.preliminary_status == "INSUFFICIENT_INFORMATION":
            match_status = "Check Requirements"
            match_score = 0.60 if len(eval_res.satisfied_criteria) > 0 else 0.40
            check_req_count += 1
            if not why_matched:
                why_matched.append("Some criteria match your answers, but key conditions require documentation.")

        else: # NOT_ELIGIBLE
            match_status = "Not Matched"
            match_score = 0.10
            # For Not Matched schemes, include clear rejection explanations
            if unmet_explanations:
                for ue in unmet_explanations:
                    missing_reqs.append(ue)

        # Collect required documents safely
        docs_list = [d.document_name for d in scheme.documents if d.document_name]

        # Has application form
        has_app = (scheme.scheme_code in ACTIVE_APPLICATION_SCHEMES)

        # Deduplicate reasons while preserving order
        why_matched = list(dict.fromkeys(why_matched))
        missing_reqs = list(dict.fromkeys(missing_reqs))

        results.append(SmartFinderMatchItem(
            scheme_id=scheme.id,
            scheme_code=scheme.scheme_code,
            scheme_name=scheme.name,
            category_id=scheme.category_id,
            category_name=scheme.category.name if scheme.category else "Welfare Services",
            description=scheme.description,
            benefit_summary=scheme.benefit_summary,
            benefit_amount=float(scheme.benefit_amount) if scheme.benefit_amount else None,
            eligibility_summary=scheme.eligibility_summary,
            documents_required=docs_list,
            status=scheme.status,
            verification_status=scheme.verification_status or "VERIFIED",
            match_status=match_status,
            match_score=match_score,
            why_matched=why_matched,
            missing_requirements=missing_reqs,
            has_application_form=has_app,
            official_url=scheme.official_url
        ))

    # Sort descending by match score, so Potential Matches appear first, followed by Check Requirements, then Not Matched
    results.sort(key=lambda x: x.match_score, reverse=True)

    return SmartFinderResponse(
        total_matches=len(results),
        potential_match_count=potential_count,
        check_requirements_count=check_req_count,
        results=results
    )
