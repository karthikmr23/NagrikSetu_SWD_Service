with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Citizen Profile Guard
old_profile_head = """        {/* VIEW: CITIZEN PROFILE */}
        {activeTab === 'citizen-profile' && ("""

new_profile_head = """        {/* VIEW: CITIZEN PROFILE */}
        {activeTab === 'citizen-profile' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Access Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Citizen profiles can only be accessed by authenticated citizens.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : ("""

old_profile_tail = """                      <span className="status-badge APPROVED" style={{ display: 'inline-block', marginTop: '0.25rem' }}>
                        <CheckCircle size={12} style={{ display: 'inline', marginRight: '4px' }} />
                        Aadhaar Bridge Linked & Active
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}"""

new_profile_tail = """                      <span className="status-badge APPROVED" style={{ display: 'inline-block', marginTop: '0.25rem' }}>
                        <CheckCircle size={12} style={{ display: 'inline', marginRight: '4px' }} />
                        Aadhaar Bridge Linked & Active
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          )
        )}"""

# 2. Tracking Guard
old_tracking_head = """        {/* VIEW: APPLICATION TRACKING & TIMELINE & DOCUMENT UPLOAD */}
        {activeTab === 'tracking' && selectedApp && ("""

new_tracking_head = """        {/* VIEW: APPLICATION TRACKING & TIMELINE & DOCUMENT UPLOAD */}
        {activeTab === 'tracking' && selectedApp && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Tracking Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Detailed citizen dossier tracking is reserved for authenticated citizens. Administrative officers should use the scrutiny queue.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : ("""

old_tracking_tail = """                {/* Uploaded Documents List */}
                <h4 style={{ color: 'var(--navy-dark)', marginTop: '2rem', marginBottom: '0.65rem' }}>Uploaded Files</h4>
                {selectedApp.documents && selectedApp.documents.length > 0 ? (
                  <ul style={{ listStyle: 'none' }}>
                    {selectedApp.documents.map((d: any) => (
                      <li key={d.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#334155', padding: '0.4rem 0', borderBottom: '1px solid #f1f5f9' }}>
                        <FileText size={14} color="#64748b" />
                        <span><strong>{d.document_code}</strong>: {d.file_name} ({Math.round(d.file_size_bytes/1024)} KB)</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>No documents uploaded yet.</p>
                )}
              </div>
            </div>
          </div>
        )}"""

new_tracking_tail = """                {/* Uploaded Documents List */}
                <h4 style={{ color: 'var(--navy-dark)', marginTop: '2rem', marginBottom: '0.65rem' }}>Uploaded Files</h4>
                {selectedApp.documents && selectedApp.documents.length > 0 ? (
                  <ul style={{ listStyle: 'none' }}>
                    {selectedApp.documents.map((d: any) => (
                      <li key={d.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#334155', padding: '0.4rem 0', borderBottom: '1px solid #f1f5f9' }}>
                        <FileText size={14} color="#64748b" />
                        <span><strong>{d.document_code}</strong>: {d.file_name} ({Math.round(d.file_size_bytes/1024)} KB)</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>No documents uploaded yet.</p>
                )}
              </div>
            </div>
          </div>
          )
        )}"""

# 3. Apply form tail
old_apply_tail = """                <button type="submit" className="btn-orange" disabled={loading || !applyConsent}>
                  {loading ? "Submitting Application..." : "Confirm & Submit"}
                </button>
              </div>
            </form>
          </div>
        )}"""

new_apply_tail = """                <button type="submit" className="btn-orange" disabled={loading || !applyConsent}>
                  {loading ? "Submitting Application..." : "Confirm & Submit"}
                </button>
              </div>
            </form>
          </div>
          )
        )}"""

# 4. MY APPLICATIONS HEAD AND TAIL
old_my_apps_head = """        {/* VIEW: CITIZEN MY APPLICATIONS */}
        {activeTab === 'my-applications' && ("""

new_my_apps_head = """        {/* VIEW: CITIZEN MY APPLICATIONS */}
        {activeTab === 'my-applications' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Access Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Only authenticated <strong>Citizens</strong> can view their application portfolio.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : ("""

# Replace
if old_profile_head in text:
    text = text.replace(old_profile_head, new_profile_head)
    print("Replaced old_profile_head")

if old_profile_tail in text:
    text = text.replace(old_profile_tail, new_profile_tail)
    print("Replaced old_profile_tail")

if old_tracking_head in text:
    text = text.replace(old_tracking_head, new_tracking_head)
    print("Replaced old_tracking_head")

if old_tracking_tail in text:
    text = text.replace(old_tracking_tail, new_tracking_tail)
    print("Replaced old_tracking_tail")

if old_apply_tail in text:
    text = text.replace(old_apply_tail, new_apply_tail)
    print("Replaced old_apply_tail")

if old_my_apps_head in text:
    text = text.replace(old_my_apps_head, new_my_apps_head)
    print("Replaced old_my_apps_head")

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated all route guards in App.tsx successfully")
