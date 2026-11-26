import React, { useState, useEffect } from 'react';
import { 
  Building2, Users, FileText, CheckCircle2, Clock, 
  AlertCircle, ChevronRight, Search, Filter, Eye, RefreshCw, 
  Check, X, AlertTriangle, ArrowLeft, Download, Shield, Bell, Send,
  ShieldCheck, RotateCcw, XCircle, Info, Landmark, HelpCircle
} from 'lucide-react';
import * as api from '../services/api';

interface WelfareAdminProps {
  token: string;
  userName: string;
  userRole: string;
  onLogout: () => void;
  onViewReceipt: (applicationId: number) => void;
}

export const GovernmentWelfareAdminPortal: React.FC<WelfareAdminProps> = ({
  token,
  userName,
  userRole,
  onLogout,
  onViewReceipt
}) => {
  const [activeTab, setActiveTab] = useState<
    'dashboard' | 'schemes' | 'categories' | 'category-detail' | 'form-builder' |
    'applications' | 'scrutiny' | 'scheme-applications' | 'application-detail' | 
    'beneficiaries' | 'dbt' | 'grievances' | 'reports' | 'notifications' | 'profile'
  >('dashboard');

  const [beneficiaries, setBeneficiaries] = useState<api.Beneficiary[]>([]);
  // Form Builder State
  const [builderScheme, setBuilderScheme] = useState<api.Scheme | null>(null);
  const [allSchemes, setAllSchemes] = useState<api.Scheme[]>([]);
  const [formTitle, setFormTitle] = useState<string>('');
  const [formDesc, setFormDesc] = useState<string>('');
  const [formVersion, setFormVersion] = useState<number>(1);
  const [formFields, setFormFields] = useState<Array<{
    field_name: string;
    field_label: string;
    field_type: string;
    placeholder: string;
    help_text: string;
    is_required: boolean;
    display_order: number;
    options_json: string[];
  }>>([]);
  const [builderMsg, setBuilderMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [builderLoading, setBuilderLoading] = useState<boolean>(false);

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
  }
  
  // Dashboard & Category data
  const [categoryStats, setCategoryStats] = useState<api.CategoryStats[]>([]);
  const [dashboardStats, setDashboardStats] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);

  // Selected Category & Scheme breakdown
  const [selectedCategory, setSelectedCategory] = useState<api.CategoryStats | null>(null);
  const [selectedScheme, setSelectedScheme] = useState<api.SchemeBreakdown | null>(null);

  // Applications List & Filter
  const [applications, setApplications] = useState<api.Application[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<number | undefined>(undefined);
  const [schemeFilter, setSchemeFilter] = useState<number | undefined>(undefined);
  const [districtFilter, setDistrictFilter] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  // Review Modal / Scrutiny Action
  const [selectedApp, setSelectedApp] = useState<api.Application | null>(null);
  const [reviewDecision, setReviewDecision] = useState<string>('APPROVED');
  const [reviewRemarks, setReviewRemarks] = useState<string>('');
  const [sanctionAmount, setSanctionAmount] = useState<number>(10000);
  const [actionLoading, setActionLoading] = useState<boolean>(false);
  const [actionMsg, setActionMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Grievance Management State
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);
  const [selectedGrievance, setSelectedGrievance] = useState<api.Grievance | null>(null);
  const [grievanceResolution, setGrievanceResolution] = useState<string>('');
  const [grievanceStatusDecision, setGrievanceStatusDecision] = useState<string>('RESOLVED');
  const [grievanceActionLoading, setGrievanceActionLoading] = useState<boolean>(false);
  const [grievanceMsg, setGrievanceMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Load initial data
  useEffect(() => {
    loadPortalData();
  }, [token]);

  async function loadPortalData() {
    setLoading(true);
    try {
      const [statsData, dashData, appsData, grvData, schemesData, bensData] = await Promise.all([
        api.fetchCategoryApplicationStats(token).catch(err => {
          console.warn('Could not load category application stats:', err);
          return [];
        }),
        api.fetchAdminDashboard(token).catch(err => {
          console.warn('Could not load admin dashboard:', err);
          return null;
        }),
        api.fetchAdminApplications(token).catch(err => {
          console.warn('Could not load admin applications:', err);
          return [];
        }),
        api.fetchGrievances(undefined, token).catch(() => []),
        api.fetchSchemes().catch(err => {
          console.warn('Could not load schemes:', err);
          return [];
        }),
        api.fetchBeneficiaries(token).catch(err => {
          console.warn('Could not load beneficiaries:', err);
          return [];
        })
      ]);
      if (statsData) setCategoryStats(statsData);
      if (dashData) setDashboardStats(dashData);
      if (appsData) setApplications(appsData);
      if (grvData) setGrievances(grvData);
      if (bensData) setBeneficiaries(bensData);
      if (schemesData && schemesData.length > 0) {
        setAllSchemes(schemesData);
        if (!builderScheme) {
          loadSchemeForBuilder(schemesData[0]);
        }
      }
    } catch (err) {
      console.error('Failed to load Government Welfare Admin data', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  async function handleResolveGrievance(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedGrievance) return;
    if (!grievanceResolution.trim()) {
      setGrievanceMsg({ type: 'error', text: 'Officer resolution remarks are required.' });
      return;
    }
    setGrievanceActionLoading(true);
    setGrievanceMsg(null);
    try {
      await api.resolveGrievance(selectedGrievance.id, {
        status: grievanceStatusDecision,
        officer_response: grievanceResolution.trim()
      }, token);
      setGrievanceMsg({ type: 'success', text: `Grievance ${selectedGrievance.grievance_number} updated successfully.` });
      const updated = await api.fetchGrievances(undefined, token);
      setGrievances(updated);
      setSelectedGrievance(null);
      setGrievanceResolution('');
    } catch (err: any) {
      setGrievanceMsg({ type: 'error', text: err.message || 'Failed to update grievance.' });
    } finally {
      setGrievanceActionLoading(false);
    }
  }

  async function loadFilteredApplications(catId?: number, scId?: number, st?: string, dist?: string, search?: string) {
    try {
      const apps = await api.fetchAdminApplications(token, {
        categoryId: catId,
        schemeId: scId,
        statusFilter: st,
        district: dist,
        search: search
      });
      setApplications(apps);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleScrutinyDecision(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedApp) return;
    if (!reviewRemarks.trim()) {
      setActionMsg({ type: 'error', text: 'Scrutiny remarks / reason are strictly required for administrative audit.' });
      return;
    }

    setActionLoading(true);
    setActionMsg(null);
    try {
      const updated = await api.recordAdminDecision(
        selectedApp.id,
        reviewDecision,
        reviewRemarks,
        reviewDecision === 'APPROVED' ? sanctionAmount : undefined,
        token
      );
      setActionMsg({ type: 'success', text: `Application ${updated.application_number} updated to ${updated.status} successfully!` });
      setSelectedApp(updated);
      // Reload stats & table in background
      loadPortalData();
    } catch (err: any) {
      setActionMsg({ type: 'error', text: err.message || 'Failed to record administrative decision.' });
    } finally {
      setActionLoading(false);
    }
  }

  async function loadSchemeForBuilder(scheme: api.Scheme) {
    setBuilderScheme(scheme);
    setBuilderMsg(null);
    setBuilderLoading(true);
    try {
      const def = await api.fetchSchemeDynamicForm(scheme.id);
      if (def) {
        setFormTitle(def.title);
        setFormDesc(def.description || '');
        setFormVersion(def.version);
        setFormFields(def.fields.map(f => ({
          field_name: f.field_name,
          field_label: f.field_label,
          field_type: f.field_type,
          placeholder: f.placeholder || '',
          help_text: f.help_text || '',
          is_required: f.is_required,
          display_order: f.display_order,
          options_json: Array.isArray(f.options_json) ? f.options_json : []
        })));
      } else {
        setFormTitle(`${scheme.name} Application Form`);
        setFormDesc(scheme.description);
        setFormVersion(1);
        setFormFields([
          {
            field_name: 'applicant_full_name',
            field_label: 'Applicant Full Name',
            field_type: 'text',
            placeholder: 'Enter official name matching revenue record',
            help_text: 'As per Aadhaar or Voter ID',
            is_required: true,
            display_order: 1,
            options_json: []
          },
          {
            field_name: 'ration_card_number',
            field_label: 'Ration Card Number / Food Security Card',
            field_type: 'text',
            placeholder: 'e.g. BPL/AAY-10928374',
            help_text: 'Required for state subsidy DBT validation',
            is_required: true,
            display_order: 2,
            options_json: []
          }
        ]);
      }
    } catch (err) {
      console.error('Failed to load scheme form definition', err);
    } finally {
      setBuilderLoading(false);
    }
  }

  async function handleSaveFormBuilder(e: React.FormEvent) {
    e.preventDefault();
    if (!builderScheme) return;
    if (!formTitle.trim()) {
      setBuilderMsg({ type: 'error', text: 'Form title is required.' });
      return;
    }
    if (formFields.length === 0) {
      setBuilderMsg({ type: 'error', text: 'At least one field is required in the application form.' });
      return;
    }

    setBuilderLoading(true);
    setBuilderMsg(null);
    try {
      const saved = await api.saveSchemeDynamicForm(builderScheme.id, {
        title: formTitle.trim(),
        description: formDesc.trim(),
        fields: formFields
      }, token);
      setFormVersion(saved.version);
      setBuilderMsg({ type: 'success', text: `Application Form for '${builderScheme.name}' successfully published (Version ${saved.version})! Citizens can now apply using this updated form.` });
    } catch (err: any) {
      setBuilderMsg({ type: 'error', text: err.message || 'Failed to save application form' });
    } finally {
      setBuilderLoading(false);
    }
  }

  function handleAddField() {
    const newIdx = formFields.length + 1;
    setFormFields([
      ...formFields,
      {
        field_name: `field_${Date.now().toString().slice(-5)}`,
        field_label: `New Questionnaire Field ${newIdx}`,
        field_type: 'text',
        placeholder: 'Enter details...',
        help_text: '',
        is_required: true,
        display_order: newIdx,
        options_json: []
      }
    ]);
  }

  function handleRemoveField(index: number) {
    setFormFields(formFields.filter((_, i) => i !== index));
  }

  function handleFieldChange(index: number, key: string, value: any) {
    const updated = [...formFields];
    updated[index] = { ...updated[index], [key]: value };
    setFormFields(updated);
  }

  // Calculate totals
  const totalApps = categoryStats.reduce((sum, c) => sum + c.total_applications, 0);
  const totalNew = categoryStats.reduce((sum, c) => sum + c.new_applications, 0);
  const totalUnderReview = categoryStats.reduce((sum, c) => sum + c.under_review, 0);
  const totalCorrection = categoryStats.reduce((sum, c) => sum + c.documents_required, 0);
  const totalApproved = categoryStats.reduce((sum, c) => sum + c.approved, 0);
  const totalRejected = categoryStats.reduce((sum, c) => sum + c.rejected, 0);

  return (
    <div className="portal-container" style={{ minHeight: '80vh', background: '#f8fafc', paddingBottom: '3rem' }}>
      {/* Sub-Header / Government Admin Banner */}
      <div style={{
        background: '#1e3a8a',
        color: '#ffffff',
        padding: '1.25rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: '#ea580c', padding: '0.6rem', borderRadius: '8px' }}>
            <Shield size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#cbd5e1' }}>
              Government of Karnataka &bull; Social Welfare
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: '2px 0 0' }}>
              Welfare Admin Portal
            </h2>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <div style={{ textAlign: 'right', fontSize: '0.8rem' }}>
            <div style={{ fontWeight: 600 }}>{userName}</div>
            <div style={{ color: '#93c5fd' }}>Role: {userRole}</div>
          </div>
          <button 
            onClick={() => { setRefreshing(true); loadPortalData(); }}
            className="btn-secondary" 
            style={{ fontSize: '0.78rem', padding: '0.4rem 0.75rem', background: 'rgba(255,255,255,0.15)', color: '#ffffff', border: '1px solid rgba(255,255,255,0.3)' }}
          >
            <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} /> Refresh
          </button>
        </div>
      </div>

      {/* Navigation Bar for Government Admin (11 Required Portal Items) */}
      <div style={{
        background: '#ffffff',
        borderBottom: '1px solid var(--line)',
        padding: '0 1.5rem',
        display: 'flex',
        gap: '0.25rem',
        overflowX: 'auto',
        alignItems: 'center'
      }}>
        {/* 1. Dashboard */}
        <button 
          className={`nav-link-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Dashboard
        </button>

        {/* 2. Scheme Management */}
        <button 
          className={`nav-link-btn ${activeTab === 'categories' || activeTab === 'category-detail' ? 'active' : ''}`}
          onClick={() => { setSelectedCategory(null); setSelectedScheme(null); setActiveTab('categories'); }}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Scheme Management
        </button>

        {/* 2b. Form Builder */}
        <button 
          className={`nav-link-btn ${activeTab === 'form-builder' ? 'active' : ''}`}
          onClick={() => {
            if (!builderScheme && allSchemes.length > 0) {
              loadSchemeForBuilder(allSchemes[0]);
            }
            setActiveTab('form-builder');
          }}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600, color: '#ea580c' }}
        >
          Form Builder
        </button>

        {/* 3. Application Management */}
        <button 
          className={`nav-link-btn ${activeTab === 'applications' ? 'active' : ''}`}
          onClick={() => {
            setCategoryFilter(undefined);
            setSchemeFilter(undefined);
            loadFilteredApplications();
            setActiveTab('applications');
          }}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Application Management ({totalApps})
        </button>

        {/* 4. Application Scrutiny */}
        <button 
          className={`nav-link-btn ${activeTab === 'scrutiny' ? 'active' : ''}`}
          onClick={() => {
            setStatusFilter('');
            setCategoryFilter(undefined);
            setSchemeFilter(undefined);
            loadFilteredApplications();
            setActiveTab('scrutiny');
          }}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Application Scrutiny ({totalNew + totalUnderReview})
        </button>

        {/* 5. Beneficiary Management */}
        <button 
          className={`nav-link-btn ${activeTab === 'beneficiaries' ? 'active' : ''}`}
          onClick={() => setActiveTab('beneficiaries')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Beneficiary Registry ({beneficiaries.length > 0 ? beneficiaries.length : totalApproved})
        </button>

        {/* 6. DBT Management */}
        <button 
          className={`nav-link-btn ${activeTab === 'dbt' ? 'active' : ''}`}
          onClick={() => setActiveTab('dbt')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          DBT Management
        </button>

        {/* 7. Grievance Management */}
        <button 
          className={`nav-link-btn ${activeTab === 'grievances' ? 'active' : ''}`}
          onClick={() => setActiveTab('grievances')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Grievance Management ({grievances.length})
        </button>

        {/* 8. Reports */}
        <button 
          className={`nav-link-btn ${activeTab === 'reports' ? 'active' : ''}`}
          onClick={() => setActiveTab('reports')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Reports
        </button>

        {/* 9. Notifications */}
        <button 
          className={`nav-link-btn ${activeTab === 'notifications' ? 'active' : ''}`}
          onClick={() => setActiveTab('notifications')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Notifications
        </button>

        {/* 10. Profile */}
        <button 
          className={`nav-link-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Profile
        </button>

        {/* 11. Logout */}
        <button 
          className="nav-link-btn"
          onClick={onLogout}
          style={{ padding: '0.85rem 0.95rem', fontSize: '0.82rem', fontWeight: 600, color: '#dc2626', marginLeft: 'auto' }}
        >
          Logout
        </button>
      </div>

      <div style={{ padding: '1.5rem 2rem' }}>
        {/* TAB 1: OVERVIEW DASHBOARD */}
        {activeTab === 'dashboard' && (
          <div>
            {/* Top KPI Metrics Row */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.75rem' }}>
              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Applications</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: 'var(--navy-dark)', marginTop: '0.35rem' }}>{totalApps}</div>
                <div style={{ fontSize: '0.72rem', color: '#10b981', marginTop: '0.25rem' }}>{categoryStats.length} categories</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>New Submissions</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#ea580c', marginTop: '0.35rem' }}>{totalNew}</div>
                <div style={{ fontSize: '0.72rem', color: '#ea580c', marginTop: '0.25rem' }}>Awaiting review</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>In Review</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#3b82f6', marginTop: '0.35rem' }}>{totalUnderReview}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Under scrutiny</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Action Required</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#f59e0b', marginTop: '0.35rem' }}>{totalCorrection}</div>
                <div style={{ fontSize: '0.72rem', color: '#f59e0b', marginTop: '0.25rem' }}>Pending citizen action</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Approved</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#10b981', marginTop: '0.35rem' }}>{totalApproved}</div>
                <div style={{ fontSize: '0.72rem', color: '#10b981', marginTop: '0.25rem' }}>Sanctioned</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', boxShadow: '0 1px 4px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Rejected</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#ef4444', marginTop: '0.35rem' }}>{totalRejected}</div>
                <div style={{ fontSize: '0.72rem', color: '#ef4444', marginTop: '0.25rem' }}>Not approved</div>
              </div>
            </div>

            {/* Category Quick Navigation Cards */}
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Welfare Scheme Categories
                </h3>
                <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                  Select a category to view schemes
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
                {categoryStats.map(cat => (
                  <div 
                    key={cat.category_id}
                    onClick={() => {
                      setSelectedCategory(cat);
                      setActiveTab('category-detail');
                    }}
                    style={{
                      background: '#ffffff',
                      border: '1px solid var(--line)',
                      borderRadius: '8px',
                      padding: '1.25rem',
                      cursor: 'pointer',
                      transition: 'transform 0.15s ease, box-shadow 0.15s ease',
                      boxShadow: '0 2px 6px rgba(0,0,0,0.04)'
                    }}
                    onMouseEnter={e => (e.currentTarget.style.borderColor = '#ea580c')}
                    onMouseLeave={e => (e.currentTarget.style.borderColor = 'var(--line)')}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, background: '#eff6ff', color: '#1d4ed8', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                        {cat.category_code}
                      </span>
                      <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#0f172a' }}>
                        {cat.total_applications} Apps
                      </span>
                    </div>

                    <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.35rem' }}>
                      {cat.category_name}
                    </h4>
                    <p style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: '0.85rem', lineHeight: '1.4' }}>
                      {cat.description || 'Verified welfare programs and direct benefit delivery mechanisms.'}
                    </p>

                    {/* Mini Stats Bar */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem', background: '#f8fafc', padding: '0.5rem', borderRadius: '6px', fontSize: '0.72rem', textAlign: 'center' }}>
                      <div>
                        <div style={{ color: '#ea580c', fontWeight: 700 }}>{cat.new_applications}</div>
                        <div style={{ color: '#64748b' }}>New</div>
                      </div>
                      <div>
                        <div style={{ color: '#3b82f6', fontWeight: 700 }}>{cat.under_review}</div>
                        <div style={{ color: '#64748b' }}>Review</div>
                      </div>
                      <div>
                        <div style={{ color: '#10b981', fontWeight: 700 }}>{cat.approved}</div>
                        <div style={{ color: '#64748b' }}>Approved</div>
                      </div>
                      <div>
                        <div style={{ color: '#ef4444', fontWeight: 700 }}>{cat.rejected}</div>
                        <div style={{ color: '#64748b' }}>Rejected</div>
                      </div>
                    </div>

                    <div style={{ marginTop: '0.85rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: '#ea580c', fontWeight: 600 }}>
                      <span>{cat.schemes.length} Schemes Assigned</span>
                      <span>Open Category Desk &rarr;</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: CATEGORIES LIST */}
        {activeTab === 'categories' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Welfare Scheme Category Desks
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Applications submitted by citizens are automatically categorized based on the scheme's department assignment.
                </p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('dashboard')}>
                &larr; Back to Dashboard
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem' }}>
              {categoryStats.map(cat => (
                <div 
                  key={cat.category_id}
                  style={{
                    background: '#ffffff',
                    border: '1px solid var(--line)',
                    borderRadius: '8px',
                    padding: '1.5rem',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.04)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <h4 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                      {cat.category_name}
                    </h4>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, background: '#eff6ff', color: '#1d4ed8', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                      {cat.category_code}
                    </span>
                  </div>

                  <p style={{ fontSize: '0.82rem', color: '#64748b', marginBottom: '1rem' }}>
                    {cat.description}
                  </p>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', marginBottom: '1rem', background: '#f8fafc', padding: '0.75rem', borderRadius: '6px', textAlign: 'center' }}>
                    <div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--navy-dark)' }}>{cat.total_applications}</div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b' }}>Total Apps</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ea580c' }}>{cat.new_applications}</div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b' }}>New / Pending</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#10b981' }}>{cat.approved}</div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b' }}>Approved</div>
                    </div>
                  </div>

                  <div style={{ borderTop: '1px solid var(--line)', paddingTop: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.78rem', color: '#64748b' }}>
                      <strong>{cat.schemes.length}</strong> Schemes Assigned
                    </span>
                    <button 
                      className="btn-primary" 
                      style={{ fontSize: '0.78rem', padding: '0.4rem 0.85rem' }}
                      onClick={() => {
                        setSelectedCategory(cat);
                        setActiveTab('category-detail');
                      }}
                    >
                      Manage Category &rarr;
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: CATEGORY DETAIL WITH SCHEME-WISE BREAKDOWN */}
        {activeTab === 'category-detail' && selectedCategory && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <button 
                  onClick={() => setActiveTab('categories')}
                  className="btn-secondary" 
                  style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem', marginBottom: '0.5rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                >
                  <ArrowLeft size={13} /> Back to Categories
                </button>
                <h3 style={{ fontSize: '1.35rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Category Desk: {selectedCategory.category_name}
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  {selectedCategory.description}
                </p>
              </div>

              <button 
                className="btn-primary"
                onClick={() => {
                  setCategoryFilter(selectedCategory.category_id);
                  setSchemeFilter(undefined);
                  loadFilteredApplications(selectedCategory.category_id);
                  setActiveTab('applications');
                }}
              >
                View Applications ({selectedCategory.total_applications}) &rarr;
              </button>
            </div>

            {/* Scheme-wise Breakdown Grid inside this Category */}
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.75rem' }}>
                Schemes Under {selectedCategory.category_name} ({selectedCategory.schemes.length})
              </h4>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.25rem' }}>
                {selectedCategory.schemes.map(sc => (
                  <div 
                    key={sc.scheme_id}
                    style={{
                      background: '#ffffff',
                      border: '1px solid var(--line)',
                      borderRadius: '8px',
                      padding: '1.25rem',
                      boxShadow: '0 2px 6px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.72rem', fontWeight: 600, background: '#f1f5f9', color: '#334155', padding: '0.2rem 0.45rem', borderRadius: '4px' }}>
                        {sc.scheme_code}
                      </span>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, background: '#eff6ff', color: '#1d4ed8', padding: '0.2rem 0.45rem', borderRadius: '4px' }}>
                        {sc.application_mode.replace('_', ' ')}
                      </span>
                    </div>

                    <h5 style={{ fontSize: '1rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.75rem' }}>
                      {sc.scheme_name}
                    </h5>

                    {/* Stats for this scheme */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.35rem', background: '#f8fafc', padding: '0.5rem', borderRadius: '6px', fontSize: '0.72rem', textAlign: 'center', marginBottom: '0.85rem' }}>
                      <div>
                        <div style={{ fontWeight: 700, color: 'var(--navy-dark)' }}>{sc.total_applications}</div>
                        <div style={{ color: '#64748b' }}>Total</div>
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, color: '#ea580c' }}>{sc.submitted}</div>
                        <div style={{ color: '#64748b' }}>New</div>
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, color: '#3b82f6' }}>{sc.under_review}</div>
                        <div style={{ color: '#64748b' }}>Review</div>
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, color: '#10b981' }}>{sc.approved}</div>
                        <div style={{ color: '#64748b' }}>Approved</div>
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, color: '#ef4444' }}>{sc.rejected}</div>
                        <div style={{ color: '#64748b' }}>Rejected</div>
                      </div>
                    </div>

                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      <button 
                        className="btn-secondary" 
                        style={{ flex: 1, fontSize: '0.75rem', padding: '0.4rem', textAlign: 'center', justifyContent: 'center' }}
                        onClick={() => {
                          setSelectedScheme(sc);
                          setCategoryFilter(selectedCategory.category_id);
                          setSchemeFilter(sc.scheme_id);
                          loadFilteredApplications(selectedCategory.category_id, sc.scheme_id);
                          setActiveTab('applications');
                        }}
                      >
                        Apps ({sc.total_applications}) &rarr;
                      </button>
                      <button 
                        className="btn-orange" 
                        style={{ fontSize: '0.75rem', padding: '0.4rem 0.65rem', textAlign: 'center' }}
                        onClick={() => {
                          const fullScheme = allSchemes.find(s => s.id === sc.scheme_id);
                          if (fullScheme) {
                            loadSchemeForBuilder(fullScheme);
                          } else {
                            loadSchemeForBuilder({
                              id: sc.scheme_id,
                              name: sc.scheme_name,
                              scheme_code: sc.scheme_code,
                              category_id: selectedCategory.category_id,
                              department: 'Social Welfare Department',
                              administering_authority: 'Social Welfare Department',
                              description: sc.scheme_name,
                              benefit_summary: 'Direct Welfare Benefit',
                              benefit_type: 'DIRECT_BENEFIT_TRANSFER',
                              eligibility_summary: 'Karnataka Resident',
                              application_instructions: 'Apply online with verification',
                              application_start_date: '2026-01-01',
                              application_end_date: '2026-12-31',
                              status: 'PUBLISHED'
                            });
                          }
                          setActiveTab('form-builder');
                        }}
                        title="Configure scheme-specific dynamic application form"
                      >
                        Edit Form 📝
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 3B: UNIVERSAL APPLICATION FORM BUILDER */}
        {activeTab === 'form-builder' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div>
                <button 
                  onClick={() => setActiveTab('categories')}
                  className="btn-secondary" 
                  style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem', marginBottom: '0.5rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                >
                  <ArrowLeft size={13} /> Back to Scheme Management
                </button>
                <h3 style={{ fontSize: '1.35rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Universal Scheme Application Form Builder
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Configure independent scheme-specific application questionnaires, validations, and field controls for any welfare program.
                </p>
              </div>

              {/* Scheme Selector Dropdown */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--navy-dark)' }}>
                  Selected Scheme:
                </label>
                <select 
                  className="filter-select"
                  style={{ minWidth: '280px', fontWeight: 600 }}
                  value={builderScheme ? builderScheme.id : ''}
                  onChange={e => {
                    const found = allSchemes.find(s => s.id === Number(e.target.value));
                    if (found) loadSchemeForBuilder(found);
                  }}
                >
                  {allSchemes.map(s => (
                    <option key={s.id} value={s.id}>
                      {s.scheme_code} — {s.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {builderMsg && (
              <div style={{ 
                padding: '0.85rem 1.25rem', 
                borderRadius: '8px', 
                marginBottom: '1.25rem',
                fontSize: '0.85rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                background: builderMsg.type === 'success' ? '#ecfdf5' : '#fef2f2',
                color: builderMsg.type === 'success' ? '#065f46' : '#991b1b',
                border: `1px solid ${builderMsg.type === 'success' ? '#a7f3d0' : '#fecaca'}`
              }}>
                {builderMsg.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
                <span>{builderMsg.text}</span>
              </div>
            )}

            {builderLoading ? (
              <div style={{ textAlign: 'center', padding: '3.5rem', color: '#64748b' }}>
                <RefreshCw size={24} className="animate-spin" style={{ margin: '0 auto 0.5rem' }} />
                <p>Loading scheme form configuration...</p>
              </div>
            ) : builderScheme ? (
              <form onSubmit={handleSaveFormBuilder}>
                <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                  {/* Left Column: Form Header & Fields */}
                  <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.75rem' }}>
                      <div>
                        <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', fontWeight: 700, margin: 0 }}>
                          Form Configuration: {builderScheme.scheme_code}
                        </h4>
                        <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                          Active Version: <strong>v{formVersion}</strong> &bull; Total Fields: <strong>{formFields.length}</strong>
                        </span>
                      </div>
                      <button
                        type="button"
                        onClick={handleAddField}
                        className="btn-orange"
                        style={{ fontSize: '0.78rem', padding: '0.4rem 0.85rem' }}
                      >
                        + Add Custom Field
                      </button>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                        Form Title <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <input 
                        type="text" 
                        required 
                        className="form-input" 
                        value={formTitle}
                        onChange={e => setFormTitle(e.target.value)}
                        placeholder="e.g. Gruha Lakshmi Beneficiary Registration Form"
                      />
                    </div>

                    <div style={{ marginBottom: '1.25rem' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                        Scheme Form Instructions & Purpose
                      </label>
                      <textarea 
                        rows={2} 
                        className="form-input" 
                        value={formDesc}
                        onChange={e => setFormDesc(e.target.value)}
                        placeholder="Describe eligibility conditions and purpose of this specific form..."
                      />
                    </div>

                    {/* Field List Editor */}
                    <h5 style={{ fontSize: '0.92rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.75rem' }}>
                      Configured Application Fields
                    </h5>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {formFields.map((f, idx) => (
                        <div key={idx} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '6px', padding: '1rem', position: 'relative' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#1e40af' }}>
                              Field #{idx + 1} &bull; Identifier: {f.field_name}
                            </span>
                            <button
                              type="button"
                              onClick={() => handleRemoveField(idx)}
                              style={{ background: 'none', border: 'none', color: '#dc2626', cursor: 'pointer', fontSize: '0.75rem', fontWeight: 600 }}
                            >
                              Remove &times;
                            </button>
                          </div>

                          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '0.75rem', marginBottom: '0.5rem' }}>
                            <div>
                              <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '0.2rem' }}>Field Label</label>
                              <input 
                                type="text"
                                className="form-input"
                                value={f.field_label}
                                onChange={e => handleFieldChange(idx, 'field_label', e.target.value)}
                              />
                            </div>
                            <div>
                              <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '0.2rem' }}>Input Type</label>
                              <select 
                                className="form-input"
                                value={f.field_type}
                                onChange={e => handleFieldChange(idx, 'field_type', e.target.value)}
                              >
                                <option value="text">Short Text</option>
                                <option value="number">Number</option>
                                <option value="textarea">Long Text / Address</option>
                                <option value="date">Date</option>
                                <option value="select">Dropdown Select</option>
                                <option value="radio">Radio Buttons</option>
                                <option value="checkbox">Declaration Checkbox</option>
                              </select>
                            </div>
                          </div>

                          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.5rem' }}>
                            <div>
                              <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '0.2rem' }}>Placeholder Text</label>
                              <input 
                                type="text"
                                className="form-input"
                                value={f.placeholder}
                                onChange={e => handleFieldChange(idx, 'placeholder', e.target.value)}
                              />
                            </div>
                            <div>
                              <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '0.2rem' }}>Help / Guidance Text</label>
                              <input 
                                type="text"
                                className="form-input"
                                value={f.help_text}
                                onChange={e => handleFieldChange(idx, 'help_text', e.target.value)}
                              />
                            </div>
                          </div>

                          {(f.field_type === 'select' || f.field_type === 'radio') && (
                            <div style={{ marginBottom: '0.5rem' }}>
                              <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#475569', marginBottom: '0.2rem' }}>
                                Options (comma-separated)
                              </label>
                              <input 
                                type="text"
                                className="form-input"
                                placeholder="Option 1, Option 2, Option 3"
                                value={f.options_json.join(', ')}
                                onChange={e => handleFieldChange(idx, 'options_json', e.target.value.split(',').map(s => s.trim()).filter(Boolean))}
                              />
                            </div>
                          )}

                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.4rem' }}>
                            <input 
                              type="checkbox"
                              id={`req-${idx}`}
                              checked={f.is_required}
                              onChange={e => handleFieldChange(idx, 'is_required', e.target.checked)}
                            />
                            <label htmlFor={`req-${idx}`} style={{ fontSize: '0.78rem', color: '#334155', cursor: 'pointer' }}>
                              Mandatory Field (Validation Required)
                            </label>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                      <button 
                        type="button"
                        onClick={() => loadSchemeForBuilder(builderScheme)}
                        className="btn-secondary"
                        disabled={builderLoading}
                      >
                        Reset Changes
                      </button>
                      <button 
                        type="submit"
                        className="btn-orange"
                        style={{ padding: '0.65rem 1.75rem', fontWeight: 700 }}
                        disabled={builderLoading}
                      >
                        {builderLoading ? 'Publishing Form...' : 'Publish Form Version &rarr;'}
                      </button>
                    </div>
                  </div>

                  {/* Right Column: Live Citizen Form Preview */}
                  <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.5rem', height: 'fit-content' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.75rem' }}>
                      <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#ea580c', background: '#fff7ed', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                        LIVE CITIZEN PREVIEW
                      </span>
                      <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                        (Exact interactive view rendered for applicant)
                      </span>
                    </div>

                    <div style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                      <h4 style={{ fontSize: '1.1rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.35rem' }}>
                        {formTitle || 'Application Form Title'}
                      </h4>
                      <p style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: '1.25rem' }}>
                        {formDesc || 'Scheme application instructions and eligibility criteria...'}
                      </p>

                      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {formFields.map((f, idx) => (
                          <div key={idx}>
                            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '0.25rem' }}>
                              {f.field_label} {f.is_required && <span style={{ color: '#dc2626' }}>*</span>}
                            </label>
                            {f.field_type === 'textarea' ? (
                              <textarea rows={2} className="form-input" placeholder={f.placeholder} disabled />
                            ) : f.field_type === 'select' ? (
                              <select className="form-input" disabled>
                                <option>-- Select {f.field_label} --</option>
                                {f.options_json.map((opt, i) => <option key={i}>{opt}</option>)}
                              </select>
                            ) : f.field_type === 'radio' ? (
                              <div style={{ display: 'flex', gap: '0.75rem' }}>
                                {f.options_json.map((opt, i) => (
                                  <label key={i} style={{ fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                    <input type="radio" disabled /> {opt}
                                  </label>
                                ))}
                              </div>
                            ) : f.field_type === 'checkbox' ? (
                              <label style={{ fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                                <input type="checkbox" disabled /> I confirm and agree
                              </label>
                            ) : (
                              <input type={f.field_type} className="form-input" placeholder={f.placeholder} disabled />
                            )}
                            {f.help_text && (
                              <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '0.2rem' }}>{f.help_text}</div>
                            )}
                          </div>
                        ))}
                      </div>

                      <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid #e2e8f0' }}>
                        <button type="button" className="btn-orange" style={{ width: '100%', opacity: 0.7 }} disabled>
                          Submit Scheme Application (Preview)
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            ) : (
              <div style={{ textAlign: 'center', padding: '3.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <p style={{ color: '#64748b' }}>Select a scheme above to configure its application form.</p>
              </div>
            )}
          </div>
        )}

        {/* TAB 4: APPLICATIONS LIST WITH MULTI-FILTERING & ACTIONS */}
        {activeTab === 'applications' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Application Scrutiny
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  {applications.length} applications
                </p>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="btn-secondary"
                  onClick={() => {
                    setCategoryFilter(undefined);
                    setSchemeFilter(undefined);
                    setStatusFilter('');
                    setDistrictFilter('');
                    setSearchQuery('');
                    loadFilteredApplications();
                  }}
                  style={{ fontSize: '0.8rem' }}
                >
                  Clear All Filters
                </button>
              </div>
            </div>

            {/* Filter Bar */}
            <div style={{
              background: '#ffffff',
              border: '1px solid var(--line)',
              borderRadius: '8px',
              padding: '1rem',
              display: 'flex',
              flexWrap: 'wrap',
              gap: '0.75rem',
              alignItems: 'center',
              marginBottom: '1.25rem'
            }}>
              <input 
                type="text" 
                placeholder="Search Application #, Citizen Name, or Citizen ID..."
                className="filter-input"
                style={{ flex: '1 1 240px' }}
                value={searchQuery}
                onChange={e => {
                  setSearchQuery(e.target.value);
                  loadFilteredApplications(categoryFilter, schemeFilter, statusFilter, districtFilter, e.target.value);
                }}
              />

              <select 
                className="filter-select"
                value={categoryFilter || ''}
                onChange={e => {
                  const val = e.target.value ? parseInt(e.target.value) : undefined;
                  setCategoryFilter(val);
                  setSchemeFilter(undefined);
                  loadFilteredApplications(val, undefined, statusFilter, districtFilter, searchQuery);
                }}
                style={{ flex: '0 1 200px' }}
              >
                <option value="">All Categories</option>
                {categoryStats.map(c => (
                  <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
                ))}
              </select>

              <select 
                className="filter-select"
                value={statusFilter}
                onChange={e => {
                  setStatusFilter(e.target.value);
                  loadFilteredApplications(categoryFilter, schemeFilter, e.target.value, districtFilter, searchQuery);
                }}
                style={{ flex: '0 1 180px' }}
              >
                <option value="">All Statuses</option>
                <option value="SUBMITTED">SUBMITTED</option>
                <option value="UNDER_REVIEW">UNDER_REVIEW</option>
                <option value="DOCUMENTS_REQUIRED">DOCUMENTS_REQUIRED</option>
                <option value="APPROVED">APPROVED</option>
                <option value="REJECTED">REJECTED</option>
              </select>

              <select 
                className="filter-select"
                value={districtFilter}
                onChange={e => {
                  setDistrictFilter(e.target.value);
                  loadFilteredApplications(categoryFilter, schemeFilter, statusFilter, e.target.value, searchQuery);
                }}
                style={{ flex: '0 1 180px' }}
              >
                <option value="">All Districts</option>
                <option value="Bengaluru Urban">Bengaluru Urban</option>
                <option value="Bengaluru Rural">Bengaluru Rural</option>
                <option value="Mysuru">Mysuru</option>
                <option value="Dharwad">Dharwad</option>
                <option value="Belagavi">Belagavi</option>
                <option value="Kalaburagi">Kalaburagi</option>
                <option value="Dakshina Kannada">Dakshina Kannada</option>
              </select>
            </div>

            {/* Applications Table */}
            {applications.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <FileText size={36} color="#94a3b8" style={{ margin: '0 auto 0.75rem' }} />
                <h4 style={{ fontSize: '1.1rem', color: '#0f172a' }}>No Applications Found</h4>
                <p style={{ color: '#64748b', fontSize: '0.85rem' }}>No submitted applications matched your current category or search criteria.</p>
              </div>
            ) : (
              <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflowX: 'auto', boxShadow: '0 2px 6px rgba(0,0,0,0.03)' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.82rem' }}>
                  <thead>
                    <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', color: '#475569' }}>
                      <th style={{ padding: '0.75rem 1rem' }}>Application ID</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Citizen Details</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Scheme & Category</th>
                      <th style={{ padding: '0.75rem 1rem' }}>District</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Status</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Submitted On</th>
                      <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Scrutiny Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {applications.map(app => (
                      <tr key={app.id} style={{ borderBottom: '1px solid var(--line)' }}>
                        <td style={{ padding: '0.75rem 1rem', fontWeight: 700, fontFamily: 'monospace', color: '#1e3a8a' }}>
                          {app.application_number}
                          {app.is_duplicate_suspect && (
                            <span style={{ display: 'block', fontSize: '0.68rem', color: '#dc2626', fontWeight: 600 }}>
                              ⚠️ Duplicate Suspect
                            </span>
                          )}
                        </td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <div style={{ fontWeight: 600, color: '#0f172a' }}>{app.citizen_name}</div>
                          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{app.citizen_id} &bull; {app.citizen_phone}</div>
                        </td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <div style={{ fontWeight: 600, color: 'var(--navy-dark)' }}>{app.scheme?.name || `Scheme #${app.scheme_id}`}</div>
                          <div style={{ fontSize: '0.72rem', color: '#ea580c', fontWeight: 600 }}>
                            {app.scheme?.category_id ? `Category #${app.scheme.category_id}` : 'General Category'}
                          </div>
                        </td>
                        <td style={{ padding: '0.75rem 1rem', color: '#475569' }}>{app.residence_district}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <span className={`status-badge ${app.status}`}>
                            {app.status.replace('_', ' ')}
                          </span>
                        </td>
                        <td style={{ padding: '0.75rem 1rem', color: '#64748b' }}>
                          {app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}
                        </td>
                        <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                          <button 
                            className="btn-primary" 
                            style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem' }}
                            onClick={() => {
                              setSelectedApp(app);
                              setReviewDecision('APPROVED');
                              setReviewRemarks('');
                              setActionMsg(null);
                              setActiveTab('application-detail');
                            }}
                          >
                            Scrutinize & Review &rarr;
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* TAB 5: APPLICATION DETAIL & SCRUTINY PANEL */}
        {activeTab === 'application-detail' && selectedApp && (
          <div style={{ maxWidth: '900px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <button 
                className="btn-secondary" 
                onClick={() => setActiveTab('applications')}
                style={{ fontSize: '0.78rem', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <ArrowLeft size={14} /> Back to Applications List
              </button>
              
              <button 
                className="btn-secondary"
                onClick={() => onViewReceipt(selectedApp.id)}
                style={{ fontSize: '0.78rem', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <Download size={14} /> Download PDF Receipt
              </button>
            </div>

            {/* Dossier Header Card */}
            <div style={{
              background: '#ffffff',
              border: '1px solid var(--line)',
              borderRadius: '8px',
              padding: '1.5rem',
              boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
              marginBottom: '1.5rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.85rem' }}>
                <div>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                    Welfare Dossier Review
                  </span>
                  <h3 style={{ fontSize: '1.35rem', color: 'var(--navy-dark)', fontWeight: 700, fontFamily: 'monospace' }}>
                    {selectedApp.application_number}
                  </h3>
                  <div style={{ fontSize: '0.85rem', color: '#ea580c', fontWeight: 600 }}>
                    {selectedApp.scheme?.name || `Scheme #${selectedApp.scheme_id}`}
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <span className={`status-badge ${selectedApp.status}`} style={{ fontSize: '0.85rem', padding: '0.35rem 0.75rem' }}>
                    {selectedApp.status.replace('_', ' ')}
                  </span>
                  <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.35rem' }}>
                    Submitted: {selectedApp.created_at ? new Date(selectedApp.created_at).toLocaleString() : 'N/A'}
                  </div>
                </div>
              </div>

              {/* Citizen Personal & Bank Particulars */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', fontSize: '0.82rem', marginBottom: '1.25rem' }}>
                <div>
                  <div style={{ color: '#64748b' }}>Applicant Name:</div>
                  <div style={{ fontWeight: 600, color: '#0f172a' }}>{selectedApp.citizen_name}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Citizen Permanent ID:</div>
                  <div style={{ fontWeight: 600, fontFamily: 'monospace' }}>{selectedApp.citizen_id}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Contact Phone:</div>
                  <div style={{ fontWeight: 600 }}>{selectedApp.citizen_phone}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Email:</div>
                  <div style={{ fontWeight: 600 }}>{selectedApp.citizen_email || 'Not provided'}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Annual Income:</div>
                  <div style={{ fontWeight: 600, color: '#15803d' }}>Rs. {Number(selectedApp.annual_income).toLocaleString()}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Caste / Social Category:</div>
                  <div style={{ fontWeight: 600 }}>{selectedApp.caste_category}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Residence District:</div>
                  <div style={{ fontWeight: 600 }}>{selectedApp.residence_district}</div>
                </div>
                <div>
                  <div style={{ color: '#64748b' }}>Aadhaar Seeded Bank Account:</div>
                  <div style={{ fontWeight: 600, fontFamily: 'monospace' }}>
                    {selectedApp.bank_account_number || 'N/A'} (IFSC: {selectedApp.bank_ifsc || 'N/A'})
                  </div>
                </div>
              </div>

              {/* Dynamic Scheme-Specific Submitted Form Responses */}
              {selectedApp.application_data_json && Object.keys(selectedApp.application_data_json).length > 0 && (
                <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '6px', border: '1px solid var(--line)', marginBottom: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.9rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.65rem' }}>
                    Scheme-Specific Dynamic Form Responses
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '0.75rem', fontSize: '0.8rem' }}>
                    {Object.entries(selectedApp.application_data_json).map(([k, v]) => (
                      <div key={k} style={{ background: '#ffffff', padding: '0.5rem 0.75rem', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                        <div style={{ color: '#64748b', fontSize: '0.72rem', textTransform: 'capitalize' }}>
                          {k.replace(/_/g, ' ')}
                        </div>
                        <div style={{ fontWeight: 600, color: '#0f172a', wordBreak: 'break-word' }}>
                          {typeof v === 'boolean' ? (v ? 'Yes' : 'No') : String(v)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Existing Admin Remarks if any */}
              {selectedApp.admin_remarks && (
                <div style={{ background: '#fffbeb', border: '1px solid #fde68a', padding: '0.85rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1.25rem' }}>
                  <strong style={{ color: '#b45309' }}>Previous Scrutiny Remarks:</strong> {selectedApp.admin_remarks}
                </div>
              )}

              {/* REDESIGNED WELFARE OFFICER OFFICIAL APPLICATION SCRUTINY & DECISION WORKFLOW */}
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
              </div>
            </div>
          </div>
        )}
        {/* TAB 4: CITIZEN GRIEVANCES */}
        {activeTab === 'grievances' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Citizen Grievances & Appeals
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '4px 0 0' }}>
                  Review and resolve citizen grievances, delays, document clarification appeals, and DBT queries.
                </p>
              </div>
              <button 
                onClick={loadPortalData}
                className="btn-secondary" 
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
              >
                <RefreshCw size={14} /> Refresh Grievances
              </button>
            </div>

            {grievanceMsg && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '6px',
                marginBottom: '1rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                background: grievanceMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                color: grievanceMsg.type === 'success' ? '#15803d' : '#b91c1c',
                border: `1px solid ${grievanceMsg.type === 'success' ? '#bbf7d0' : '#fecaca'}`
              }}>
                {grievanceMsg.text}
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: selectedGrievance ? '1.2fr 1fr' : '1fr', gap: '1.5rem' }}>
              <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.82rem' }}>
                  <thead>
                    <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', color: '#475569' }}>
                      <th style={{ padding: '0.75rem 1rem' }}>Grievance #</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Citizen</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Category & Subject</th>
                      <th style={{ padding: '0.75rem 1rem' }}>Status</th>
                      <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {grievances.length === 0 ? (
                      <tr>
                        <td colSpan={5} style={{ padding: '2.5rem', textAlign: 'center', color: '#64748b' }}>
                          No grievances logged. All citizen appeals are up to date.
                        </td>
                      </tr>
                    ) : (
                      grievances.map(g => (
                        <tr key={g.id} style={{ borderBottom: '1px solid var(--line)', background: selectedGrievance?.id === g.id ? '#f0f9ff' : 'transparent' }}>
                          <td style={{ padding: '0.75rem 1rem', fontFamily: 'monospace', fontWeight: 700, color: 'var(--navy-dark)' }}>
                            {g.grievance_number}
                          </td>
                          <td style={{ padding: '0.75rem 1rem' }}>
                            <div style={{ fontWeight: 600 }}>{g.citizen_name}</div>
                            <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{g.citizen_id}</div>
                          </td>
                          <td style={{ padding: '0.75rem 1rem' }}>
                            <div style={{ fontWeight: 600, color: 'var(--navy-dark)' }}>{g.subject}</div>
                            <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{g.category}</div>
                          </td>
                          <td style={{ padding: '0.75rem 1rem' }}>
                            <span className={`status-badge ${g.status === 'RESOLVED' ? 'APPROVED' : g.status === 'SUBMITTED' ? 'UNDER_REVIEW' : 'MORE_INFORMATION_REQUIRED'}`}>
                              {g.status}
                            </span>
                          </td>
                          <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                            <button 
                              className="btn-secondary"
                              onClick={() => {
                                setSelectedGrievance(g);
                                setGrievanceResolution(g.officer_response || '');
                                setGrievanceStatusDecision(g.status === 'SUBMITTED' ? 'RESOLVED' : g.status);
                              }}
                              style={{ fontSize: '0.75rem', padding: '0.3rem 0.65rem' }}
                            >
                              Review & Reply
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>

              {selectedGrievance && (
                <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem', height: 'fit-content' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h4 style={{ fontSize: '1rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                      Respond to Grievance
                    </h4>
                    <button 
                      onClick={() => setSelectedGrievance(null)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                    >
                      <X size={18} />
                    </button>
                  </div>

                  <div style={{ background: '#f8fafc', padding: '0.85rem', borderRadius: '6px', marginBottom: '1rem', fontSize: '0.8rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                      <span style={{ fontWeight: 700, fontFamily: 'monospace' }}>{selectedGrievance.grievance_number}</span>
                      <span style={{ color: '#64748b' }}>{selectedGrievance.citizen_name}</span>
                    </div>
                    <div style={{ fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>{selectedGrievance.subject}</div>
                    <p style={{ margin: 0, color: '#475569', fontSize: '0.78rem' }}>{selectedGrievance.description}</p>
                  </div>

                  <form onSubmit={handleResolveGrievance}>
                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                        Grievance Status Decision
                      </label>
                      <select 
                        value={grievanceStatusDecision}
                        onChange={e => setGrievanceStatusDecision(e.target.value)}
                        className="form-input"
                      >
                        <option value="UNDER_REVIEW">UNDER_REVIEW (Investigating)</option>
                        <option value="RESOLVED">RESOLVED (Action Taken)</option>
                        <option value="REJECTED">REJECTED (Invalid / Ineligible)</option>
                      </select>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.35rem' }}>
                        Officer Response to Citizen <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <textarea 
                        rows={4}
                        className="form-input"
                        placeholder="State official explanation, disbursement timeline, or instructions for the citizen..."
                        value={grievanceResolution}
                        onChange={e => setGrievanceResolution(e.target.value)}
                        required
                      />
                    </div>

                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button 
                        type="submit"
                        className="btn-primary"
                        disabled={grievanceActionLoading}
                        style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}
                      >
                        {grievanceActionLoading ? 'Saving...' : 'Send Official Response'}
                      </button>
                      <button 
                        type="button"
                        className="btn-secondary"
                        onClick={() => setSelectedGrievance(null)}
                        style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
          </div>
        )}
        {/* TAB 8: APPLICATION SCRUTINY */}
        {activeTab === 'scrutiny' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Application Scrutiny & Direct Verification Queue
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Filter and prioritize applications awaiting documentary validation, caste checks, and sanction mandates.
                </p>
              </div>
              <button 
                className="btn-secondary"
                onClick={() => {
                  setStatusFilter('UNDER_REVIEW');
                  loadFilteredApplications();
                }}
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
              >
                <RefreshCw size={14} /> Refresh Scrutiny Queue
              </button>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1rem', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
                <div style={{ flex: 1, minWidth: '220px' }}>
                  <input 
                    type="text" 
                    placeholder="Search applicant name, phone, or application ID..." 
                    className="filter-input"
                    style={{ width: '100%' }}
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                  />
                </div>
                <div style={{ width: '180px' }}>
                  <select 
                    className="filter-select"
                    style={{ width: '100%' }}
                    value={statusFilter}
                    onChange={e => setStatusFilter(e.target.value)}
                  >
                    <option value="">All Review Statuses (New & Review)</option>
                    <option value="SUBMITTED">SUBMITTED (New Submissions)</option>
                    <option value="UNDER_REVIEW">UNDER_REVIEW (Active Scrutiny)</option>
                    <option value="MORE_INFORMATION_REQUIRED">ACTION_REQUIRED (Docs Needed)</option>
                  </select>
                </div>
                <button 
                  className="btn-orange"
                  style={{ fontSize: '0.8rem', padding: '0.55rem 1rem' }}
                  onClick={() => loadFilteredApplications()}
                >
                  <Search size={14} /> Filter Queue
                </button>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflow: 'hidden' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Applicant Name</th>
                    <th>Scheme / Category</th>
                    <th>District</th>
                    <th>Income</th>
                    <th>Duplicate Suspect</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {applications.filter(a => !statusFilter || a.status === statusFilter).length === 0 ? (
                    <tr>
                      <td colSpan={8} style={{ textAlign: 'center', padding: '2.5rem', color: '#94a3b8' }}>
                        No applications in scrutiny for the selected filter.
                      </td>
                    </tr>
                  ) : (
                    applications.filter(a => !statusFilter || a.status === statusFilter).map(app => (
                      <tr key={app.id}>
                        <td style={{ fontWeight: 700, fontFamily: 'monospace' }}>{app.application_number}</td>
                        <td>{app.citizen_name}</td>
                        <td>{app.scheme_name || 'SWD Welfare Scheme'}</td>
                        <td>{app.residence_district}</td>
                        <td>₹{Number(app.annual_income).toLocaleString('en-IN')}</td>
                        <td>
                          {app.is_duplicate_suspect ? (
                            <span style={{ color: '#dc2626', fontWeight: 700, fontSize: '0.75rem' }}>Suspect Flagged</span>
                          ) : (
                            <span style={{ color: '#16a34a', fontSize: '0.75rem' }}>Verified Clear</span>
                          )}
                        </td>
                        <td>
                          <span className={`status-badge ${app.status}`}>{app.status.replace('_', ' ')}</span>
                        </td>
                        <td>
                          <button 
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
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 9: BENEFICIARY MANAGEMENT */}
        {activeTab === 'beneficiaries' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Sanctioned Beneficiary Registry
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Roster of approved citizens eligible for simulated DBT assistance across all SWD programs.
                </p>
              </div>
              <button 
                className="btn-secondary"
                onClick={() => {
                  setStatusFilter('APPROVED');
                  loadFilteredApplications();
                }}
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
              >
                <RefreshCw size={14} /> Refresh Beneficiaries
              </button>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflow: 'hidden' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Beneficiary Citizen</th>
                    <th>Contact</th>
                    <th>Sanction Mandate</th>
                    <th>Bank IFSC / A/C</th>
                    <th>Approval Date</th>
                    <th>Receipt</th>
                  </tr>
                </thead>
                <tbody>
                  {beneficiaries.length === 0 ? (
                    <tr>
                      <td colSpan={7} style={{ textAlign: 'center', padding: '2.5rem', color: '#94a3b8' }}>
                        No sanctioned beneficiaries found in current database records.
                      </td>
                    </tr>
                  ) : (
                    beneficiaries.map(ben => (
                      <tr key={ben.id}>
                        <td style={{ fontWeight: 700, fontFamily: 'monospace' }}>{ben.beneficiary_code}</td>
                        <td style={{ fontWeight: 600 }}>
                          {ben.citizen_name}
                          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{ben.citizen_id}</div>
                        </td>
                        <td>{allSchemes.find(s => s.id === ben.scheme_id)?.name || `Scheme #${ben.scheme_id}`}</td>
                        <td style={{ color: '#15803d', fontWeight: 700 }}>
                          ₹{Number(ben.sanctioned_amount || 10000).toLocaleString('en-IN')}
                        </td>
                        <td style={{ fontFamily: 'monospace', fontSize: '0.78rem' }}>
                          <span style={{ padding: '2px 6px', background: '#ecfdf5', color: '#065f46', borderRadius: '4px', fontSize: '0.72rem' }}>
                            {ben.disbursement_mode || 'DIRECT_BENEFIT_TRANSFER'}
                          </span>
                        </td>
                        <td>{ben.sanctioned_at ? new Date(ben.sanctioned_at).toLocaleDateString() : 'ACTIVE'}</td>
                        <td>
                          <button 
                            className="btn-secondary"
                            style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                            onClick={() => onViewReceipt(ben.application_id || ben.id)}
                          >
                            <Download size={13} /> Mandate
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 10: DBT MANAGEMENT */}
        {activeTab === 'dbt' && (
          <div>
            <div style={{
              backgroundColor: '#fffbeb',
              border: '2px solid #f59e0b',
              borderRadius: '8px',
              padding: '1rem 1.25rem',
              marginBottom: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.85rem'
            }}>
              <AlertTriangle size={24} color="#d97706" />
              <div>
                <strong style={{ color: '#92400e', fontSize: '0.9rem', display: 'block' }}>
                  DIRECT BENEFIT TRANSFER (DBT) SIMULATED CONSOLE
                </strong>
                <p style={{ color: '#b45309', fontSize: '0.78rem', margin: 0 }}>
                  This interface manages batch disbursement mandates and verifies duplicate payment controls. No live financial transactions are executed.
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
              <div className="admin-stat-card">
                <div className="stat-label">Total Approved for DBT</div>
                <div className="stat-val" style={{ color: '#15803d' }}>
                  {applications.filter(a => a.status === 'APPROVED').length}
                </div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Active DBT Mandates</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Total Mandate Value</div>
                <div className="stat-val" style={{ color: 'var(--navy-dark)' }}>
                  ₹{(applications.filter(a => a.status === 'APPROVED').reduce((sum, a) => sum + Number(a.sanctioned_amount || 10000), 0) / 100000).toFixed(2)}L
                </div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Aadhaar Bridge Direct</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Disbursement Engine Mode</div>
                <div className="stat-val" style={{ fontSize: '1.1rem', color: '#0284c7' }}>
                  Simulated APB
                </div>
                <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '0.25rem' }}>Ledger Intact & Seeded</div>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.5rem', textAlign: 'center' }}>
              <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>Direct Benefit Transfer Operations</h4>
              <p style={{ color: '#64748b', fontSize: '0.85rem', maxWidth: '600px', margin: '0 auto 1.25rem' }}>
                All approved applications are automatically queued for monthly DBT batch processing through the simulated Aadhaar Payment Bridge.
              </p>
              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                <a 
                  href={api.getBatchDbtReportUrl()} 
                  target="_blank" 
                  rel="noreferrer"
                  className="btn-secondary"
                  style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.5rem 1rem' }}
                >
                  <Download size={14} /> Download DBT Mandate Ledger (CSV)
                </a>
              </div>
            </div>
          </div>
        )}

        {/* TAB 11: REPORTS & DISTRICT ANALYTICS */}
        {activeTab === 'reports' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Social Welfare Performance & District Reports
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Comprehensive overview of application distribution, approval ratios, and taluk coverage across Karnataka.
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.75rem' }}>
              <div className="admin-stat-card">
                <div className="stat-label">Total Schemes Audited</div>
                <div className="stat-val">35</div>
                <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '0.25rem' }}>Active Catalogue</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Total Applications Received</div>
                <div className="stat-val">{totalApps}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Across All Districts</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Approval Ratio</div>
                <div className="stat-val" style={{ color: '#15803d' }}>
                  {totalApps > 0 ? Math.round((totalApproved / totalApps) * 100) : 0}%
                </div>
                <div style={{ fontSize: '0.72rem', color: '#15803d', marginTop: '0.25rem' }}>{totalApproved} Sanctioned</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Resolution Rate (Grievances)</div>
                <div className="stat-val" style={{ color: '#0284c7' }}>
                  {grievances.length > 0 ? Math.round((grievances.filter(g => g.status === 'RESOLVED').length / grievances.length) * 100) : 100}%
                </div>
                <div style={{ fontSize: '0.72rem', color: '#0284c7', marginTop: '0.25rem' }}>SWD Grievance Cell</div>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem' }}>
              <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem' }}>Category Application Distribution</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {categoryStats.map(c => (
                  <div key={c.category_id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 0.85rem', background: '#f8fafc', borderRadius: '6px' }}>
                    <span style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--navy-dark)' }}>{c.category_name}</span>
                    <div style={{ display: 'flex', gap: '1.25rem', fontSize: '0.78rem' }}>
                      <span>Total: <strong>{c.total_applications}</strong></span>
                      <span style={{ color: '#d97706' }}>Under Review: <strong>{c.under_review}</strong></span>
                      <span style={{ color: '#15803d' }}>Approved: <strong>{c.approved}</strong></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 12: NOTIFICATIONS */}
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
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div style={{ padding: '1rem', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '6px' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#166534', marginBottom: '0.25rem' }}>
                    DBT Direct Linkage Compliance Reminder
                  </div>
                  <p style={{ fontSize: '0.78rem', color: '#334155', margin: 0, lineHeight: 1.4 }}>
                    Ensure all sanction mandates carry verified Aadhaar seeded account credentials to prevent bridge rejections.
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '6px' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#1e40af', marginBottom: '0.25rem' }}>
                    Post-Matric Hostel Scrutiny Cycle 2026
                  </div>
                  <p style={{ fontSize: '0.78rem', color: '#334155', margin: 0, lineHeight: 1.4 }}>
                    Jurisdictional officers are requested to complete physical document verification for eligible applicants by end of the current quarter.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 13: OFFICER PROFILE */}
        {activeTab === 'profile' && (
          <div style={{ maxWidth: '640px', margin: '0 auto' }}>
            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.75rem' }}>
              <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                Welfare Officer Credentials
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.85rem', color: '#334155' }}>
                <div><strong>Officer Name:</strong> {userName}</div>
                <div><strong>Assigned Role:</strong> {userRole}</div>
                <div><strong>Department:</strong> Social Welfare Department (SWD)</div>
                <div><strong>Administrative Jurisdiction:</strong> Karnataka State Welfare Head Office</div>
                <div><strong>Portal Access Tier:</strong> Scrutiny, Mandate Issuance & Grievance Resolution</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
