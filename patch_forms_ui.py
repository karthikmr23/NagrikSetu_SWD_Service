import sys

filepath = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Application Form
old_app_form = """            <form onSubmit={handleApplicationSubmit}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem', marginBottom: '1.5rem' }}>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Applicant Full Name</label>
                  <input type="text" required className="filter-input" style={{ width: '100%' }} value={applyFullName} onChange={e => setApplyFullName(e.target.value)} />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Mobile Phone Number</label>
                  <input type="tel" required className="filter-input" style={{ width: '100%' }} value={applyPhone} onChange={e => setApplyPhone(e.target.value)} />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Permanent Residence District</label>
                  <input type="text" required className="filter-input" style={{ width: '100%' }} value={applyDistrict} onChange={e => setApplyDistrict(e.target.value)} />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Social Category</label>
                  <select className="filter-input" style={{ width: '100%' }} value={applyCategory} onChange={e => setApplyCategory(e.target.value)}>
                    <option value="General">General</option>
                    <option value="SC">SC</option>
                    <option value="ST">ST</option>
                    <option value="OBC">OBC</option>
                    <option value="Category 1">Category 1</option>
                    <option value="Category 2A">Category 2A</option>
                    <option value="Category 2B">Category 2B</option>
                    <option value="Category 3A">Category 3A</option>
                    <option value="Category 3B">Category 3B</option>
                    <option value="Minority">Minority</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Aadhaar-Seeded Bank Account Number</label>
                  <input type="text" required className="filter-input" style={{ width: '100%' }} value={applyBankAcc} onChange={e => setApplyBankAcc(e.target.value)} />
                </div>
                <div>
                  <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Bank IFSC Code</label>
                  <input type="text" required className="filter-input" style={{ width: '100%' }} value={applyIfsc} onChange={e => setApplyIfsc(e.target.value)} />
                </div>
              </div>

              {/* SCHEME-SPECIFIC DYNAMIC FORM SECTION */}
              <div style={{
                background: '#ffffff',
                border: '1px solid #bfdbfe',
                borderRadius: '8px',
                padding: '1.25rem',
                marginBottom: '1.5rem',
                boxShadow: '0 2px 6px rgba(59,130,246,0.06)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.5rem' }}>
                  <Award size={18} color="#2563eb" />
                  <h3 style={{ fontSize: '1rem', color: '#1e3a8a', fontWeight: 700, margin: 0 }}>
                    {schemeDynamicForm ? schemeDynamicForm.title : `${selectedScheme.name} — Specific Requirements`}
                  </h3>
                </div>

                {loadingSchemeForm ? (
                  <div style={{ textAlign: 'center', padding: '1.5rem', color: '#64748b' }}>
                    Loading scheme-specific requirements and fields...
                  </div>
                ) : schemeDynamicForm && schemeDynamicForm.fields && schemeDynamicForm.fields.length > 0 ? (
                  <DynamicFormRenderer 
                    fields={schemeDynamicForm.fields}
                    formData={dynamicFormData}
                    onChange={(name, val) => setDynamicFormData(prev => ({ ...prev, [name]: val }))}
                  />
                ) : (
                  <div style={{ fontSize: '0.82rem', color: '#64748b', fontStyle: 'italic' }}>
                    Standard applicant verification applies for this welfare service.
                  </div>
                )}
              </div>

              <div style={{ backgroundColor: "#fffbeb", padding: "1rem", borderRadius: "8px", border: "1px solid #fde68a", marginBottom: "1.5rem", fontSize: "0.8rem", color: "#92400e" }}>
                <label style={{ display: "flex", alignItems: "flex-start", gap: "0.65rem", cursor: "pointer", margin: 0 }}>
                  <input type="checkbox" required checked={applyConsent} onChange={e => setApplyConsent(e.target.checked)} style={{ marginTop: "0.2rem" }} />
                  <span>
                    <strong>Declaration & Consent:</strong> I hereby declare that the particulars provided above are authentic to the best of my knowledge and match my official revenue records. I authorize NagrikSetu SWD to authenticate my Aadhaar bank seeding for Direct Benefit Transfer.
                  </span>
                </label>
              </div>

              <div style={{ display: "flex", gap: "0.85rem" }}>
                <button type="submit" className="btn-orange" disabled={loading || !applyConsent}>
                  {loading ? "Submitting Application..." : "Confirm & Submit"}
                </button>
              </div>
            </form>"""

