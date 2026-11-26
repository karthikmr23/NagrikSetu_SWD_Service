const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// Insert right before </main>
const anchor = "      </main>";

const officeAndGrievanceViews = `
        {/* VIEW: DISTRICT & TALUK WELFARE OFFICE LOCATOR */}
        {activeTab === 'office-locator' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>District & Taluk Social Welfare Office Locator</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Find contact information, addresses, verified locations and services for Karnataka Social Welfare Department field offices.
                </p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>
                &larr; Back to Home
              </button>
            </div>

            {/* Filter Bar */}
            <div className="filter-bar" style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '1.5rem' }}>
              <input 
                type="text" 
                placeholder="Search office name, address, or service..." 
                className="filter-input" 
                style={{ flex: '1 1 240px' }}
                value={officeSearchQuery}
                onChange={(e) => {
                  setOfficeSearchQuery(e.target.value);
                  loadOffices(officeDistrictFilter || undefined, officeTalukFilter || undefined, e.target.value || undefined);
                }}
              />
              <select 
                className="filter-select"
                style={{ flex: '0 1 200px' }}
                value={officeDistrictFilter}
                onChange={(e) => {
                  const dist = e.target.value;
                  setOfficeDistrictFilter(dist);
                  setOfficeTalukFilter('');
                  loadOffices(dist || undefined, undefined, officeSearchQuery || undefined);
                }}
              >
                <option value="">All Districts (Karnataka)</option>
                <option value="Bengaluru Urban">Bengaluru Urban</option>
                <option value="Mysuru">Mysuru</option>
                <option value="Dharwad">Dharwad</option>
                <option value="Belagavi">Belagavi</option>
                <option value="Kalaburagi">Kalaburagi</option>
                <option value="Dakshina Kannada">Dakshina Kannada</option>
              </select>

              {officeDistrictFilter && (
                <select 
                  className="filter-select"
                  style={{ flex: '0 1 200px' }}
                  value={officeTalukFilter}
                  onChange={(e) => {
                    const tlk = e.target.value;
                    setOfficeTalukFilter(tlk);
                    loadOffices(officeDistrictFilter, tlk || undefined, officeSearchQuery || undefined);
                  }}
                >
                  <option value="">All Taluks</option>
                  {officeDistrictFilter === 'Bengaluru Urban' && (
                    <>
                      <option value="Bengaluru North">Bengaluru North</option>
                      <option value="Bengaluru South">Bengaluru South</option>
                      <option value="Bengaluru East">Bengaluru East</option>
                    </>
                  )}
                  {officeDistrictFilter === 'Mysuru' && (
                    <>
                      <option value="Mysuru">Mysuru</option>
                      <option value="Nanjangud">Nanjangud</option>
                    </>
                  )}
                  {officeDistrictFilter === 'Dharwad' && (
                    <>
                      <option value="Dharwad">Dharwad</option>
                      <option value="Hubballi Urban">Hubballi Urban</option>
                    </>
                  )}
                  {officeDistrictFilter === 'Belagavi' && (
                    <option value="Belagavi">Belagavi</option>
                  )}
                  {officeDistrictFilter === 'Kalaburagi' && (
                    <option value="Kalaburagi">Kalaburagi</option>
                  )}
                  {officeDistrictFilter === 'Dakshina Kannada' && (
                    <option value="Mangaluru">Mangaluru</option>
                  )}
                </select>
              )}

              {(officeDistrictFilter || officeTalukFilter || officeSearchQuery) && (
                <button 
                  className="btn-secondary" 
                  style={{ padding: '0.45rem 0.85rem', fontSize: '0.78rem' }}
                  onClick={() => {
                    setOfficeDistrictFilter('');
                    setOfficeTalukFilter('');
                    setOfficeSearchQuery('');
                    loadOffices();
                  }}
                >
                  Clear Filters
                </button>
              )}
            </div>

            {/* Office Cards Grid */}
            {officeLoading ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>Loading jurisdictional offices...</div>
            ) : offices.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <p style={{ color: '#64748b' }}>No departmental offices matched your search criteria.</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.25rem' }}>
                {offices.map(off => (
                  <div 
                    key={off.id} 
                    style={{
                      background: '#ffffff',
                      border: '1px solid var(--line)',
                      borderRadius: '10px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                        <span style={{
                          backgroundColor: off.office_type.includes('District') ? '#eff6ff' : '#f0fdf4',
                          color: off.office_type.includes('District') ? '#1d4ed8' : '#15803d',
                          fontWeight: 700,
                          fontSize: '0.72rem',
                          padding: '0.2rem 0.5rem',
                          borderRadius: '4px'
                        }}>
                          {off.office_type}
                        </span>
                        <span style={{ fontSize: '0.72rem', color: '#16a34a', fontWeight: 600 }}>
                          &bull; {off.verification_status}
                        </span>
                      </div>

                      <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', marginBottom: '0.4rem' }}>
                        {off.name}
                      </h4>
                      <p style={{ fontSize: '0.8rem', color: '#64748b', display: 'flex', alignItems: 'flex-start', gap: '0.4rem', marginBottom: '0.75rem' }}>
                        <MapPin size={15} style={{ flexShrink: 0, marginTop: '2px', color: '#ea580c' }} />
                        <span>{off.address}</span>
                      </p>

                      <div style={{ fontSize: '0.78rem', color: '#334155', display: 'flex', flexDirection: 'column', gap: '0.35rem', marginBottom: '0.85rem' }}>
                        <div><strong>Contact:</strong> {off.contact_number}</div>
                        <div><strong>Official Email:</strong> {off.email}</div>
                        <div><strong>Hours:</strong> {off.working_hours}</div>
                        <div style={{ marginTop: '0.25rem', background: '#f8fafc', padding: '0.4rem 0.6rem', borderRadius: '4px', fontSize: '0.75rem' }}>
                          <strong>Services:</strong> {off.services_offered}
                        </div>
                      </div>
                    </div>

                    <div style={{ borderTop: '1px solid var(--line)', paddingTop: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                        Taluk: <strong>{off.taluk}</strong> &bull; District: <strong>{off.district}</strong>
                      </span>
                      <a 
                        href={off.map_link} 
                        target="_blank" 
                        rel="noreferrer" 
                        className="btn-secondary" 
                        style={{ fontSize: '0.75rem', padding: '0.3rem 0.65rem', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                      >
                        Directions <ExternalLink size={12} />
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* VIEW: CITIZEN GRIEVANCE & HELPDESK */}
        {activeTab === 'grievance' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Citizen Grievance & Welfare Helpdesk</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Register complaints, request verification escalations, and track redressal by Social Welfare Officers.
                </p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('citizen-dashboard')}>
                &larr; Back to Dashboard
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.75rem' }}>
              {/* Form Section */}
              <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                  Register New Grievance
                </h4>

                {grievanceSuccessMsg && (
                  <div style={{ backgroundColor: '#ecfdf5', color: '#065f46', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <CheckCircle size={16} />
                    <span>{grievanceSuccessMsg}</span>
                  </div>
                )}

                {grievanceErrorMsg && (
                  <div style={{ backgroundColor: '#fee2e2', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <AlertCircle size={16} />
                    <span>{grievanceErrorMsg}</span>
                  </div>
                )}

                <form onSubmit={handleGrievanceSubmit}>
                  <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                      Grievance Category <span style={{ color: '#dc2626' }}>*</span>
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%' }}
                      value={grievanceCategory}
                      onChange={e => setGrievanceCategory(e.target.value)}
                    >
                      <option value="DELAY_IN_SANCTION">Delay in Scheme Sanction / Verification</option>
                      <option value="DBT_PAYMENT_FAILURE">Aadhaar Bridge DBT Payment Failure</option>
                      <option value="DOCUMENT_REJECTION">Document Rejection Discrepancy</option>
                      <option value="OFFICE_INQUIRY">Taluk / District Welfare Office Inquiry</option>
                      <option value="OTHER_ASSISTANCE">Other Citizen Assistance</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                      Subject / Brief Summary <span style={{ color: '#dc2626' }}>*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      placeholder="e.g. Verification delay for post-matric hostel application" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={grievanceSubject}
                      onChange={e => setGrievanceSubject(e.target.value)}
                    />
                  </div>

                  <div style={{ marginBottom: '1.25rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                      Detailed Complaint / Explanation <span style={{ color: '#dc2626' }}>*</span>
                    </label>
                    <textarea 
                      required 
                      placeholder="Please specify scheme name, application reference number, and exact issue faced..." 
                      className="filter-input" 
                      style={{ width: '100%', minHeight: '110px' }}
                      value={grievanceDesc}
                      onChange={e => setGrievanceDesc(e.target.value)}
                    />
                  </div>

                  <button 
                    type="submit" 
                    className="btn-orange" 
                    style={{ width: '100%', padding: '0.65rem' }}
                    disabled={grievanceLoading}
                  >
                    {grievanceLoading ? 'Submitting Grievance...' : 'Submit Grievance to SWD'}
                  </button>
                </form>
              </div>

              {/* History Table */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <h4 style={{ color: 'var(--navy-dark)' }}>My Submitted Grievances</h4>
                  <button className="btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }} onClick={() => loadGrievances()}>
                    <RefreshCw size={12} /> Refresh
                  </button>
                </div>

                {grievances.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '2.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                    <p style={{ color: '#64748b', fontSize: '0.85rem' }}>No grievances submitted. Use the form on the left to report any issue.</p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                    {grievances.map(g => (
                      <div key={g.id} style={{ background: '#ffffff', padding: '1.15rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                          <span style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: '0.82rem', color: 'var(--navy-dark)' }}>{g.grievance_number}</span>
                          <span className={\`status-badge \${g.status === 'RESOLVED' ? 'APPROVED' : g.status === 'SUBMITTED' ? 'UNDER_REVIEW' : 'MORE_INFORMATION_REQUIRED'}\`}>
                            {g.status}
                          </span>
                        </div>
                        <h5 style={{ fontSize: '0.9rem', color: 'var(--navy-dark)', marginBottom: '0.3rem' }}>{g.subject}</h5>
                        <p style={{ fontSize: '0.78rem', color: '#475569', marginBottom: '0.6rem' }}>{g.description}</p>
                        
                        {g.officer_response ? (
                          <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '0.6rem 0.75rem', borderRadius: '6px', fontSize: '0.78rem', color: '#166534' }}>
                            <strong>Official Response ({g.resolved_by || 'SWD Cell'}):</strong> {g.officer_response}
                          </div>
                        ) : (
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', fontStyle: 'italic' }}>
                            Under assignment to the jurisdictional Social Welfare Officer.
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
`;

content = content.replace(anchor, officeAndGrievanceViews + "\n" + anchor);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 5 office and grievance views applied successfully");
