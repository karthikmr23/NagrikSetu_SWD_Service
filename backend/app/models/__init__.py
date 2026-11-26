from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date, 
    Numeric, ForeignKey, JSON, Enum
)
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum

class UserRole(str, enum.Enum):
    CITIZEN = "CITIZEN"
    WELFARE_OFFICER = "WELFARE_OFFICER"
    ADMINISTRATOR = "ADMINISTRATOR"

class SchemeStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"
    INACTIVE = "INACTIVE"

class BenefitType(str, enum.Enum):
    DIRECT_BENEFIT_TRANSFER = "DIRECT_BENEFIT_TRANSFER"
    FINANCIAL_ASSISTANCE = "FINANCIAL_ASSISTANCE"
    SCHOLARSHIP = "SCHOLARSHIP"
    SUBSIDY = "SUBSIDY"
    IN_KIND = "IN_KIND"

class OperatorType(str, enum.Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    IN = "IN"
    NOT_IN = "NOT_IN"

class ValueType(str, enum.Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    LIST = "LIST"

class ApplicationStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    DOCUMENTS_REQUIRED = "DOCUMENTS_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BENEFIT_PROCESSED = "BENEFIT_PROCESSED"

class BeneficiaryStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"

class DbtTransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"

class GrievanceStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class OutboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    citizen_id = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), default="CITIZEN", index=True)
    phone = Column(String(20), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), default="Karnataka")
    annual_income = Column(Numeric(12, 2), default=0.0)
    caste_category = Column(String(50), nullable=True)
    disability_percentage = Column(Numeric(5, 2), default=0.0)
    bank_account_number = Column(String(50), nullable=True)
    bank_ifsc = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    taluk = Column(String(100), nullable=True)
    pin_code = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SchemeCategory(Base):
    __tablename__ = "scheme_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    name_kannada = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="HeartHandshake")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schemes = relationship("Scheme", back_populates="category")

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    name_kannada = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("scheme_categories.id"), nullable=False)
    department = Column(String(150), default="Social Welfare Department, Government of Karnataka")
    administering_authority = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    benefit_summary = Column(Text, nullable=False)
    benefit_type = Column(String(50), default="DIRECT_BENEFIT_TRANSFER")
    benefit_amount = Column(Numeric(12, 2), nullable=True)
    eligibility_summary = Column(Text, nullable=False)
    application_instructions = Column(Text, nullable=False)
    official_url = Column(String(500), nullable=True)
    application_start_date = Column(Date, nullable=False)
    application_end_date = Column(Date, nullable=False)
    status = Column(String(20), default="DRAFT", index=True)
    is_duplicate_check_enabled = Column(Boolean, default=True)
    beneficiary_categories = Column(Text, nullable=True)
    verification_status = Column(String(50), default="VERIFIED")
    application_mode = Column(String(50), default="ONLINE_FORM")
    created_by = Column(String(100), default="SYSTEM_ADMIN")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("SchemeCategory", back_populates="schemes")
    rules = relationship("EligibilityRule", back_populates="scheme", cascade="all, delete-orphan")
    documents = relationship("SchemeDocument", back_populates="scheme", cascade="all, delete-orphan")
    applications = relationship("SchemeApplication", back_populates="scheme")

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    operator = Column(String(30), nullable=False)
    expected_value = Column(String(255), nullable=False)
    value_type = Column(String(20), default="STRING")
    is_mandatory = Column(Boolean, default=True)
    description = Column(String(255), nullable=False)
    rule_version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scheme = relationship("Scheme", back_populates="rules")

class SchemeDocument(Base):
    __tablename__ = "scheme_documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    document_code = Column(String(50), nullable=False)
    document_name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    is_mandatory = Column(Boolean, default=True)
    allowed_extensions = Column(String(100), default="pdf,jpg,jpeg,png")
    max_size_mb = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)

    scheme = relationship("Scheme", back_populates="documents")

class SchemeApplication(Base):
    __tablename__ = "scheme_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_number = Column(String(60), unique=True, nullable=False, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("scheme_categories.id"), nullable=True, index=True)
    form_version_id = Column(Integer, nullable=True)
    citizen_id = Column(String(100), nullable=False, index=True)
    citizen_name = Column(String(200), nullable=False)
    citizen_email = Column(String(150), nullable=True)
    citizen_phone = Column(String(20), nullable=False)
    annual_income = Column(Numeric(12, 2), nullable=False)
    caste_category = Column(String(50), nullable=False)
    residence_district = Column(String(100), nullable=False)
    disability_percentage = Column(Numeric(5, 2), default=0.00)
    bank_account_number = Column(String(50), nullable=False)
    bank_ifsc = Column(String(20), nullable=False)
    application_data_json = Column(JSON, nullable=True)
    status = Column(String(30), default="SUBMITTED", index=True)
    is_duplicate_suspect = Column(Boolean, default=False)
    duplicate_reason = Column(String(255), nullable=True)
    admin_remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scheme = relationship("Scheme", back_populates="applications")
    category = relationship("SchemeCategory")
    documents = relationship("ApplicationDocument", back_populates="application", cascade="all, delete-orphan")
    history = relationship("ApplicationHistory", back_populates="application", cascade="all, delete-orphan")
    beneficiary = relationship("Beneficiary", back_populates="application", uselist=False)
    officer_reviews = relationship("OfficerReview", back_populates="application", cascade="all, delete-orphan")

