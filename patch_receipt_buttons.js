const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// 1. In my-applications table, add Receipt button next to Track Dossier
const oldMyAppAction = `                        <td>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem' }}
                            onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                          >
                            Track Dossier &rarr;
                          </button>
                        </td>`;

const newMyAppAction = `                        <td>
                          <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                            <button 
                              className="btn-secondary" 
                              style={{ padding: '0.35rem 0.65rem' }}
                              onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                            >
                              Track Dossier &rarr;
                            </button>
                            <button 
                              className="btn-orange" 
                              style={{ padding: '0.35rem 0.65rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                              onClick={() => downloadReceiptPdf(app.id)}
                              title="Download Official PDF Application Receipt"
                            >
                              <Download size={13} /> Receipt
                            </button>
                          </div>
                        </td>`;

if (content.includes(oldMyAppAction)) {
  content = content.replace(oldMyAppAction, newMyAppAction);
  console.log("Updated my-applications action column with Receipt download button!");
} else {
  console.log("oldMyAppAction string not matched exactly.");
}

// 2. In tracking dossier view, add prominent Download Receipt button in header
const oldTrackingHdr = `          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Dossier Tracking: {selectedApp.application_number}</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Status: <span className={\`status-badge \${selectedApp.status}\`}>{selectedApp.status.replace('_', ' ')}</span></p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to Portfolio</button>
            </div>`;

const newTrackingHdr = `          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Dossier Tracking: {selectedApp.application_number}</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Status: <span className={\`status-badge \${selectedApp.status}\`}>{selectedApp.status.replace('_', ' ')}</span></p>
              </div>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                <button 
                  className="btn-orange" 
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.85rem' }}
                  onClick={() => downloadReceiptPdf(selectedApp.id)}
                >
                  <Download size={15} /> Download Application Receipt (PDF)
                </button>
                <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to Portfolio</button>
              </div>
            </div>`;

if (content.includes(oldTrackingHdr)) {
  content = content.replace(oldTrackingHdr, newTrackingHdr);
  console.log("Updated tracking dossier header with Download Application Receipt button!");
} else {
  console.log("oldTrackingHdr string not matched exactly.");
}

// 3. In the Scrutinize Application modal: Ensure 'Select Action' dropdown has all requested status choices:
// (Under Review, Awaiting Documents, Correction Required, Approve, Reject with reason)
const oldModalActions = `            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Select Action</label>
              <select className="filter-select" style={{ width: '100%' }} value={actionType} onChange={e => setActionType(e.target.value as any)}>
                <option value="APPROVE">Approve & Issue Sanction Mandate</option>
                <option value="REJECT">Reject Application</option>
                <option value="REQUEST_INFO">Request Supplementary Information / Document</option>
              </select>
            </div>`;

const newModalActions = `            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Select Review Decision / Status</label>
              <select className="filter-select" style={{ width: '100%' }} value={actionType} onChange={e => setActionType(e.target.value as any)}>
                <option value="APPROVE">Approve & Issue Sanction Mandate (APPROVED)</option>
                <option value="REJECT">Reject Application (REJECTED)</option>
                <option value="REQUEST_INFO">Request Supplementary Information / Document (Awaiting Documents)</option>
                <option value="UNDER_REVIEW">Mark Application In Scrutiny (Under Review)</option>
                <option value="CORRECTION_REQUIRED">Mark Correction Required by Citizen</option>
              </select>
            </div>`;

if (content.includes(oldModalActions)) {
  content = content.replace(oldModalActions, newModalActions);
  console.log("Updated action modal with all review options!");
}

fs.writeFileSync(filePath, content, "utf8");
console.log("Finished patching buttons!");