new_app_form = """            <form onSubmit={handleApplicationSubmit}>
              {/* SECTION 1: CITIZEN REGISTRY & DIRECT BENEFIT TRANSFER PROFILE */}
              <div className="swd-form-section">
                <div className="swd-form-section-header">
                  <User size={18} color="#ea580c" />
                  <div>
                    <h3 className="swd-form-section-title">1. Citizen Identity & Direct Benefit Transfer Profile</h3>
                    <p className="swd-form-section-desc">
                      Pre-filled from your authenticated citizen account. Used to verify Aadhaar seeding and disburse benefits.
                    </p>
                  </div>
                </div>

                <div className="form-grid-2">
                  <div className="form-group">
                    <label className="form-label">
                      <span>Applicant Full Name</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyFullName} 
                      onChange={e => setApplyFullName(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Mobile Phone Number</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="tel" 
                      required 
                      className="form-input" 
                      value={applyPhone} 
                      onChange={e => setApplyPhone(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Permanent Residence District</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyDistrict} 
                      onChange={e => setApplyDistrict(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Social Category</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <select 
                      className="form-input form-select" 
                      value={applyCategory} 
                      onChange={e => setApplyCategory(e.target.value)}
                    >
                      <option value="General">General</option>
                      <option value="SC">SC</option>
                      <option value="ST">ST</option>
                      <option value="OBC">OBC</option>
                      <option value="Category 1">Category 1</option>
                      <option value="Category 2A">Category 2A</option>
                      <option value="Category 2B">Category 2B</option>
                      <option value="Category 3A">Category 3A</option>
                      <option value="Category 3B">Category 3B</option>
                      <option value="Minority">Minority</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Aadhaar-Seeded Bank Account Number</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyBankAcc} 
                      onChange={e => setApplyBankAcc(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Bank IFSC Code</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyIfsc} 
                      onChange={e => setApplyIfsc(e.target.value)} 
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 2: SCHEME-SPECIFIC REQUIREMENTS & DOSSIER */}
              <div className="swd-form-section" style={{ border: '1px solid #bfdbfe' }}>
                <div className="swd-form-section-header">
                  <Award size={18} color="#2563eb" />
                  <div>
                    <h3 className="swd-form-section-title" style={{ color: '#1e3a8a' }}>
                      2. {schemeDynamicForm ? schemeDynamicForm.title : `${selectedScheme.name} — Specific Requirements`}
                    </h3>
                    <p className="swd-form-section-desc">
                      Official statutory criteria and application details required by the administering department.
                    </p>
                  </div>
                </div>

                {loadingSchemeForm ? (
                  <div style={{ textAlign: 'center', padding: '2rem 1.5rem', color: '#64748b' }}>
                    Loading scheme-specific requirements and fields...
                  </div>
                ) : schemeDynamicForm && schemeDynamicForm.fields && schemeDynamicForm.fields.length > 0 ? (
                  <DynamicFormRenderer 
                    fields={schemeDynamicForm.fields}
                    formData={dynamicFormData}
                    onChange={(name, val) => setDynamicFormData(prev => ({ ...prev, [name]: val }))}
                  />
                ) : (
                  <div style={{ fontSize: '0.84rem', color: '#64748b', fontStyle: 'italic', padding: '1rem', background: '#f8fafc', borderRadius: '6px' }}>
                    Standard applicant verification applies for this welfare service.
                  </div>
                )}
              </div>

              {/* SECTION 3: STATUTORY DECLARATION & CONSENT */}
              <div className="swd-declaration-box">
                <label>
                  <input 
                    type="checkbox" 
                    required 
                    checked={applyConsent} 
                    onChange={e => setApplyConsent(e.target.checked)} 
                  />
                  <span>
                    <strong>Declaration & Consent:</strong> I hereby declare that the particulars provided above are authentic to the best of my knowledge and match my official revenue records. I authorize NagrikSetu SWD to authenticate my Aadhaar bank seeding for Direct Benefit Transfer.
                  </span>
                </label>
              </div>

              <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center" }}>
                <button 
                  type="submit" 
                  className="btn-orange" 
                  style={{ minWidth: '180px', height: '44px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}
                  disabled={loading || !applyConsent}
                >
                  {loading ? "Submitting Application..." : "Confirm & Submit Application"}
                </button>
                <button 
                  type="button" 
                  className="btn-secondary" 
                  style={{ height: '44px' }}
                  onClick={() => setActiveTab('schemes')}
                >
                  Cancel
                </button>
              </div>
            </form>"""

