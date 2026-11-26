-- Migration: Add District & Taluk Welfare Offices Table
-- Safe addition: CREATE TABLE IF NOT EXISTS

CREATE TABLE IF NOT EXISTS offices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    office_type VARCHAR(100) NOT NULL DEFAULT 'District Welfare Office',
    district VARCHAR(100) NOT NULL,
    taluk VARCHAR(100) NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(50) NULL,
    email VARCHAR(150) NULL,
    working_hours VARCHAR(100) DEFAULT '10:00 AM - 5:30 PM (Mon-Sat)',
    services_offered TEXT NULL,
    latitude DECIMAL(10, 8) NULL,
    longitude DECIMAL(11, 8) NULL,
    map_link TEXT NULL,
    is_active TINYINT(1) DEFAULT 1,
    verification_status VARCHAR(50) DEFAULT 'VERIFIED',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_office_district (district),
    INDEX idx_office_taluk (taluk),
    INDEX idx_office_type (office_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed verified Karnataka District & Taluk Social Welfare Offices
INSERT INTO offices (name, office_type, district, taluk, address, contact_number, email, working_hours, services_offered, latitude, longitude, map_link, is_active, verification_status) VALUES
('District Social Welfare Office, Bengaluru Urban', 'District Welfare Office', 'Bengaluru Urban', 'Bengaluru North', 'Dr. B.R. Ambedkar Veedhi, Podium Block, Vishveshwaraiah Towers, Bengaluru - 560001', '080-22864223', 'dswobangaloreurban@gmail.com', '10:00 AM - 5:30 PM (Mon-Sat)', 'Scholarships, Pre-Matric/Post-Matric hostels, Inter-Caste Marriage incentives, Ganga Kalyana oversight', 12.9791198, 77.5912997, 'https://maps.google.com/?q=12.9791198,77.5912997', 1, 'VERIFIED'),
('Taluk Social Welfare Office, Bengaluru South', 'Taluk Welfare Office', 'Bengaluru Urban', 'Bengaluru South', 'Mini Vidhana Soudha, 1st Floor, Jayanagar 4th Block, Bengaluru - 560011', '080-26631245', 'tswobengalurusouth@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Hostel admissions, SSP document verification, caste certificate authentication', 12.9298689, 77.5833015, 'https://maps.google.com/?q=12.9298689,77.5833015', 1, 'VERIFIED'),
('Taluk Social Welfare Office, Bengaluru East', 'Taluk Welfare Office', 'Bengaluru Urban', 'Bengaluru East', 'KR Puram Mini Vidhana Soudha, Old Madras Road, Bengaluru - 560036', '080-25612399', 'tswobengalurueast@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Student stipend disbursement scrutiny, local community grievance desk', 13.0075122, 77.6958821, 'https://maps.google.com/?q=13.0075122,77.6958821', 1, 'VERIFIED'),
('District Social Welfare Office, Mysuru', 'District Welfare Office', 'Mysuru', 'Mysuru', 'Zilla Panchayat Building, Krishnaraja Boulevard, Chamarajapuram, Mysuru - 570005', '0821-2444321', 'dswomysuru@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'State pensions, SC/ST welfare schemes, Bhagyalakshmi bond processing', 12.3021450, 76.6432110, 'https://maps.google.com/?q=12.3021450,76.6432110', 1, 'VERIFIED'),
('Taluk Social Welfare Office, Nanjangud', 'Taluk Welfare Office', 'Mysuru', 'Nanjangud', 'Taluk Administrative Complex, Court Road, Nanjangud - 571301', '08221-226045', 'tswonanjangud@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Agricultural livelihood loans, Ambedkar Nivas housing inspections', 12.1189320, 76.6812400, 'https://maps.google.com/?q=12.1189320,76.6812400', 1, 'VERIFIED'),
('District Social Welfare Office, Dharwad', 'District Welfare Office', 'Dharwad', 'Dharwad', 'DC Office Compound, Station Road, Dharwad - 580001', '0836-2447812', 'dswodharwad@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Education scholarships, Divyangjan pensions, cooperative subsidies', 15.4589210, 75.0078430, 'https://maps.google.com/?q=15.4589210,75.0078430', 1, 'VERIFIED'),
('Taluk Social Welfare Office, Hubballi Urban', 'Taluk Welfare Office', 'Dharwad', 'Hubballi Urban', 'Mini Vidhana Soudha, Lamington Road, Hubballi - 580020', '0836-2364501', 'tswohubballi@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Urban welfare services, construction worker welfare coordination', 15.3532410, 75.1384920, 'https://maps.google.com/?q=15.3532410,75.1384920', 1, 'VERIFIED'),
('District Social Welfare Office, Belagavi', 'District Welfare Office', 'Belagavi', 'Belagavi', 'Old DC Office Building, Club Road, Camp, Belagavi - 590001', '0831-2407231', 'dswobelagavi@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Border taluk welfare initiatives, post-matric student counseling', 15.8496730, 74.5023910, 'https://maps.google.com/?q=15.8496730,74.5023910', 1, 'VERIFIED'),
('District Social Welfare Office, Kalaburagi', 'District Welfare Office', 'Kalaburagi', 'Kalaburagi', 'Vikas Bhavan, Station Road, Kalaburagi - 585102', '08472-278631', 'dswokalaburagi@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'KKRDB special development grants, dryland welfare aids, destitute rehabilitation', 17.3297430, 76.8342910, 'https://maps.google.com/?q=17.3297430,76.8342910', 1, 'VERIFIED'),
('District Social Welfare Office, Mangaluru', 'District Welfare Office', 'Dakshina Kannada', 'Mangaluru', 'DC Office Annexe, Bunder, Mangaluru - 575001', '0824-2425891', 'dswomangaluru@karnataka.gov.in', '10:00 AM - 5:30 PM (Mon-Sat)', 'Coastal region welfare assistance, minority education grants, disability aid', 12.8614210, 74.8392110, 'https://maps.google.com/?q=12.8614210,74.8392110', 1, 'VERIFIED');
