import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd'
)
cur = conn.cursor()

# 1. dynamic_form_definitions
cur.execute('''
CREATE TABLE IF NOT EXISTS dynamic_form_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_id INT NOT NULL,
    version INT NOT NULL DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (scheme_id) REFERENCES schemes(id),
    UNIQUE KEY uq_scheme_version (scheme_id, version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
''')

# 2. dynamic_form_fields
cur.execute('''
CREATE TABLE IF NOT EXISTS dynamic_form_fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    field_label VARCHAR(255) NOT NULL,
    field_type VARCHAR(50) NOT NULL,
    placeholder VARCHAR(255),
    help_text VARCHAR(255),
    is_required TINYINT(1) DEFAULT 1,
    display_order INT DEFAULT 0,
    options_json JSON,
    validation_rules_json JSON,
    conditional_visibility_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES dynamic_form_definitions(id) ON DELETE CASCADE,
    INDEX idx_form_order (form_id, display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
''')

# 3. officer_category_assignments
cur.execute('''
CREATE TABLE IF NOT EXISTS officer_category_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    officer_id INT NOT NULL,
    category_id INT NOT NULL,
    assigned_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (officer_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES scheme_categories(id),
    UNIQUE KEY uq_officer_cat (officer_id, category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
''')

# 4. Check if scheme_applications has category_id and form_version_id
cur.execute("SHOW COLUMNS FROM scheme_applications LIKE 'category_id';")
if not cur.fetchone():
    cur.execute("ALTER TABLE scheme_applications ADD COLUMN category_id INT AFTER scheme_id;")
    cur.execute("ALTER TABLE scheme_applications ADD FOREIGN KEY (category_id) REFERENCES scheme_categories(id);")
    print("Added category_id to scheme_applications")

cur.execute("SHOW COLUMNS FROM scheme_applications LIKE 'form_version_id';")
if not cur.fetchone():
    cur.execute("ALTER TABLE scheme_applications ADD COLUMN form_version_id INT AFTER category_id;")
    print("Added form_version_id to scheme_applications")

# Backfill category_id
cur.execute('''
UPDATE scheme_applications sa
JOIN schemes s ON sa.scheme_id = s.id
SET sa.category_id = s.category_id
WHERE sa.category_id IS NULL;
''')
print("Backfilled category_id. Rows affected:", cur.rowcount)

# 5. Check if schemes has application_mode
cur.execute("SHOW COLUMNS FROM schemes LIKE 'application_mode';")
if not cur.fetchone():
    cur.execute("ALTER TABLE schemes ADD COLUMN application_mode VARCHAR(50) DEFAULT 'ONLINE_FORM' AFTER status;")
    print("Added application_mode to schemes")

conn.commit()
print("Migration completed successfully!")
conn.close()
