const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// We will insert sign-in-select and admin-login right before "{/* VIEW: CITIZEN REGISTRATION (SEPARATE DEDICATED PAGE) */}"
const anchor = "{/* VIEW: CITIZEN REGISTRATION (SEPARATE DEDICATED PAGE) */}";

const signInSelectAndAdminLoginViews = `
        {/* VIEW: SEPARATED SIGN IN SELECTION PORTAL */}
        {activeTab === 'sign-in-select' && (
          <div className="swd-view-container" style={{ maxWidth: '880px', margin: '0 auto', padding: '2rem 1rem' }}>
            <div className="swd-view-header" style={{ textAlign: 'center', justifyContent: 'center', marginBottom: '2rem' }}>
              <div>
                <h2 style={{ fontSize: '1.65rem', color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>
                  Select Authentication Gateway
                </h2>
                <p style={{ fontSize: '0.9rem', color: '#64748b', maxWidth: '600px', margin: '0 auto' }}>
                  Please choose your intended portal. Citizens can access welfare schemes, applications, and receipts. Administrative officers access verification, scrutiny, and DBT processing.
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '2rem' }}>
              {/* Option 1: Citizen Portal Card */}
              <div style={{
                background: '#ffffff',
                border: '2px solid #ea580c',
                borderRadius: '12px',
                padding: '2rem',
                boxShadow: '0 4px 16px rgba(234, 88, 12, 0.08)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '12px',
                    backgroundColor: '#fff7ed',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '1.25rem'
                  }}>
                    <User size={28} color="#ea580c" />
                  </div>
                  <h3 style={{ fontSize: '1.25rem', color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>
                    Citizen Portal
                  </h3>
                  <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.5rem' }}>
                    For Karnataka residents to apply for social welfare schemes, track dossier lifecycle, download official PDF acknowledgement receipts, file helpdesk grievances, and manage citizen registry profile.
                  </p>
                </div>

                <div>
                  <button
                    className="btn-orange"
                    style={{ width: '100%', padding: '0.75rem', fontSize: '0.95rem', marginBottom: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                    onClick={() => {
                      setAuthError('');
                      setActiveTab('citizen-login');
                    }}
                  >
                    <LogIn size={16} /> Citizen Login &rarr;
                  </button>
                  <button
                    className="btn-secondary"
                    style={{ width: '100%', padding: '0.65rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                    onClick={() => {
                      setRegError('');
                      setRegSuccessMsg('');
                      setActiveTab('citizen-register');
                    }}
                  >
                    <UserPlus size={15} /> Register as Citizen
                  </button>
                </div>
              </div>

              {/* Option 2: Admin Portal Card */}
              <div style={{
                background: '#ffffff',
                border: '2px solid var(--navy-dark)',
                borderRadius: '12px',
                padding: '2rem',
                boxShadow: '0 4px 16px rgba(15, 36, 68, 0.08)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{
                    width: '56px',
                    height: '56px',
                    borderRadius: '12px',
                    backgroundColor: '#f1f5f9',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '1.25rem'
                  }}>
                    <Shield size={28} color="#0f2444" />
                  </div>
                  <h3 style={{ fontSize: '1.25rem', color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>
                    Admin & Officer Portal
                  </h3>
                  <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.5rem' }}>
                    Dedicated command desk for Taluk & District Social Welfare Officers and Platform Administrators. Review applications, record official scrutiny decisions, disburse batch DBT, and resolve citizen grievances.
                  </p>
                </div>

                <div>
                  <button
                    className="btn-header-navy"
                    style={{ width: '100%', padding: '0.75rem', fontSize: '0.95rem', backgroundColor: 'var(--navy-dark)', color: '#ffffff', borderRadius: '6px', marginBottom: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                    onClick={() => {
                      setAuthError('');
                      setLoginEmail('swd.admin@nagriksetu.local');
                      setLoginPassword('SWDAdmin@2026!');
                      setActiveTab('admin-login');
                    }}
                  >
                    <Shield size={16} /> Admin Login &rarr;
                  </button>
                  <p style={{ fontSize: '0.75rem', color: '#94a3b8', textAlign: 'center', margin: 0 }}>
                    Restricted Government Intranet Access. Public registration disabled.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW: DEDICATED ADMIN LOGIN PAGE */}
        {activeTab === 'admin-login' && (
          <div className="swd-view-container" style={{ maxWidth: '480px', margin: '0 auto', padding: '2rem 1rem' }}>
            <div className="swd-view-header" style={{ justifyContent: 'center', textAlign: 'center', marginBottom: '1.25rem' }}>
              <div>
                <div style={{ display: 'inline-flex', padding: '0.5rem', borderRadius: '50%', background: '#f1f5f9', marginBottom: '0.5rem' }}>
                  <Shield size={32} color="#0f2444" />
                </div>
                <h2>SWD Administrative Sign In</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Department officer & administrator access to the Social Welfare Review & DBT Command Desk.
                </p>
              </div>
            </div>

            <div style={{ background: '#ffffff', padding: '2rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 4px 14px rgba(0,0,0,0.06)' }}>
              {authError && (
                <div style={{ backgroundColor: '#fee2e2', border: '1px solid #fca5a5', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <AlertCircle size={16} />
                  <span>{authError}</span>
                </div>
              )}

              <form onSubmit={handleDedicatedLogin}>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                    Official Email / Officer ID <span style={{ color: '#dc2626' }}>*</span>
                  </label>
                  <input 
                    type="email" 
                    required 
                    placeholder="swd.admin@nagriksetu.local"
                    className="filter-input" 
                    style={{ width: '100%' }}
                    value={loginEmail}
                    onChange={e => setLoginEmail(e.target.value)}
                  />
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                    Officer Access Key / Password <span style={{ color: '#dc2626' }}>*</span>
                  </label>
                  <div style={{ position: 'relative' }}>
                    <input 
                      type={showPassword ? "text" : "password"} 
                      required 
                      placeholder="Enter administrator password"
                      className="filter-input" 
                      style={{ width: '100%', paddingRight: '2.5rem' }}
                      value={loginPassword}
                      onChange={e => setLoginPassword(e.target.value)}
                    />
                    <button 
                      type="button" 
                      onClick={() => setShowPassword(!showPassword)}
                      style={{ position: 'absolute', right: '8px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                    >
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>

                <button 
                  type="submit" 
                  className="btn-header-navy" 
                  style={{ width: '100%', padding: '0.75rem', fontSize: '0.9rem', backgroundColor: 'var(--navy-dark)', color: '#ffffff', borderRadius: '6px', marginBottom: '1.25rem' }}
                  disabled={loginLoading}
                >
                  {loginLoading ? 'Verifying Credentials...' : 'Authenticate Officer Session'}
                </button>

                <div style={{ textAlign: 'center', borderTop: '1px solid var(--line)', paddingTop: '1rem', fontSize: '0.82rem', color: '#64748b' }}>
                  Are you a citizen?{' '}
                  <button 
                    type="button" 
                    className="nav-link-btn" 
                    style={{ color: '#ea580c', fontWeight: 700, padding: 0, textDecoration: 'underline' }}
                    onClick={() => {
                      setAuthError('');
                      setActiveTab('citizen-login');
                    }}
                  >
                    Go to Citizen Portal
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
`;

content = content.replace(anchor, signInSelectAndAdminLoginViews + "\n" + anchor);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 4 auth views applied successfully");
