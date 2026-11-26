-- ==============================================================================
-- NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
-- DEDICATED DATABASE ARCHITECTURE & SCHEMA REFERENCE
-- Database: nagriksetu_swd
-- Dedicated User: swd_app
-- MySQL Workbench Connection Name: NagrikSetu_SWD_DB
-- Host: 127.0.0.1 / localhost
-- Port: 3306 (or Docker-forwarded 3308)
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `nagriksetu_swd`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `nagriksetu_swd`;

-- 1. SCHEME CATEGORIES (Department Welfare Streams)
-- Holds official categories (e.g. Education, Pensions, Housing, Women, Disability)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Table: scheme_categories

-- 2. SCHEMES (Karnataka Welfare Scheme Catalogue)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Unique: scheme_code (e.g. KAR-SWD-001)
-- Table: schemes

-- 3. ELIGIBILITY RULES (Rules Engine Predicates)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Foreign Key: scheme_id -> schemes(id)
-- Table: eligibility_rules

-- 4. SCHEME DOCUMENTS (Mandatory and Supporting Document Checklists)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Foreign Key: scheme_id -> schemes(id)
-- Table: scheme_documents

-- 5. USERS & CITIZENS (Citizen Registry & Administrative Officer Profiles)
-- Primary Key: id (INT AUTO_INCREMENT) - Permanent Numeric Citizen Primary Key
-- Unique: citizen_id (Formatted String: CIT-KA-YYYY-XXXXXX)
-- Unique: email
-- Table: users

-- 6. SCHEME APPLICATIONS (Citizen Dossier Submissions)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Unique: application_number (e.g. SWD-APP-2026-XXXXXX)
-- Foreign Key: scheme_id -> schemes(id)
-- Indexed: citizen_id, status
-- Table: scheme_applications

-- 7. APPLICATION DOCUMENTS (Uploaded Verification Documents)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Foreign Key: application_id -> scheme_applications(id)
-- Table: application_documents

-- 8. APPLICATION HISTORY (Audit Trail of Lifecycle Transitions)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Foreign Key: application_id -> scheme_applications(id)
-- Table: application_history

-- 9. BENEFICIARIES (Authorized Welfare Grant Beneficiary Ledger)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Unique: beneficiary_code (e.g. BEN-2026-SWD-XXXXXX)
-- Foreign Key: application_id -> scheme_applications(id)
-- Table: beneficiaries

-- 10. DBT TRANSACTIONS (Simulated Direct Benefit Transfer Ledger)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Unique: transaction_reference
-- Table: dbt_transactions

-- 11. OFFICER REVIEWS (Administrative Reviewer Notes & Decisions)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Foreign Key: application_id -> scheme_applications(id)
-- Table: officer_reviews

-- 12. GRIEVANCES (Citizen Welfare Helpdesk & Redressal Cell)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Unique: grievance_number (e.g. GRV-SWD-2026-XXXXXX)
-- Table: grievances

-- 13. NOTIFICATIONS (Citizen & Officer Notification Centre)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Indexed: user_id, is_read
-- Table: notifications

-- 14. AUDIT LOGS (Security & Compliance Event Audit Trail)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Table: audit_logs

-- 15. OFFICES (District & Taluk Social Welfare Offices)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Indexed: district, taluk, is_active
-- Table: offices

-- 16. OUTBOX EVENTS (Reliable Event Publishing / Messaging Pattern)
-- Primary Key: id (INT AUTO_INCREMENT)
-- Table: outbox_events
