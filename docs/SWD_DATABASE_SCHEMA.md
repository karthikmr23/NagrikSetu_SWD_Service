# NAGRIKSETU — SWD DATABASE SCHEMA SPECIFICATION
## MySQL 8.0 & MySQL Workbench 8.0 CE Reference

### 1. Schema Overview
* **Database Name:** `swd_db`
* **Storage Engine:** InnoDB
* **Character Set:** `utf8mb4`
* **Collation:** `utf8mb4_unicode_ci`
* **Total Tables:** 10

### 2. Entity-Relationship & Table Details

```
+-------------------+       1:N       +-------------------+
| scheme_categories | <-------------- |      schemes      |
+-------------------+                 +-------------------+
                                                | 1:N
               +--------------------------------+--------------------------------+
               | 1:N                            | 1:N                            | 1:N
               v                                v                                v
     +-------------------+            +-------------------+            +---------------------+
     | eligibility_rules |            | scheme_documents  |            | scheme_applications |
     +-------------------+            +-------------------+            +---------------------+
                                                                                 |
                                                       +-------------------------+-------------------------+
                                                       | 1:N                     | 1:N                     | 1:1
                                                       v                         v                         v
                                             +-----------------------+ +---------------------+ +---------------+
                                             | application_documents | | application_history | | beneficiaries |
                                             +-----------------------+ +---------------------+ +---------------+

Independent Logging Tables:
- audit_logs (Actor ID, Role, Action, Entity, IP, JSON Details, Created At)
- outbox_events (Event ID, Type, Schema Version, Correlation ID, Payload, Status)
```

### 3. Verification in MySQL Workbench 8.0 CE
1. Open **MySQL Workbench 8.0 CE**.
2. Connect to your MySQL 8.0 instance (default port `3306` or Docker port).
3. In SQL Query tab, execute:
   ```sql
   SHOW DATABASES;
   USE swd_db;
   SHOW TABLES;
   SELECT * FROM schemes;
   SELECT * FROM scheme_applications;
   SELECT * FROM beneficiaries;
   ```
4. All tables, foreign key constraints, and seed data will be visible and queryable.
