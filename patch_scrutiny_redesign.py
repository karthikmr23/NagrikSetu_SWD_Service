# Patch GovernmentWelfareAdminPortal.tsx with the redesigned 3-part Application Scrutiny & Official Decision UI

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\GovernmentWelfareAdminPortal.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Lucide-react imports to ensure ShieldCheck, RotateCcw, XCircle, Info, Landmark are imported
old_import = """import { 
  Building2, Users, FileText, CheckCircle2, Clock, 
  AlertCircle, ChevronRight, Search, Filter, Eye, RefreshCw, 
  Check, X, AlertTriangle, ArrowLeft, Download, Shield, Bell, Send
} from 'lucide-react';"""

new_import = """import { 
  Building2, Users, FileText, CheckCircle2, Clock, 
  AlertCircle, ChevronRight, Search, Filter, Eye, RefreshCw, 
  Check, X, AlertTriangle, ArrowLeft, Download, Shield, Bell, Send,
  ShieldCheck, RotateCcw, XCircle, Info, Landmark, HelpCircle
} from 'lucide-react';"""

assert old_import in content, "old_import not found"
content = content.replace(old_import, new_import)

# 2. Redesign the Official Scrutiny Decision Form (lines 1482-1582)
old_form = """              {/* Scrutiny Decision Form */}
              <div style={{ borderTop: '2px solid var(--line)', paddingTop: '1.25rem' }}>
                <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.75rem' }}>
                  Official Scrutiny Decision & Status Transition
                </h4>

                {actionMsg && (
                  <div style={{
                    padding: '0.65rem 1rem',
                    borderRadius: '6px',
                    fontSize: '0.82rem',
                    marginBottom: '1rem',
                    backgroundColor: actionMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                    color: actionMsg.type === 'success' ? '#15803d' : '#b91c1c',
                    border: `1px solid ${actionMsg.type === 'success' ? '#bbf7d0' : '#fecaca'}`
                  }}>
                    {actionMsg.text}
                  </div>
                )}

                <form onSubmit={handleScrutinyDecision} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                      Administrative Decision <span style={{ color: '#dc2626' }}>*</span>
                    </label>
                    <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                      {[
                        { val: 'APPROVED', label: 'Approve & Sanction Benefit', color: '#10b981' },
                        { val: 'UNDER_REVIEW', label: 'Mark Under Deep Scrutiny', color: '#3b82f6' },
                        { val: 'DOCUMENTS_REQUIRED', label: 'Return for Correction / Documents', color: '#f59e0b' },
                        { val: 'REJECTED', label: 'Reject Application', color: '#ef4444' }
                      ].map(d => (
                        <label 
                          key={d.val}
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.4rem',
                            padding: '0.45rem 0.85rem',
                            borderRadius: '6px',
                            border: reviewDecision === d.val ? `2px solid ${d.color}` : '1px solid var(--line)',
                            background: reviewDecision === d.val ? '#f8fafc' : '#ffffff',
                            cursor: 'pointer',
                            fontSize: '0.8rem',
                            fontWeight: reviewDecision === d.val ? 700 : 500
                          }}
                        >
                          <input 
                            type="radio" 
                            name="decision" 
                            value={d.val} 
                            checked={reviewDecision === d.val} 
                            onChange={() => setReviewDecision(d.val)}
                          />
                          <span>{d.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {reviewDecision === 'APPROVED' && (
                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                        Sanctioned Financial Assistance Amount (Rs.)
                      </label>
                      <input 
                        type="number"
                        className="form-input"
                        value={sanctionAmount}
                        onChange={e => setSanctionAmount(Number(e.target.value))}
                        style={{ maxWidth: '300px' }}
                      />
                    </div>
                  )}

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                      Official Scrutiny Remarks / Justification <span style={{ color: '#dc2626' }}>*</span>
                    </label>
                    <textarea 
                      className="form-input"
                      rows={3}
                      placeholder="State the verification findings, documents verified, or reasons for approval/rejection/correction..."
                      value={reviewRemarks}
                      onChange={e => setReviewRemarks(e.target.value)}
                      required
                    />
                  </div>

                  <div>
                    <button 
                      type="submit" 
                      className="btn-primary" 
                      disabled={actionLoading}
                      style={{ padding: '0.6rem 1.5rem', fontSize: '0.85rem' }}
                    >
                      {actionLoading ? 'Saving...' : 'Save Decision'}
                    </button>
                  </div>
                </form>
              </div>"""

