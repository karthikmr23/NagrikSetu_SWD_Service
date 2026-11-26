const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);

console.log("Total lines:", lines.length);

// Find index where `{!token ? (` begins after line 850
let guestStartIndex = -1;
for (let i = 850; i < lines.length && i < 1100; i++) {
  if (lines[i].includes("{!token ? (")) {
    guestStartIndex = i;
    break;
  }
}

console.log("guestStartIndex:", guestStartIndex);

if (guestStartIndex !== -1) {
  // Find where `) : (` happens
  let guestEndIndex = -1;
  for (let j = guestStartIndex; j < guestStartIndex + 50; j++) {
    if (lines[j].includes(") : (")) {
      guestEndIndex = j;
      break;
    }
  }

  console.log("guestEndIndex:", guestEndIndex);

  // Replacement for guest navigation:
  const newGuestLines = [
    `          <button `,
    `            className={\`nav-link-btn \${activeTab === 'office-locator' ? 'active' : ''}\`}`,
    `            onClick={() => { setActiveTab('office-locator'); loadOffices(); }}`,
    `          >`,
    `            <Building2 size={14} style={{ display: 'inline', marginRight: '4px' }} /> Office Locator`,
    `          </button>`,
    ``,
    `          {token && userRole === 'CITIZEN' && (`,
    `            <button `,
    `              className={\`nav-link-btn \${activeTab === 'grievance' ? 'active' : ''}\`}`,
    `              onClick={() => { setActiveTab('grievance'); loadGrievances(); }}`,
    `            >`,
    `              <MessageSquare size={14} style={{ display: 'inline', marginRight: '4px' }} /> Grievance Desk`,
    `            </button>`,
    `          )}`,
    ``,
    `          {!token ? (`,
    `            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginLeft: '0.5rem' }}>`,
    `              <button `,
    `                className={\`btn-header-navy \${activeTab === 'sign-in-select' || activeTab === 'citizen-login' || activeTab === 'admin-login' ? 'active' : ''}\`}`,
    `                style={{ fontWeight: 700, padding: '0.5rem 1.1rem', backgroundColor: 'var(--navy-dark)', color: '#ffffff', borderRadius: '6px', display: 'flex', alignItems: 'center', gap: '0.4rem' }}`,
    `                onClick={() => {`,
    `                  setAuthError('');`,
    `                  setActiveTab('sign-in-select');`,
    `                }}`,
    `              >`,
    `                <LogIn size={15} /> Sign In`,
    `              </button>`,
    `            </div>`,
    `          ) : (`
  ];

  lines.splice(guestStartIndex, (guestEndIndex - guestStartIndex + 1), ...newGuestLines);
  console.log("Guest navbar replaced!");
}

// Now find user block for Notification Bell
let userBlockIndex = -1;
for (let i = 850; i < lines.length && i < 1100; i++) {
  if (lines[i].includes("<div style={{ textAlign: 'right' }}>") && lines[i-1] && lines[i-1].includes("alignItems: 'center', gap: '0.75rem'")) {
    userBlockIndex = i;
    break;
  }
}

console.log("userBlockIndex:", userBlockIndex);

if (userBlockIndex !== -1) {
  const bellLines = [
    `              {/* Notification Centre Bell */} `,
    `              <div style={{ position: 'relative' }}>`,
    `                <button`,
    `                  type="button"`,
    `                  onClick={() => {`,
    `                    setShowNotificationsDropdown(!showNotificationsDropdown);`,
    `                    if (!showNotificationsDropdown) loadNotifications();`,
    `                  }}`,
    `                  style={{`,
    `                    position: 'relative',`,
    `                    background: '#f1f5f9',`,
    `                    border: '1px solid #cbd5e1',`,
    `                    borderRadius: '50%',`,
    `                    width: '36px',`,
    `                    height: '36px',`,
    `                    display: 'flex',`,
    `                    alignItems: 'center',`,
    `                    justifyContent: 'center',`,
    `                    cursor: 'pointer',`,
    `                    color: 'var(--navy-dark)'`,
    `                  }}`,
    `                  title="View Notifications"`,
    `                >`,
    `                  <Bell size={18} />`,
    `                  {notifications.filter(n => !n.is_read).length > 0 && (`,
    `                    <span style={{`,
    `                      position: 'absolute',`,
    `                      top: '-4px',`,
    `                      right: '-4px',`,
    `                      background: '#ea580c',`,
    `                      color: '#ffffff',`,
    `                      borderRadius: '50%',`,
    `                      width: '18px',`,
    `                      height: '18px',`,
    `                      fontSize: '0.68rem',`,
    `                      fontWeight: 800,`,
    `                      display: 'flex',`,
    `                      alignItems: 'center',`,
    `                      justifyContent: 'center'`,
    `                    }}>`,
    `                      {notifications.filter(n => !n.is_read).length}`,
    `                    </span>`,
    `                  )}`,
    `                </button>`,
    `                {showNotificationsDropdown && (`,
    `                  <div style={{`,
    `                    position: 'absolute',`,
    `                    right: 0,`,
    `                    top: '44px',`,
    `                    width: '340px',`,
    `                    background: '#ffffff',`,
    `                    border: '1px solid var(--line)',`,
    `                    borderRadius: '8px',`,
    `                    boxShadow: '0 10px 25px rgba(0,0,0,0.15)',`,
    `                    zIndex: 1000,`,
    `                    overflow: 'hidden'`,
    `                  }}>`,
    `                    <div style={{ padding: '0.75rem 1rem', background: 'var(--navy-dark)', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>`,
    `                      <div style={{ fontWeight: 700, fontSize: '0.85rem' }}>Notifications ({notifications.filter(n => !n.is_read).length} unread)</div>`,
    `                      {notifications.some(n => !n.is_read) && (`,
    `                        <button type="button" onClick={handleMarkAllRead} style={{ background: 'transparent', border: 'none', color: '#fed7aa', fontSize: '0.72rem', cursor: 'pointer', textDecoration: 'underline' }}>Mark all read</button>`,
    `                      )}`,
    `                    </div>`,
    `                    <div style={{ maxHeight: '320px', overflowY: 'auto' }}>`,
    `                      {notifications.length === 0 ? (`,
    `                        <div style={{ padding: '1.5rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.8rem' }}>No notifications yet.</div>`,
    `                      ) : (`,
    `                        notifications.map(n => (`,
    `                          <div key={n.id} style={{ padding: '0.75rem 1rem', borderBottom: '1px solid #f1f5f9', backgroundColor: n.is_read ? '#ffffff' : '#f8fafc', cursor: 'pointer' }} onClick={() => !n.is_read && handleMarkOneRead(n.id)}>`,
    `                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.2rem' }}>`,
    `                              <span style={{ fontWeight: 700, fontSize: '0.8rem', color: 'var(--navy-dark)' }}>{n.title}</span>`,
    `                              <span style={{ fontSize: '0.68rem', color: '#94a3b8' }}>{new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>`,
    `                            </div>`,
    `                            <p style={{ fontSize: '0.75rem', color: '#475569', margin: 0, lineHeight: 1.4 }}>{n.message}</p>`,
    `                          </div>`,
    `                        ))`,
    `                      )}`,
    `                    </div>`,
    `                  </div>`,
    `                )}`,
    `              </div>`
  ];

  lines.splice(userBlockIndex, 0, ...bellLines);
  console.log("Bell component inserted!");
}

fs.writeFileSync(filePath, lines.join("\n"), "utf8");
console.log("File saved with precision splice!");
