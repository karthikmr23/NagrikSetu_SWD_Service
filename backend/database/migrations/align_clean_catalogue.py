import os
from app.database.connection import SessionLocal
from app.models import SchemeCategory, Scheme, SchemeApplication, OfficerCategoryAssignment

def align_categories_and_schemes():
    db = SessionLocal()
    try:
        # Define the exact 9 categories required by the prompt:
        # 1. Education and Scholarships (SCHOLARSHIPS)
        # 2. Women and Child Welfare (WOMEN_CHILDREN)
        # 3. Disability Welfare (DISABILITY_WELFARE)
        # 4. Senior Citizen and Social Security Pensions (SENIOR_CITIZEN_PENSIONS)
        # 5. SC/ST Welfare (SC_ST_WELFARE)
        # 6. OBC and Minority Welfare (OBC_MINORITY_WELFARE)
        # 7. Farmer and Rural Welfare (FARMER_RURAL_WELFARE)
        # 8. Labour and Housing Welfare (LABOUR_HOUSING)
        # 9. Karnataka Government Guarantee Schemes (GOVERNMENT_GUARANTEES)

        cat_updates = {
            1: {"code": "SCHOLARSHIPS", "name": "Education and Scholarships", "desc": "Educational assistance, scholarships, and fee concessions for students"},
            2: {"code": "DISABILITY_WELFARE", "name": "Disability Welfare", "desc": "Pensions, assistive devices, and rehabilitation grants for Persons with Disabilities (PwD)"},
            3: {"code": "SENIOR_CITIZEN_PENSIONS", "name": "Senior Citizen and Social Security Pensions", "desc": "Monthly financial pensions and social security assistance for elderly and destitute citizens"},
            4: {"code": "SC_ST_WELFARE", "name": "SC/ST Welfare", "desc": "Incentive grants, overseas scholarships, and welfare programs for SC and ST communities"},
            5: {"code": "GOVERNMENT_GUARANTEES", "name": "Karnataka Government Guarantee Schemes", "desc": "Flagship 5 Guarantee Schemes of Government of Karnataka"},
            6: {"code": "WOMEN_CHILDREN", "name": "Women and Child Welfare", "desc": "Maternal care, financial assistance, self-employment, and nutrition for women and children"},
            7: {"code": "FARMER_RURAL_WELFARE", "name": "Farmer and Rural Welfare", "desc": "Agricultural incentives, micro-irrigation, cooperative health insurance, and rural livelihoods"},
            8: {"code": "OBC_MINORITY_WELFARE", "name": "OBC and Minority Welfare", "desc": "Education loans, hostel stipends, and community development for OBC and Minority citizens"},
            9: {"code": "LABOUR_HOUSING", "name": "Labour and Housing Welfare", "desc": "Housing allotments, unorganized worker security, and welfare board benefits"}
        }

        for cat_id, data in cat_updates.items():
            cat = db.get(SchemeCategory, cat_id)
            if cat:
                cat.code = data["code"]
                cat.name = data["name"]
                cat.description = data["desc"]
                print(f"Updated Category {cat_id}: {cat.name}")

        # Scheme Category Re-assignments and clean Department mappings:
        scheme_alignments = {
            # Scheme 1: Post-Matric Scholarship (SSP) -> Cat 1 (Education and Scholarships)
            1: {"cat_id": 1, "dept": "Social Welfare Department, Government of Karnataka"},
            # Scheme 2: Disability Maintenance & Assistive Aid Grant -> Cat 2 (Disability Welfare)
            2: {"cat_id": 2, "dept": "Directorate for the Empowerment of Differently Abled and Senior Citizens"},
            # Scheme 3: Sandhya Suraksha Senior Citizen Pension Scheme -> Cat 3 (Senior Citizen and Social Security Pensions)
            3: {"cat_id": 3, "dept": "Revenue Department (Social Security and Pensions), Government of Karnataka"},
            # Scheme 4: Financial Incentive Scheme for Inter-Caste Marriages -> Cat 5 (SC/ST Welfare)
            4: {"cat_id": 5, "dept": "Social Welfare Department, Government of Karnataka"},
            # Scheme 5: Gruha Lakshmi Scheme -> Cat 9 (Karnataka Government Guarantee Schemes)
            5: {"cat_id": 5, "dept": "Department of Women and Child Development, Government of Karnataka"},
            # Scheme 6: Gruha Jyothi Scheme -> Cat 9 (Karnataka Government Guarantee Schemes)
            6: {"cat_id": 5, "dept": "Energy Department, Government of Karnataka"},
            # Scheme 7: Shakti Free Bus Travel Scheme -> Cat 9 (Karnataka Government Guarantee Schemes)
            7: {"cat_id": 5, "dept": "Transport Department, Government of Karnataka"},
            # Scheme 8: Anna Bhagya Scheme -> Cat 9 (Karnataka Government Guarantee Schemes)
            8: {"cat_id": 5, "dept": "Food, Civil Supplies and Consumer Affairs Department"},
            # Scheme 9: Yuva Nidhi & Yuvanidhi Plus Scheme -> Cat 9 (Karnataka Government Guarantee Schemes)
            9: {"cat_id": 5, "dept": "Skill Development, Entrepreneurship and Livelihood Department"},
            # Scheme 10: Udyogini Scheme -> Cat 2 (Women and Child Welfare)
            10: {"cat_id": 6, "dept": "Karnataka State Women's Development Corporation (KSWDC)"},
            # Scheme 11: Bhagyalakshmi Scheme -> Cat 2 (Women and Child Welfare)
            11: {"cat_id": 6, "dept": "Department of Women and Child Development, Government of Karnataka"},
            # Scheme 12: Matru Poorna Scheme -> Cat 2 (Women and Child Welfare)
            12: {"cat_id": 6, "dept": "Department of Women and Child Development, Government of Karnataka"},
            # Scheme 13: Thayi Bhagya & Prasoothi Araike Scheme -> Cat 2 (Women and Child Welfare)
            13: {"cat_id": 6, "dept": "Department of Health and Family Welfare, Government of Karnataka"},
            # Scheme 14: Madilu Kit Scheme -> Cat 2 (Women and Child Welfare)
            14: {"cat_id": 6, "dept": "Department of Health and Family Welfare, Government of Karnataka"},
            # Scheme 15: Santhwana Scheme -> Cat 2 (Women and Child Welfare)
            15: {"cat_id": 6, "dept": "Karnataka State Women's Development Corporation (KSWDC)"},
            # Scheme 16: Dhanashree & Chetana Scheme -> Cat 2 (Women and Child Welfare)
            16: {"cat_id": 6, "dept": "Karnataka State Women's Development Corporation (KSWDC)"},
            # Scheme 17: Chief Minister Raitha Vidya Nidhi -> Cat 7 (Farmer and Rural Welfare)
            17: {"cat_id": 7, "dept": "Agriculture Department, Government of Karnataka"},
            # Scheme 18: Ganga Kalyana Scheme -> Cat 7 (Farmer and Rural Welfare)
            18: {"cat_id": 7, "dept": "Social Welfare Department & Backward Classes Welfare Department"},
            # Scheme 19: Krishi Bhagya Scheme -> Cat 7 (Farmer and Rural Welfare)
            19: {"cat_id": 7, "dept": "Agriculture Department, Government of Karnataka"},
            # Scheme 20: Farmer Irrigation Assistance Scheme (Micro-Irrigation) -> Cat 7 (Farmer and Rural Welfare)
            20: {"cat_id": 7, "dept": "Horticulture Department & Agriculture Department"},
            # Scheme 21: Krushi Aranya Protsaha Yojane (KAPY) -> Cat 7 (Farmer and Rural Welfare)
            21: {"cat_id": 7, "dept": "Forest, Ecology and Environment Department, Government of Karnataka"},
            # Scheme 22: Yeshasvini Cooperative Health Insurance Scheme -> Cat 7 (Farmer and Rural Welfare)
            22: {"cat_id": 7, "dept": "Cooperation Department, Government of Karnataka"},
            # Scheme 23: Raitha Siri Scheme -> Cat 7 (Farmer and Rural Welfare)
            23: {"cat_id": 7, "dept": "Agriculture Department, Government of Karnataka"},
            # Scheme 24: Arivu Education Loan Scheme -> Cat 8 (OBC and Minority Welfare)
            24: {"cat_id": 8, "dept": "Minorities Welfare Department & Backward Classes Welfare Department"},
            # Scheme 25: Vidyasiri (Food & Accommodation Stipend) -> Cat 8 (OBC and Minority Welfare)
            25: {"cat_id": 8, "dept": "Backward Classes Welfare Department, Government of Karnataka"},
            # Scheme 26: Prabuddha & Dr. B.R. Ambedkar Overseas Scholarships -> Cat 5 (SC/ST Welfare)
            26: {"cat_id": 4, "dept": "Social Welfare Department, Government of Karnataka"},
            # Scheme 27: ELEVATE & ELEVATE NxT Startup Grants -> Cat 1 (Education and Scholarships / Youth)
            27: {"cat_id": 1, "dept": "Department of Electronics, IT, Bt and S&T, Government of Karnataka"},
            # Scheme 28: Rajiv Gandhi Entrepreneurship Program -> Cat 1 (Education and Scholarships / Youth)
            28: {"cat_id": 1, "dept": "Department of Electronics, IT, Bt and S&T, Government of Karnataka"},
            # Scheme 29: Karnataka Construction Workers (KBOCWWB) Schemes -> Cat 9 (Labour and Housing Welfare)
            29: {"cat_id": 9, "dept": "Labour Department, Government of Karnataka"},
            # Scheme 30: Karnataka State Gig Workers Insurance Scheme -> Cat 9 (Labour and Housing Welfare)
            30: {"cat_id": 9, "dept": "Labour Department, Government of Karnataka"},
            # Scheme 31: Ambedkar Karmika Sahaya Hastha -> Cat 9 (Labour and Housing Welfare)
            31: {"cat_id": 9, "dept": "Labour Department, Government of Karnataka"},
            # Scheme 32: Swavalambi Sarathi Scheme -> Cat 5 (SC/ST Welfare)
            32: {"cat_id": 4, "dept": "Social Welfare Department & Backward Classes Welfare Department"},
            # Scheme 33: Shrama Shakthi Loan Scheme -> Cat 8 (OBC and Minority Welfare)
            33: {"cat_id": 8, "dept": "Minorities Welfare Department, Government of Karnataka"},
            # Scheme 34: Basava Vasati & Dr. B.R. Ambedkar Nivas Yojane -> Cat 9 (Labour and Housing Welfare)
            34: {"cat_id": 9, "dept": "Housing Department, Government of Karnataka"},
            # Scheme 35: Gruha Arogya Yojana -> Cat 6 (Women and Child Welfare / Health)
            35: {"cat_id": 6, "dept": "Department of Health and Family Welfare, Government of Karnataka"}
        }

        for s_id, align in scheme_alignments.items():
            scheme = db.get(Scheme, s_id)
            if scheme:
                scheme.category_id = align["cat_id"]
                scheme.department = align["dept"]
                print(f"Aligned Scheme {s_id} ({scheme.name}) -> Cat {align['cat_id']} | Dept: {align['dept']}")

        db.commit()

        # Update existing applications so category_id matches scheme.category_id
        apps = db.query(SchemeApplication).all()
        for app in apps:
            scheme = db.get(Scheme, app.scheme_id)
            if scheme:
                app.category_id = scheme.category_id
        db.commit()
        print(f"Synchronized {len(apps)} applications to matching category_id")

        # Ensure OfficerCategoryAssignment has all categories 1..9
        officer_cats = db.query(OfficerCategoryAssignment).filter(OfficerCategoryAssignment.officer_id == 2).all()
        existing_assigned = {oc.category_id for oc in officer_cats}
        for c_id in range(1, 10):
            if c_id not in existing_assigned:
                db.add(OfficerCategoryAssignment(officer_id=2, category_id=c_id))
        db.commit()
        print("Officer category assignments verified for categories 1..9")

    finally:
        db.close()

if __name__ == "__main__":
    align_categories_and_schemes()
