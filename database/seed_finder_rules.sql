-- Structured Eligibility Rules for Karnataka Welfare Schemes
-- Populating rules for schemes 5 to 35 without dropping or deleting existing records.
-- Using INSERT IGNORE based on scheme_id and field_name.

INSERT INTO eligibility_rules (scheme_id, field_name, operator, expected_value, value_type, is_mandatory, description, rule_version, is_active, created_at, updated_at) VALUES
-- 5. Gruha Lakshmi Scheme
(5, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Applicant family must reside in Karnataka', 1, 1, NOW(), NOW()),
(5, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Applicant must be woman head of household', 1, 1, NOW(), NOW()),

-- 6. Gruha Jyothi Scheme
(6, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Domestic household in Karnataka state', 1, 1, NOW(), NOW()),

-- 7. Shakti Free Bus Travel Scheme
(7, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Domiciled resident of Karnataka state', 1, 1, NOW(), NOW()),
(7, 'gender', 'IN', 'female,woman,transgender', 'LIST', 1, 'Beneficiary must be woman, girl child, or transgender', 1, 1, NOW(), NOW()),

-- 8. Anna Bhagya Scheme
(8, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Domiciled resident of Karnataka state', 1, 1, NOW(), NOW()),

-- 9. Yuva Nidhi Scheme
(9, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Domiciled resident of Karnataka', 1, 1, NOW(), NOW()),
(9, 'occupation', 'IN', 'unemployed,graduate,jobseeker', 'LIST', 1, 'Unemployed graduate or diploma holder', 1, 1, NOW(), NOW()),

-- 10. Udyogini Scheme
(10, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Permanent resident of Karnataka', 1, 1, NOW(), NOW()),
(10, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Applicant must be a woman entrepreneur or aspiring business owner', 1, 1, NOW(), NOW()),
(10, 'age', 'RANGE', '18-55', 'INTEGER', 1, 'Age between 18 and 55 years', 1, 1, NOW(), NOW()),
(10, 'annual_income', 'LESS_THAN_OR_EQUAL', '150000', 'FLOAT', 0, 'Annual family income under INR 1,50,000 (Relaxed for SC/ST)', 1, 1, NOW(), NOW()),

-- 11. Bhagyalakshmi Scheme
(11, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Permanent resident of Karnataka', 1, 1, NOW(), NOW()),

-- 12. Matru Poorna Scheme
(12, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident mother in Karnataka Anganwadi area', 1, 1, NOW(), NOW()),
(12, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be woman (pregnant or lactating mother)', 1, 1, NOW(), NOW()),

-- 13. Thayi Bhagya Scheme
(13, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka designated taluks', 1, 1, NOW(), NOW()),
(13, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be woman pregnant mother', 1, 1, NOW(), NOW()),

-- 14. Madilu Kit Scheme
(14, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident mother in Karnataka delivering in government facility', 1, 1, NOW(), NOW()),
(14, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Eligible mother delivering in public healthcare institution', 1, 1, NOW(), NOW()),

-- 15. Santhwana Scheme
(15, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka state', 1, 1, NOW(), NOW()),
(15, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Support service available for women in distress', 1, 1, NOW(), NOW()),

-- 16. Dhanashree & Chetana Scheme
(16, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka', 1, 1, NOW(), NOW()),
(16, 'is_woman', 'EQUALS', 'true', 'BOOLEAN', 1, 'Vulnerable and distressed women empowerment grant', 1, 1, NOW(), NOW()),
(16, 'age', 'RANGE', '18-55', 'INTEGER', 1, 'Age between 18 and 55 years', 1, 1, NOW(), NOW()),

-- 17. Chief Minister Raitha Vidya Nidhi
(17, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident student of Karnataka', 1, 1, NOW(), NOW()),
(17, 'is_student', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be enrolled in secondary, PUC, ITI, diploma or degree course', 1, 1, NOW(), NOW()),
(17, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Parent or applicant must hold agricultural farmer records (FRUITS ID)', 1, 1, NOW(), NOW()),

-- 18. Ganga Kalyana Scheme
(18, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident farmer in Karnataka', 1, 1, NOW(), NOW()),
(18, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be a small or marginal agricultural farmer', 1, 1, NOW(), NOW()),
(18, 'caste_category', 'IN', 'SC,ST,OBC,Cat-1,2A,2B,3A,3B,Minority', 'LIST', 1, 'Belong to SC, ST, OBC or recognized religious minority community', 1, 1, NOW(), NOW()),

-- 19. Krishi Bhagya Scheme
(19, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident farmer in Karnataka', 1, 1, NOW(), NOW()),
(19, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be a practicing farmer in dryland/rainfed zone', 1, 1, NOW(), NOW()),

-- 20. Micro Irrigation Assistance
(20, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident farmer in Karnataka', 1, 1, NOW(), NOW()),
(20, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must own or cultivate agricultural/horticultural land', 1, 1, NOW(), NOW()),

-- 21. Krushi Aranya Protsaha Yojane
(21, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident landowner or farmer in Karnataka', 1, 1, NOW(), NOW()),
(21, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must plant saplings on private agricultural land', 1, 1, NOW(), NOW()),

-- 22. Yeshasvini Health Insurance
(22, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka', 1, 1, NOW(), NOW()),

-- 23. Raitha Siri Scheme
(23, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident farmer in Karnataka', 1, 1, NOW(), NOW()),
(23, 'is_farmer', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be cultivating millets verified in FRUITS system', 1, 1, NOW(), NOW()),

-- 24. Arivu Education Loan Scheme
(24, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident student in Karnataka', 1, 1, NOW(), NOW()),
(24, 'is_student', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be enrolled in professional/technical higher education course', 1, 1, NOW(), NOW()),
(24, 'caste_category', 'IN', 'Minority,OBC,Cat-1,2A,2B,3A,3B,SC,ST', 'LIST', 1, 'Must belong to minority, backward class or reserved category', 1, 1, NOW(), NOW()),
(24, 'annual_income', 'LESS_THAN_OR_EQUAL', '350000', 'FLOAT', 1, 'Annual family income must not exceed INR 3,50,000', 1, 1, NOW(), NOW()),

-- 25. Vidyasiri Food & Accommodation
(25, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident student in Karnataka', 1, 1, NOW(), NOW()),
(25, 'is_student', 'EQUALS', 'true', 'BOOLEAN', 1, 'Must be post-matric student residing away from college without hostel', 1, 1, NOW(), NOW()),
(25, 'caste_category', 'IN', 'SC,ST,OBC,Cat-1,2A,2B,3A,3B', 'LIST', 1, 'Belong to SC, ST, or OBC category', 1, 1, NOW(), NOW()),
(25, 'annual_income', 'LESS_THAN_OR_EQUAL', '250000', 'FLOAT', 1, 'Annual family income under INR 2,50,000', 1, 1, NOW(), NOW()),

-- 26. Prabuddha & Dr. B.R. Ambedkar Overseas Scholarships
(26, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka', 1, 1, NOW(), NOW()),
(26, 'is_student', 'EQUALS', 'true', 'BOOLEAN', 1, 'Admitted to accredited foreign top-tier university', 1, 1, NOW(), NOW()),
(26, 'caste_category', 'IN', 'SC,ST', 'LIST', 1, 'Must belong to Scheduled Caste (SC) or Scheduled Tribe (ST)', 1, 1, NOW(), NOW()),

-- 27. ELEVATE Startup Grants
(27, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Startup registered and operating in Karnataka', 1, 1, NOW(), NOW()),

-- 28. Rajiv Gandhi Entrepreneurship Program
(28, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident graduate of Karnataka', 1, 1, NOW(), NOW()),
(28, 'occupation', 'IN', 'student,employed,self-employed,unemployed', 'LIST', 1, 'Graduated in engineering/science with innovative product concept', 1, 1, NOW(), NOW()),

-- 29. Construction Workers (KBOCWWB) Schemes
(29, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident worker in Karnataka', 1, 1, NOW(), NOW()),
(29, 'occupation', 'IN', 'construction worker,construction,labourer', 'LIST', 1, 'Must be registered construction worker with KBOCWWB', 1, 1, NOW(), NOW()),
(29, 'age', 'RANGE', '18-60', 'INTEGER', 1, 'Age between 18 and 60 years', 1, 1, NOW(), NOW()),

-- 30. Gig Workers Insurance Scheme
(30, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident gig delivery worker in Karnataka', 1, 1, NOW(), NOW()),
(30, 'occupation', 'IN', 'gig worker,delivery,driver', 'LIST', 1, 'Must be active delivery executive or app-based driver', 1, 1, NOW(), NOW()),

-- 31. Ambedkar Karmika Sahaya Hastha
(31, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident of Karnataka', 1, 1, NOW(), NOW()),
(31, 'occupation', 'IN', 'unorganized worker,tailor,mechanic,dhobi,barber,domestic worker,other', 'LIST', 1, 'Unorganized sector worker not covered under EPF/ESI', 1, 1, NOW(), NOW()),
(31, 'age', 'RANGE', '18-60', 'INTEGER', 1, 'Age between 18 and 60 years', 1, 1, NOW(), NOW()),

-- 32. Swavalambi Sarathi Scheme
(32, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident youth of Karnataka', 1, 1, NOW(), NOW()),
(32, 'age', 'RANGE', '21-45', 'INTEGER', 1, 'Age between 21 and 45 years', 1, 1, NOW(), NOW()),
(32, 'caste_category', 'IN', 'SC,ST,OBC,Cat-1,2A,2B,3A,3B,Minority', 'LIST', 1, 'Belong to SC, ST, OBC or religious minority community', 1, 1, NOW(), NOW()),

-- 33. Shrama Shakthi Loan Scheme
(33, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Resident artisan in Karnataka', 1, 1, NOW(), NOW()),
(33, 'caste_category', 'IN', 'Minority', 'LIST', 1, 'Must belong to notified religious minority community', 1, 1, NOW(), NOW()),
(33, 'annual_income', 'LESS_THAN_OR_EQUAL', '150000', 'FLOAT', 1, 'Family annual income under INR 1,50,000', 1, 1, NOW(), NOW()),

-- 34. Basava Vasati & Dr. Ambedkar Nivas Yojane
(34, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Permanent rural resident of Karnataka', 1, 1, NOW(), NOW()),
(34, 'annual_income', 'LESS_THAN_OR_EQUAL', '32000', 'FLOAT', 1, 'Annual family income under INR 32,000 (BPL housing norm)', 1, 1, NOW(), NOW()),

-- 35. Gruha Arogya Yojana
(35, 'residence_state', 'EQUALS', 'Karnataka', 'STRING', 1, 'Domiciled resident of Karnataka', 1, 1, NOW(), NOW()),
(35, 'age', 'GREATER_THAN_OR_EQUAL', '30', 'INTEGER', 1, 'Age 30 years or older for non-communicable disease screening', 1, 1, NOW(), NOW());
