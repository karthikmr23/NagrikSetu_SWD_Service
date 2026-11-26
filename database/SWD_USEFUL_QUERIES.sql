-- ==============================================================================
-- NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
-- USEFUL DATABASE QUERIES FOR MYSQL WORKBENCH
-- Connection: NagrikSetu_SWD_DB (Host: 127.0.0.1, Port: 3306 or 3308, User: swd_app)
-- Database: nagriksetu_swd
-- ==============================================================================

USE `nagriksetu_swd`;

-- 1. VERIFY ALL 16 TABLES IN SWD SCHEMA
SHOW TABLES;

-- 2. CITIZEN REGISTRY & PERMANENT NUMERIC CITIZEN IDS
-- Note: id is the permanent MySQL AUTO_INCREMENT numeric ID; citizen_id is the citizen display code.
SELECT id, citizen_id, full_name, email, phone, role, district, caste_category, created_at 
FROM users 
ORDER BY id ASC;

-- 3. KARNATAKA WELFARE SCHEMES OVERVIEW
SELECT id, scheme_code, name, department, status, benefit_amount, application_start_date, application_end_date 
FROM schemes 
ORDER BY id ASC;

-- 4. ACTIVE CITIZEN APPLICATIONS & PROCESSING STATUSES
SELECT id, application_number, scheme_id, citizen_id, citizen_name, caste_category, residence_district, status, created_at 
FROM scheme_applications 
ORDER BY id DESC;

-- 5. AUDIT TRAIL OF APPLICATION STATUS TRANSITIONS
SELECT h.id, a.application_number, h.from_status, h.to_status, h.changed_by, h.action_type, h.remarks, h.created_at 
FROM application_history h 
JOIN scheme_applications a ON h.application_id = a.id 
ORDER BY h.id DESC;

-- 6. AUTHORIZED WELFARE BENEFICIARIES LEDGER
SELECT id, beneficiary_code, application_id, citizen_id, citizen_name, sanctioned_amount, disbursement_mode, status, sanctioned_at 
FROM beneficiaries 
ORDER BY id DESC;

-- 7. SIMULATED DBT TRANSACTIONS LEDGER
SELECT id, transaction_reference, batch_reference, beneficiary_name, scheme_name, amount, status, processed_at, remarks 
FROM dbt_transactions 
ORDER BY id DESC;

-- 8. CITIZEN GRIEVANCE & HELPDESK RECORDS
SELECT id, grievance_number, citizen_id, citizen_name, category, subject, status, officer_response, resolved_by, created_at 
FROM grievances 
ORDER BY id DESC;

-- 9. NOTIFICATION CENTRE DISPATCHED NOTIFICATIONS
SELECT id, user_id, title, message, is_read, notification_type, created_at 
FROM notifications 
ORDER BY id DESC;

-- 10. VERIFIED DISTRICT & TALUK SOCIAL WELFARE OFFICES
SELECT id, name, office_type, district, taluk, contact_number, email, working_hours, verification_status 
FROM offices 
ORDER BY district ASC, name ASC;

-- 11. AUDIT LOG OF ADMINISTRATIVE ACTIONS
SELECT id, actor_id, actor_role, action, entity_type, entity_id, timestamp 
FROM audit_logs 
ORDER BY id DESC 
LIMIT 50;