class ApplicationDocument(Base):
    __tablename__ = "application_documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("scheme_applications.id"), nullable=False)
    document_code = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    verification_status = Column(String(50), default="PENDING")
    uploaded_by = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("SchemeApplication", back_populates="documents")

class ApplicationHistory(Base):
    __tablename__ = "application_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("scheme_applications.id"), nullable=False)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=False)
    changed_by = Column(String(100), nullable=False)
    action_type = Column(String(50), default="STATUS_CHANGE")
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("SchemeApplication", back_populates="history")

class OfficerReview(Base):
    __tablename__ = "officer_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("scheme_applications.id"), nullable=False)
    officer_id = Column(String(100), nullable=False, index=True)
    officer_name = Column(String(200), nullable=False)
    review_status = Column(String(50), nullable=False)
    remarks = Column(Text, nullable=True)
    documents_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("SchemeApplication", back_populates="officer_reviews")

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    beneficiary_code = Column(String(60), unique=True, nullable=False, index=True)
    application_id = Column(Integer, ForeignKey("scheme_applications.id"), unique=True, nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    citizen_id = Column(String(100), nullable=False, index=True)
    citizen_name = Column(String(200), nullable=False)
    sanctioned_amount = Column(Numeric(12, 2), nullable=False)
    disbursement_mode = Column(String(50), default="DIRECT_BENEFIT_TRANSFER")
    status = Column(String(20), default="ACTIVE")
    sanctioned_by = Column(String(100), nullable=False)
    sanctioned_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("SchemeApplication", back_populates="beneficiary")
    scheme = relationship("Scheme")
    dbt_transactions = relationship("DbtTransaction", back_populates="beneficiary")

class DbtTransaction(Base):
    __tablename__ = "dbt_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_reference = Column(String(64), unique=True, nullable=False, index=True)
    batch_reference = Column(String(64), nullable=True, index=True)
    beneficiary_id = Column(Integer, ForeignKey("beneficiaries.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_mode = Column(String(50), default="SIMULATED_AADHAAR_BRIDGE")
    status = Column(String(30), default="SUCCESSFUL", index=True)
    bank_account_last4 = Column(String(10), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)
    initiated_by = Column(String(100), default="SWD_ADMIN")
    remarks = Column(String(255), nullable=True)

    beneficiary = relationship("Beneficiary", back_populates="dbt_transactions")
    scheme = relationship("Scheme")

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    grievance_number = Column(String(64), unique=True, nullable=False, index=True)
    citizen_id = Column(String(100), nullable=False, index=True)
    citizen_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="SUBMITTED", index=True)
    officer_response = Column(Text, nullable=True)
    resolved_by = Column(String(100), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    notification_type = Column(String(50), default="INFO")
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    actor_id = Column(String(100), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=True)
    correlation_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(String(64), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    schema_version = Column(String(10), default="1.0")
    correlation_id = Column(String(64), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String(20), default="PENDING", index=True)
    retry_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)


class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    office_type = Column(String(100), default="District Welfare Office", index=True)
    district = Column(String(100), nullable=False, index=True)
    taluk = Column(String(100), nullable=True, index=True)
    address = Column(Text, nullable=False)
    contact_number = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    working_hours = Column(String(100), default="10:00 AM - 5:30 PM (Mon-Sat)")
    services_offered = Column(Text, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    map_link = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    verification_status = Column(String(50), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DynamicFormDefinition(Base):
    __tablename__ = "dynamic_form_definitions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scheme = relationship("Scheme")
    fields = relationship("DynamicFormField", back_populates="form", cascade="all, delete-orphan", order_by="DynamicFormField.display_order")


class DynamicFormField(Base):
    __tablename__ = "dynamic_form_fields"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey("dynamic_form_definitions.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False)
    placeholder = Column(String(255), nullable=True)
    help_text = Column(String(255), nullable=True)
    is_required = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    options_json = Column(JSON, nullable=True)
    validation_rules_json = Column(JSON, nullable=True)
    conditional_visibility_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    form = relationship("DynamicFormDefinition", back_populates="fields")


class OfficerCategoryAssignment(Base):
    __tablename__ = "officer_category_assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("scheme_categories.id"), nullable=False, index=True)
    assigned_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    officer = relationship("User", foreign_keys=[officer_id])
    category = relationship("SchemeCategory", foreign_keys=[category_id])

