app_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate start of grievance view and end of my-grievances view
start_marker = "{/* VIEW: CITIZEN GRIEVANCE (REGISTER FORM ONLY) */}"
end_marker = "{/* VIEW: CITIZEN NOTIFICATIONS (FULL VIEW) */}"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

print(f"Start index: {idx_start}, End index: {idx_end}")

consolidated_grievance_view = """{/* VIEW: CONSOLIDATED CITIZEN GRIEVANCES (SUBMISSION & STATUS TRACKING) */}
        {(activeTab === 'grievance' || activeTab === 'my-grievances') && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Citizen Grievance Redressal Portal</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Submit complaints, track ticket investigation status, review official responses, and inspect resolution history.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  className={grievanceActiveSubTab === 'track' ? 'btn-orange' : 'btn-secondary'} 
                  onClick={() => { setGrievanceActiveSubTab('track'); loadGrievances(); }}
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.82rem' }}
                >
                  <FileText size={14} /> My Submitted Grievances ({grievances.length})
                </button>
                <button 
                  className={grievanceActiveSubTab === 'submit' ? 'btn-orange' : 'btn-secondary'} 
                  onClick={() => setGrievanceActiveSubTab('submit')}
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.82rem' }}
                >
                  <Send size={14} /> + Submit New Grievance
                </button>
                <button className="btn-secondary" onClick={() => loadGrievances()} title="Refresh Tickets">
                  <RefreshCw size={14} />
                </button>
                <button className="btn-secondary" onClick={() => setActiveTab('citizen-dashboard')}>
                  &larr; Dashboard
                </button>
              </div>
            </div>

            {/* Sub-tab Navigation Banner */}
            <div style={{ display: 'flex', borderBottom: '2px solid var(--line)', marginBottom: '1.5rem', gap: '1rem' }}>
              <button
                type="button"
                onClick={() => { setGrievanceActiveSubTab('track'); loadGrievances(); }}
                style={{
                  padding: '0.65rem 1.25rem',
                  background: 'none',
                  border: 'none',
                  borderBottom: grievanceActiveSubTab === 'track' ? '3px solid #ea580c' : '3px solid transparent',
                  color: grievanceActiveSubTab === 'track' ? '#ea580c' : '#475569',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem'
                }}
              >
                <FileCheck size={16} /> My Grievances & Status Tracking ({grievances.length})
              </button>
              <button
                type="button"
                onClick={() => setGrievanceActiveSubTab('submit')}
                style={{
                  padding: '0.65rem 1.25rem',
                  background: 'none',
                  border: 'none',
                  borderBottom: grievanceActiveSubTab === 'submit' ? '3px solid #ea580c' : '3px solid transparent',
                  color: grievanceActiveSubTab === 'submit' ? '#ea580c' : '#475569',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem'
                }}
              >
                <MessageSquare size={16} /> Register New Complaint
              </button>
            </div>

            {/* TAB 1: MY SUBMITTED GRIEVANCES & STATUS TRACKING */}
            {grievanceActiveSubTab === 'track' && (
              <div>
                {grievances.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '3.5rem 1.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                    <p style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1rem' }}>No grievances submitted yet.</p>
                    <button className="btn-orange" onClick={() => setGrievanceActiveSubTab('submit')}>
                      Submit Your First Grievance
                    </button>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {grievances.map(g => (
                      <div key={g.id} style={{ background: '#ffffff', padding: '1.25rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                            <span style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: '0.85rem', color: 'var(--navy-dark)' }}>{g.grievance_number}</span>
                            <span style={{ fontSize: '0.72rem', color: '#64748b', background: '#f1f5f9', padding: '2px 8px', borderRadius: '4px' }}>
                              {(g.category || '').replace('_', ' ')}
                            </span>
                          </div>
                          <span className={`status-badge ${g.status === 'RESOLVED' ? 'APPROVED' : g.status === 'SUBMITTED' ? 'UNDER_REVIEW' : 'MORE_INFORMATION_REQUIRED'}`}>
                            {g.status}
                          </span>
                        </div>
                        <h5 style={{ fontSize: '0.95rem', color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>{g.subject}</h5>
                        <p style={{ fontSize: '0.82rem', color: '#475569', marginBottom: '0.75rem', lineHeight: 1.5 }}>{g.description}</p>
                        
                        {g.officer_response ? (
                          <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', color: '#166534', marginTop: '0.5rem' }}>
                            <strong>Official Resolution ({g.resolved_by || 'Jurisdictional Welfare Officer'}):</strong> {g.officer_response}
                          </div>
                        ) : (
                          <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontStyle: 'italic', background: '#f8fafc', padding: '0.5rem 0.75rem', borderRadius: '4px' }}>
                            Status: Under review by jurisdictional Social Welfare Officer. You will receive an update once reviewed.
                          </div>
                        )}

                        <div style={{ marginTop: '0.65rem', paddingTop: '0.5rem', borderTop: '1px solid #f8fafc', fontSize: '0.72rem', color: '#94a3b8', display: 'flex', justifyContent: 'space-between' }}>
                          <span>Submitted: {new Date(g.created_at).toLocaleString()}</span>
                          {g.updated_at && <span>Last Updated: {new Date(g.updated_at).toLocaleString()}</span>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: REGISTER NEW GRIEVANCE */}
            {grievanceActiveSubTab === 'submit' && (
              <div style={{ maxWidth: '780px', margin: '0 auto' }}>
                <div style={{ background: '#ffffff', padding: '1.75rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                  <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                    Register New Grievance Ticket
                  </h4>

                  {grievanceSuccessMsg && (
                    <div style={{ backgroundColor: '#ecfdf5', color: '#065f46', padding: '0.85rem 1rem', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <CheckCircle size={18} />
                        <span>{grievanceSuccessMsg}</span>
                      </div>
                      <button 
                        className="btn-orange" 
                        style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
                        onClick={() => { setGrievanceActiveSubTab('track'); loadGrievances(); }}
                      >
                        Track Ticket &rarr;
                      </button>
                    </div>
                  )}

                  {grievanceErrorMsg && (
                    <div style={{ backgroundColor: '#fee2e2', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <AlertCircle size={16} />
                      <span>{grievanceErrorMsg}</span>
                    </div>
                  )}

                  <form onSubmit={async (e) => {
                    await handleGrievanceSubmit(e);
                    setGrievanceActiveSubTab('track');
                  }}>
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
                        <option value="APPLICATION_DELAY">Application delay</option>
                        <option value="REJECTION_DISPUTE">Application rejection dispute</option>
                        <option value="DOCUMENT_ISSUE">Document-related issue</option>
                        <option value="SCHEME_INFO_ISSUE">Scheme information issue</option>
                        <option value="TECHNICAL_ISSUE">Technical issue</option>
                        <option value="OTHER">Other</option>
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
                        style={{ width: '100%', minHeight: '120px' }}
                        value={grievanceDesc}
                        onChange={e => setGrievanceDesc(e.target.value)}
                      />
                    </div>

                    <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                      <button 
                        type="button" 
                        className="btn-secondary"
                        onClick={() => {
                          setGrievanceSubject('');
                          setGrievanceDesc('');
                          setGrievanceErrorMsg('');
                        }}
                      >
                        Clear
                      </button>
                      <button 
                        type="submit" 
                        className="btn-orange" 
                        style={{ padding: '0.65rem 1.5rem', fontWeight: 700 }}
                        disabled={grievanceLoading}
                      >
                        {grievanceLoading ? 'Submitting Grievance...' : 'Submit Grievance Ticket'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        """

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + consolidated_grievance_view + content[idx_end:]
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully consolidated Grievance views!")
else:
    print("Error: Could not locate markers in content!")
