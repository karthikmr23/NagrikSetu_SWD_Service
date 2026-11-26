const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// Locate the actionModalApp select
const oldModalSelect = `            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Select Action</label>
              <select className="filter-select" style={{ width: '100%' }} value={actionType} onChange={e => setActionType(e.target.value as any)}>
                <option value="APPROVE">Approve & Issue Sanction Mandate</option>
                <option value="REJECT">Reject Application</option>
                <option value="REQUEST_INFO">Request Supplementary Information / Document</option>
              </select>
            </div>`;

const newModalSelect = `            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Select Review Decision / Status</label>
              <select className="filter-select" style={{ width: '100%' }} value={actionType} onChange={e => setActionType(e.target.value as any)}>
                <option value="APPROVE">Approve & Issue Sanction Mandate (APPROVED)</option>
                <option value="REJECT">Reject Application (REJECTED)</option>
                <option value="REQUEST_INFO">Request Information / Documents (Awaiting Documents)</option>
                <option value="UNDER_REVIEW">Mark In Scrutiny (UNDER_REVIEW)</option>
                <option value="CORRECTION_REQUIRED">Mark Correction Required</option>
              </select>
            </div>`;

content = content.replace(oldModalSelect, newModalSelect);

// Now update handleAdminActionSubmit
const oldActionHandler = `  async function handleAdminActionSubmit() {
    if (!actionModalApp || !token) return;
    try {
      if (actionType === 'REQUEST_INFO') {
        await api.requestAdminInformation(actionModalApp.id, actionRemarks, token);
      } else {
        await api.recordAdminDecision(
          actionModalApp.id,
          actionType === 'APPROVE' ? 'APPROVED' : 'REJECTED',
          actionRemarks,
          actionType === 'APPROVE' ? actionSanctionAmount : undefined,
          token
        );
      }
      setActionModalApp(null);
      setActionRemarks('');
      loadAdminData(token);
    } catch (err: any) {
      alert(err.message);
    }
  }`;

const newActionHandler = `  async function handleAdminActionSubmit() {
    if (!actionModalApp || !token) return;
    try {
      if (actionType === 'REQUEST_INFO') {
        await api.requestAdminInformation(actionModalApp.id, actionRemarks, token);
      } else {
        let decStatus = 'APPROVED';
        if (actionType === 'REJECT') decStatus = 'REJECTED';
        else if (actionType === 'UNDER_REVIEW') decStatus = 'UNDER_REVIEW';
        else if (actionType === 'CORRECTION_REQUIRED') decStatus = 'CORRECTION_REQUIRED';
        else decStatus = 'APPROVED';

        await api.recordAdminDecision(
          actionModalApp.id,
          decStatus,
          actionRemarks,
          actionType === 'APPROVE' ? actionSanctionAmount : undefined,
          token
        );
      }
      setActionModalApp(null);
      setActionRemarks('');
      await loadAdminData(token);
      alert('Application review decision recorded and citizen notified successfully!');
    } catch (err: any) {
      alert(err.message);
    }
  }`;

content = content.replace(oldActionHandler, newActionHandler);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 7 review panel updates applied successfully");
