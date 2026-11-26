from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Scheme
from app.schemas import SchemeRecommendationResult, EligibilityCheckRequest
from app.services.eligibility_engine import assess_scheme_eligibility

router = APIRouter(prefix="/api/swd", tags=["SWD Recommendation Integration"])

CATALOGUE_HIDDEN_CODES = [
    "KAR-FLAG-SHAKTI",
    "KAR-SSP-POSTMATRIC",
    "KAR-DIVYANGJAN-PENSION",
    "KAR-AGR-MICRO-IRRIGATION",
    "KAR-EDU-ELEVATE",
    "KAR-EDU-RAJIV-GANDHI-ENTREPRENEUR",
    "KAR-LAB-AMBEDKAR-KARMIKA"
]

@router.post("/recommendations/match", response_model=List[SchemeRecommendationResult])
def match_schemes_for_recommendation_engine(
    profile_req: EligibilityCheckRequest,
    db: Session = Depends(get_db)
):
    """
    FR-REC-015 to FR-REC-018:
    Shared integration endpoint called by Member 3's Recommendation Engine and Agentic AI.
    Pre-filters published schemes, runs preliminary criteria assessment, and returns
    explainable matching scores with LIKELY_MATCH, POSSIBLE_MATCH, UNMET_CRITERIA, or INSUFFICIENT_INFORMATION.
    """
    published_schemes = db.query(Scheme).filter(
        Scheme.status == "PUBLISHED",
        ~Scheme.scheme_code.in_(CATALOGUE_HIDDEN_CODES),
        ~Scheme.scheme_code.ilike("%SHAKTI%"),
        ~Scheme.name.ilike("%SHAKTI%")
    ).all()
    results = []

    for scheme in published_schemes:
        eval_res = assess_scheme_eligibility(scheme, profile_req.citizen_attributes)

        total_rules = len(eval_res.satisfied_criteria) + len(eval_res.unmet_criteria) + len(eval_res.unknown_criteria)
        satisfied_count = len(eval_res.satisfied_criteria)

        if eval_res.preliminary_status == "LIKELY_ELIGIBLE":
            match_category = "LIKELY_MATCH"
            score = 0.95
            explanation = "Your profile matches all preliminary criteria configured for this scheme."
        elif eval_res.preliminary_status == "INSUFFICIENT_INFORMATION":
            match_category = "INSUFFICIENT_INFORMATION"
            score = 0.50 if satisfied_count > 0 else 0.30
            explanation = f"Potential match based on partial data. Supplementary details required for: {', '.join(eval_res.missing_fields)}."
        else:
            match_category = "UNMET_CRITERIA"
            score = 0.10
            explanation = f"Currently does not meet {len(eval_res.unmet_criteria)} essential requirements."

        results.append(SchemeRecommendationResult(
            scheme_id=scheme.id,
            scheme_code=scheme.scheme_code,
            scheme_name=scheme.name,
            category_name=scheme.category.name if scheme.category else "Welfare",
            benefit_summary=scheme.benefit_summary,
            benefit_amount=float(scheme.benefit_amount) if scheme.benefit_amount else None,
            match_category=match_category,
            score=score,
            relevance_explanation=explanation,
            missing_fields=eval_res.missing_fields
        ))

    # Sort descending by match score
    results.sort(key=lambda x: x.score, reverse=True)
    return results
