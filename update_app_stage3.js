const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// Replace hero sign in button to navigate to sign-in-select
content = content.replace(
`                {!token ? (
                  <button 
                    className="hero-btn-green"
                    onClick={() => {
                      setAuthError('');
                      setActiveTab('citizen-login');
                    }}
                  >
                    <LogIn size={16} /> Sign In
                  </button>
                ) : (`,
`                {!token ? (
                  <button 
                    className="hero-btn-green"
                    onClick={() => {
                      setAuthError('');
                      setActiveTab('sign-in-select');
                    }}
                  >
                    <LogIn size={16} /> Sign In
                  </button>
                ) : (`
);

// Replace the 3rd civic card on the landing page (which currently has Admin Portal):
// Change it to "District & Taluk Welfare Office Locator" or "Citizen Grievance & Helpdesk"
const oldCivicThirdCard = `              <div className="civic-card" style={{ cursor: 'pointer' }} onClick={() => {
                if (token && (userRole === 'SWD_ADMIN' || userRole === 'ADMINISTRATOR' || userRole === 'WELFARE_OFFICER')) setActiveTab('admin-dashboard');
                else { setLoginRoleMode('ADMIN'); setShowLoginModal(true); }
              }}>
                <div className="civic-card-icon orange"><Shield size={20} /></div>
                <div>
                  <h5 className="civic-card-title">SWD Administrative Command</h5>
                  <p className="civic-card-desc">Officer review desk for application scrutiny, duplicate detection, information requests, and beneficiary ledger creation.</p>
                </div>
              </div>`;

const newCivicThirdCard = `              <div className="civic-card" style={{ cursor: 'pointer' }} onClick={() => {
                setActiveTab('office-locator');
                loadOffices();
              }}>
                <div className="civic-card-icon orange"><Building2 size={20} /></div>
                <div>
                  <h5 className="civic-card-title">District & Taluk Office Locator</h5>
                  <p className="civic-card-desc">Locate verified Karnataka Social Welfare Department jurisdictional offices, officer contact numbers, addresses, and working hours.</p>
                </div>
              </div>`;

content = content.replace(oldCivicThirdCard, newCivicThirdCard);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 3 landing page updates applied successfully");
