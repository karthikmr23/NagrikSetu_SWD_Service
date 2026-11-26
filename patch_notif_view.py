app_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace any lingering setActiveTab('my-grievances') with consolidated pattern
content = content.replace("setActiveTab('my-grievances');", "setActiveTab('grievance'); setGrievanceActiveSubTab('track');")
content = content.replace("setActiveTab('my-grievances')", "setActiveTab('grievance'); setGrievanceActiveSubTab('track')")

# Enhance Notifications Full View with navigation handler
old_notif_card = """                  <div 
                    key={n.id} 
                    style={{ 
                      background: '#ffffff', 
                      padding: '1.25rem', 
                      borderRadius: '8px', 
                      border: n.is_read ? '1px solid var(--line)' : '2px solid #bfdbfe',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                      cursor: n.is_read ? 'default' : 'pointer'
                    }}
                    onClick={() => !n.is_read && handleMarkOneRead(n.id)}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {!n.is_read && (
                          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#ea580c' }} />
                        )}
                        <h4 style={{ fontSize: '0.95rem', color: 'var(--navy-dark)', margin: 0 }}>{n.title}</h4>
                      </div>
                      <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                        {new Date(n.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p style={{ fontSize: '0.82rem', color: '#475569', margin: '0.4rem 0 0', lineHeight: 1.5 }}>
                      {n.message}
                    </p>
                  </div>"""

new_notif_card = """                  <div 
                    key={n.id} 
                    style={{ 
                      background: '#ffffff', 
                      padding: '1.25rem', 
                      borderRadius: '8px', 
                      border: n.is_read ? '1px solid var(--line)' : '2px solid #ea580c',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                      cursor: 'pointer',
                      transition: 'border-color 0.15s'
                    }}
                    onClick={() => {
                      if (!n.is_read) handleMarkOneRead(n.id);
                      // Smart deep navigation based on notification context
                      const t = (n.title + ' ' + n.message).toLowerCase();
                      if (t.includes('application') || t.includes('swd-app-') || t.includes('sanction') || t.includes('document')) {
                        setActiveTab('my-applications');
                        loadMyApplications();
                      } else if (t.includes('grievance') || t.includes('complaint')) {
                        setActiveTab('grievance');
                        setGrievanceActiveSubTab('track');
                        loadGrievances();
                      } else if (t.includes('scheme') || t.includes('welfare')) {
                        setActiveTab('schemes');
                        api.fetchSchemes().then(setSchemes);
                      }
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {!n.is_read && (
                          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#ea580c' }} />
                        )}
                        <h4 style={{ fontSize: '0.95rem', color: 'var(--navy-dark)', margin: 0 }}>{n.title}</h4>
                        {!n.is_read && (
                          <span style={{ fontSize: '0.65rem', background: '#ffedd5', color: '#c2410c', padding: '1px 6px', borderRadius: '4px', fontWeight: 700 }}>NEW</span>
                        )}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                          {new Date(n.created_at).toLocaleString()}
                        </span>
                        <span style={{ fontSize: '0.72rem', color: '#ea580c', fontWeight: 600 }}>View Details &rarr;</span>
                      </div>
                    </div>
                    <p style={{ fontSize: '0.82rem', color: '#475569', margin: '0.4rem 0 0', lineHeight: 1.5 }}>
                      {n.message}
                    </p>
                  </div>"""

if old_notif_card in content:
    content = content.replace(old_notif_card, new_notif_card, 1)
    print("Enhanced Notifications full view with smart deep navigation!")
else:
    print("Warning: old_notif_card not found in content!")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved grievance & notification deep linking.")