new_form = """              {/* REDESIGNED WELFARE OFFICER OFFICIAL APPLICATION SCRUTINY & DECISION WORKFLOW */}
              <div className="scrutiny-decision-container">
                <div className="scrutiny-header">
                  <h4>
                    <ShieldCheck size={20} color="#0f172a" />
                    Application Scrutiny & Official Decision
                  </h4>
                  <p>
                    Review the beneficiary's application and record the appropriate administrative decision after completing the required verification.
                  </p>
                </div>

                {actionMsg && (
                  <div style={{
                    padding: '0.75rem 1.15rem',
                    borderRadius: '8px',
                    fontSize: '0.85rem',
                    fontWeight: 500,
                    marginBottom: '1.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.6rem',
                    backgroundColor: actionMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                    color: actionMsg.type === 'success' ? '#15803d' : '#b91c1c',
                    border: `1.5px solid ${actionMsg.type === 'success' ? '#bbf7d0' : '#fecaca'}`
                  }}>
                    {actionMsg.type === 'success' ? <CheckCircle2 size={18} /> : <AlertTriangle size={18} />}
                    <span>{actionMsg.text}</span>
                  </div>
                )}

                <form onSubmit={handleScrutinyDecision} noValidate>
                  {/* PART 1 — DECISION SELECTION */}
                  <div style={{ marginBottom: '1.5rem' }}>
                    <div className="scrutiny-part-header">
                      <span className="scrutiny-part-number">1</span>
                      <span className="scrutiny-part-title">Decision Selection</span>
                    </div>

                    <div className="scrutiny-cards-grid" role="radiogroup" aria-label="Administrative Decision Options">
                      {/* OPTION 1 — APPROVE & SANCTION BENEFIT */}
                      <div 
                        className={`scrutiny-card card-approve ${reviewDecision === 'APPROVED' ? 'selected' : ''}`}
                        onClick={() => setReviewDecision('APPROVED')}
                        role="radio"
                        aria-checked={reviewDecision === 'APPROVED'}
                        tabIndex={0}
                        onKeyDown={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); setReviewDecision('APPROVED'); } }}
                      >
                        <div className="scrutiny-card-top">
                          <div className="scrutiny-icon-box">
                            <CheckCircle2 size={18} />
                          </div>
                          <div className="scrutiny-radio-indicator">
                            {reviewDecision === 'APPROVED' && <div className="scrutiny-radio-dot" />}
                          </div>
                        </div>
                        <div className="scrutiny-card-title">Approve & Sanction Benefit</div>
                        <p className="scrutiny-card-desc">
                          Approve the beneficiary's application and authorize the applicable financial assistance.
                        </p>
                      </div>

                      {/* OPTION 2 — MARK UNDER DEEP SCRUTINY */}
                      <div 
                        className={`scrutiny-card card-scrutiny ${reviewDecision === 'UNDER_REVIEW' ? 'selected' : ''}`}
                        onClick={() => setReviewDecision('UNDER_REVIEW')}
                        role="radio"
                        aria-checked={reviewDecision === 'UNDER_REVIEW'}
                        tabIndex={0}
                        onKeyDown={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); setReviewDecision('UNDER_REVIEW'); } }}
                      >
                        <div className="scrutiny-card-top">
                          <div className="scrutiny-icon-box">
                            <Clock size={18} />
                          </div>
                          <div className="scrutiny-radio-indicator">
                            {reviewDecision === 'UNDER_REVIEW' && <div className="scrutiny-radio-dot" />}
                          </div>
                        </div>
                        <div className="scrutiny-card-title">Mark Under Deep Scrutiny</div>
                        <p className="scrutiny-card-desc">
                          Send the application for additional verification before making a final decision.
                        </p>
                      </div>

                      {/* OPTION 3 — RETURN FOR CORRECTION / DOCUMENTS */}
                      <div 
                        className={`scrutiny-card card-return ${reviewDecision === 'DOCUMENTS_REQUIRED' ? 'selected' : ''}`}
                        onClick={() => setReviewDecision('DOCUMENTS_REQUIRED')}
                        role="radio"
                        aria-checked={reviewDecision === 'DOCUMENTS_REQUIRED'}
                        tabIndex={0}
                        onKeyDown={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); setReviewDecision('DOCUMENTS_REQUIRED'); } }}
                      >
                        <div className="scrutiny-card-top">
                          <div className="scrutiny-icon-box">
                            <RotateCcw size={18} />
                          </div>
                          <div className="scrutiny-radio-indicator">
                            {reviewDecision === 'DOCUMENTS_REQUIRED' && <div className="scrutiny-radio-dot" />}
                          </div>
                        </div>
                        <div className="scrutiny-card-title">Return for Correction / Documents</div>
                        <p className="scrutiny-card-desc">
                          Return the application to the beneficiary for correction or submission of missing documents.
                        </p>
                      </div>

                      {/* OPTION 4 — REJECT APPLICATION */}
                      <div 
                        className={`scrutiny-card card-reject ${reviewDecision === 'REJECTED' ? 'selected' : ''}`}
                        onClick={() => setReviewDecision('REJECTED')}
                        role="radio"
                        aria-checked={reviewDecision === 'REJECTED'}
                        tabIndex={0}
                        onKeyDown={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); setReviewDecision('REJECTED'); } }}
                      >
                        <div className="scrutiny-card-top">
                          <div className="scrutiny-icon-box">
                            <XCircle size={18} />
                          </div>
                          <div className="scrutiny-radio-indicator">
                            {reviewDecision === 'REJECTED' && <div className="scrutiny-radio-dot" />}
                          </div>
                        </div>
                        <div className="scrutiny-card-title">Reject Application</div>
                        <p className="scrutiny-card-desc">
                          Reject the application with an appropriate official justification.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* PART 2 — DECISION DETAILS & OFFICIAL REMARKS */}
                  <div style={{ marginBottom: '1.5rem' }}>
                    <div className="scrutiny-part-header">
                      <span className="scrutiny-part-number">2</span>
                      <span className="scrutiny-part-title">Decision Details & Official Remarks</span>
                    </div>

                    <div className="scrutiny-details-panel">
                      {/* A. APPROVE CONTEXT */}
                      {reviewDecision === 'APPROVED' && (
                        <>
                          <div className="scrutiny-info-callout info-approve">
                            <Landmark size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                            <div>
                              <strong>Financial Assistance Mandate:</strong> Approving this application will generate an official beneficiary code in the Social Welfare Department registry and authorize simulated Direct Benefit Transfer (DBT) disbursement.
                            </div>
                          </div>

                          <div className="scrutiny-field-group">
                            <label className="scrutiny-field-label">
                              <span>Sanctioned Financial Assistance Amount</span>
                              <span className="req">*</span>
                            </label>
                            <div className="scrutiny-input-wrapper">
                              <span className="scrutiny-currency-prefix">₹</span>
                              <input 
                                type="number"
                                className="scrutiny-amount-input"
                                value={sanctionAmount}
                                onChange={e => setSanctionAmount(Math.max(0, Number(e.target.value)))}
                                min={1}
                                step={100}
                                placeholder="Enter sanctioned amount"
                                required
                              />
                            </div>
                            <div style={{ fontSize: '0.76rem', color: '#64748b', marginTop: '0.35rem' }}>
                              Currency in Indian Rupees (INR). Default entitlement based on scheme financial sanction matrix.
                            </div>
                          </div>

                          <div className="scrutiny-field-group">
                            <label className="scrutiny-field-label">
                              <span>Official Scrutiny Remarks & Verification Findings</span>
                              <span className="req">*</span>
                            </label>
                            <textarea 
                              className="scrutiny-textarea"
                              placeholder="Record the official verification findings, eligibility confirmations (income, caste, domicile), and sanction justification for the administrative audit log..."
                              value={reviewRemarks}
                              onChange={e => setReviewRemarks(e.target.value)}
                              required
                            />
                          </div>
                        </>
                      )}

                      {/* B. UNDER DEEP SCRUTINY CONTEXT */}
                      {reviewDecision === 'UNDER_REVIEW' && (
                        <>
                          <div className="scrutiny-info-callout info-scrutiny">
                            <Info size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                            <div>
                              <strong>Field Verification Required:</strong> This application will remain in active scrutiny queue pending secondary physical verification, field inspection by taluk welfare officers, or revenue document cross-checks.
                            </div>
                          </div>

                          <div className="scrutiny-field-group">
                            <label className="scrutiny-field-label">
                              <span>Reason for Additional Scrutiny & Official Observations</span>
                              <span className="req">*</span>
                            </label>
                            <textarea 
                              className="scrutiny-textarea"
                              placeholder="Detail the specific doubts, cross-verification requirements, or department clarifications needed before a final determination can be made..."
                              value={reviewRemarks}
                              onChange={e => setReviewRemarks(e.target.value)}
                              required
                            />
                          </div>
                        </>
                      )}

                      {/* C. RETURN FOR CORRECTION / DOCUMENTS CONTEXT */}
                      {reviewDecision === 'DOCUMENTS_REQUIRED' && (
                        <>
                          <div className="scrutiny-info-callout info-return">
                            <RotateCcw size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                            <div>
                              <strong>Beneficiary Action Notification:</strong> The citizen will receive an official notification directing them to re-upload clear document scans or correct conflicting application details through their citizen dashboard.
                            </div>
                          </div>

                          <div className="scrutiny-field-group">
                            <label className="scrutiny-field-label">
                              <span>Correction Instructions & Missing Documents Specification</span>
                              <span className="req">*</span>
                            </label>
                            <textarea 
                              className="scrutiny-textarea"
                              placeholder="Provide clear, actionable instructions for the citizen (e.g. 'Aadhaar copy is unreadable; please upload a clear scanned PDF showing full address and DOB. Income certificate expired on 31-03-2026; please upload renewal slip.')..."
                              value={reviewRemarks}
                              onChange={e => setReviewRemarks(e.target.value)}
                              required
                            />
                          </div>
                        </>
                      )}

                      {/* D. REJECT APPLICATION CONTEXT */}
                      {reviewDecision === 'REJECTED' && (
                        <>
                          <div className="scrutiny-info-callout info-reject">
                            <AlertCircle size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
                            <div>
                              <strong>Official Disqualification Notice:</strong> Rejecting this application will close the dossier and notify the citizen with the official statutory reasons. Rejection requires complete justification for administrative and grievance review.
                            </div>
                          </div>

                          <div className="scrutiny-field-group">
                            <label className="scrutiny-field-label">
                              <span>Official Justification & Ineligibility Grounds</span>
                              <span className="req">*</span>
                            </label>
                            <textarea 
                              className="scrutiny-textarea"
                              placeholder="Provide the exact statutory or regulatory grounds for rejection (e.g. 'Family annual income exceeds scheme ceiling of ₹2,50,000 as per Revenue Department data. Citizen does not possess Karnataka resident status.')..."
                              value={reviewRemarks}
                              onChange={e => setReviewRemarks(e.target.value)}
                              required
                            />
                          </div>
                        </>
                      )}
                    </div>
                  </div>

                  {/* PART 3 — DECISION REVIEW & SUBMISSION */}
                  <div>
                    <div className="scrutiny-part-header">
                      <span className="scrutiny-part-number">3</span>
                      <span className="scrutiny-part-title">Decision Review & Submission</span>
                    </div>

                    <div className="scrutiny-summary-box">
                      <div>
                        <div className="scrutiny-summary-text">
                          {reviewDecision === 'APPROVED' && (
                            <>
                              <strong>Decision Summary:</strong> You are approving this beneficiary's application and sanctioning ₹{Number(sanctionAmount || 0).toLocaleString('en-IN')} in financial assistance.
                            </>
                          )}
                          {reviewDecision === 'UNDER_REVIEW' && (
                            <>
                              <strong>Decision Summary:</strong> This application will be held in the deep scrutiny queue for secondary investigation and document cross-checking.
                            </>
                          )}
                          {reviewDecision === 'DOCUMENTS_REQUIRED' && (
                            <>
                              <strong>Decision Summary:</strong> This application will be returned to the citizen with the recorded correction instructions and missing document checklist.
                            </>
                          )}
                          {reviewDecision === 'REJECTED' && (
                            <>
                              <strong>Decision Summary:</strong> This application will be officially rejected with the recorded justification and permanently recorded in the audit trail.
                            </>
                          )}
                        </div>

                        {reviewDecision === 'REJECTED' && (
                          <div className="scrutiny-rejection-warning">
                            <AlertTriangle size={15} />
                            <span>Warning: This action formally closes the dossier and informs the applicant of disqualification.</span>
                          </div>
                        )}
                      </div>

                      <div className="scrutiny-action-row">
                        <button 
                          type="submit" 
                          disabled={actionLoading || !reviewRemarks.trim()}
                          className={`btn-scrutiny-submit ${
                            reviewDecision === 'APPROVED' ? 'submit-approve' :
                            reviewDecision === 'UNDER_REVIEW' ? 'submit-scrutiny' :
                            reviewDecision === 'DOCUMENTS_REQUIRED' ? 'submit-return' : 'submit-reject'
                          }`}
                        >
                          {actionLoading ? (
                            <>
                              <RefreshCw size={16} className="spin" />
                              <span>Recording Decision...</span>
                            </>
                          ) : (
                            <>
                              {reviewDecision === 'APPROVED' && (
                                <>
                                  <CheckCircle2 size={16} />
                                  <span>Approve & Sanction (₹{Number(sanctionAmount || 0).toLocaleString('en-IN')})</span>
                                </>
                              )}
                              {reviewDecision === 'UNDER_REVIEW' && (
                                <>
                                  <Clock size={16} />
                                  <span>Save Scrutiny Decision</span>
                                </>
                              )}
                              {reviewDecision === 'DOCUMENTS_REQUIRED' && (
                                <>
                                  <RotateCcw size={16} />
                                  <span>Return Application</span>
                                </>
                              )}
                              {reviewDecision === 'REJECTED' && (
                                <>
                                  <XCircle size={16} />
                                  <span>Confirm Rejection</span>
                                </>
                              )}
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>"""

assert old_form in content, "old_form not found in GovernmentWelfareAdminPortal.tsx"
content = content.replace(old_form, new_form)

# 3. Also fix Scrutinize button on line 1859 in Tab 8 (Queue table) so it opens application-detail view like Tab 6
old_tab8_button = """                          <button 
                            className="btn-orange"
                            style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
                            onClick={() => setSelectedApp(app)}
                          >
                            Scrutinize &rarr;
                          </button>"""

new_tab8_button = """                          <button 
                            className="btn-orange"
                            style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
                            onClick={() => {
                              setSelectedApp(app);
                              setReviewDecision('APPROVED');
                              setReviewRemarks('');
                              setActionMsg(null);
                              setActiveTab('application-detail');
                            }}
                          >
                            Scrutinize &rarr;
                          </button>"""

if old_tab8_button in content:
    content = content.replace(old_tab8_button, new_tab8_button)
    print("Updated Tab 8 Scrutinize button to switch activeTab to application-detail")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched GovernmentWelfareAdminPortal.tsx with 3-part redesign")
