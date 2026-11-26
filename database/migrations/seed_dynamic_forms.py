import json
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='swd_app',
    password='swd-secure-pass-2026',
    database='nagriksetu_swd'
)
cur = conn.cursor()

# Scheme mappings: (scheme_id, application_mode, form_title, form_desc, fields)
# Application modes:
# 'ONLINE_FORM' - Direct scheme-specific online application on NagrikSetu
# 'RENEWAL_FORM' - Renewal / continuation of existing benefit
# 'EXTERNAL_PORTAL' - Official verified portal redirection with verification checklist
# 'OFFLINE_ASSISTED' - Grama One / Bangalore One / Taluk SWD office assisted submission

SCHEME_FORM_SPECS = [
    # 1. Post-Matric Scholarship
    (
        1, "ONLINE_FORM",
        "Post-Matric Scholarship Application Form (SSP Integration)",
        "Scheme-specific application for post-matric course fee exemption, maintenance stipend, and hostel allowance.",
        [
            {"name": "student_admission_number", "label": "College / University Admission Number", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. UUCMS-2026-98124"},
            {"name": "institution_name", "label": "Current Educational Institution Name", "type": "text", "required": 1, "order": 2, "placeholder": "Government First Grade College / University"},
            {"name": "course_name", "label": "Course of Study", "type": "select", "required": 1, "order": 3, "options": ["B.A / B.Com / B.Sc", "B.E / B.Tech / B.Arch", "M.B.B.S / B.D.S / Nursing", "M.A / M.Com / M.Sc", "M.Tech / M.B.A / M.C.A", "Ph.D / Research Scholar", "Polytechnic / Diploma"]},
            {"name": "current_academic_year", "label": "Academic Year", "type": "select", "required": 1, "order": 4, "options": ["1st Year", "2nd Year", "3rd Year", "4th Year / Final Year"]},
            {"name": "previous_year_marks_percentage", "label": "Previous Academic Year Aggregate Marks (%)", "type": "number", "required": 1, "order": 5, "placeholder": "e.g. 78.5"},
            {"name": "hostel_stay_type", "label": "Hostel / Accommodation Status", "type": "select", "required": 1, "order": 6, "options": ["SWD Departmental Hostel Resident", "College Attached Hostel", "Day Scholar (Local Resident)"]},
            {"name": "ssp_student_id", "label": "State Scholarship Portal (SSP) ID (If previously registered)", "type": "text", "required": 0, "order": 7, "placeholder": "Optional SSP ID (e.g. 1920045612)"},
            {"name": "declaration_non_receipt", "label": "I hereby declare that I am not receiving any dual scholarship from any other public department.", "type": "checkbox", "required": 1, "order": 8, "options": ["Yes, I confirm"]}
        ]
    ),

    # 2. Disability Maintenance & Assistive Aid Grant
    (
        2, "ONLINE_FORM",
        "Disability Maintenance & Assistive Aid Grant Application",
        "Monthly maintenance support and grant for prosthetic, orthotic, and motorized tricycles for Divyangjan citizens.",
        [
            {"name": "udid_card_number", "label": "Unique Disability ID (UDID) / Sadarem Certificate No.", "type": "text", "required": 1, "order": 1, "placeholder": "KA-29-001-2023-XXXXXX"},
            {"name": "disability_type", "label": "Type of Benchmark Disability", "type": "select", "required": 1, "order": 2, "options": ["Locomotor Disability", "Visual Impairment / Blindness", "Hearing & Speech Impairment", "Intellectual Disability", "Multiple Disabilities / Cerebral Palsy"]},
            {"name": "disability_severity_percentage", "label": "Disability Severity Percentage (%)", "type": "number", "required": 1, "order": 3, "placeholder": "e.g. 60 (Minimum 40% required)"},
            {"name": "assistive_equipment_requested", "label": "Specific Assistive Equipment / Maintenance Required", "type": "select", "required": 1, "order": 4, "options": ["Monthly Maintenance Grant (Rs. 2,000/month)", "Motorized Battery Tricycle", "Digital Hearing Aid & Speech Synthesizer", "Wheelchair & Calipers", "Braille Learning Kit & Smart Cane"]},
            {"name": "guardian_or_caretaker_name", "label": "Nominated Caretaker / Guardian Name (If severe disability)", "type": "text", "required": 0, "order": 5, "placeholder": "Parent / Sibling / Legal Guardian Name"},
            {"name": "medical_board_authority", "label": "District Medical Board / Hospital Name", "type": "text", "required": 1, "order": 6, "placeholder": "e.g. Victoria Hospital, Bengaluru"}
        ]
    ),

    # 3. Sandhya Suraksha Senior Citizen Pension Scheme
    (
        3, "ONLINE_FORM",
        "Sandhya Suraksha Senior Citizen Pension Application",
        "Monthly direct benefit pension (Rs. 1,200/month) for elderly senior citizens aged 65 and above.",
        [
            {"name": "senior_age_proof_type", "label": "Proof of Age Document", "type": "select", "required": 1, "order": 1, "options": ["Aadhaar Card (Showing 65+ Years)", "Electoral Photo Identity Card (EPIC)", "School Leaving Certificate", "Medical Officer Age Assessment"]},
            {"name": "applicant_occupation_history", "label": "Primary Prior Occupation / Livelihood", "type": "select", "required": 1, "order": 2, "options": ["Agricultural Labourer", "Weaver / Handloom Worker", "Construction / Unorganized Worker", "Artisan / Potter / Carpenter", "Fisherfolk / Domestic Worker", "Destitute / No Prior Fixed Occupation"]},
            {"name": "household_joint_income", "label": "Total Combined Household Annual Income (Rs.)", "type": "number", "required": 1, "order": 3, "placeholder": "Must not exceed Rs. 32,000 for rural or Rs. 50,000 for urban"},
            {"name": "existing_pension_status", "label": "Are you currently receiving any other pension (EPFO/Central/State)?", "type": "radio", "required": 1, "order": 4, "options": ["No (Eligible)", "Yes (Ineligible)"]},
            {"name": "bank_passbook_branch", "label": "Bank Name and Branch Location", "type": "text", "required": 1, "order": 5, "placeholder": "State Bank of India, Jayanagar Branch"}
        ]
    ),

    # 4. Financial Incentive Scheme for Inter-Caste Marriages
    (
        4, "ONLINE_FORM",
        "Inter-Caste Marriage Incentive Grant Application",
        "One-time incentive grant (Rs. 2.50 to 3.00 Lakhs) for registered marriages between SC/ST and other communities.",
        [
            {"name": "spouse_full_name", "label": "Spouse's Full Legal Name", "type": "text", "required": 1, "order": 1, "placeholder": "Full legal name as per marriage certificate"},
            {"name": "spouse_social_category", "label": "Spouse's Social / Caste Category", "type": "select", "required": 1, "order": 2, "options": ["Scheduled Caste (SC)", "Scheduled Tribe (ST)", "General / Other Backward Community"]},
            {"name": "marriage_registration_number", "label": "Sub-Registrar Marriage Certificate Number", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. SRO-BLR-MR-2025-4512"},
            {"name": "marriage_date", "label": "Date of Marriage Registration", "type": "date", "required": 1, "order": 4},
            {"name": "sub_registrar_office_location", "label": "Sub-Registrar Jurisdiction Office Location", "type": "text", "required": 1, "order": 5, "placeholder": "Sub-Registrar Office, Shivajinagar, Bengaluru"},
            {"name": "joint_bank_account_number", "label": "Aadhaar-Linked Joint Bank Account Number", "type": "text", "required": 1, "order": 6, "placeholder": "Joint account held by both spouses"},
            {"name": "joint_bank_ifsc", "label": "Joint Bank IFSC Code", "type": "text", "required": 1, "order": 7, "placeholder": "SBIN0001234"}
        ]
    ),

    # 5. Gruha Lakshmi Scheme
    (
        5, "ONLINE_FORM",
        "Gruha Lakshmi Scheme Registration Dossier",
        "Universal monthly financial empowerment assistance of Rs. 2,000 for female heads of household.",
        [
            {"name": "ration_card_number", "label": "BPL / AAY / APL Ration Card (RC) Number", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. 100984512398"},
            {"name": "ration_card_type", "label": "Ration Card Type", "type": "select", "required": 1, "order": 2, "options": ["Antyodaya Anna Yojana (AAY)", "Below Poverty Line (BPL / PHH)", "Above Poverty Line (APL / NPHH)"]},
            {"name": "female_head_name_on_rc", "label": "Name of Female Head of Family (as specified on RC)", "type": "text", "required": 1, "order": 3, "placeholder": "Name matching family card"},
            {"name": "husband_aadhaar_number", "label": "Husband's Aadhaar Number (if married)", "type": "text", "required": 0, "order": 4, "placeholder": "12-digit Aadhaar number"},
            {"name": "income_tax_payer_declaration", "label": "Do you or your spouse pay Income Tax (IT) or file GST returns?", "type": "radio", "required": 1, "order": 5, "options": ["No (Eligible)", "Yes (Ineligible)"]},
            {"name": "preferred_disbursement_mode", "label": "Preferred DBT Payment Method", "type": "select", "required": 1, "order": 6, "options": ["Aadhaar-Enabled Payment System (AePS Direct NPCI)", "Direct Bank NEFT to Seeded Account"]}
        ]
    ),

    # 6. Gruha Jyothi Scheme
    (
        6, "ONLINE_FORM",
        "Gruha Jyothi Free Electricity Scheme Enrolment",
        "Up to 200 units of free domestic electricity per month for registered residential households.",
        [
            {"name": "escom_name", "label": "Electricity Supply Company (ESCOM)", "type": "select", "required": 1, "order": 1, "options": ["BESCOM (Bengaluru Electricity Supply Company)", "MESCOM (Mangalore Electricity Supply Company)", "HESCOM (Hubli Electricity Supply Company)", "GESCOM (Gulbarga Electricity Supply Company)", "CESC (Chamundeshwari Electricity Supply Corporation)"]},
            {"name": "consumer_account_id", "label": "Consumer Account ID / Account ID on Electricity Bill", "type": "text", "required": 1, "order": 2, "placeholder": "10-digit Account ID printed on utility bill"},
            {"name": "meter_number", "label": "Physical Electricity Meter Serial Number", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. BESC-M-991244"},
            {"name": "residence_tenure_type", "label": "Premises Occupancy Status", "type": "select", "required": 1, "order": 4, "options": ["Owner Resident", "Tenant / Rental Agreement Holder"]},
            {"name": "average_monthly_consumption_units", "label": "Average Monthly Consumption (Units / kWh)", "type": "number", "required": 1, "order": 5, "placeholder": "Average units consumed over past 12 months (e.g. 110)"}
        ]
    ),

    # 7. Shakti Free Bus Travel Scheme
    (
        7, "ONLINE_FORM",
        "Apply for Welfare Scheme: Shakti Free Bus Travel Scheme",
        "Zero-fare public bus transport across Karnataka for all domicile women and transgender citizens.",
        [
            {"name": "applicant_full_name", "label": "Applicant Full Name", "type": "text", "required": 1, "order": 1, "placeholder": "Full legal name as per government ID"},
            {"name": "mobile_phone_number", "label": "Mobile Phone Number", "type": "mobile", "required": 1, "order": 2, "placeholder": "10-digit mobile phone number"},
            {"name": "permanent_residence_district", "label": "Permanent Residence District", "type": "select", "required": 1, "order": 3, "options": ["Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Dharwad", "Belagavi", "Kalaburagi", "Dakshina Kannada", "Ballari", "Tumakuru", "Shivamogga", "Hassan", "Vijayapura", "Raichur", "Udupi", "Other Karnataka District"]},
            {"name": "social_category", "label": "Social Category", "type": "select", "required": 1, "order": 4, "options": ["SC", "ST", "OBC (Cat-1)", "OBC (2A)", "OBC (2B)", "OBC (3A)", "OBC (3B)", "General"]},
            {"name": "aadhaar_seeded_bank_account", "label": "Aadhaar-Seeded Bank Account Number", "type": "text", "required": 1, "order": 5, "placeholder": "Account number for smart-card biometric verification"},
            {"name": "bank_ifsc_code", "label": "Bank IFSC Code", "type": "text", "required": 1, "order": 6, "placeholder": "11-character bank branch IFSC code"},
            {"name": "declaration_consent", "label": "I declare that I am a bonafide resident of Karnataka and all particulars submitted are truthful.", "type": "checkbox", "required": 1, "order": 7, "options": ["Yes, I accept"]}
        ]
    ),

    # 8. Anna Bhagya Scheme
    (
        8, "ONLINE_FORM",
        "Anna Bhagya Additional Food Grain / Cash-in-Lieu Subsidy Enrolment",
        "Monthly 5 kg additional rice per person or cash equivalent of Rs. 170 per person per month via Direct Benefit Transfer.",
        [
            {"name": "ration_card_number", "label": "Ration Card (RC) Number", "type": "text", "required": 1, "order": 1, "placeholder": "BPL / Antyodaya RC number"},
            {"name": "total_family_members", "label": "Number of Listed Family Members on Card", "type": "number", "required": 1, "order": 2, "placeholder": "e.g. 4"},
            {"name": "fair_price_shop_number", "label": "Jurisdictional Fair Price Shop (FPS) Number", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. FPS-BLR-041"},
            {"name": "dbt_active_bank_account", "label": "Aadhaar NPCI-Mapped Bank Account Number (Head of Family)", "type": "text", "required": 1, "order": 4, "placeholder": "Account mapped with NPCI mapper"}
        ]
    ),

    # 9. Yuva Nidhi Scheme
    (
        9, "ONLINE_FORM",
        "Yuva Nidhi Unemployment Assistance & Skill Training Enrolment",
        "Monthly stipend of Rs. 3,000 for graduates and Rs. 1,500 for diploma holders unemployed for 6 months after passing.",
        [
            {"name": "degree_type", "label": "Educational Qualification Completed", "type": "select", "required": 1, "order": 1, "options": ["Bachelor's Degree (General - B.A/B.Sc/B.Com)", "Professional Degree (B.E/B.Tech/MBBS)", "Post Graduate Degree (M.A/M.Com/M.Sc/MBA)", "State Board Polytechnic Diploma"]},
            {"name": "graduation_passing_year", "label": "Passing Out Year", "type": "select", "required": 1, "order": 2, "options": ["2023", "2024", "2025", "2026"]},
            {"name": "university_registration_number", "label": "Degree / Diploma Roll / Registration Number", "type": "text", "required": 1, "order": 3, "placeholder": "Registration / Exam Roll Number"},
            {"name": "months_unemployed", "label": "Duration of Unemployment Post Graduation (Months)", "type": "number", "required": 1, "order": 4, "placeholder": "Minimum 6 months required (e.g. 7)"},
            {"name": "epfo_esic_declaration", "label": "Are you registered with EPFO or receiving income from government/private job?", "type": "radio", "required": 1, "order": 5, "options": ["No, Unemployed (Eligible)", "Yes, Employed (Ineligible)"]},
            {"name": "skill_training_preference", "label": "Preferred Skill Enhancement Training Domain", "type": "select", "required": 1, "order": 6, "options": ["IT & Software Development", "AI & Data Science", "Banking & Financial Services", "Advanced Manufacturing & CNC", "Healthcare & Paramedical", "Logistics & Supply Chain"]}
        ]
    ),

    # 10. Udyogini Scheme
    (
        10, "ONLINE_FORM",
        "Udyogini Women Entrepreneurship Subsidized Loan Application",
        "Subsidized business capital loans up to Rs. 3,00,000 with up to 30% government capital subsidy for women.",
        [
            {"name": "proposed_business_activity", "label": "Proposed Trade / Micro-Enterprise Activity", "type": "select", "required": 1, "order": 1, "options": ["Tailoring & Garment Manufacturing", "Bakery, Catering & Food Processing", "Beauty Parlour & Wellness Salon", "Dairy, Poultry & Livestock Rearing", "Retail Grocery / General Store", "Handicrafts & Artisanal Goods"]},
            {"name": "total_project_cost", "label": "Estimated Total Capital Cost (Rs.)", "type": "number", "required": 1, "order": 2, "placeholder": "Up to Rs. 3,00,000"},
            {"name": "subsidy_category_claim", "label": "Target Social Category for Subsidy %", "type": "select", "required": 1, "order": 3, "options": ["SC / ST (30% Capital Subsidy - Max Rs. 90,000)", "General / Special Category Women (20% Subsidy - Max Rs. 60,000)"]},
            {"name": "financing_bank_preference", "label": "Preferred Financing Commercial / Grameena Bank", "type": "text", "required": 1, "order": 4, "placeholder": "Karnataka Gramin Bank / Canara Bank Branch"}
        ]
    ),

    # 11. Bhagyalakshmi Scheme
    (
        11, "ONLINE_FORM",
        "Bhagyalakshmi Girl Child Bond & Insurance Enrolment",
        "Health insurance coverage and term financial maturity bond of Rs. 1,00,000 for girl children born in BPL families.",
        [
            {"name": "child_birth_certificate_number", "label": "Girl Child Birth Registration Certificate Number", "type": "text", "required": 1, "order": 1, "placeholder": "Municipal / Gram Panchayat Birth Reg No."},
            {"name": "child_date_of_birth", "label": "Child Date of Birth", "type": "date", "required": 1, "order": 2},
            {"name": "birth_order", "label": "Child Birth Order in Family", "type": "select", "required": 1, "order": 3, "options": ["First Girl Child", "Second Girl Child (Max 2 girl children per family)"]},
            {"name": "mother_aadhaar_number", "label": "Mother's Aadhaar Number", "type": "text", "required": 1, "order": 4, "placeholder": "12-digit Aadhaar number"},
            {"name": "sukanya_samriddhi_or_lic_account", "label": "Postal Sukanya Samriddhi / Departmental LIC Bond Number", "type": "text", "required": 0, "order": 5, "placeholder": "Existing Account No. if registered"}
        ]
    ),

    # 12. Matru Poorna Scheme
    (
        12, "ONLINE_FORM",
        "Matru Poorna Anganwadi Hot-Cooked Nutrition Meal Enrolment",
        "One wholesome nutritious hot-cooked meal and calcium/iron supplements every day for pregnant and lactating mothers.",
        [
            {"name": "mcts_or_rch_id", "label": "Mother and Child Tracking System (MCTS) / RCH ID", "type": "text", "required": 1, "order": 1, "placeholder": "12-digit Reproductive & Child Health ID"},
            {"name": "anganwadi_centre_code", "label": "Local Anganwadi Centre (AWC) Name / Code", "type": "text", "required": 1, "order": 2, "placeholder": "e.g. AWC-KRPURAM-014"},
            {"name": "current_status", "label": "Beneficiary Status", "type": "select", "required": 1, "order": 3, "options": ["Pregnant Mother (Antenatal)", "Lactating Mother (Postnatal - Up to 6 months)"]},
            {"name": "expected_date_of_delivery", "label": "Expected Delivery Date (EDD) / Actual Delivery Date", "type": "date", "required": 1, "order": 4}
        ]
    ),

    # 13. Thayi Bhagya & Prasoothi Araike Scheme
    (
        13, "ONLINE_FORM",
        "Thayi Bhagya Institutional Delivery Cash Assistance Form",
        "Cash assistance of Rs. 6,000 in tranches for safe institutional delivery in government hospitals and accredited private health centres.",
        [
            {"name": "thayi_card_number", "label": "Thayi Card (Mother Card) Number", "type": "text", "required": 1, "order": 1, "placeholder": "Mother & Child Protection Card Registration No."},
            {"name": "hospital_type_of_delivery", "label": "Institutional Delivery Facility", "type": "select", "required": 1, "order": 2, "options": ["Government Taluk / District Hospital", "Community Health Centre (CHC) / PHC", "Accredited Private Maternity Nursing Home"]},
            {"name": "hospital_name", "label": "Healthcare Institution Name", "type": "text", "required": 1, "order": 3, "placeholder": "General Hospital, District Center"},
            {"name": "asha_worker_name", "label": "Attending ASHA Worker Name", "type": "text", "required": 0, "order": 4, "placeholder": "Local ASHA facilitator name"}
        ]
    ),

    # 14. Madilu Kit Scheme
    (
        14, "ONLINE_FORM",
        "Madilu Post-Delivery Mother & Newborn Care Kit Application",
        "Post-delivery care package containing 19 essential hygiene, clothing, and care items for mother and newborn.",
        [
            {"name": "delivery_discharge_certificate_no", "label": "Institutional Delivery Discharge Summary Number", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. DIS-GH-2026-8912"},
            {"name": "delivery_date", "label": "Date of Child Delivery", "type": "date", "required": 1, "order": 2},
            {"name": "delivering_hospital_name", "label": "Delivering Government Facility Name", "type": "text", "required": 1, "order": 3, "placeholder": "Maternity Hospital / Primary Health Centre"},
            {"name": "kit_dispatch_preference", "label": "Collection / Delivery Preference", "type": "select", "required": 1, "order": 4, "options": ["Direct Handover at Hospital Discharge", "Collection via Jurisdictional Anganwadi Centre"]}
        ]
    ),

    # 15. Santhwana Scheme
    (
        15, "ONLINE_FORM",
        "Santhwana Women in Distress Relief & Legal Aid Application",
        "Immediate emergency financial relief (up to Rs. 50,000), trauma counseling, shelter, and legal support for women victims of violence.",
        [
            {"name": "incident_category", "label": "Nature of Assistance Required", "type": "select", "required": 1, "order": 1, "options": ["Domestic Violence / Marital Cruelty", "Dowry Harassment", "Trafficking & Exploitation", "Sexual Assault / Rape Victim Compensation", "Desertion / Destitution Relief"]},
            {"name": "fir_or_complaint_number", "label": "Police FIR / Station Diary / Protection Officer Report No.", "type": "text", "required": 0, "order": 2, "placeholder": "Police station and crime number if registered"},
            {"name": "immediate_shelter_needed", "label": "Immediate Shelter & Protection Home Needed?", "type": "radio", "required": 1, "order": 3, "options": ["Yes, emergency transit shelter needed", "No, legal & financial relief only"]},
            {"name": "case_narrative_summary", "label": "Confidential Summary of Incident & Relief Needed", "type": "textarea", "required": 1, "order": 4, "placeholder": "Briefly state the circumstances requiring administrative intervention"}
        ]
    ),

    # 16. Dhanashree & Chetana Scheme
    (
        16, "ONLINE_FORM",
        "Dhanashree & Chetana Economic Rehabilitation Application",
        "Subsidized micro-credit assistance (Rs. 50,000 grant + loan) for rehabilitation of HIV-positive women, commercial sex workers, and transgender individuals.",
        [
            {"name": "rehabilitation_stream", "label": "Target Assistance Stream", "type": "select", "required": 1, "order": 1, "options": ["Dhanashree (Rehabilitation for HIV-affected Women)", "Chetana (Economic Exit & Livelihood for Sex Workers)", "Transgender Livelihood Self-Employment Grant"]},
            {"name": "self_employment_plan", "label": "Chosen Micro-Enterprise Skill Activity", "type": "select", "required": 1, "order": 2, "options": ["Apparel & Bag Stitching Unit", "Tea Stall / Fast Food Cart", "Vegetable / Fruit Retail Cart", "Home Supplies / Cleaning Products Manufacturing", "Petty Shop / Stationery Counter"]},
            {"name": "counselor_or_ngo_reference", "label": "Supporting NGO / District AIDS Prevention Society (DAPCU) Reference", "type": "text", "required": 0, "order": 3, "placeholder": "Name of assisting case officer or counselor"}
        ]
    ),

    # 17. Chief Minister Raitha Vidya Nidhi
    (
        17, "ONLINE_FORM",
        "Chief Minister Raitha Vidya Nidhi Student Scholarship Form",
        "Annual scholarship of Rs. 2,000 to Rs. 11,000 for children of land-owning and tenant agricultural farmers.",
        [
            {"name": "farmer_parent_fid", "label": "Farmer Registration ID (FRUITS FID Number)", "type": "text", "required": 1, "order": 1, "placeholder": "10-digit FRUITS Portal Farmer ID (e.g. 1023456789)"},
            {"name": "rtc_pahani_survey_number", "label": "Land Survey Number / RTC Pahani Number", "type": "text", "required": 1, "order": 2, "placeholder": "Survey No. matching revenue records"},
            {"name": "student_admission_number", "label": "Student College Roll Number / UUCMS ID", "type": "text", "required": 1, "order": 3, "placeholder": "College admission registration number"},
            {"name": "course_tier", "label": "Course Category Enrolled", "type": "select", "required": 1, "order": 4, "options": ["PUC / ITI / Diploma (Rs. 2,500 - 3,000/yr)", "General Degree - B.A/B.Sc/B.Com (Rs. 5,000 - 5,500/yr)", "Post Graduate Courses (Rs. 10,000/yr)", "Professional Degrees - MBBS/B.E/B.Tech (Rs. 11,000/yr)"]}
        ]
    ),

    # 18. Ganga Kalyana Scheme
    (
        18, "ONLINE_FORM",
        "Ganga Kalyana Agricultural Irrigation Borewell Application",
        "Drilling of borewells, pump set installation, and electrification for small/marginal farmers from SC/ST and OBC communities.",
        [
            {"name": "fruits_farmer_fid", "label": "Farmer Registration ID (FID)", "type": "text", "required": 1, "order": 1, "placeholder": "FRUITS Portal ID"},
            {"name": "land_holding_acres", "label": "Total Combined Land Holding (Acres)", "type": "number", "required": 1, "order": 2, "placeholder": "Must be between 1.20 to 5.00 acres"},
            {"name": "land_survey_numbers", "label": "Revenue Land Survey / Hissa Numbers", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. Sy. No. 45/2B, Kasaba Hobli"},
            {"name": "village_name", "label": "Village and Gram Panchayat", "type": "text", "required": 1, "order": 4, "placeholder": "e.g. Harohalli Village"},
            {"name": "water_source_assessment", "label": "Hydrogeological Feasibility / Ground Water Zone Status", "type": "select", "required": 1, "order": 5, "options": ["Safe Groundwater Assessment Zone", "Semi-Critical Zone", "Borewell Drilling with Micro-Irrigation Network"]},
            {"name": "escom_subdivision", "label": "Jurisdictional ESCOM Sub-Division for Power Connection", "type": "text", "required": 1, "order": 6, "placeholder": "e.g. BESCOM Doddaballapura Sub-Division"}
        ]
    ),

    # 19. Krishi Bhagya Scheme
    (
        19, "ONLINE_FORM",
        "Krishi Bhagya Rainwater Harvesting Farm Pond & Polyhouse Subsidy",
        "Subsidy up to 80-90% for constructing farm ponds (Krishi Honda), polythene lining, diesel pump sets, and shade net polyhouses.",
        [
            {"name": "agro_climatic_zone", "label": "Rainfed Dryland Agricultural Zone", "type": "select", "required": 1, "order": 1, "options": ["Northern Dry Zone", "Central Dry Zone", "Southern Dry Zone", "Eastern Dry Zone", "Transition Zone"]},
            {"name": "infrastructure_component_requested", "label": "Irrigation Package Component Requested", "type": "select", "required": 1, "order": 2, "options": ["Farm Pond (Krishi Honda) with Polythene Lining", "Diesel Pump Set & Field Delivery Piping", "Drip / Sprinkler Micro-Irrigation Package", "Shade Net Polyhouse (Protected Cultivation)"]},
            {"name": "dryland_holding_acres", "label": "Dryland Farming Area (Acres)", "type": "number", "required": 1, "order": 3, "placeholder": "e.g. 3.5"},
            {"name": "fruits_id", "label": "FRUITS Farmer Registration Number", "type": "text", "required": 1, "order": 4, "placeholder": "10-digit FID"}
        ]
    ),

    # 20. Micro-Irrigation Scheme
    (
        20, "ONLINE_FORM",
        "Micro-Irrigation (Drip & Sprinkler) 90% Subsidy Application",
        "Up to 90% financial assistance for installing modern drip and sprinkler irrigation networks.",
        [
            {"name": "crop_type", "label": "Principal Crop Cultivated", "type": "select", "required": 1, "order": 1, "options": ["Horticulture Fruits & Plantation (Areca/Coconut/Mango)", "Vegetables & Commercial Floriculture", "Sugarcane / Maize / Cotton", "Pulses & Oilseeds"]},
            {"name": "irrigation_technology_type", "label": "Selected Micro-Irrigation System", "type": "select", "required": 1, "order": 2, "options": ["Inline Drip Irrigation System", "Online Drip Irrigation System", "Portable Sprinkler Network", "Micro-Sprinkler / Raingun"]},
            {"name": "existing_water_source", "label": "Available Perennial Water Source", "type": "select", "required": 1, "order": 3, "options": ["Existing Borewell with Electric Pump", "Farm Pond / Open Irrigation Well", "Canal Lift Irrigation Point"]},
            {"name": "fruits_farmer_fid", "label": "FRUITS Farmer ID", "type": "text", "required": 1, "order": 4, "placeholder": "FRUITS Portal Registration Number"}
        ]
    ),

    # 21. Krushi Aranya Protsaha Yojane (KAPY)
    (
        21, "ONLINE_FORM",
        "Krushi Aranya Protsaha Yojane Agro-Forestry Seedling Subsidy",
        "Incentive grant of Rs. 100 per surviving tree seedling planted on farmlands and bunds over 3 years.",
        [
            {"name": "seedling_species_requested", "label": "Preferred Tree Sapling Varieties", "type": "select", "required": 1, "order": 1, "options": ["Teak, Rosewood & Mahogany", "Sandalwood & Red Sanders", "Silver Oak & Casuarina", "Fruit Bearing (Jackfruit, Tamarind, Jamun, Amla)"]},
            {"name": "number_of_seedlings_to_plant", "label": "Total Number of Seedlings Planned", "type": "number", "required": 1, "order": 2, "placeholder": "e.g. 200 (Max 400 per acre)"},
            {"name": "plantation_model", "label": "Plantation Method", "type": "select", "required": 1, "order": 3, "options": ["Field Bund Agroforestry", "Block Plantation on Fallow Land", "Intercropping with Agricultural Crops"]},
            {"name": "range_forest_office", "label": "Nearest Range Forest Office (RFO) Jurisdiction", "type": "text", "required": 1, "order": 4, "placeholder": "e.g. RFO Devanahalli Range"}
        ]
    ),

    # 22. Yeshasvini Cooperative Health Insurance Scheme
    (
        22, "ONLINE_FORM",
        "Yeshasvini Cooperative Health Card Enrolment Application",
        "Cashless surgical and inpatient medical coverage up to Rs. 5,00,000 per family per year in network hospitals.",
        [
            {"name": "cooperative_society_name", "label": "Primary Agriculture Credit Cooperative Society (PACS) / Milk Union Name", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. Harohalli VSSN / KMF Dairy Cooperative"},
            {"name": "society_membership_number", "label": "Cooperative Society Membership Share Number", "type": "text", "required": 1, "order": 2, "placeholder": "Member Ledger No. (e.g. MEM-2022-412)"},
            {"name": "family_head_designation", "label": "Family Type", "type": "select", "required": 1, "order": 3, "options": ["Rural Cooperative Family (Premium Rs. 500/member)", "Urban Cooperative Family (Premium Rs. 1,000/member)"]},
            {"name": "number_of_dependent_beneficiaries", "label": "Number of Enrolled Dependent Family Members", "type": "number", "required": 1, "order": 4, "placeholder": "e.g. 4"}
        ]
    ),

    # 23. Raitha Siri Scheme
    (
        23, "ONLINE_FORM",
        "Raitha Siri Millet Farmers Direct Cash Incentive Application",
        "Direct DBT incentive of Rs. 10,000 per hectare for farmers cultivating Siri Dhanya (nutri-cereals / millets).",
        [
            {"name": "millet_variety_cultivated", "label": "Siri Dhanya Millet Type", "type": "select", "required": 1, "order": 1, "options": ["Ragi (Finger Millet)", "Jowar (Sorghum)", "Navane (Foxtail Millet)", "Same (Little Millet)", "Haraka (Kodo Millet)", "Oodalu (Barnyard Millet)", "Baragu (Proso Millet)"]},
            {"name": "millet_cultivation_area_hectares", "label": "Cultivated Area under Millets (Hectares)", "type": "number", "required": 1, "order": 2, "placeholder": "e.g. 1.50 (Max 2 hectares eligible)"},
            {"name": "crop_survey_verification_code", "label": "Karnataka Digital Crop Survey Farmer Verification ID", "type": "text", "required": 1, "order": 3, "placeholder": "Crop Survey App GPS Geo-referenced ID"},
            {"name": "fruits_farmer_fid", "label": "FRUITS ID Number", "type": "text", "required": 1, "order": 4, "placeholder": "10-digit FID"}
        ]
    ),

    # 24. Arivu Education Loan Scheme
    (
        24, "ONLINE_FORM",
        "Arivu Minority Education Loan Scheme Application",
        "Low-interest educational loans up to Rs. 5,00,000 per year at 2% interest for minority students pursuing higher professional courses.",
        [
            {"name": "cet_neet_roll_number", "label": "KEA CET / NEET / PGCET Hall Ticket / Rank Number", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. CET-2025-BLR-8924"},
            {"name": "allotted_college_name", "label": "KEA Allotted Institution Name", "type": "text", "required": 1, "order": 2, "placeholder": "Medical / Engineering / Law College"},
            {"name": "annual_course_tuition_fee", "label": "Annual Approved Tuition Fee Amount (Rs.)", "type": "number", "required": 1, "order": 3, "placeholder": "e.g. 150000"},
            {"name": "minority_community_type", "label": "Religious Minority Classification", "type": "select", "required": 1, "order": 4, "options": ["Muslim", "Christian", "Jain", "Buddhist", "Sikh", "Parsi"]}
        ]
    ),

    # 25. Vidyasiri Food & Accommodation Stipend
    (
        25, "ONLINE_FORM",
        "Vidyasiri Food & Accommodation Stipend Application",
        "Monthly stipend of Rs. 1,500 for 10 months for backward classes students studying post-matric courses without departmental hostel accommodation.",
        [
            {"name": "hostel_non_availability_certificate", "label": "Taluk BCM Office Hostel Non-Availability Number", "type": "text", "required": 1, "order": 1, "placeholder": "Certificate No. confirming no vacant seat"},
            {"name": "private_stay_rental_address", "label": "Current Rented Room / Paying Guest Address", "type": "textarea", "required": 1, "order": 2, "placeholder": "Address of current PG or rented room near college"},
            {"name": "distance_from_home_to_college_km", "label": "Distance from Native Town to College (KM)", "type": "number", "required": 1, "order": 3, "placeholder": "Minimum 5 km (e.g. 35)"},
            {"name": "college_attendance_percentage", "label": "Current Semester Attendance (%)", "type": "number", "required": 1, "order": 4, "placeholder": "Must be at least 75%"}
        ]
    ),

    # 26. Prabuddha & Dr. B.R. Ambedkar Overseas Scholarships
    (
        26, "ONLINE_FORM",
        "Prabuddha Overseas Education Scholarship Application",
        "Full financial sponsorship (up to Rs. 20 Lakhs/year) for SC/ST students accepted into top-ranked global universities abroad.",
        [
            {"name": "foreign_university_name", "label": "Admitted Global University Name", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. Imperial College London / Carnegie Mellon University"},
            {"name": "country_of_study", "label": "Destination Country", "type": "select", "required": 1, "order": 2, "options": ["United Kingdom (UK)", "United States of America (USA)", "Canada", "Germany", "Australia", "Singapore / Other Global Hub"]},
            {"name": "degree_level", "label": "Level of Higher Education", "type": "select", "required": 1, "order": 3, "options": ["Master's Degree (Postgraduate)", "Ph.D. / Post-Doctoral Fellowship"]},
            {"name": "qs_or_times_world_rank", "label": "University Global QS / Times World Ranking", "type": "number", "required": 1, "order": 4, "placeholder": "Must be within top 500 universities (e.g. 42)"},
            {"name": "passport_number", "label": "Valid Indian Passport Number", "type": "text", "required": 1, "order": 5, "placeholder": "Passport Booklet Number (e.g. Z-891244)"}
        ]
    ),

    # 27. ELEVATE & ELEVATE NxT Startup Grants
    (
        27, "ONLINE_FORM",
        "ELEVATE Tech Startup Idea Grant Application",
        "Seed funding grants up to Rs. 50 Lakhs for early-stage technology innovations and SC/ST/Women-led startups.",
        [
            {"name": "startup_entity_name", "label": "Registered Startup / Enterprise Name", "type": "text", "required": 1, "order": 1, "placeholder": "e.g. AgroTech Innovations Pvt Ltd"},
            {"name": "dpiit_or_startup_karnataka_id", "label": "DPIIT Recognition Number / Startup Karnataka Reg ID", "type": "text", "required": 1, "order": 2, "placeholder": "DIPP-XXXXX"},
            {"name": "innovation_domain", "label": "Deep-Tech / Innovation Vertical", "type": "select", "required": 1, "order": 3, "options": ["Artificial Intelligence & IoT", "Agritech & Rural Technology", "Medtech & Healthcare Devices", "Clean Energy & EV Mobility", "Edutech & Social Impact Tech"]},
            {"name": "patent_or_prototype_status", "label": "Product Stage", "type": "select", "required": 1, "order": 4, "options": ["Working Prototype (TRL 4-5)", "Market Validation / Early Traction (TRL 6-7)", "Commercial Scaling Stage"]}
        ]
    ),

    # 28. Rajiv Gandhi Entrepreneurship Program
    (
        28, "ONLINE_FORM",
        "Rajiv Gandhi Entrepreneurship Incubation Fellow Application",
        "Monthly stipend of Rs. 25,000 for 12 months plus incubation support for science and engineering graduates.",
        [
            {"name": "engineering_college_name", "label": "College Where Degree Completed", "type": "text", "required": 1, "order": 1, "placeholder": "VTU Affiliated / Autonomous College"},
            {"name": "technical_specialization", "label": "Engineering Branch / Domain", "type": "select", "required": 1, "order": 2, "options": ["Computer Science & IT", "Electronics & Communication", "Mechanical & Mechatronics", "Biotechnology & Chemical Engg", "Civil & Environmental Engg"]},
            {"name": "proposed_venture_concept", "label": "High-Level Product / Venture Abstract", "type": "textarea", "required": 1, "order": 3, "placeholder": "Describe the innovative technological solution you plan to build"},
            {"name": "host_incubation_centre", "label": "Preferred K-tech Incubation Center", "type": "select", "required": 1, "order": 4, "options": ["C-CAMP Bengaluru", "K-Tech CoE Kalaburagi", "STEP Mangaluru", "IISC / C-DOT Incubation Hub"]}
        ]
    ),

    # 29. Karnataka Construction Workers (KBOCWWB) Schemes
    (
        29, "ONLINE_FORM",
        "Building & Other Construction Workers (KBOCWWB) Welfare Claim",
        "Tools kit subsidy, marriage assistance (Rs. 50,000), educational scholarships, and accidental insurance for construction workers.",
        [
            {"name": "kbocwwb_smart_card_no", "label": "KBOCWWB Construction Worker Labour Smart Card Number", "type": "text", "required": 1, "order": 1, "placeholder": "KA-BOCW-XXXX-XXXXXX"},
            {"name": "trade_occupation", "label": "Construction Trade Skill", "type": "select", "required": 1, "order": 2, "options": ["Mason (Goundi)", "Carpenter (Badagi)", "Bar Bender / Steel Fixer", "Plumber & Pipe Fitter", "Electrician & Wireman", "Painter & Tile Layer", "Earthwork Excavator / Labourer"]},
            {"name": "specific_welfare_benefit_claimed", "label": "Benefit Claimed under Board", "type": "select", "required": 1, "order": 3, "options": ["Karmika Tool Kit Grant (Rs. 10,000 value)", "Karmika Kalyana Marriage Incentive (Rs. 50,000)", "Maternity Assistance (Rs. 50,000)", "Worker Children Education Aid (Rs. 6,000 - 25,000)"]},
            {"name": "employer_contractor_details", "label": "Principal Contractor / Construction Site Details", "type": "text", "required": 1, "order": 4, "placeholder": "Contractor name and site location"}
        ]
    ),

    # 30. Karnataka State Gig Workers Insurance Scheme
    (
        30, "ONLINE_FORM",
        "Karnataka Platform-Based Gig Workers Accident Insurance Enrolment",
        "Rs. 4 Lakhs life and accident insurance cover (Rs. 2 Lakh accidental death + Rs. 2 Lakh permanent disability) for gig delivery workers.",
        [
            {"name": "gig_platform_aggregator", "label": "Platform / Delivery Aggregator Entity", "type": "select", "required": 1, "order": 1, "options": ["Swiggy", "Zomato", "Blinkit / Zepto / Instamart", "Ola / Uber / Rapido", "Amazon / Flipkart Delivery", "Porter / Dunzo / Urban Company"]},
            {"name": "partner_delivery_id", "label": "Platform Delivery Partner / Rider ID", "type": "text", "required": 1, "order": 2, "placeholder": "Rider Partner ID on delivery application"},
            {"name": "driving_licence_number", "label": "Valid Two-Wheeler / Commercial Driving Licence (DL)", "type": "text", "required": 1, "order": 3, "placeholder": "DL Number (e.g. KA-01-2022-XXXXXXX)"},
            {"name": "nominee_name", "label": "Nominee Full Legal Name", "type": "text", "required": 1, "order": 4, "placeholder": "Spouse / Parent / Offspring"},
            {"name": "nominee_relation", "label": "Relationship with Nominee", "type": "select", "required": 1, "order": 5, "options": ["Spouse", "Father", "Mother", "Son / Daughter"]}
        ]
    ),

    # 31. Ambedkar Karmika Sahaya Hastha
    (
        31, "ONLINE_FORM",
        "Ambedkar Karmika Sahaya Hastha Unorganized Workers Smart Card",
        "Social security registry and welfare benefits kit distribution for unorganized urban domestic, roadside, and informal labourers.",
        [
            {"name": "eshram_uan_number", "label": "National e-Shram Universal Account Number (UAN)", "type": "text", "required": 1, "order": 1, "placeholder": "12-digit UAN on e-Shram Card"},
            {"name": "informal_trade_type", "label": "Unorganized Sector Category", "type": "select", "required": 1, "order": 2, "options": ["Domestic Maid / Cleaner", "Street Vendor / Hawker", "Auto Rickshaw / Taxi Driver", "Cobbler & Leather Worker", "Dhobi / Laundry Worker", "Waste Picker & Sanitation Worker"]},
            {"name": "workplace_city_taluk", "label": "Primary City / Town of Work", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. Bengaluru Urban / Mysuru"}
        ]
    ),

    # 32. Swavalambi Sarathi Scheme
    (
        32, "ONLINE_FORM",
        "Swavalambi Sarathi Commercial Vehicle 50-75% Subsidy Application",
        "Up to 75% capital subsidy (up to Rs. 4,00,000) for purchase of commercial goods/passenger vehicles by youth from SC/ST and backward classes.",
        [
            {"name": "vehicle_type_chosen", "label": "Proposed Commercial Vehicle Type", "type": "select", "required": 1, "order": 1, "options": ["Four-Wheeler Light Commercial Vehicle (LCV / Pick-up)", "Auto Rickshaw (Passenger / E-Rickshaw)", "Tourist Taxi / Passenger Cab", "Delivery Van / Goods Mini-Truck"]},
            {"name": "commercial_badge_dl_number", "label": "Valid Commercial Transport Driving Licence Number", "type": "text", "required": 1, "order": 2, "placeholder": "Transport licence number"},
            {"name": "dealer_quotation_cost", "label": "Total On-Road Vehicle Quotation Amount (Rs.)", "type": "number", "required": 1, "order": 3, "placeholder": "e.g. 750000"},
            {"name": "authorized_dealership_name", "label": "Vehicle Showroom / Dealer Name & Location", "type": "text", "required": 1, "order": 4, "placeholder": "Authorized OEM Dealer, Bengaluru"}
        ]
    ),

    # 33. Shrama Shakthi Loan Scheme
    (
        33, "ONLINE_FORM",
        "Shrama Shakthi Low-Interest Artisan Loan Scheme",
        "Financial assistance of Rs. 50,000 (50% subsidy + 50% term loan at 4% interest) for skilled artisans from minority groups.",
        [
            {"name": "traditional_craft_type", "label": "Traditional Craft / Artisan Skill", "type": "select", "required": 1, "order": 1, "options": ["Zari & Embroidery Craft", "Leather & Footwear Craft", "Carpentry & Wood Inlay", "Blacksmith & Iron Fabrication", "Pottery & Terracotta", "Motor Mechanics & Repair"]},
            {"name": "years_of_craft_experience", "label": "Years of Experience in Selected Trade", "type": "number", "required": 1, "order": 2, "placeholder": "e.g. 5"},
            {"name": "minority_certificate_no", "label": "Religious Minority Declaration Certificate Number", "type": "text", "required": 1, "order": 3, "placeholder": "Tahasildar issued Certificate No."}
        ]
    ),

    # 34. Basava Vasati & Dr. B.R. Ambedkar Nivas Yojane
    (
        34, "ONLINE_FORM",
        "Basava Vasati / Dr. B.R. Ambedkar Nivas Pucca Housing Grant",
        "Direct financial grant of Rs. 1.75 to 2.00 Lakhs in 4 construction milestone stages for homeless BPL rural households.",
        [
            {"name": "housing_scheme_category", "label": "Specific Housing Scheme Stream", "type": "select", "required": 1, "order": 1, "options": ["Dr. B.R. Ambedkar Nivas Yojane (SC/ST - Rs. 2.00 Lakhs Grant)", "Basava Vasati Yojane (Rural BPL - Rs. 1.75 Lakhs Grant)"]},
            {"name": "homeless_status", "label": "Current Shelter Condition", "type": "select", "required": 1, "order": 2, "options": ["Houseless (Site Available, No Pucca House)", "Kutcha House (Thatch / Mud Wall Damaged Structure)"]},
            {"name": "ashraya_site_allotment_number", "label": "Ashraya / Hakku Patra Site Number / E-Swathu ID", "type": "text", "required": 1, "order": 3, "placeholder": "Gram Panchayat Site Hakku Patra Number"},
            {"name": "gram_panchayat_approval_resolution", "label": "Gram Sabha Beneficiary Approval Resolution Date", "type": "date", "required": 1, "order": 4}
        ]
    ),

    # 35. Gruha Arogya Yojana
    (
        35, "ONLINE_FORM",
        "Gruha Arogya Doorstep NCD Health Screening & Free Medication",
        "Doorstep screening for diabetes, hypertension, and cancer, with free monthly medicine kits delivered at home.",
        [
            {"name": "chronic_conditions_reported", "label": "Existing Non-Communicable Diseases (NCDs) Reported", "type": "select", "required": 1, "order": 1, "options": ["Hypertension (High Blood Pressure)", "Diabetes Mellitus", "Hypertension & Diabetes Both", "Cardiovascular / Kidney Illness", "Cancer Screening Follow-up"]},
            {"name": "current_blood_pressure_status", "label": "Last Measured BP / Sugar Status", "type": "select", "required": 1, "order": 2, "options": ["Under Regular Medication", "Newly Diagnosed / Irregular Treatment", "Screening Requested for First Time"]},
            {"name": "primary_health_centre_jurisdiction", "label": "Jurisdictional Primary Health Centre (PHC) Name", "type": "text", "required": 1, "order": 3, "placeholder": "e.g. Kadugodi PHC"},
            {"name": "doorstep_delivery_elderly_status", "label": "Is the patient bedridden or senior citizen aged 65+?", "type": "radio", "required": 1, "order": 4, "options": ["Yes (Priority Doorstep Medicine Delivery)", "No (Sub-Centre Collection)"]}
        ]
    ),

    # 36. Vidyasiri Hostel Alternate Scheme
    (
        36, "ONLINE_FORM",
        "Vidyasiri Hostel Alternate Food Grant Application",
        "Direct financial stipend for backward classes students unable to secure SWD government hostel admission.",
        [
            {"name": "college_affiliation_number", "label": "College Registration / AISHE Code", "type": "text", "required": 1, "order": 1, "placeholder": "AISHE Code or University Reg No."},
            {"name": "bcm_hostel_waitlist_rank", "label": "BCM Departmental Hostel Waitlist Serial Number", "type": "text", "required": 1, "order": 2, "placeholder": "e.g. WL-2026-089"},
            {"name": "monthly_rent_amount", "label": "Monthly Room / Lodging Rent Paid (Rs.)", "type": "number", "required": 1, "order": 3, "placeholder": "e.g. 2500"}
        ]
    )
]

for spec in SCHEME_FORM_SPECS:
    scheme_id, app_mode, title, desc, fields = spec

    # 1. Update schemes table application_mode
    cur.execute("UPDATE schemes SET application_mode = %s WHERE id = %s;", (app_mode, scheme_id))

    # 2. Insert or update dynamic_form_definitions
    cur.execute('''
    INSERT INTO dynamic_form_definitions (scheme_id, version, title, description, is_active)
    VALUES (%s, 1, %s, %s, 1)
    ON DUPLICATE KEY UPDATE title = VALUES(title), description = VALUES(description), is_active = 1;
    ''', (scheme_id, title, desc))

    # Retrieve form_id
    cur.execute("SELECT id FROM dynamic_form_definitions WHERE scheme_id = %s AND version = 1;", (scheme_id,))
    form_id = cur.fetchone()[0]

    # Clean existing fields to re-seed cleanly
    cur.execute("DELETE FROM dynamic_form_fields WHERE form_id = %s;", (form_id,))

    # 3. Insert fields
    for f in fields:
        opt_json = json.dumps(f.get("options")) if f.get("options") else None
        val_json = json.dumps(f.get("validation")) if f.get("validation") else None
        cond_json = json.dumps(f.get("conditional")) if f.get("conditional") else None
        cur.execute('''
        INSERT INTO dynamic_form_fields 
        (form_id, field_name, field_label, field_type, placeholder, help_text, is_required, display_order, options_json, validation_rules_json, conditional_visibility_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (
            form_id,
            f["name"],
            f["label"],
            f["type"],
            f.get("placeholder", ""),
            f.get("help", ""),
            f.get("required", 1),
            f.get("order", 0),
            opt_json,
            val_json,
            cond_json
        ))

conn.commit()
print(f"Successfully seeded dynamic form definitions and fields for all {len(SCHEME_FORM_SPECS)} schemes!")

# Seed default category assignments for officer user 2
cur.execute("SELECT id FROM scheme_categories;")
cat_ids = [r[0] for r in cur.fetchall()]
for cid in cat_ids:
    cur.execute('''
    INSERT IGNORE INTO officer_category_assignments (officer_id, category_id, assigned_by)
    VALUES (2, %s, 3);
    ''', (cid,))
conn.commit()
print("Assigned all categories to Welfare Officer (ID 2).")

conn.close()
