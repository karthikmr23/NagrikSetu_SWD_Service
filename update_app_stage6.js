const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// 1. In my-applications table, add the Download Application Receipt button
const oldMyAppsAction = `<button 
                          className="btn-secondary" 
                          style={{ padding: '0.35rem 0.65rem' }}
                          onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                        >
                          Track Dossier &rarr;
                        </button>`;

const newMyAppsAction = `<div style={{ display: 'flex', gap: '0.4rem' }}>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem' }}
                            onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                          >
                            Track Dossier &rarr;
                          </button>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem', color: '#1d4ed8' }}
                            onClick={() => downloadReceiptPdf(app.id)}
                            title="Download Official PDF Acknowledgement Receipt"
                          >
                            <Download size={13} /> Receipt
                          </button>
                        </div>`;

content = content.replace(oldMyAppsAction, newMyAppsAction);

// 2. In tracking dossier view, add prominent Download Official PDF Receipt button in the header
const oldTrackingHeader = `              <div className="swd-view-header">
                <div>
                  <h2>Dossier Tracking: {selectedApp.application_number}</h2>
                  <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Status: <span className={\`status-badge \${selectedApp.status}\`}>{selectedApp.status.replace('_', ' ')}</span></p>
                </div>
                <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to Portfolio</button>
              </div>`;

const newTrackingHeader = `              <div className="swd-view-header">
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
                    <Download size={14} /> Download Application Receipt (PDF)
                  </button>
                  <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to Portfolio</button>
                </div>
              </div>`;

content = content.replace(oldTrackingHeader, newTrackingHeader);

// 3. In the second occurrence of tracking view (if any):
content = content.replace(
`              <div className="swd-view-header">
                <div>
                  <h2>Dossier Tracking: {selectedApp.application_number}</h2>
                  <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Status: <span className={\`status-badge \${selectedApp.status}\`}>{selectedApp.status.replace('_', ' ')}</span></p>
                </div>
                <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to Portfolio</button>
              </div>`,
newTrackingHeader
);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 6 PDF buttons added successfully");