if old_app_form not in text:
    print('ERROR: old_app_form not found in App.tsx')
    sys.exit(1)

text = text.replace(old_app_form, new_app_form, 1)

# 2. Update Citizen Registration Form
old_reg_form = """                  {/* Section 1: Required Account Credentials */}
                  <h4 style={{ color: 'var(--navy-dark)', fontSize: '0.95rem', marginBottom: '0.75rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.4rem' }}>
                    1. Account Credentials
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1.25rem' }}>
                    <div style={{ gridColumn: 'span 2' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Full Legal Name <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <input 
                        type="text" 
                        required 
                        placeholder="e.g. Anand Kumar Nayak" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regFullName}
                        onChange={e => setRegFullName(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Email Address <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <input 
                        type="email" 
                        required 
                        placeholder="anand@example.com" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regEmail}
                        onChange={e => setRegEmail(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Mobile Number (10 digits) <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <input 
                        type="tel" 
                        required 
                        maxLength={10}
                        placeholder="9845012345" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regPhone}
                        onChange={e => setRegPhone(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Password <span style={{ color: '#dc2626' }}>* (min 6 characters)</span>
                      </label>
                      <div style={{ position: 'relative' }}>
                        <input 
                          type={showPassword ? "text" : "password"} 
                          required 
                          minLength={6}
                          placeholder="Create strong password" 
                          className="filter-input" 
                          style={{ width: '100%', paddingRight: '2.5rem' }}
                          value={regPassword}
                          onChange={e => setRegPassword(e.target.value)}
                        />
                        <button 
                          type="button" 
                          onClick={() => setShowPassword(!showPassword)}
                          style={{ position: 'absolute', right: '8px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                          title={showPassword ? "Hide password" : "Show password"}
                        >
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Confirm Password <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <div style={{ position: 'relative' }}>
                        <input 
                          type={showConfirmPassword ? "text" : "password"} 
                          required 
                          minLength={6}
                          placeholder="Re-enter password" 
                          className="filter-input" 
                          style={{ width: '100%', paddingRight: '2.5rem' }}
                          value={regConfirmPassword}
                          onChange={e => setRegConfirmPassword(e.target.value)}
                        />
                        <button 
                          type="button" 
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          style={{ position: 'absolute', right: '8px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                          title={showConfirmPassword ? "Hide password" : "Show password"}
                        >
                          {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Section 2: Demographic & Domicile Details */}
                  <h4 style={{ color: 'var(--navy-dark)', fontSize: '0.95rem', marginBottom: '0.75rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.4rem', marginTop: '1.25rem' }}>
                    2. Citizen Demographics & Welfare Profile (Optional / Supporting)
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>Date of Birth</label>
                      <input 
                        type="date" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regDob}
                        onChange={e => setRegDob(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>Gender</label>
                      <select 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regGender}
                        onChange={e => setRegGender(e.target.value)}
                      >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Transgender">Transgender</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>


                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>District (Karnataka)</label>
                      <input 
                        type="text" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regDistrict}
                        onChange={e => setRegDistrict(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>Taluk</label>
                      <input 
                        type="text" 
                        placeholder="e.g. Bengaluru North"
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regTaluk}
                        onChange={e => setRegTaluk(e.target.value)}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>PIN Code</label>
                      <input 
                        type="text" 
                        maxLength={6}
                        placeholder="e.g. 560001"
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regPinCode}
                        onChange={e => setRegPinCode(e.target.value)}
                      />
                    </div>

                    <div style={{ gridColumn: 'span 2' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>Residential Address</label>
                      <input 
                        type="text" 
                        placeholder="Door / Flat No, Street, Locality"
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={regAddress}
                        onChange={e => setRegAddress(e.target.value)}
                      />
                    </div>

                  </div>"""

