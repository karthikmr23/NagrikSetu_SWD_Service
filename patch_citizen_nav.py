app_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Exact old nav block
target_old_nav = """          ) : userRole === 'CITIZEN' ? (
            /* EXACT 11 CITIZEN NAVIGATION OPTIONS */
            <>
              {/* 1. Dashboard */}
              <button 
                className={`nav-link-btn ${activeTab === 'citizen-dashboard' ? 'active' : ''}`}
                onClick={() => { setActiveTab('citizen-dashboard'); loadMyApplications(); }}
              >
                Dashboard
              </button>

              {/* 2. Welfare Schemes */}
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' || activeTab === 'scheme-detail' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Welfare Schemes
              </button>

              {/* 3. Eligibility Checker */}
              <button 
                className={`nav-link-btn ${activeTab === 'eligibility' ? 'active' : ''}`}
                onClick={() => setActiveTab('eligibility')}
              >
                Eligibility Checker
              </button>

              {/* 4. Smart Scheme Finder */}
              <button
                className={`nav-link-btn ${activeTab === 'smart-finder' ? 'active' : ''}`}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: activeTab === 'smart-finder' ? '#ea580c' : '#0f2444', fontWeight: 600 }}
                onClick={openSmartFinder}
              >
                <Sparkles size={14} color="#ea580c" /> Smart Scheme Finder
              </button>

              {/* 5. My Applications (Tracking is strictly inside this page) */}
              <button 
                className={`nav-link-btn ${activeTab === 'my-applications' || activeTab === 'tracking' ? 'active' : ''}`}
                onClick={() => { setActiveTab('my-applications'); loadMyApplications(); }}
              >
                My Applications
              </button>

              {/* 6. Grievances (Register new complaint) */}
              <button 
                className={`nav-link-btn ${activeTab === 'grievance' ? 'active' : ''}`}
                onClick={() => { setActiveTab('grievance'); loadGrievances(); }}
              >
                Grievances
              </button>

              {/* 7. My Grievances (Track submitted tickets) */}
              <button 
                className={`nav-link-btn ${activeTab === 'my-grievances' ? 'active' : ''}`}
                onClick={() => { setActiveTab('my-grievances'); loadGrievances(); }}
              >
                My Grievances
              </button>

              {/* 8. Office Locator */}
              <button 
                className={`nav-link-btn ${activeTab === 'office-locator' ? 'active' : ''}`}
                onClick={() => { setActiveTab('office-locator'); loadOffices(); }}
              >
                Office Locator
              </button>

              {/* 9. Notifications */}
              <button 
                className={`nav-link-btn ${activeTab === 'notifications-view' ? 'active' : ''}`}
                onClick={() => { setActiveTab('notifications-view'); loadNotifications(); }}
                style={{ position: 'relative' }}
              >
                Notifications
                {notifications.filter(n => !n.is_read).length > 0 && (
                  <span style={{
                    marginLeft: '5px',
                    background: '#ea580c',
                    color: '#ffffff',
                    borderRadius: '10px',
                    padding: '1px 6px',
                    fontSize: '0.68rem',
                    fontWeight: 700
                  }}>
                    {notifications.filter(n => !n.is_read).length}
                  </span>
                )}
              </button>

              {/* 10. My Profile */}
              <button 
                className={`nav-link-btn ${activeTab === 'citizen-profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('citizen-profile')}
              >
                My Profile
              </button>

              {/* Profile & Notifications Bell Widget */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginLeft: '0.5rem' }}>"""

target_new_nav = """          ) : userRole === 'CITIZEN' ? (
            /* EXACT 9 PRIMARY CITIZEN NAVIGATION OPTIONS */
            <>
              {/* 1. Home */}
              <button 
                className={`nav-link-btn ${activeTab === 'swd-home' ? 'active' : ''}`}
                onClick={() => setActiveTab('swd-home')}
              >
                Home
              </button>

              {/* 2. Welfare Schemes */}
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' || activeTab === 'scheme-detail' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Welfare Schemes
              </button>

              {/* 3. Eligibility Checker */}
              <button 
                className={`nav-link-btn ${activeTab === 'eligibility' ? 'active' : ''}`}
                onClick={() => setActiveTab('eligibility')}
              >
                Eligibility Checker
              </button>

              {/* 4. Smart Scheme Finder */}
              <button
                className={`nav-link-btn ${activeTab === 'smart-finder' ? 'active' : ''}`}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: activeTab === 'smart-finder' ? '#ea580c' : '#0f2444', fontWeight: 600 }}
                onClick={openSmartFinder}
              >
                <Sparkles size={14} color="#ea580c" /> Smart Scheme Finder
              </button>

              {/* 5. My Applications (Tracking is strictly inside this page) */}
              <button 
                className={`nav-link-btn ${activeTab === 'my-applications' || activeTab === 'tracking' ? 'active' : ''}`}
                onClick={() => { setActiveTab('my-applications'); loadMyApplications(); }}
              >
                My Applications
              </button>

              {/* 6. Grievances (Consolidated: New Submission + Tracking) */}
              <button 
                className={`nav-link-btn ${activeTab === 'grievance' || activeTab === 'my-grievances' ? 'active' : ''}`}
                onClick={() => { setActiveTab('grievance'); loadGrievances(); }}
              >
                Grievances
              </button>

              {/* 7. Office Locator */}
              <button 
                className={`nav-link-btn ${activeTab === 'office-locator' ? 'active' : ''}`}
                onClick={() => { setActiveTab('office-locator'); loadOffices(); }}
              >
                Office Locator
              </button>

              {/* 8. Notifications */}
              <button 
                className={`nav-link-btn ${activeTab === 'notifications-view' ? 'active' : ''}`}
                onClick={() => { setActiveTab('notifications-view'); loadNotifications(); }}
                style={{ position: 'relative' }}
              >
                Notifications
                {notifications.filter(n => !n.is_read).length > 0 && (
                  <span style={{
                    marginLeft: '5px',
                    background: '#ea580c',
                    color: '#ffffff',
                    borderRadius: '10px',
                    padding: '1px 6px',
                    fontSize: '0.68rem',
                    fontWeight: 700
                  }}>
                    {notifications.filter(n => !n.is_read).length}
                  </span>
                )}
              </button>

              {/* 9. My Profile */}
              <button 
                className={`nav-link-btn ${activeTab === 'citizen-profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('citizen-profile')}
              >
                My Profile
              </button>

              {/* Profile & Header Action Controls: Citizen Dashboard Shortcut + Notification Bell + User Badge */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginLeft: '0.5rem' }}>
                {/* Visible Citizen Dashboard Shortcut */}
                <button
                  type="button"
                  className={`btn-header-orange ${activeTab === 'citizen-dashboard' ? 'active' : ''}`}
                  style={{
                    backgroundColor: activeTab === 'citizen-dashboard' ? 'var(--navy-dark)' : '#ea580c',
                    color: '#ffffff',
                    padding: '0.38rem 0.75rem',
                    fontSize: '0.78rem',
                    fontWeight: 700,
                    borderRadius: '6px',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    border: 'none',
                    cursor: 'pointer'
                  }}
                  onClick={() => { setActiveTab('citizen-dashboard'); loadMyApplications(); }}
                  title="Open Citizen Dashboard"
                >
                  <User size={13} /> Dashboard
                </button>"""

if target_old_nav in content:
    content = content.replace(target_old_nav, target_new_nav, 1)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced Citizen Navigation with 9 primary items + Dashboard shortcut button!")
else:
    print("Error: target_old_nav not found!")
