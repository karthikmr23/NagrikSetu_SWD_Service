from datetime import datetime, date
from typing import List, Optional, Any, Dict
from datetime import date
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

VALID_OPERATORS = {
    "EQUALS", "NOT_EQUALS", "LESS_THAN", "LESS_THAN_OR_EQUAL",
    "GREATER_THAN", "GREATER_THAN_OR_EQUAL", "IN", "NOT_IN"
}

VALID_VALUE_TYPES = {"STRING", "INTEGER", "FLOAT", "BOOLEAN", "LIST"}

# ----------------- User & Auth Schemas -----------------
class UserRegisterRequest(BaseModel):
    citizen_id: Optional[str] = None
    email: EmailStr
    password: str
    confirm_password: Optional[str] = None
    full_name: str
    phone: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = "Bengaluru Urban"
    taluk: Optional[str] = None
    pin_code: Optional[str] = None
    state: Optional[str] = "Karnataka"
    annual_income: Optional[float] = 180000.0
    caste_category: Optional[str] = "SC"
    disability_percentage: Optional[float] = 0.0
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Full Name is required and must be at least 2 characters")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[^\d]", "", v or "")
        if len(cleaned) < 10 or len(cleaned) > 12:
            raise ValueError("Mobile number must be a valid 10-digit number")
        return cleaned[-10:]

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not v or len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    pin_code: Optional[str] = None
    state: Optional[str] = None
    annual_income: Optional[float] = None
    caste_category: Optional[str] = None
    disability_percentage: Optional[float] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    citizen_id: str
    email: str
    full_name: str
    role: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    pin_code: Optional[str] = None
    state: Optional[str] = "Karnataka"
    annual_income: Optional[float] = 0.0
    caste_category: Optional[str] = None
    disability_percentage: Optional[float] = 0.0
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    citizen_id: str
    email: str
    name: str

# ----------------- Scheme Category Schemas -----------------
class SchemeCategoryBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = "HeartHandshake"
    is_active: bool = True

class SchemeCategoryCreate(SchemeCategoryBase):
    pass

