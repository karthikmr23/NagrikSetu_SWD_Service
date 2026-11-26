-- ==============================================================================
-- NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
-- SCRIPT 03: VERIFY DATABASE CREATION & STRICT PERMISSION ISOLATION
-- COMPATIBLE WITH: MySQL Server 8.0 & MySQL Workbench 8.0
-- ==============================================================================

-- 1. Verify that nagriksetu_swd exists
SELECT 
    SCHEMA_NAME,
    DEFAULT_CHARACTER_SET_NAME,
    DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME IN ('nagriksetu_swd', 'skill_db');

-- 2. Verify that skill_db is intact and completely untouched
SELECT 
    TABLE_SCHEMA, 
    COUNT(*) AS total_tables 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA IN ('nagriksetu_swd', 'skill_db')
GROUP BY TABLE_SCHEMA;

-- 3. Verify user existence
SELECT User, Host, plugin 
FROM mysql.user 
WHERE User = 'swd_app';

-- 4. Verify privileges of swd_app (must only have grants on nagriksetu_swd.*)
SHOW GRANTS FOR 'swd_app'@'%';

-- 5. Confirm that swd_app CANNOT access skill_db
SELECT 
    GRANTEE, 
    TABLE_SCHEMA, 
    PRIVILEGE_TYPE 
FROM information_schema.SCHEMA_PRIVILEGES 
WHERE GRANTEE LIKE "'swd_app'%" ;