new_reg_form = """                  {/* Section 1: Required Account Credentials */}
                  <div className="swd-form-section" style={{ marginBottom: '1.25rem' }}>
                    <div className="swd-form-section-header">
                      <User size={18} color="#ea580c" />
                      <div>
                        <h4 className="swd-form-section-title">1. Account Credentials & Login Details</h4>
                        <p className="swd-form-section-desc">Required for citizen authentication and scheme application submission.</p>
                      </div>
                    </div>
                    
                    <div className="form-grid-2">
                      <div className="form-group form-grid-full">
                        <label className="form-label">
                          <span>Full Legal Name</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="text" 
                          required 
                          placeholder="e.g. Anand Kumar Nayak" 
                          className="form-input" 
                          value={regFullName}
                          onChange={e => setRegFullName(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Email Address</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="email" 
                          required 
                          placeholder="anand@example.com" 
                          className="form-input" 
                          value={regEmail}
                          onChange={e => setRegEmail(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Mobile Number (10 digits)</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="tel" 
                          required 
                          maxLength={10}
                          placeholder="9845012345" 
                          className="form-input" 
                          value={regPhone}
                          onChange={e => setRegPhone(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Password (min 6 characters)</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <div style={{ position: 'relative' }}>
                          <input 
                            type={showPassword ? "text" : "password"} 
                            required 
                            minLength={6}
                            placeholder="Create strong password" 
                            className="form-input" 
                            style={{ paddingRight: '2.5rem' }}
                            value={regPassword}
                            onChange={e => setRegPassword(e.target.value)}
                          />
                          <button 
                            type="button" 
                            onClick={() => setShowPassword(!showPassword)}
                            style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                            title={showPassword ? "Hide password" : "Show password"}
                          >
                            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Confirm Password</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <div style={{ position: 'relative' }}>
                          <input 
                            type={showConfirmPassword ? "text" : "password"} 
                            required 
                            minLength={6}
                            placeholder="Re-enter password" 
                            className="form-input" 
                            style={{ paddingRight: '2.5rem' }}
                            value={regConfirmPassword}
                            onChange={e => setRegConfirmPassword(e.target.value)}
                          />
                          <button 
                            type="button" 
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                            title={showConfirmPassword ? "Hide password" : "Show password"}
                          >
                            {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Section 2: Demographic & Domicile Details */}
                  <div className="swd-form-section" style={{ marginBottom: '1.5rem' }}>
                    <div className="swd-form-section-header">
                      <Building2 size={18} color="#2563eb" />
                      <div>
                        <h4 className="swd-form-section-title">2. Citizen Demographics & Welfare Profile</h4>
                        <p className="swd-form-section-desc">Used to accelerate scheme eligibility evaluation and taluk administration.</p>
                      </div>
                    </div>

                    <div className="form-grid-3">
                      <div className="form-group">
                        <label className="form-label">Date of Birth</label>
                        <input 
                          type="date" 
                          className="form-input" 
                          value={regDob}
                          onChange={e => setRegDob(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">Gender</label>
                        <select 
                          className="form-input form-select" 
                          value={regGender}
                          onChange={e => setRegGender(e.target.value)}
                        >
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Transgender">Transgender</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label className="form-label">District (Karnataka)</label>
                        <input 
                          type="text" 
                          className="form-input" 
                          value={regDistrict}
                          onChange={e => setRegDistrict(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">Taluk</label>
                        <input 
                          type="text" 
                          placeholder="e.g. Bengaluru North"
                          className="form-input" 
                          value={regTaluk}
                          onChange={e => setRegTaluk(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">PIN Code</label>
                        <input 
                          type="text" 
                          maxLength={6}
                          placeholder="e.g. 560001"
                          className="form-input" 
                          value={regPinCode}
                          onChange={e => setRegPinCode(e.target.value)}
                        />
                      </div>

                      <div className="form-group form-grid-full">
                        <label className="form-label">Residential Address</label>
                        <input 
                          type="text" 
                          placeholder="Door / Flat No, Street, Locality"
                          className="form-input" 
                          value={regAddress}
                          onChange={e => setRegAddress(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>"""

if old_reg_form not in text:
    print('ERROR: old_reg_form not found in App.tsx')
    sys.exit(1)

text = text.replace(old_reg_form, new_reg_form, 1)

