# MySQL Workbench 8.0 — Database Setup & Verification Guide

This guide provides step-by-step instructions to create and verify the dedicated Social Welfare Department (SWD) database schema on your existing MySQL 8.0 server on port **3308** without affecting `skill_db`.

---

## Prerequisites
- **MySQL Server 8.0** running on port **3308**.
- **MySQL Workbench 8.0** installed on Windows.

---

## Step 1: Open MySQL Workbench & Connect to Port 3308
1. Launch **MySQL Workbench 8.0** on your Windows desktop.
2. In the MySQL Connections list, select your existing connection configured for port **3308** (e.g. `Local Instance MySQL80` or `Port 3308`).
3. Connect using your administrative credentials (`root`).

---

## Step 2: Open and Execute Script 01 (Create Database)
1. In MySQL Workbench, click **File → Open SQL Script...** (or press `Ctrl + O`).
2. Navigate to:
   `C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\database\01_create_database.sql`
3. Click the **Execute** button (the yellow lightning bolt icon ⚡) or press `Ctrl + Shift + Enter`.
4. In the Output window at the bottom, confirm that `nagriksetu_swd` is created with character set `utf8mb4` and collation `utf8mb4_unicode_ci`.

---

## Step 3: Open and Execute Script 02 (Create Dedicated SWD User)
1. In MySQL Workbench, open:
   `C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\database\02_create_swd_user.sql`
2. **Review Password**: Line 16 and 19 define the password. The default matches your configured application environment:
   `'swd-secure-pass-2026'`
   *(If you change this password, update `DB_PASSWORD` in your project `.env` file accordingly).*
3. Click **Execute** (⚡).
4. Verify that `'swd_app'@'%'` is created and granted privileges **strictly on `nagriksetu_swd.*`**.

---

## Step 4: Open and Execute Script 03 (Verify Isolation & Grants)
1. In MySQL Workbench, open:
   `C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\database\03_verify_database.sql`
2. Click **Execute** (⚡).
3. Confirm in the Result Grid:
   - `nagriksetu_swd` exists alongside `skill_db`.
   - `skill_db` remains completely untouched.
   - The user `'swd_app'` only has grants on `nagriksetu_swd.*`.

---

## Step 5: Refresh Schemas Panel
1. In the left sidebar of MySQL Workbench, look under the **Navigator → Schemas** section.
2. Click the circular **Refresh** button next to "SCHEMAS".
3. Verify that both `nagriksetu_swd` and `skill_db` appear as independent databases in the list.
