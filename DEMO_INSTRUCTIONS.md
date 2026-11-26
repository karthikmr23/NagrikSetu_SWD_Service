# NagrikSetu SWD — Final Academic Demonstration Guide

This guide provides the exact demonstration sequence, URLs, test credentials, and viva explanations for your faculty presentation tomorrow.

---

## 1. Quick Startup Commands

Open PowerShell or Command Prompt on Windows:
```powershell
cd 'C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD\SWD_FINAL'
docker compose up -d
```

Verify containers are running:
```powershell
docker ps
```
*Expected: `nagriksetu-swd-frontend`, `nagriksetu-swd-backend`, and `nagriksetu-swd-mysql8` are Up.*

---

## 2. Portal URLs & Access Endpoints

- **Citizen & Admin Web Interface:** [http://localhost:5174](http://localhost:5174) (or [http://localhost:5175](http://localhost:5175))
- **Interactive Backend API Documentation (Swagger UI):** [http://localhost:8005/docs](http://localhost:8005/docs)
- **Backend Health Check:** [http://localhost:8005/health](http://localhost:8005/health)

---

## 3. Demonstration Credentials

| Role | Email Address | Password | Key Demonstration Action |
| :--- | :--- | :--- | :--- |
| **Citizen (Mukesh)** | `mukesh2345@gmail.com` | `CitizenPass@2026` | Track application `SWD-APP-2026-98E64D`, view scrutiny notes, download PDF receipt. |
| **Citizen (Mahesh)** | `mahesh123@gmail.com` | `CitizenPass@2026` | Test Smart Scheme Finder (Male, General, Student) -> 0 false positives. |
| **Government Welfare Admin** | `welfareadmin@example.com` | `AdminPass@2026` | View scrutiny queue, review applicant details & marksheets, transition status. |
| **Platform Administrator** | `platformadmin@example.com` | `AdminPass@2026` | Inspect User Directory (39 accounts), Scheme Taxonomy, and live Security Audit Logs. |

---

## 4. Recommended Demonstration Flow (Step-by-Step)

### Step 1: Citizen Discovery & Eligibility Assessment (Mahesh)
1. Open [http://localhost:5174](http://localhost:5174).
2. Click **Smart Scheme Finder** on the navigation bar.
3. Show that Mahesh's profile is prefilled with realistic attributes:
   - Gender: **Male**, Age: **28**, Category: **General**, Income: **₹1,80,000**, Occupation: **Student**.
4. Click **Find Matching Schemes**.
5. **Point out to faculty:**
   - Girl-child and maternal schemes (Bhagyalakshmi, Gruha Lakshmi, Udyogini) are correctly placed under **Not Matched** with clear explanations.
   - Anna Bhagya, Gruha Jyothi, and Yeshasvini are placed under **Check Requirements** because specific prerequisites (ration card, meter, cooperative membership) require documentation.
   - **Zero false positives are displayed.**

### Step 2: Citizen Application Tracking & PDF Receipt (Mukesh)
1. Click **Sign In** -> select **Citizen Sign In**.
2. Log in with `mukesh2345@gmail.com` / `CitizenPass@2026`.
3. Click **Track Application** in the citizen dashboard.
4. Locate application **`SWD-APP-2026-98E64D`** (*Thayi Bhagya & Prasoothi Araike Scheme*).
5. **Show faculty:**
   - Status badge is **UNDER_REVIEW**.
   - Reviewer remarks display: *"Not satisfied with the provided documents, please provide all the relevant documents"*.
   - Uploaded marksheet PDF is listed and downloadable.
6. Click **Download Official Acknowledgement**.
   - Show the instantly generated, styled PDF receipt with department seal, reference numbers, and timestamp.

### Step 3: Official Scrutiny & Decision Workflow (Welfare Admin)
1. Log out, then click **Sign In** -> select **Government Welfare Admin**.
2. Log in with `welfareadmin@example.com` / `AdminPass@2026`.
3. Show the dynamic dashboard metrics:
   - **44 Total Applications**, **28 Published Schemes**, **28 Beneficiaries**.
4. Click **Application Scrutiny** in the sidebar.
5. Locate Mukesh's application (Record ID `36`, `SWD-APP-2026-98E64D`).
6. Click **Inspect & Decide**:
   - Show applicant details side-by-side with uploaded certificates.
   - Demonstrate the decision options: **APPROVED**, **RETURNED FOR CLARIFICATION**, **REJECTED**.

### Step 4: System Governance & Security Audit Trails (Platform Admin)
1. Log in with `platformadmin@example.com` / `AdminPass@2026`.
2. Navigate to **Platform Administration**:
   - **User Monitoring:** Displays all 39 registered accounts.
   - **Audit Logs:** Displays immutable security and administrative events (logins, status changes) with exact timestamps.
   - **Grievance Redressal:** Shows citizen grievance tickets and officer resolution notes.

---

## 5. Answers to Likely Faculty Viva Questions

**Q1: How does your system eliminate false positives in scheme recommendations?**  
*Answer:* "We replaced simple keyword and domicile matching with a deterministic relational rule engine in MySQL. Every scheme defines mandatory criteria with specific operators (EQUALS, RANGE, IN). The backend assesses the applicant's multidimensional profile and only grants 'Potential Match' when all mandatory criteria are verified. If a mandatory criterion is violated (e.g. male applicant for a girl-child scheme), it is immediately flagged as 'Not Matched' with an explicit explanation."

**Q2: How do you generate PDF receipts inside Docker without reportlab crashes?**  
*Answer:* "We developed a pure-Python streaming PDF generator that writes compliant Adobe PDF 1.4 binary streams using native byte streams. It creates PDF objects, font dictionaries, and cross-reference tables directly without depending on external C libraries or system packages."

**Q3: How is data consistency maintained when an officer changes application status?**  
*Answer:* "State transitions are managed as atomic database transactions using SQLAlchemy and MySQL InnoDB. When an officer records a decision, the system writes the updated status to `scheme_applications` and simultaneously appends an immutable audit step to `application_history`. If any operation fails, the entire transaction rolls back."

**Q4: How do you handle role-based security across citizens and administrators?**  
*Answer:* "We use OAuth2 Password Bearer authentication with JWT tokens (HS256). Every API endpoint is protected by FastAPI dependency injection with role guards (`require_role`). If a citizen attempts to access an administrative endpoint, the backend immediately rejects the request with HTTP 403 Forbidden."