# 3. Update Citizen Profile Edit Form (lines 1940-2059)
old_profile_form = """              <form onSubmit={handleSaveProfile} style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                  Edit Profile
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.25rem', marginBottom: '1.5rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Full Name</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.full_name || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, full_name: e.target.value })} 
                      required 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Contact Phone</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.phone || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, phone: e.target.value })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>District</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.district || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, district: e.target.value })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>State</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.state || 'Karnataka'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, state: e.target.value })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Annual Family Income (INR)</label>
                    <input 
                      type="number" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.annual_income !== undefined ? profileEditForm.annual_income : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, annual_income: Number(e.target.value) })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Caste / Category</label>
                    <select 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.caste_category || 'SC'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, caste_category: e.target.value })}
                    >
                      <option value="SC">Scheduled Caste (SC)</option>
                      <option value="ST">Scheduled Tribe (ST)</option>
                      <option value="OBC">Other Backward Class (OBC)</option>
                      <option value="Minority">Minority</option>
                      <option value="General">General</option>
                    </select>
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Disability Percentage (%)</label>
                    <input 
                      type="number" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.disability_percentage !== undefined ? profileEditForm.disability_percentage : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, disability_percentage: Number(e.target.value) })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Bank Account Number</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.bank_account_number || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_account_number: e.target.value })} 
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>Bank IFSC</label>
                    <input 
                      type="text" 
                      className="filter-input" 
                      style={{ width: '100%' }}
                      value={profileEditForm.bank_ifsc || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_ifsc: e.target.value })} 
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem', borderTop: '1px solid var(--line)', paddingTop: '1rem' }}>
                  <button type="submit" className="btn-orange" disabled={profileLoading}>
                    {profileLoading ? 'Saving Changes...' : 'Save Changes'}
                  </button>
                  <button type="button" className="btn-secondary" onClick={handleCancelEditProfile} disabled={profileLoading}>
                    Cancel
                  </button>
                </div>
              </form>"""

new_profile_form = """              <form onSubmit={handleSaveProfile} className="swd-form-card">
                <div className="swd-form-section-header">
                  <User size={18} color="#ea580c" />
                  <div>
                    <h4 className="swd-form-section-title">Edit Citizen Profile</h4>
                    <p className="swd-form-section-desc">Keep your official citizen registry details and DBT bank information up to date.</p>
                  </div>
                </div>

                <div className="form-grid-2" style={{ marginBottom: '1.5rem' }}>
                  <div className="form-group">
                    <label className="form-label">
                      <span>Full Legal Name</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.full_name || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, full_name: e.target.value })} 
                      required 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Contact Phone</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.phone || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, phone: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">District</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.district || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, district: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">State</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.state || 'Karnataka'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, state: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Annual Family Income (INR)</label>
                    <input 
                      type="number" 
                      className="form-input" 
                      value={profileEditForm.annual_income !== undefined ? profileEditForm.annual_income : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, annual_income: Number(e.target.value) })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Caste / Category</label>
                    <select 
                      className="form-input form-select" 
                      value={profileEditForm.caste_category || 'SC'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, caste_category: e.target.value })}
                    >
                      <option value="SC">Scheduled Caste (SC)</option>
                      <option value="ST">Scheduled Tribe (ST)</option>
                      <option value="OBC">Other Backward Class (OBC)</option>
                      <option value="Minority">Minority</option>
                      <option value="General">General</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Disability Percentage (%)</label>
                    <input 
                      type="number" 
                      className="form-input" 
                      value={profileEditForm.disability_percentage !== undefined ? profileEditForm.disability_percentage : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, disability_percentage: Number(e.target.value) })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Bank Account Number (DBT)</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.bank_account_number || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_account_number: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Bank IFSC</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.bank_ifsc || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_ifsc: e.target.value })} 
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '1rem', borderTop: '1px solid var(--line)', paddingTop: '1.25rem', alignItems: 'center' }}>
                  <button type="submit" className="btn-orange" style={{ minWidth: '160px', height: '44px' }} disabled={profileLoading}>
                    {profileLoading ? 'Saving Changes...' : 'Save Changes'}
                  </button>
                  <button type="button" className="btn-secondary" style={{ height: '44px' }} onClick={handleCancelEditProfile} disabled={profileLoading}>
                    Cancel
                  </button>
                </div>
              </form>"""

if old_profile_form not in text:
    print('ERROR: old_profile_form not found in App.tsx')
    sys.exit(1)

text = text.replace(old_profile_form, new_profile_form, 1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: All 3 forms (Application Form, Citizen Registration, Citizen Profile) fully upgraded!')
