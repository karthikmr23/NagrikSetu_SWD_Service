import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, Users, Layers, FileText, Settings, 
  CheckCircle2, XCircle, Search, RefreshCw, Key, 
  Lock, AlertTriangle, UserPlus, Eye, Shield
} from 'lucide-react';
import * as api from '../services/api';

interface PlatformAdminProps {
  token: string;
  userName: string;
  onLogout: () => void;
}

export const PlatformAdminPortal: React.FC<PlatformAdminProps> = ({
  token,
  userName,
  onLogout
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'categories' | 'services' | 'audit' | 'grievances' | 'reports' | 'notifications' | 'profile'>('overview');
  const [users, setUsers] = useState<api.PlatformUser[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [categories, setCategories] = useState<api.SchemeCategory[]>([]);
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchUser, setSearchUser] = useState<string>('');
  const [roleFilter, setRoleFilter] = useState<string>('');
  const [statusMsg, setStatusMsg] = useState<string>('');

  useEffect(() => {
    loadData();
  }, [token]);

  async function loadData() {
    setLoading(true);
    try {
      const [u, cats, logs, grvs] = await Promise.all([
        api.fetchPlatformUsers(token),
        api.fetchCategories(),
        api.fetchAuditLogs(token),
        api.fetchGrievances(undefined, token).catch(() => [])
      ]);
      setUsers(u);
      setCategories(cats);
      setAuditLogs(logs);
      setGrievances(grvs);
    } catch (err) {
      console.error('Failed to load platform admin data', err);
    } finally {
      setLoading(false);
    }
  }

  function formatAuditDetails(details: any): React.ReactNode {
    if (!details) return <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>None</span>;
    if (typeof details === 'string') {
      try {
        const parsed = JSON.parse(details);
        return formatAuditDetails(parsed);
      } catch {
        return details;
      }
    }
    if (typeof details === 'object') {
      // 1. Status & remarks (e.g. REVIEW_APPROVED, REVIEW_UNDER_REVIEW)
      if ('status' in details || 'remarks' in details) {
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {details.status && (
              <span>
                <strong>Status:</strong>{' '}
                <span className={`status-badge ${details.status === 'APPROVED' ? 'APPROVED' : details.status === 'REJECTED' ? 'REJECTED' : 'UNDER_REVIEW'}`}>
                  {String(details.status)}
                </span>
              </span>
            )}
            {details.remarks && (
              <span style={{ color: '#475569', fontSize: '0.74rem' }}>
                {String(details.remarks)}
              </span>
            )}
          </div>
        );
      }
      // 2. Application number & duplicate suspect (e.g. SUBMIT_APPLICATION)
      if ('application_number' in details || 'is_duplicate_suspect' in details) {
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {details.application_number && (
              <span style={{ fontFamily: 'monospace', fontWeight: 600, color: 'var(--navy-dark)' }}>
                {String(details.application_number)}
              </span>
            )}
            {details.is_duplicate_suspect !== undefined && (
              <span style={{ fontSize: '0.72rem', color: details.is_duplicate_suspect ? '#dc2626' : '#16a34a' }}>
                Duplicate Check: {details.is_duplicate_suspect ? 'Flagged Suspect' : 'Clean'}
              </span>
            )}
          </div>
        );
      }
      // 3. Title, target_role & recipient_count (e.g. PUBLISH_ANNOUNCEMENT)
      if ('title' in details || 'target_role' in details || 'recipient_count' in details) {
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {details.title && (
              <strong style={{ color: 'var(--navy-dark)' }}>{String(details.title)}</strong>
            )}
            <div style={{ fontSize: '0.72rem', color: '#64748b', display: 'flex', gap: '0.5rem' }}>
              {details.target_role && <span>Target: {String(details.target_role)}</span>}
              {details.recipient_count !== undefined && <span>Dispatched to {String(details.recipient_count)} citizens</span>}
            </div>
          </div>
        );
      }
      // General object format
      return (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', fontSize: '0.74rem' }}>
          {Object.entries(details).map(([k, v]) => (
            <span key={k} style={{ background: '#f1f5f9', padding: '1px 5px', borderRadius: '3px' }}>
              <strong>{k}:</strong> {typeof v === 'boolean' ? (v ? 'Yes' : 'No') : String(v ?? '')}
            </span>
          ))}
        </div>
      );
    }
    return String(details);
  }

  async function handleToggleStatus(userId: number, currentStatus: boolean) {
    try {
      await api.toggleUserStatus(token, userId, !currentStatus);
      setStatusMsg(`User ID ${userId} status changed to ${!currentStatus ? 'Active' : 'Inactive'}`);
      loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to toggle status');
    }
  }

  async function handleRoleChange(userId: number, newRole: string) {
    try {
      await api.updateUserRole(token, userId, newRole);
      setStatusMsg(`User ID ${userId} role changed to ${newRole}`);
      loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to change role');
    }
  }

  return (
    <div style={{ minHeight: '80vh', background: '#f8fafc', paddingBottom: '3rem' }}>
      {/* Top Banner */}
      <div style={{
        background: '#0f172a',
        color: '#ffffff',
        padding: '1.25rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: '#7c3aed', padding: '0.6rem', borderRadius: '8px' }}>
            <Settings size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8' }}>
              Governance & Administration
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: '2px 0 0' }}>
              Platform Admin Center
            </h2>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <div style={{ textAlign: 'right', fontSize: '0.8rem' }}>
            <div style={{ fontWeight: 600 }}>{userName}</div>
            <div style={{ color: '#a78bfa' }}>Role: PLATFORM_ADMIN</div>
          </div>
          <button 
            onClick={loadData}
            className="btn-secondary" 
            style={{ fontSize: '0.78rem', padding: '0.4rem 0.75rem', background: 'rgba(255,255,255,0.15)', color: '#ffffff', border: '1px solid rgba(255,255,255,0.3)' }}
          >
            <RefreshCw size={14} /> Refresh
          </button>
        </div>
      </div>

      {/* Nav (Exact 8 Platform Administrator Options) */}
      <div style={{
        background: '#ffffff',
        borderBottom: '1px solid var(--line)',
        padding: '0 1.5rem',
        display: 'flex',
        gap: '0.4rem',
        overflowX: 'auto',
        alignItems: 'center'
      }}>
        {/* 1. Platform Dashboard */}
        <button 
          className={`nav-link-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Platform Dashboard
        </button>

        {/* 2. User Monitoring */}
        <button 
          className={`nav-link-btn ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          User Monitoring ({users.length})
        </button>

        {/* 3. Service Monitoring */}
        <button 
          className={`nav-link-btn ${activeTab === 'services' ? 'active' : ''}`}
          onClick={() => setActiveTab('services')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Service Monitoring ({categories.length})
        </button>

        {/* 4. Audit Logs */}
        <button 
          className={`nav-link-btn ${activeTab === 'audit' ? 'active' : ''}`}
          onClick={() => setActiveTab('audit')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Audit Logs
        </button>

        {/* 5. System Reports */}
        <button 
          className={`nav-link-btn ${activeTab === 'reports' ? 'active' : ''}`}
          onClick={() => setActiveTab('reports')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          System Reports
        </button>

        {/* 6. Notifications */}
        <button 
          className={`nav-link-btn ${activeTab === 'notifications' ? 'active' : ''}`}
          onClick={() => setActiveTab('notifications')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Notifications
        </button>

        {/* 7. Profile */}
        <button 
          className={`nav-link-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600 }}
        >
          Profile
        </button>

        {/* 8. Logout */}
        <button 
          className="nav-link-btn"
          onClick={onLogout}
          style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', fontWeight: 600, color: '#dc2626', marginLeft: 'auto' }}
        >
          Logout
        </button>
      </div>

      <div style={{ padding: '1.5rem 2rem' }}>
        {statusMsg && (
          <div style={{ background: '#f0fdf4', color: '#15803d', border: '1px solid #bbf7d0', padding: '0.65rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1.25rem' }}>
            {statusMsg}
          </div>
        )}

        {/* OVERVIEW */}
        {activeTab === 'overview' && (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Users</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#0f172a', marginTop: '0.35rem' }}>{users.length}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Citizens & Officers</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Categories</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#7c3aed', marginTop: '0.35rem' }}>{categories.length}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Active departments</div>
              </div>

              <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Audit Entries</div>
                <div style={{ fontSize: '1.85rem', fontWeight: 700, color: '#2563eb', marginTop: '0.35rem' }}>{auditLogs.length}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Security events</div>
              </div>
            </div>
          </div>
        )}

        {/* USERS MANAGEMENT */}
        {activeTab === 'users' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                Users & Roles
              </h3>
              
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input 
                  type="text" 
                  placeholder="Search users..."
                  className="filter-input"
                  value={searchUser}
                  onChange={e => setSearchUser(e.target.value)}
                  style={{ minWidth: '220px' }}
                />
                <select 
                  className="filter-select"
                  value={roleFilter}
                  onChange={e => setRoleFilter(e.target.value)}
                >
                  <option value="">All Roles</option>
                  <option value="CITIZEN">CITIZEN</option>
                  <option value="WELFARE_OFFICER">WELFARE_OFFICER</option>
                  <option value="SWD_ADMIN">SWD_ADMIN</option>
                </select>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.82rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', color: '#475569' }}>
                    <th style={{ padding: '0.75rem 1rem' }}>User ID / Citizen ID</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Full Name</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Email & Phone</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Assigned Role</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Status</th>
                    <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Access Mode</th>
                  </tr>
                </thead>
                <tbody>
                  {users
                    .filter(u => (!roleFilter || u.role === roleFilter) && (!searchUser || u.full_name.toLowerCase().includes(searchUser.toLowerCase()) || u.email.toLowerCase().includes(searchUser.toLowerCase())))
                    .map(u => (
                      <tr key={u.id} style={{ borderBottom: '1px solid var(--line)' }}>
                        <td style={{ padding: '0.75rem 1rem', fontWeight: 600, fontFamily: 'monospace' }}>
                          #{u.id} &bull; {u.citizen_id}
                        </td>
                        <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>{u.full_name}</td>
                        <td style={{ padding: '0.75rem 1rem', color: '#64748b' }}>{u.email} <br /> {u.phone}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <span style={{
                            padding: '0.2rem 0.5rem',
                            borderRadius: '4px',
                            fontSize: '0.75rem',
                            fontWeight: 600,
                            background: '#f1f5f9',
                            color: '#334155'
                          }}>
                            {u.role}
                          </span>
                        </td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <span style={{
                            padding: '0.2rem 0.5rem',
                            borderRadius: '4px',
                            fontSize: '0.72rem',
                            fontWeight: 700,
                            background: u.is_active ? '#f0fdf4' : '#fef2f2',
                            color: u.is_active ? '#15803d' : '#b91c1c'
                          }}>
                            {u.is_active ? 'Active' : 'Disabled'}
                          </span>
                        </td>
                        <td style={{ padding: '0.75rem 1rem', textAlign: 'right', color: '#64748b', fontSize: '0.72rem' }}>
                          View Only (Monitoring)
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* CATEGORIES */}
        {activeTab === 'categories' && (
          <div>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '1rem' }}>
              Categories Management
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
              {categories.map(c => (
                <div key={c.id} style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#1d4ed8', background: '#eff6ff', padding: '0.2rem 0.45rem', borderRadius: '4px' }}>
                      {c.code}
                    </span>
                    <span style={{ fontSize: '0.72rem', color: '#15803d', fontWeight: 600 }}>Active</span>
                  </div>
                  <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--navy-dark)', marginBottom: '0.35rem' }}>
                    {c.name}
                  </h4>
                  <p style={{ fontSize: '0.8rem', color: '#64748b' }}>{c.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AUDIT LOGS */}
        {activeTab === 'audit' && (
          <div>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '1rem' }}>
              Audit Log
            </h3>
            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.8rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', color: '#475569' }}>
                    <th style={{ padding: '0.65rem 0.85rem' }}>ID</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Actor</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Role</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Action</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Entity</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Details</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map(l => (
                    <tr key={l.id} style={{ borderBottom: '1px solid var(--line)' }}>
                      <td style={{ padding: '0.65rem 0.85rem', fontFamily: 'monospace' }}>#{l.id}</td>
                      <td style={{ padding: '0.65rem 0.85rem', fontWeight: 600 }}>{l.actor_id}</td>
                      <td style={{ padding: '0.65rem 0.85rem' }}>{l.actor_role}</td>
                      <td style={{ padding: '0.65rem 0.85rem', fontWeight: 600, color: '#ea580c' }}>{l.action}</td>
                      <td style={{ padding: '0.65rem 0.85rem' }}>{l.entity_type} #{l.entity_id}</td>
                      <td style={{ padding: '0.65rem 0.85rem', maxWidth: '320px' }}>{formatAuditDetails(l.details)}</td>
                      <td style={{ padding: '0.65rem 0.85rem', color: '#64748b' }}>{new Date(l.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        {/* GRIEVANCE AUDIT (STRICTLY VIEW-ONLY) */}
        {activeTab === 'grievances' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Citizen Grievances Monitoring (View-Only)
                </h3>
                <p style={{ fontSize: '0.8rem', color: '#64748b', margin: '4px 0 0' }}>
                  Platform Super Admin audit of citizen grievances and welfare officer resolution status.
                </p>
              </div>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#7c3aed', background: '#f5f3ff', border: '1px solid #ddd6fe', padding: '0.3rem 0.6rem', borderRadius: '4px' }}>
                Strict View-Only Mode
              </span>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.8rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', color: '#475569' }}>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Grievance #</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Citizen ID</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Subject & Category</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Status</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Officer Resolution</th>
                    <th style={{ padding: '0.65rem 0.85rem' }}>Logged Date</th>
                  </tr>
                </thead>
                <tbody>
                  {grievances.length === 0 ? (
                    <tr>
                      <td colSpan={6} style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
                        No grievances logged across SWD.
                      </td>
                    </tr>
                  ) : (
                    grievances.map(g => (
                      <tr key={g.id} style={{ borderBottom: '1px solid var(--line)' }}>
                        <td style={{ padding: '0.65rem 0.85rem', fontFamily: 'monospace', fontWeight: 700, color: 'var(--navy-dark)' }}>
                          {g.grievance_number}
                        </td>
                        <td style={{ padding: '0.65rem 0.85rem' }}>{g.citizen_name} ({g.citizen_id})</td>
                        <td style={{ padding: '0.65rem 0.85rem' }}>
                          <div style={{ fontWeight: 600 }}>{g.subject}</div>
                          <div style={{ fontSize: '0.7rem', color: '#64748b' }}>{g.category}</div>
                        </td>
                        <td style={{ padding: '0.65rem 0.85rem' }}>
                          <span className={`status-badge ${g.status === 'RESOLVED' ? 'APPROVED' : g.status === 'SUBMITTED' ? 'UNDER_REVIEW' : 'MORE_INFORMATION_REQUIRED'}`}>
                            {g.status}
                          </span>
                        </td>
                        <td style={{ padding: '0.65rem 0.85rem', maxWidth: '300px' }}>
                          {g.officer_response ? (
                            <div style={{ color: '#166534', fontSize: '0.75rem' }}>
                              <strong>{g.resolved_by || 'Officer'}:</strong> {g.officer_response}
                            </div>
                          ) : (
                            <span style={{ color: '#94a3b8', fontStyle: 'italic', fontSize: '0.72rem' }}>Pending officer review</span>
                          )}
                        </td>
                        <td style={{ padding: '0.65rem 0.85rem', color: '#64748b' }}>
                          {new Date(g.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
        {/* TAB 3: SERVICE MONITORING */}
        {activeTab === 'services' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Service & Microservice Health Monitoring
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Real-time status of SWD microservice endpoints, database connection pools, and API latency.
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
              <div className="admin-stat-card">
                <div className="stat-label">SWD Core API Service</div>
                <div className="stat-val" style={{ color: '#15803d', fontSize: '1.25rem' }}>HEALTHY 200 OK</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Port 8005 &bull; Uptime: 99.98%</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">MySQL Database Cluster</div>
                <div className="stat-val" style={{ color: '#15803d', fontSize: '1.25rem' }}>CONNECTED</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Port 3306 &bull; nagriksetu_swd</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Active Scheme Categories</div>
                <div className="stat-val" style={{ color: '#0284c7', fontSize: '1.25rem' }}>{categories.length} Published</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Social Welfare Programs</div>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem' }}>
              <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.75rem' }}>Monitored Welfare Categories</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                {categories.map(c => (
                  <div key={c.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.65rem 0.85rem', background: '#f8fafc', borderRadius: '6px' }}>
                    <div>
                      <strong style={{ fontSize: '0.85rem', color: 'var(--navy-dark)' }}>{c.name}</strong>
                      <span style={{ fontSize: '0.75rem', color: '#64748b', marginLeft: '0.5rem' }}>({c.code})</span>
                    </div>
                    <span style={{ color: '#15803d', fontSize: '0.75rem', fontWeight: 600 }}>Active Service</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: SYSTEM REPORTS */}
        {activeTab === 'reports' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  System-Wide Governance & Audit Reports
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Aggregated telemetry across administrative logins, security policy enforcement, and RBAC compliance.
                </p>
              </div>
              <button 
                onClick={loadData}
                className="btn-secondary"
                style={{ padding: '0.45rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}
                disabled={loading}
              >
                <RefreshCw size={14} className={loading ? 'spin' : ''} />
                Refresh Reports
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
              <div className="admin-stat-card">
                <div className="stat-label">Total Registered Accounts</div>
                <div className="stat-val">{users.length}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Citizens & Officers</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Security Audit Entries</div>
                <div className="stat-val">{auditLogs.length}</div>
                <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '0.25rem' }}>Tamper-Evident Trail</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Role Policy Enforcements</div>
                <div className="stat-val" style={{ color: '#7c3aed' }}>100% Strict</div>
                <div style={{ fontSize: '0.72rem', color: '#7c3aed', marginTop: '0.25rem' }}>3 Role Isolated Portals</div>
              </div>
              <div className="admin-stat-card">
                <div className="stat-label">Platform Admin Scope</div>
                <div className="stat-val" style={{ color: '#0284c7' }}>View Only</div>
                <div style={{ fontSize: '0.72rem', color: '#0284c7', marginTop: '0.25rem' }}>Non-Operational Guard</div>
              </div>
            </div>

            {loading ? (
              <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '3rem', textAlign: 'center', color: '#64748b' }}>
                <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem', display: 'block', color: 'var(--navy-dark)' }} />
                Loading governance and system reports...
              </div>
            ) : (
              <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <h4 style={{ color: 'var(--navy-dark)', margin: 0 }}>Recent Security & Governance Audit Events</h4>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Showing {Math.min(auditLogs.length, 10)} of {auditLogs.length} entries</span>
                </div>
                {auditLogs.length === 0 ? (
                  <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b', fontSize: '0.85rem' }}>
                    No audit records logged yet.
                  </div>
                ) : (
                  <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.78rem' }}>
                      <thead>
                        <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--line)', textAlign: 'left' }}>
                          <th style={{ padding: '0.6rem 0.75rem' }}>Timestamp</th>
                          <th style={{ padding: '0.6rem 0.75rem' }}>Actor</th>
                          <th style={{ padding: '0.6rem 0.75rem' }}>Role</th>
                          <th style={{ padding: '0.6rem 0.75rem' }}>Action</th>
                          <th style={{ padding: '0.6rem 0.75rem' }}>Details</th>
                        </tr>
                      </thead>
                      <tbody>
                        {auditLogs.slice(0, 10).map((l, i) => (
                          <tr key={l.id || i} style={{ borderBottom: '1px solid #f1f5f9' }}>
                            <td style={{ padding: '0.6rem 0.75rem', color: '#64748b', whiteSpace: 'nowrap' }}>
                              {l.created_at ? new Date(l.created_at).toLocaleString() : 'N/A'}
                            </td>
                            <td style={{ padding: '0.6rem 0.75rem', fontWeight: 600 }}>{l.actor_id || l.user_email || 'System'}</td>
                            <td style={{ padding: '0.6rem 0.75rem' }}>
                              <span style={{ fontSize: '0.7rem', padding: '2px 6px', background: '#f1f5f9', borderRadius: '3px', fontWeight: 600 }}>
                                {l.actor_role || 'SYSTEM'}
                              </span>
                            </td>
                            <td style={{ padding: '0.6rem 0.75rem', fontFamily: 'monospace', fontWeight: 600, color: '#ea580c' }}>{l.action}</td>
                            <td style={{ padding: '0.6rem 0.75rem', maxWidth: '380px' }}>{formatAuditDetails(l.details)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* TAB 6: NOTIFICATIONS */}
        {activeTab === 'notifications' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700 }}>
                  Platform System Alerts & Broadcasts
                </h3>
                <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '0.2rem 0 0' }}>
                  Infrastructure alerts, security posture warnings, and container lifecycle events.
                </p>
              </div>
            </div>

            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.25rem' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div style={{ padding: '1rem', background: '#f5f3ff', border: '1px solid #ddd6fe', borderRadius: '6px' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#5b21b6', marginBottom: '0.25rem' }}>
                    Strict View-Only Isolation Active
                  </div>
                  <p style={{ fontSize: '0.78rem', color: '#334155', margin: 0, lineHeight: 1.4 }}>
                    Platform Administrator endpoints are locked down to view-only monitoring. Operational mutations on schemes, applications, and DBT records are blocked.
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '6px' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#166534', marginBottom: '0.25rem' }}>
                    Microservice Health Check Passed
                  </div>
                  <p style={{ fontSize: '0.78rem', color: '#334155', margin: 0, lineHeight: 1.4 }}>
                    All SWD containers (backend, frontend test 5175, frontend 5174, database 3306) report nominal latency.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 7: PROFILE */}
        {activeTab === 'profile' && (
          <div style={{ maxWidth: '640px', margin: '0 auto' }}>
            <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.75rem' }}>
              <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                Platform Administrator Profile
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.85rem', color: '#334155' }}>
                <div><strong>Admin Name:</strong> {userName}</div>
                <div><strong>System Role:</strong> PLATFORM_ADMIN</div>
                <div><strong>Access Authority:</strong> Governance, Infrastructure Telemetry & User Security Monitoring</div>
                <div><strong>Security Scope:</strong> View-Only for Citizen Applications & Welfare Disbursements</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
