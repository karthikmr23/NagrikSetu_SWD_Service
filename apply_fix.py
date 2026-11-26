import sys

filepath = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. State variables
old_state = "  const [platformAuthError, setPlatformAuthError] = useState<string>('');"
new_state = """  const [platformAuthError, setPlatformAuthError] = useState<string>('');
  const [pendingSchemeForApply, setPendingSchemeForApply] = useState<api.Scheme | null>(() => {
    try {
      const saved = sessionStorage.getItem('swd_pending_scheme_apply');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [citizenLoginNotice, setCitizenLoginNotice] = useState<string>(() => {
    return sessionStorage.getItem('swd_pending_scheme_apply')
      ? 'Please sign in with your Citizen account to apply for this scheme.'
      : '';
  });
  const [adminApplyNoticeModal, setAdminApplyNoticeModal] = useState<string | null>(null);"""

if old_state not in text:
    print('ERROR: old_state not found')
    sys.exit(1)
text = text.replace(old_state, new_state, 1)

# 2. useEffect restoration
old_use_effect = """      } else if (userRole === 'CITIZEN') {
        loadMyApplications();
        loadProfileData(token);
      }"""

new_use_effect = """      } else if (userRole === 'CITIZEN') {
        loadMyApplications();
        loadProfileData(token);
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            const parsedScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
            openSchemeApplication(parsedScheme);
          }
        } catch (e) {
          console.error('Failed to restore pending scheme application:', e);
        }
      }"""

if old_use_effect not in text:
    print('ERROR: old_use_effect not found')
    sys.exit(1)
text = text.replace(old_use_effect, new_use_effect, 1)

# 3. handlePortalLogin
old_portal_login = """      } else {
        setActiveTab('swd-home');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);
      }"""

new_portal_login = """      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          openSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }"""

if old_portal_login not in text:
    print('ERROR: old_portal_login not found')
    sys.exit(1)
text = text.replace(old_portal_login, new_portal_login, 1)

# 4. handleDedicatedLogin
old_ded_login = """      } else {
        setActiveTab('swd-home');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);
      }
    } catch (err: any) {"""

new_ded_login = """      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          openSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }
    } catch (err: any) {"""

if old_ded_login not in text:
    print('ERROR: old_ded_login not found')
    sys.exit(1)
text = text.replace(old_ded_login, new_ded_login, 1)

# 5. handleLogin modal
old_modal_login = """      } else {
        setActiveTab('swd-home');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);
      }
    } catch (err: any) {
      setAuthError(err.message || 'Authentication failed. Please verify credentials.');"""

new_modal_login = """      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          openSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }
    } catch (err: any) {
      setAuthError(err.message || 'Authentication failed. Please verify credentials.');"""

if old_modal_login not in text:
    print('ERROR: old_modal_login not found')
    sys.exit(1)
text = text.replace(old_modal_login, new_modal_login, 1)

# 6. openSchemeApplication
old_open_app = """  async function openSchemeApplication(scheme: api.Scheme) {
    setSelectedScheme(scheme);
    setDynamicFormData({});
    setLoadingSchemeForm(true);
    setActiveTab('apply');
    try {
      const formDef = await api.fetchSchemeDynamicForm(scheme.id);
      setSchemeDynamicForm(formDef);
    } catch (err) {
      console.error('Failed to load scheme dynamic form', err);
      setSchemeDynamicForm(null);
    } finally {
      setLoadingSchemeForm(false);
    }
  }"""

new_open_app = """  async function openSchemeApplication(scheme: api.Scheme) {
    // 1. Unauthenticated Visitor Flow: Preserve pending scheme and redirect to Citizen Sign In with clear notice
    if (!token) {
      setSelectedScheme(scheme);
      setPendingSchemeForApply(scheme);
      try {
        sessionStorage.setItem('swd_pending_scheme_apply', JSON.stringify(scheme));
      } catch (e) {
        console.error('Failed to save pending scheme to sessionStorage:', e);
      }
      setCitizenLoginNotice('Please sign in with your Citizen account to apply for this scheme.');
      setActiveTab('sign-in-select');
      return;
    }

    // 2. Administrative Users Restriction: Keep logged in, do not redirect or switch roles, show friendly explanation
    if (userRole !== 'CITIZEN') {
      const roleTitle = (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN')
        ? 'Platform Administrator'
        : 'Government Welfare Officer';
      setAdminApplyNoticeModal(
        `Notice: Scheme applications can only be submitted through a Citizen account. As an authenticated ${roleTitle}, you have administrative and scrutiny permissions only. To submit a welfare scheme application as a beneficiary, please sign in with a registered Citizen account.`
      );
      return;
    }

    // 3. Authenticated Citizen: Directly proceed to Scheme Application Form
    setSelectedScheme(scheme);
    setDynamicFormData({});
    setLoadingSchemeForm(true);
    setActiveTab('apply');
    try {
      const formDef = await api.fetchSchemeDynamicForm(scheme.id);
      setSchemeDynamicForm(formDef);
    } catch (err) {
      console.error('Failed to load scheme dynamic form', err);
      setSchemeDynamicForm(null);
    } finally {
      setLoadingSchemeForm(false);
    }
  }"""

if old_open_app not in text:
    print('ERROR: old_open_app not found')
    sys.exit(1)
text = text.replace(old_open_app, new_open_app, 1)

# 7. SmartSchemeFinderView onApplyScheme callback
old_smart_apply = """            onApplyScheme={(scheme) => {
              setSelectedScheme(scheme);
              setActiveTab('apply');
            }}"""

