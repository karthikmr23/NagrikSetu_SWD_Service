-- ==============================================================================
-- NAGRIKSETU SOCIAL WELFARE DEPARTMENT (SWD) MICROSERVICE
-- SCRIPT 01: CREATE DEDICATED DATABASE SCHEMA
-- COMPATIBLE WITH: MySQL Server 8.0 & MySQL Workbench 8.0
-- ==============================================================================
-- TARGET DATABASE: nagriksetu_swd
-- PORT: 3308
-- STRICT ISOLATION: skill_db remains untouched
-- ==============================================================================

-- 1. Create database if it does not already exist
CREATE DATABASE IF NOT EXISTS `nagriksetu_swd`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2. Verify creation output
SELECT 
    SCHEMA_NAME AS `Database`,
    DEFAULT_CHARACTER_SET_NAME AS `Charset`,
    DEFAULT_COLLATION_NAME AS `Collation`
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'nagriksetu_swd';
