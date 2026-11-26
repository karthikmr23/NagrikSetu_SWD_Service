const fs = require('fs');
const path = require('path');

const modelsPath = path.join(__dirname, 'backend', 'app', 'models', '__init__.py');
let content = fs.readFileSync(modelsPath, 'utf8');

const officeModel = `
class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    office_type = Column(String(100), default="District Welfare Office", index=True)
    district = Column(String(100), nullable=False, index=True)
    taluk = Column(String(100), nullable=True, index=True)
    address = Column(Text, nullable=False)
    contact_number = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    working_hours = Column(String(100), default="10:00 AM - 5:30 PM (Mon-Sat)")
    services_offered = Column(Text, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    map_link = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    verification_status = Column(String(50), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
`;

if (!content.includes('class Office(Base):')) {
  content += '\n' + officeModel;
  fs.writeFileSync(modelsPath, content, 'utf8');
  console.log('Appended Office model to models/__init__.py');
} else {
  console.log('Office model already present in models/__init__.py');
}