new_smart_apply = """            onApplyScheme={(scheme) => {
              openSchemeApplication(scheme);
            }}"""

if old_smart_apply not in text:
    print('ERROR: old_smart_apply not found')
    sys.exit(1)
text = text.replace(old_smart_apply, new_smart_apply, 1)

# 8. Render banner inside Citizen Login Card on sign-in-select
old_citizen_card_header = """                  {/* CITIZEN LOGIN FORM */}
                  <div style={{ background: '#fffaf5', border: '1px solid #fed7aa', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>"""

new_citizen_card_header = """                  {/* PENDING SCHEME APPLICATION NOTICE BANNER */}
                  {citizenLoginNotice && (
                    <div style={{
                      backgroundColor: '#eff6ff',
                      border: '1px solid #93c5fd',
                      borderRadius: '8px',
                      padding: '0.85rem 1rem',
                      marginBottom: '1rem',
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.65rem'
                    }}>
                      <AlertCircle size={20} color="#1d4ed8" style={{ marginTop: '0.1rem', flexShrink: 0 }} />
                      <div style={{ flex: 1, fontSize: '0.82rem', color: '#1e3a8a', lineHeight: 1.5 }}>
                        <strong>{citizenLoginNotice}</strong>
                        {pendingSchemeForApply && (
                          <div style={{ marginTop: '0.25rem', fontSize: '0.78rem', color: '#2563eb' }}>
                            Target Scheme: <strong>{pendingSchemeForApply.name}</strong>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* CITIZEN LOGIN FORM */}
                  <div style={{ background: '#fffaf5', border: '1px solid #fed7aa', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>"""

if old_citizen_card_header not in text:
    print('ERROR: old_citizen_card_header not found')
    sys.exit(1)
text = text.replace(old_citizen_card_header, new_citizen_card_header, 1)

# 9. Update the apply view guard (replace technical 403 with friendly notices)
old_apply_guard = """        {/* VIEW: APPLICATION FORM */}
        {activeTab === 'apply' && selectedScheme && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Applications Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Only authenticated <strong>Citizens</strong> are permitted to apply for welfare schemes. Administrative officers cannot submit scheme applications.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>View Schemes</button>
                  <button className="btn-orange" onClick={() => setActiveTab('sign-in-select')}>Citizen Sign In</button>
                </div>
              </div>
            </div>
          ) : ("""

new_apply_guard = """        {/* VIEW: APPLICATION FORM */}
        {activeTab === 'apply' && selectedScheme && (
          !token ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #bfdbfe', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(37, 99, 235, 0.08)' }}>
                <AlertCircle size={52} color="#2563eb" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#1e3a8a', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>Citizen Authentication Required</h3>
                <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Please sign in with your Citizen account to apply for <strong>{selectedScheme.name}</strong>. Your selected scheme will open immediately after signing in.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>Browse Schemes</button>
                  <button className="btn-orange" onClick={() => {
                    setCitizenLoginNotice('Please sign in with your Citizen account to apply for this scheme.');
                    try {
                      sessionStorage.setItem('swd_pending_scheme_apply', JSON.stringify(selectedScheme));
                    } catch {}
                    setPendingSchemeForApply(selectedScheme);
                    setActiveTab('sign-in-select');
                  }}>Citizen Sign In</button>
                </div>
              </div>
            </div>
          ) : userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '540px', margin: '0 auto', background: '#fff', border: '1px solid #fed7aa', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(234, 88, 12, 0.08)' }}>
                <Shield size={52} color="#ea580c" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#9a3412', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>Citizen Account Required for Scheme Applications</h3>
                <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Scheme applications can only be submitted through a Citizen account. As an administrative officer, you can review and scrutinize applications in your portal.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>Return to Catalogue</button>
                  <button className="btn-orange" onClick={() => {
                    if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') {
                      setActiveTab('platform-admin');
                    } else {
                      setActiveTab('gov-welfare-admin');
                    }
                  }}>Open Admin Portal</button>
                </div>
              </div>
            </div>
          ) : ("""

if old_apply_guard not in text:
    print('ERROR: old_apply_guard not found')
    sys.exit(1)
text = text.replace(old_apply_guard, new_apply_guard, 1)

# 10. Admin notice modal dialog
old_dbt_modal = """      {/* BATCH DBT CONFIRMATION MODAL */}"""
new_dbt_modal = """      {/* ADMINISTRATIVE USER APPLY RESTRICTION MODAL */}
      {adminApplyNoticeModal && (
        <div className="modal-overlay" style={{ zIndex: 9999 }}>
          <div className="modal-content" style={{ maxWidth: '520px', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <div style={{
                width: '44px',
                height: '44px',
                borderRadius: '8px',
                backgroundColor: '#fff7ed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <Shield size={24} color="#ea580c" />
              </div>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', margin: 0, fontWeight: 700 }}>
                  Citizen Application Only
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#ea580c', fontWeight: 600 }}>Administrative Access Restriction</span>
              </div>
            </div>

            <p style={{ fontSize: '0.86rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.5rem' }}>
              {adminApplyNoticeModal}
            </p>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                className="btn-primary"
                style={{ padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
                onClick={() => setAdminApplyNoticeModal(null)}
              >
                Understood
              </button>
            </div>
          </div>
        </div>
      )}

      {/* BATCH DBT CONFIRMATION MODAL */}"""

if old_dbt_modal not in text:
    print('ERROR: old_dbt_modal not found')
    sys.exit(1)
text = text.replace(old_dbt_modal, new_dbt_modal, 1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: All 10 replacements successfully written to App.tsx!')
