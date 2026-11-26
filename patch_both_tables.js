const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// Occurrence 1: in Citizen Dashboard table
const occ1 = `<button 
                          className="btn-secondary" 
                          style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
                          onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                        >
                          Track Dossier &rarr;
                        </button>`;

const rep1 = `<div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
                            onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                          >
                            Track Dossier &rarr;
                          </button>
                          <button 
                            className="btn-orange" 
                            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                            onClick={() => downloadReceiptPdf(app.id)}
                            title="Download Official Application Receipt"
                          >
                            <Download size={13} /> Receipt
                          </button>
                        </div>`;

// Occurrence 2: in My Applications Portfolio table
const occ2 = `<button 
                          className="btn-secondary" 
                          style={{ padding: '0.35rem 0.65rem' }}
                          onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                        >
                          Track Dossier &rarr;
                        </button>`;

const rep2 = `<div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
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
                            title="Download Official Application Receipt"
                          >
                            <Download size={13} /> Receipt
                          </button>
                        </div>`;

content = content.replace(occ1, rep1);
content = content.replace(occ2, rep2);

fs.writeFileSync(filePath, content, "utf8");
console.log("Successfully added receipt buttons to both citizen application tables!");