class SchemeCategoryResponse(SchemeCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Scheme Eligibility Rule Schemas -----------------
class EligibilityRuleBase(BaseModel):
    field_name: str
    operator: str
    expected_value: str
    value_type: str = "STRING"
    is_mandatory: bool = True
    description: str
    rule_version: int = 1
    is_active: bool = True

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        upper_op = v.strip().upper()
        if upper_op not in VALID_OPERATORS:
            raise ValueError(f"Unsupported operator '{v}'. Supported: {', '.join(sorted(VALID_OPERATORS))}")
        return upper_op

    @field_validator("value_type")
    @classmethod
    def validate_value_type(cls, v: str) -> str:
        upper_vt = v.strip().upper()
        if upper_vt not in VALID_VALUE_TYPES:
            raise ValueError(f"Unsupported value_type '{v}'. Supported: {', '.join(sorted(VALID_VALUE_TYPES))}")
        return upper_vt

    @field_validator("field_name", "expected_value", "description")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

class EligibilityRuleCreate(EligibilityRuleBase):
    pass

class EligibilityRuleResponse(EligibilityRuleBase):
    id: int
    scheme_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Scheme Required Document Schemas -----------------
class SchemeDocumentBase(BaseModel):
    document_code: str
    document_name: str
    description: Optional[str] = None
    is_mandatory: bool = True
    allowed_extensions: str = "pdf,jpg,jpeg,png"
    max_size_mb: int = 5

class SchemeDocumentCreate(SchemeDocumentBase):
    pass

class SchemeDocumentResponse(SchemeDocumentBase):
    id: int
    scheme_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Scheme Master Schemas -----------------
class SchemeBase(BaseModel):
    scheme_code: str
    name: str
    category_id: int
    department: str = "Social Welfare Department, Government of Karnataka"
    administering_authority: str
    description: str
    benefit_summary: str
    benefit_type: str = "DIRECT_BENEFIT_TRANSFER"
    benefit_amount: Optional[float] = None
    eligibility_summary: str
    application_instructions: str
    official_url: Optional[str] = None
    application_start_date: date
    application_end_date: date
    status: str = "PUBLISHED"
    is_duplicate_check_enabled: bool = True
    beneficiary_categories: Optional[str] = None
    verification_status: Optional[str] = "VERIFIED"
    application_mode: Optional[str] = "ONLINE_FORM"

class SchemeCreate(SchemeBase):
    rules: Optional[List[EligibilityRuleCreate]] = None
    documents: Optional[List[SchemeDocumentCreate]] = None

class SchemeUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    administering_authority: Optional[str] = None
    description: Optional[str] = None
    benefit_summary: Optional[str] = None
    benefit_type: Optional[str] = None
    benefit_amount: Optional[float] = None
    eligibility_summary: Optional[str] = None
    application_instructions: Optional[str] = None
    official_url: Optional[str] = None
    application_start_date: Optional[date] = None
    application_end_date: Optional[date] = None
    status: Optional[str] = None
    is_duplicate_check_enabled: Optional[bool] = None
    beneficiary_categories: Optional[str] = None
    verification_status: Optional[str] = None

class SchemeResponse(SchemeBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: datetime
    category: Optional[SchemeCategoryResponse] = None
    rules: Optional[List[EligibilityRuleResponse]] = None
    documents: Optional[List[SchemeDocumentResponse]] = None

    model_config = ConfigDict(from_attributes=True)

# ----------------- Eligibility Evaluation Schemas -----------------
class CriterionResult(BaseModel):
    field_name: str
    description: str
    expected: str
    operator: str
    actual_value: Optional[Any] = None
    status: str = Field(..., description="SATISFIED, UNMET, UNKNOWN")
    is_mandatory: bool
    explanation: str

    @property
    def is_satisfied(self) -> bool:
        return self.status == "SATISFIED"

class EligibilityCheckRequest(BaseModel):
    citizen_attributes: Dict[str, Any] = Field(..., description="Citizen profile attributes e.g. age, annual_income, caste_category, residence_state")

class EligibilityCheckResponse(BaseModel):
    scheme_id: int
    scheme_code: str
    scheme_name: str
    preliminary_status: str = Field(..., description="LIKELY_ELIGIBLE, NOT_ELIGIBLE, INSUFFICIENT_INFORMATION")
    satisfied_criteria: List[CriterionResult]
    unmet_criteria: List[CriterionResult]
    unknown_criteria: List[CriterionResult]
    missing_fields: List[str] = []
    rule_version: int = 1
    summary_explanation: str
    disclaimer: str = "Preliminary guidance only. Final eligibility determined by the administering authority."
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

# ----------------- Application Schemas -----------------
class ApplicationDocumentResponse(BaseModel):
    id: int
    application_id: int
    document_code: str
    file_name: str
    file_path: str
    file_type: str
    file_size_bytes: int
    verification_status: str
    uploaded_by: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationHistoryResponse(BaseModel):
    id: int
    application_id: int
    from_status: Optional[str]
    to_status: str
    changed_by: str
    action_type: str
    remarks: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationSubmissionRequest(BaseModel):
    citizen_id: str
    citizen_name: str
    citizen_email: Optional[str] = None
    citizen_phone: str
    annual_income: float
    caste_category: str
    residence_district: str
    disability_percentage: Optional[float] = 0.0
    bank_account_number: str
    bank_ifsc: str
    application_data_json: Optional[Dict[str, Any]] = None

class ApplicationResponse(BaseModel):
    id: int
    application_number: str
    scheme_id: int
    category_id: Optional[int] = None
    form_version_id: Optional[int] = 1
    citizen_id: str
    citizen_name: str
    citizen_email: Optional[str]
    citizen_phone: str
    annual_income: float
    caste_category: str
    residence_district: str
    disability_percentage: float
    bank_account_number: Optional[str]
    bank_ifsc: Optional[str]
    application_data_json: Optional[Dict[str, Any]] = None
    status: str
    is_duplicate_suspect: bool
    duplicate_reason: Optional[str]
    admin_remarks: Optional[str]
    created_at: datetime
    updated_at: datetime
    scheme: Optional[SchemeResponse] = None
    documents: Optional[List[ApplicationDocumentResponse]] = []
    history: Optional[List[ApplicationHistoryResponse]] = []

    model_config = ConfigDict(from_attributes=True)

class RequestInformationRequest(BaseModel):
    remarks: str

class ApplicationDecisionRequest(BaseModel):
    decision: str
    remarks: str
    sanctioned_amount: Optional[float] = None
    disbursement_mode: Optional[str] = "DIRECT_BENEFIT_TRANSFER"

# ----------------- Beneficiary Schemas -----------------
class BeneficiaryResponse(BaseModel):
    id: int
    beneficiary_code: str
    application_id: int
    scheme_id: int
    citizen_id: str
    citizen_name: str
    sanctioned_amount: float
    disbursement_mode: str
    status: str
    sanctioned_by: str
    sanctioned_at: datetime
    scheme: Optional[SchemeResponse] = None

    model_config = ConfigDict(from_attributes=True)

# ----------------- DBT Transaction Schemas -----------------
class DbtTransactionResponse(BaseModel):
    id: int
    transaction_reference: str
    beneficiary_id: int
    scheme_id: int
    amount: float
    payment_mode: str
    status: str
    bank_account_last4: Optional[str]
    ifsc_code: Optional[str]
    processed_at: datetime
    remarks: Optional[str]
    beneficiary_name: Optional[str] = None
    scheme_name: Optional[str] = None
    application_number: Optional[str] = None
    batch_reference: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DbtProcessRequest(BaseModel):
    beneficiary_id: int
    remarks: Optional[str] = "Simulated Direct Benefit Transfer"
    simulate_failure: Optional[bool] = False

class DbtBatchProcessRequest(BaseModel):
    beneficiary_ids: List[int]
    remarks: Optional[str] = "Simulated DBT Batch Disbursement"
    fail_beneficiary_ids: Optional[List[int]] = []

class DbtBatchProcessResultItem(BaseModel):
    beneficiary_id: int
    beneficiary_name: str
    application_number: str
    scheme_name: str
    amount: float
    transaction_reference: str
    status: str
    remarks: str

class DbtBatchProcessResponse(BaseModel):
    batch_reference: str
    total_processed: int
    successful_count: int
    failed_count: int
    total_amount_disbursed: float
    processed_at: datetime
    notice: str = "DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED."
    results: List[DbtBatchProcessResultItem]

class DbtDashboardStats(BaseModel):
    total_approved_beneficiaries: int
    total_payments_processed: int
    successful_transactions: int
    failed_transactions: int
    pending_transactions: int
    total_simulated_disbursed: float
    allocated_budget: float = 10000000.00
    remaining_budget: float
    notice: str = "DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED."

# ----------------- Grievance Schemas -----------------
class GrievanceCreateRequest(BaseModel):
    citizen_id: str
    citizen_name: str
    category: str
    subject: str
    description: str

class GrievanceUpdateRequest(BaseModel):
    status: str
    officer_response: str

class GrievanceResponse(BaseModel):
    id: int
    grievance_number: str
    citizen_id: str
    citizen_name: str
    category: str
    subject: str
    description: str
    status: str
    officer_response: Optional[str]
    resolved_by: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Notification Schemas -----------------
class NotificationResponse(BaseModel):
    id: int
    user_id: str
    title: str
    message: str
    is_read: bool
    notification_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Officer Review Schemas -----------------
class OfficerReviewResponse(BaseModel):
    id: int
    application_id: int
    officer_id: str
    officer_name: str
    review_status: str
    remarks: Optional[str]
    documents_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Draft Rule Test Schemas -----------------
class DraftRuleTestProfileResult(BaseModel):
    profile_index: Optional[int] = None
    profile_id: Optional[str] = None
    profile: Optional[Dict[str, Any]] = None
    preliminary_status: str
    satisfied_count: Optional[int] = None
    unmet_count: Optional[int] = None
    unknown_count: Optional[int] = None
    satisfied_criteria: Optional[List[CriterionResult]] = None
    unmet_criteria: Optional[List[CriterionResult]] = None
    unknown_criteria: Optional[List[CriterionResult]] = None
    missing_fields: Optional[List[str]] = None

class DraftRuleTestRequest(BaseModel):
    scheme_id: Optional[int] = None
    draft_rules: List[EligibilityRuleCreate]
    test_profiles: Optional[List[Dict[str, Any]]] = None
    synthetic_profiles: Optional[List[Dict[str, Any]]] = None

class DraftRuleTestResponse(BaseModel):
    scheme_id: Optional[int] = None
    total_profiles_tested: int
    eligible_count: Optional[int] = None
    ineligible_count: Optional[int] = None
    insufficient_info_count: Optional[int] = None
    results: List[DraftRuleTestProfileResult]

# ----------------- Dashboard & Reports Schemas -----------------
class AdminDashboardStats(BaseModel):
    total_schemes: int
    published_schemes: int
    draft_schemes: int
    closed_schemes: int
    total_applications: int
    submitted_applications: int
    under_review_applications: int
    more_info_required_applications: int
    approved_applications: int
    rejected_applications: int
    total_beneficiaries: int
    total_sanctioned_amount: float
    total_dbt_disbursed: float
    total_grievances: int
    pending_grievances: int
    recent_applications: List[ApplicationResponse]

class SchemeRecommendationResult(BaseModel):
    scheme_id: int
    scheme_code: str
    scheme_name: str
    category_name: str
    benefit_summary: str
    benefit_amount: Optional[float] = None
    match_category: str = Field(..., description="LIKELY_MATCH, POSSIBLE_MATCH, UNMET_CRITERIA, INSUFFICIENT_INFORMATION")
    score: float
    relevance_explanation: str
    missing_fields: List[str]
    disclaimer: str = "Preliminary guidance only. Final eligibility determined by the administering authority."


# ----------------- Smart Scheme Finder Schemas -----------------
class SmartFinderQuestionnaire(BaseModel):
    age: Optional[int] = None
    district: Optional[str] = "Bengaluru Urban"
    taluk: Optional[str] = None
    gender: Optional[str] = None
    caste_category: Optional[str] = None
    annual_income: Optional[float] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    is_farmer: Optional[bool] = None
    is_student: Optional[bool] = None
    is_woman: Optional[bool] = None
    disability_status: Optional[str] = None
    disability_percentage: Optional[float] = None
    marital_status: Optional[str] = None

class SmartFinderMatchItem(BaseModel):
    scheme_id: int
    scheme_code: str
    scheme_name: str
    category_id: int
    category_name: str
    description: str
    benefit_summary: str
    benefit_amount: Optional[float] = None
    eligibility_summary: str
    documents_required: List[str] = []
    status: str
    verification_status: str
    match_status: str = Field(..., description="Potential Match | Check Requirements | Not Matched")
    match_score: float
    why_matched: List[str]
    missing_requirements: List[str] = []
    has_application_form: bool = True
    official_url: Optional[str] = None
    disclaimer: str = "These recommendations are based on the information you provided and the eligibility details currently available in the portal. Final eligibility and approval are determined by the relevant department."

class SmartFinderResponse(BaseModel):
    total_matches: int
    potential_match_count: int
    check_requirements_count: int
    results: List[SmartFinderMatchItem]
    disclaimer: str = "These recommendations are based on the information you provided and the eligibility details currently available in the portal. Final eligibility and approval are determined by the relevant department."


# ----------------- Dynamic Form Schemas -----------------
class DynamicFormFieldResponse(BaseModel):
    id: int
    form_id: int
    field_name: str
    field_label: str
    field_type: str
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    is_required: bool = True
    display_order: int = 0
    options_json: Optional[Any] = None
    validation_rules_json: Optional[Any] = None
    conditional_visibility_json: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True)

class DynamicFormDefinitionResponse(BaseModel):
    id: int
    scheme_id: int
    version: int = 1
    title: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    fields: List[DynamicFormFieldResponse] = []

    model_config = ConfigDict(from_attributes=True)

class DynamicFormFieldCreate(BaseModel):
    field_name: str
    field_label: str
    field_type: str
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    is_required: bool = True
    display_order: int = 0
    options_json: Optional[Any] = None
    validation_rules_json: Optional[Any] = None
    conditional_visibility_json: Optional[Any] = None

class DynamicFormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    fields: List[DynamicFormFieldCreate] = []

class OfficerCategoryAssignmentResponse(BaseModel):
    id: int
    officer_id: int
    category_id: int
    assigned_by: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class DepartmentAnnouncementRequest(BaseModel):
    title: str
    message: str
    announcement_type: str = 'INFO'
    target_role: Optional[str] = 'CITIZEN'
