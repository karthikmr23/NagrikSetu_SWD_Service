from typing import Dict, Any, List
from app.models import Scheme, EligibilityRule
from app.schemas import CriterionResult, EligibilityCheckResponse

def evaluate_criterion(rule: EligibilityRule, actual_value: Any) -> CriterionResult:
    # Handle missing information (FR-SWD-010: unknown values must not be treated as satisfied)
    if actual_value is None or actual_value == "":
        return CriterionResult(
            field_name=rule.field_name,
            description=rule.description,
            expected=rule.expected_value,
            operator=rule.operator,
            actual_value=None,
            status="UNKNOWN",
            is_mandatory=rule.is_mandatory,
            explanation=f"Missing information for '{rule.field_name}'. Value cannot be assumed satisfied."
        )

    op = rule.operator.upper()
    val_type = rule.value_type.upper()
    expected_str = rule.expected_value.strip()

    is_satisfied = False

    try:
        if val_type == "INTEGER":
            act = int(actual_value)
            if op == "RANGE":
                parts = [int(p.strip()) for p in expected_str.split("-")]
                is_satisfied = (parts[0] <= act <= parts[1])
            else:
                exp = int(expected_str)
                if op == "EQUALS": is_satisfied = (act == exp)
                elif op == "NOT_EQUALS": is_satisfied = (act != exp)
                elif op == "LESS_THAN": is_satisfied = (act < exp)
                elif op == "LESS_THAN_OR_EQUAL": is_satisfied = (act <= exp)
                elif op == "GREATER_THAN": is_satisfied = (act > exp)
                elif op == "GREATER_THAN_OR_EQUAL": is_satisfied = (act >= exp)

        elif val_type == "FLOAT":
            act = float(actual_value)
            if op == "RANGE":
                parts = [float(p.strip()) for p in expected_str.split("-")]
                is_satisfied = (parts[0] <= act <= parts[1])
            else:
                exp = float(expected_str)
                if op == "EQUALS": is_satisfied = (act == exp)
                elif op == "NOT_EQUALS": is_satisfied = (act != exp)
                elif op == "LESS_THAN": is_satisfied = (act < exp)
                elif op == "LESS_THAN_OR_EQUAL": is_satisfied = (act <= exp)
                elif op == "GREATER_THAN": is_satisfied = (act > exp)
                elif op == "GREATER_THAN_OR_EQUAL": is_satisfied = (act >= exp)

        elif val_type == "BOOLEAN":
            act = str(actual_value).lower() in ["true", "1", "yes"]
            exp = expected_str.lower() in ["true", "1", "yes"]
            if op == "EQUALS": is_satisfied = (act == exp)
            elif op == "NOT_EQUALS": is_satisfied = (act != exp)

        elif val_type == "LIST":
            allowed_items = [item.strip().lower() for item in expected_str.split(",")]
            act = str(actual_value).strip().lower()
            if op == "IN": is_satisfied = (act in allowed_items)
            elif op == "NOT_IN": is_satisfied = (act not in allowed_items)

        else: # STRING
            act = str(actual_value).strip().lower()
            exp = expected_str.lower()
            if op == "EQUALS": is_satisfied = (act == exp)
            elif op == "NOT_EQUALS": is_satisfied = (act != exp)
            elif op == "IN":
                allowed_items = [item.strip().lower() for item in expected_str.split(",")]
                is_satisfied = (act in allowed_items)
            elif op == "NOT_IN":
                allowed_items = [item.strip().lower() for item in expected_str.split(",")]
                is_satisfied = (act not in allowed_items)

    except (ValueError, TypeError) as e:
        return CriterionResult(
            field_name=rule.field_name,
            description=rule.description,
            expected=rule.expected_value,
            operator=rule.operator,
            actual_value=str(actual_value),
            status="UNKNOWN",
            is_mandatory=rule.is_mandatory,
            explanation=f"Format error comparing value '{actual_value}' against expected format ({val_type})."
        )

    if is_satisfied:
        return CriterionResult(
            field_name=rule.field_name,
            description=rule.description,
            expected=rule.expected_value,
            operator=rule.operator,
            actual_value=actual_value,
            status="SATISFIED",
            is_mandatory=rule.is_mandatory,
            explanation=f"Criterion met: Provided value '{actual_value}' satisfies rule requirement."
        )
    else:
        return CriterionResult(
            field_name=rule.field_name,
            description=rule.description,
            expected=rule.expected_value,
            operator=rule.operator,
            actual_value=actual_value,
            status="UNMET",
            is_mandatory=rule.is_mandatory,
            explanation=f"Criterion unmet: Provided value '{actual_value}' does not satisfy {op} {expected_str}."
        )

