with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update activeTab guard on citizen-dashboard
old_citizen_dash = '''        {/* VIEW: CITIZEN DASHBOARD */}
        {activeTab === 'citizen-dashboard' && ('''

new_citizen_dash = '''        {/* VIEW: CITIZEN DASHBOARD */}
        {activeTab === 'citizen-dashboard' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Portal Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  The <strong>Citizen Dashboard</strong> is reserved exclusively for registered citizens. Administrative officers must access their designated Administrative portals.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                  <button className="btn-orange" onClick={() => setActiveTab('sign-in-select')}>Sign In</button>
                </div>
              </div>
            </div>
          ) : ('''

# And close the ternary operator at the end of citizen-dashboard view
old_citizen_dash_end = '''              </table>
            )}
          </div>
        )}'''

new_citizen_dash_end = '''              </table>
            )}
          </div>
          )
        )}'''

# 2. Update activeTab guard on apply form
old_apply_guard = '''        {/* VIEW: APPLICATION FORM */}
        {activeTab === 'apply' && selectedScheme && ('''

new_apply_guard = '''        {/* VIEW: APPLICATION FORM */}
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
          ) : ('''

# And close the ternary at the end of apply view
old_apply_end = '''              </form>
            </div>
          </div>
        )}'''

new_apply_end = '''              </form>
            </div>
          </div>
          )
        )}'''

# 3. Update my-applications guard
old_my_apps = '''        {/* VIEW: MY APPLICATIONS */}
        {activeTab === 'my-applications' && ('''

new_my_apps = '''        {/* VIEW: MY APPLICATIONS */}
        {activeTab === 'my-applications' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Access Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Only authenticated <strong>Citizens</strong> can access this portfolio.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : ('''

old_my_apps_end = '''                </tbody>
              </table>
            )}
          </div>
        )}'''

new_my_apps_end = '''                </tbody>
              </table>
            )}
          </div>
          )
        )}'''

# 4. Strict role separation in Navigation Bar:
# Welfare Officers cannot see Platform Admin
# Platform Admin cannot see Government Welfare Admin
old_nav_gov = '''          {token && (userRole === 'GOVERNMENT_WELFARE_ADMIN' || userRole === 'WELFARE_OFFICER' || userRole === 'ADMINISTRATOR' || userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') && (
            <button 
              className={`nav-link-btn ${activeTab === 'gov-welfare-admin' ? 'active' : ''}`}
              onClick={() => setActiveTab('gov-welfare-admin')}
              style={{ color: '#0284c7', fontWeight: 700 }}
            >
              Government Welfare Admin
            </button>
          )}

          {token && (userRole === 'SWD_ADMIN' || userRole === 'PLATFORM_ADMIN') && (
            <button 
              className={`nav-link-btn ${activeTab === 'platform-admin' ? 'active' : ''}`}
              onClick={() => setActiveTab('platform-admin')}
              style={{ color: '#7c3aed', fontWeight: 700 }}
            >
              Platform Admin
            </button>
          )}'''

new_nav_gov = '''          {token && ['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole) && (
            <button 
              className={`nav-link-btn ${activeTab === 'gov-welfare-admin' ? 'active' : ''}`}
              onClick={() => setActiveTab('gov-welfare-admin')}
              style={{ color: '#0284c7', fontWeight: 700 }}
            >
              Welfare Admin
            </button>
          )}

          {token && ['SWD_ADMIN', 'PLATFORM_ADMIN'].includes(userRole) && (
            <button 
              className={`nav-link-btn ${activeTab === 'platform-admin' ? 'active' : ''}`}
              onClick={() => setActiveTab('platform-admin')}
              style={{ color: '#7c3aed', fontWeight: 700 }}
            >
              Platform Admin
            </button>
          )}'''

# 5. Strict Role Separation in gov-welfare-admin view guard:
# Only Welfare Officers can access Government Welfare Admin dashboard. Platform Admin must NOT access it.
old_gov_guard = "!token || !['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR', 'SWD_ADMIN', 'PLATFORM_ADMIN'].includes(userRole)"
new_gov_guard = "!token || !['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole)"

# 6. Hero "My Dashboard" button:
old_hero_btn = """                      if (userRole === 'SWD_ADMIN') setActiveTab('admin-dashboard');
                      else setActiveTab('citizen-dashboard');"""

new_hero_btn = """                      if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') setActiveTab('platform-admin');
                      else if (['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole)) setActiveTab('gov-welfare-admin');
                      else setActiveTab('citizen-dashboard');"""

# 7. Initial useEffect routing on refresh:
old_init_effect = """    if (token) {
      if (userRole === 'SWD_ADMIN') {
        loadAdminData(token);
      } else if (userRole === 'CITIZEN') {
        loadMyApplications();
        loadProfileData(token);
      }
    }"""

new_init_effect = """    if (token) {
      if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') {
        setActiveTab('platform-admin');
        loadAdminData(token);
      } else if (['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole)) {
        setActiveTab('gov-welfare-admin');
        loadAdminData(token);
      } else if (userRole === 'CITIZEN') {
        loadMyApplications();
        loadProfileData(token);
      }
    }"""

# 8. Server-side logout invalidation in frontend handleLogout:
old_logout = """function handleLogout() {
    setToken('');
    setUserRole('');
    localStorage.clear();
    setActiveTab('swd-home');
  }"""

new_logout = """async function handleLogout() {
    if (token) {
      try {
        await api.logoutUser(token);
      } catch (err) {
        console.error('Logout invalidation note:', err);
      }
    }
    setToken('');
    setUserRole('');
    setCitizenId('');
    setUserName('');
    localStorage.clear();
    setActiveTab('swd-home');
  }"""

# Execute replacements
changes = [
    (old_citizen_dash, new_citizen_dash, "citizen_dash guard"),
    (old_citizen_dash_end, new_citizen_dash_end, "citizen_dash end"),
    (old_apply_guard, new_apply_guard, "apply guard"),
    (old_apply_end, new_apply_end, "apply end"),
    (old_my_apps, new_my_apps, "my_apps guard"),
    (old_my_apps_end, new_my_apps_end, "my_apps end"),
    (old_nav_gov, new_nav_gov, "nav gov/platform isolation"),
    (old_gov_guard, new_gov_guard, "gov_guard role restriction"),
    (old_hero_btn, new_hero_btn, "hero dashboard button routing"),
    (old_init_effect, new_init_effect, "initial useEffect role recovery"),
    (old_logout, new_logout, "server-side logout call")
]

for old, new, label in changes:
    if old in text:
        text = text.replace(old, new)
        print(f"Applied: {label}")
    else:
        print(f"FAILED: {label}")

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated App.tsx with strict frontend role guards")
