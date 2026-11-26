-- ==============================================================================
-- NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
-- SCRIPT 02: CREATE DEDICATED RESTRICTED SWD DATABASE USER
-- COMPATIBLE WITH: MySQL Server 8.0 & MySQL Workbench 8.0
-- ==============================================================================
-- TARGET USER: 'swd_app'@'%'
-- PERMISSIONS: nagriksetu_swd.* ONLY
-- STRICT ISOLATION: Zero access to skill_db or administrative schemas
-- ==============================================================================

-- ==============================================================================
-- HOW TO CONFIGURE YOUR PASSWORD SAFELY IN MYSQL WORKBENCH:
-- 1. In MySQL Workbench, locate the placeholder text below:
--    [ENTER_YOUR_SECURE_SWD_PASSWORD_HERE]
-- 2. Replace [ENTER_YOUR_SECURE_SWD_PASSWORD_HERE] with your desired strong password
--    inside single quotes, e.g. 'MyStrongPassword123!'
-- 3. Update both line 24 and line 27 with the EXACT SAME password.
-- 4. Execute this script by clicking the lightning bolt (⚡) button.
-- 5. Then update the DB_PASSWORD in your .env file with that exact same password.
-- ==============================================================================

-- 1. Create or update the dedicated SWD user
CREATE USER IF NOT EXISTS 'swd_app'@'%' IDENTIFIED BY '[ENTER_YOUR_SECURE_SWD_PASSWORD_HERE]';

-- If user already exists, update password:
ALTER USER 'swd_app'@'%' IDENTIFIED BY '[ENTER_YOUR_SECURE_SWD_PASSWORD_HERE]';

-- 2. Revoke any global or unintended permissions
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'swd_app'@'%';

-- 3. Grant full application permissions strictly on nagriksetu_swd.*
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE
ON `nagriksetu_swd`.* TO 'swd_app'@'%';

-- 4. Apply changes
FLUSH PRIVILEGES;

-- 5. Show granted privileges for confirmation
SHOW GRANTS FOR 'swd_app'@'%';