def assess_scheme_eligibility(scheme: Scheme, citizen_attributes: Dict[str, Any]) -> EligibilityCheckResponse:
    satisfied: List[CriterionResult] = []
    unmet: List[CriterionResult] = []
    unknown: List[CriterionResult] = []
    missing_fields: List[str] = []

    active_rules = [r for r in scheme.rules if r.is_active]

    for rule in active_rules:
        # Check normalized attribute key
        act_val = citizen_attributes.get(rule.field_name)
        if act_val is None:
            # Check common synonyms and mappings
            if rule.field_name == "annual_income":
                act_val = citizen_attributes.get("income") or citizen_attributes.get("family_income")
            elif rule.field_name == "caste_category":
                act_val = citizen_attributes.get("caste") or citizen_attributes.get("category")
            elif rule.field_name == "residence_state":
                act_val = citizen_attributes.get("state") or citizen_attributes.get("domicile")
            elif rule.field_name == "education_level":
                act_val = citizen_attributes.get("education") or citizen_attributes.get("qualification")
            elif rule.field_name == "is_woman":
                # Handle gender mapping to is_woman
                gen = citizen_attributes.get("gender")
                if gen:
                    act_val = str(gen).strip().lower() in ["female", "woman"]
            elif rule.field_name == "gender":
                # Handle is_woman mapping to gender
                wom = citizen_attributes.get("is_woman")
                if wom is not None:
                    act_val = "female" if wom else "male"
            elif rule.field_name == "is_student":
                occ = citizen_attributes.get("occupation")
                if occ and str(occ).strip().lower() == "student":
                    act_val = True
            elif rule.field_name == "is_farmer":
                occ = citizen_attributes.get("occupation")
                if occ and str(occ).strip().lower() == "farmer":
                    act_val = True

        res = evaluate_criterion(rule, act_val)
        if res.status == "SATISFIED":
            satisfied.append(res)
        elif res.status == "UNMET":
            unmet.append(res)
        else: # UNKNOWN
            unknown.append(res)
            missing_fields.append(rule.field_name)

    # Determine overall preliminary status
    # If any mandatory rule is UNMET -> NOT_ELIGIBLE
    mandatory_unmet = any(r.is_mandatory for r in unmet)
    mandatory_unknown = any(r.is_mandatory for r in unknown)

    if mandatory_unmet:
        preliminary_status = "NOT_ELIGIBLE"
        unmet_descs = [u.description for u in unmet if u.is_mandatory]
        summary_explanation = f"Preliminary Result: Not Eligible. Mandatory condition violated: {'; '.join(unmet_descs)}."
    elif mandatory_unknown:
        preliminary_status = "INSUFFICIENT_INFORMATION"
        missing_descs = [f"{u.description} ({u.field_name})" for u in unknown if u.is_mandatory]
        summary_explanation = f"Preliminary Result: Needs Further Information. Mandatory requirements missing: {'; '.join(missing_descs)}."
    else:
        preliminary_status = "LIKELY_ELIGIBLE"
        summary_explanation = "You appear to meet all preliminary eligibility criteria based on the information provided."

    return EligibilityCheckResponse(
        scheme_id=scheme.id,
        scheme_code=scheme.scheme_code,
        scheme_name=scheme.name,
        preliminary_status=preliminary_status,
        satisfied_criteria=satisfied,
        unmet_criteria=unmet,
        unknown_criteria=unknown,
        missing_fields=missing_fields,
        rule_version=active_rules[0].rule_version if active_rules else 1,
        summary_explanation=summary_explanation,
        disclaimer="Final eligibility and approval are subject to verification by the authorized department."
    )

def assess_draft_rules(
    draft_rules: List[EligibilityRule],
    citizen_attributes: Dict[str, Any]
) -> Dict[str, Any]:
    satisfied: List[CriterionResult] = []
    unmet: List[CriterionResult] = []
    unknown: List[CriterionResult] = []
    missing_fields: List[str] = []

    for rule in draft_rules:
        act_val = citizen_attributes.get(rule.field_name)
        if act_val is None:
            if rule.field_name == "annual_income":
                act_val = citizen_attributes.get("income") or citizen_attributes.get("family_income")
            elif rule.field_name == "caste_category":
                act_val = citizen_attributes.get("caste") or citizen_attributes.get("category")
            elif rule.field_name == "residence_state":
                act_val = citizen_attributes.get("state") or citizen_attributes.get("domicile")
            elif rule.field_name == "education_level":
                act_val = citizen_attributes.get("education") or citizen_attributes.get("qualification")
            elif rule.field_name == "is_woman":
                gen = citizen_attributes.get("gender")
                if gen: act_val = str(gen).strip().lower() in ["female", "woman"]
            elif rule.field_name == "gender":
                wom = citizen_attributes.get("is_woman")
                if wom is not None: act_val = "female" if wom else "male"

        res = evaluate_criterion(rule, act_val)
        if res.status == "SATISFIED":
            satisfied.append(res)
        elif res.status == "UNMET":
            unmet.append(res)
        else:
            unknown.append(res)
            missing_fields.append(rule.field_name)

    mandatory_unmet = any(r.is_mandatory for r in unmet)
    mandatory_unknown = any(r.is_mandatory for r in unknown)

    if mandatory_unmet:
        status = "NOT_ELIGIBLE"
    elif mandatory_unknown:
        status = "INSUFFICIENT_INFORMATION"
    else:
        status = "LIKELY_ELIGIBLE"

    return {
        "preliminary_status": status,
        "satisfied_criteria": satisfied,
        "unmet_criteria": unmet,
        "unknown_criteria": unknown,
        "missing_fields": missing_fields
    }
