import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\GovernmentWelfareAdminPortal.tsx"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add state variables for announcement form
state_target = "  const [builderLoading, setBuilderLoading] = useState<boolean>(false);"
state_addition = """  const [builderLoading, setBuilderLoading] = useState<boolean>(false);

  // Department Announcement Broadcast State
  const [announcementTitle, setAnnouncementTitle] = useState<string>('');
  const [announcementMsg, setAnnouncementMsg] = useState<string>('');
  const [announcementType, setAnnouncementType] = useState<string>('INFO');
  const [announcementTargetRole, setAnnouncementTargetRole] = useState<string>('CITIZEN');
  const [announcementStatus, setAnnouncementStatus] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [announcementLoading, setAnnouncementLoading] = useState<boolean>(false);

  async function handleBroadcastAnnouncement(e: React.FormEvent) {
    e.preventDefault();
    if (!announcementTitle.trim() || !announcementMsg.trim()) {
      setAnnouncementStatus({ type: 'error', text: 'Please fill in both announcement title and message content.' });
      return;
    }
    try {
      setAnnouncementLoading(true);
      setAnnouncementStatus(null);
      const res = await api.publishAnnouncement({
        title: announcementTitle.trim(),
        message: announcementMsg.trim(),
        announcement_type: announcementType,
        target_role: announcementTargetRole
      }, token);
      setAnnouncementStatus({ type: 'success', text: res.message || 'Official announcement broadcast successfully to registered citizens!' });
      setAnnouncementTitle('');
      setAnnouncementMsg('');
    } catch (err: any) {
      setAnnouncementStatus({ type: 'error', text: err.message || 'Failed to broadcast announcement.' });
    } finally {
      setAnnouncementLoading(false);
    }
  }"""

assert state_target in code, "state_target not found in GovernmentWelfareAdminPortal.tsx"
code = code.replace(state_target, state_addition)

# 2. Add Broadcast Form to TAB 12 (Notifications)
notif_tab_target = """        {/* TAB 12: NOTIFICATIONS */}
        {activeTab === 'notifications' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Departmental Notifications & Advisories
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  System updates, scrutiny reminders, and policy notices issued for welfare officers.
                </p>
              </div>
            </div>"""

notif_tab_replacement = """        {/* TAB 12: NOTIFICATIONS */}
        {activeTab === 'notifications' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Departmental Announcements & Notifications
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Publish official government announcements to citizens and review administrative advisories.
                </p>
              </div>
            </div>

            {/* BROADCAST NEW ANNOUNCEMENT FORM */}
            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 6px rgba(0,0,0,0.03)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.6rem' }}>
                <Bell size={18} color="var(--accent-saffron)" />
                <h4 style={{ margin: 0, color: 'var(--navy-dark)', fontSize: '0.98rem' }}>Broadcast Official Announcement to Citizens</h4>
              </div>

              {announcementStatus && (
                <div style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '6px',
                  marginBottom: '1rem',
                  fontSize: '0.82rem',
                  backgroundColor: announcementStatus.type === 'success' ? '#ecfdf5' : '#fef2f2',
                  color: announcementStatus.type === 'success' ? '#065f46' : '#991b1b',
                  border: `1px solid ${announcementStatus.type === 'success' ? '#a7f3d0' : '#fecaca'}`
                }}>
                  {announcementStatus.text}
                </div>
              )}

              <form onSubmit={handleBroadcastAnnouncement} style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                      Announcement Title *
                    </label>
                    <input
                      type="text"
                      placeholder="e.g. FY 2026-27 Post-Matric Scholarship Applications Open"
                      value={announcementTitle}
                      onChange={(e) => setAnnouncementTitle(e.target.value)}
                      style={{ width: '100%', padding: '0.6rem 0.85rem', fontSize: '0.82rem', borderRadius: '6px', border: '1px solid var(--line)' }}
                      required
                    />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                      Notification Severity / Priority
                    </label>
                    <select
                      value={announcementType}
                      onChange={(e) => setAnnouncementType(e.target.value)}
                      style={{ width: '100%', padding: '0.6rem 0.85rem', fontSize: '0.82rem', borderRadius: '6px', border: '1px solid var(--line)' }}
                    >
                      <option value="INFO">General Information (INFO)</option>
                      <option value="SUCCESS">Welfare Launch / Grant (SUCCESS)</option>
                      <option value="WARNING">Important Deadline / Advisory (WARNING)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                    Official Announcement Details *
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Enter the full announcement text that will be persisted in MySQL and delivered directly to citizens' notification inbox..."
                    value={announcementMsg}
                    onChange={(e) => setAnnouncementMsg(e.target.value)}
                    style={{ width: '100%', padding: '0.6rem 0.85rem', fontSize: '0.82rem', borderRadius: '6px', border: '1px solid var(--line)', resize: 'vertical' }}
                    required
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.6rem' }}>
                  <button
                    type="submit"
                    className="btn-orange"
                    disabled={announcementLoading}
                    style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.6rem 1.25rem', fontWeight: 600 }}
                  >
                    <Send size={14} /> {announcementLoading ? 'Broadcasting...' : 'Publish & Dispatch Notifications'}
                  </button>
                </div>
              </form>
            </div>"""

assert notif_tab_target in code, "notif_tab_target not found in GovernmentWelfareAdminPortal.tsx"
code = code.replace(notif_tab_target, notif_tab_replacement)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("GovernmentWelfareAdminPortal.tsx successfully updated with announcement broadcasting form!")
