const API_BASE = import.meta.env.VITE_SWD_API_URL !== undefined 
  ? import.meta.env.VITE_SWD_API_URL 
  : (typeof window !== 'undefined' && (window.location.port === '5175' || window.location.port === '5174') ? 'http://localhost:8005' : '');

export interface Scheme {
  id: number;
  scheme_code: string;
  name: string;
  category_id: number;
  department: string;
  administering_authority: string;
  description: string;
  benefit_summary: string;
  benefit_type: string;
  benefit_amount?: number;
  eligibility_summary: string;
  application_instructions: string;
  official_url?: string;
  beneficiary_categories?: string;
  verification_status?: string;
  application_mode?: string;
  application_start_date: string;
  application_end_date: string;
  status: string;
  rules?: any[];
  documents?: any[];
  category?: SchemeCategory | { id?: number; name?: string; code?: string };
}

export interface SchemeCategory {
  id: number;
  code: string;
  name: string;
  description?: string;
  icon?: string;
}

export interface Application {
  id: number;
  application_number: string;
  scheme_id: number;
  scheme_name?: string;
  category_id?: number;
  form_version_id?: number;
  citizen_id: string;
  citizen_name: string;
  citizen_email?: string;
  citizen_phone: string;
  annual_income: number;
  caste_category: string;
  residence_district: string;
  disability_percentage: number;
  bank_account_number?: string;
  bank_ifsc?: string;
  application_data_json?: Record<string, any>;
  status: string;
  is_duplicate_suspect?: boolean;
  duplicate_reason?: string;
  admin_remarks?: string;
  sanctioned_amount?: number;
  approved_at?: string;
  created_at?: string;
  updated_at?: string;
  scheme?: Scheme;
  documents?: any[];
  history?: any[];
}

export interface Beneficiary {
  id: number;
  beneficiary_code: string;
  application_id: number;
  scheme_id: number;
  citizen_id: string;
  citizen_name: string;
  sanctioned_amount: number;
  disbursement_mode: string;
  status: string;
  sanctioned_by: string;
  sanctioned_at: string;
}

export async function fetchCategories(): Promise<SchemeCategory[]> {
  const res = await fetch(`${API_BASE}/api/swd/categories`);
  if (!res.ok) throw new Error('Failed to load scheme categories');
  return res.json();
}

export async function fetchSchemes(params?: { 
  category_id?: number; 
  beneficiary_category?: string; 
  department?: string; 
  search?: string; 
  status_filter?: string 
}): Promise<Scheme[]> {
  const query = new URLSearchParams();
  if (params?.category_id) query.append('category_id', params.category_id.toString());
  if (params?.beneficiary_category) query.append('beneficiary_category', params.beneficiary_category);
  if (params?.department) query.append('department', params.department);
  if (params?.search) query.append('search', params.search);
  if (params?.status_filter) query.append('status_filter', params.status_filter);
  const res = await fetch(`${API_BASE}/api/swd/schemes?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to load schemes');
  return res.json();
}

export async function fetchBeneficiaryCategories(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/swd/schemes/beneficiaries`);
  if (!res.ok) throw new Error('Failed to fetch beneficiary categories');
  return res.json();
}

export async function fetchSchemeById(id: number): Promise<Scheme> {
  const res = await fetch(`${API_BASE}/api/swd/schemes/${id}`);
  if (!res.ok) throw new Error('Scheme not found');
  return res.json();
}

export async function checkEligibility(schemeId: number, attributes: Record<string, any>) {
  const res = await fetch(`${API_BASE}/api/swd/schemes/${schemeId}/eligibility-check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ citizen_attributes: attributes })
  });
  if (!res.ok) throw new Error('Eligibility assessment failed');
  return res.json();
}

export async function submitApplication(schemeId: number, data: any, token: string) {
  const res = await fetch(`${API_BASE}/api/swd/schemes/${schemeId}/applications`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Application submission failed');
  }
  return res.json();
}

export async function fetchCitizenApplications(citizenId: string, token: string): Promise<Application[]> {
  const res = await fetch(`${API_BASE}/api/swd/applications/${citizenId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch applications');
  return res.json();
}

export async function fetchApplicationDetails(appId: number, token: string): Promise<Application> {
  const res = await fetch(`${API_BASE}/api/swd/applications/${appId}/details`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch application details');
  return res.json();
}

export async function uploadDocument(appId: number, docCode: string, file: File, token: string) {
  const formData = new FormData();
  formData.append('document_code', docCode);
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/api/swd/applications/${appId}/documents`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  });
  if (!res.ok) throw new Error('Document upload failed');
  return res.json();
}

export async function fetchAdminDashboard(token: string) {
  const res = await fetch(`${API_BASE}/api/swd/admin/dashboard`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch admin stats');
  return res.json();
}

export async function fetchAdminApplications(
  token: string, 
  filters?: { statusFilter?: string; categoryId?: number; schemeId?: number; district?: string; search?: string }
): Promise<Application[]> {
  const query = new URLSearchParams();
  if (filters?.statusFilter) query.append("status_filter", filters.statusFilter);
  if (filters?.categoryId) query.append("category_id", filters.categoryId.toString());
  if (filters?.schemeId) query.append("scheme_id", filters.schemeId.toString());
  if (filters?.district) query.append("district", filters.district);
  if (filters?.search) query.append("search", filters.search);

  const url = `${API_BASE}/api/swd/admin/applications?${query.toString()}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch admin applications');
  return res.json();
}

export async function requestAdminInformation(appId: number, remarks: string, token: string) {
  const res = await fetch(`${API_BASE}/api/swd/admin/applications/${appId}/request-information`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ remarks })
  });
  if (!res.ok) throw new Error('Failed to request information');
  return res.json();
}

export async function recordAdminDecision(appId: number, decision: string, remarks: string, sanctionedAmount: number | undefined, token: string) {
  const res = await fetch(`${API_BASE}/api/swd/admin/applications/${appId}/decision`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ decision, remarks, sanctioned_amount: sanctionedAmount })
  });
  if (!res.ok) throw new Error('Failed to record decision');
  return res.json();
}

export async function fetchBeneficiaries(token: string): Promise<Beneficiary[]> {
  const res = await fetch(`${API_BASE}/api/swd/beneficiaries`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch beneficiaries');
  return res.json();
}

export async function fetchDbtDashboardStats(token: string) {
  const res = await fetch(`${API_BASE}/api/swd/dbt/dashboard-stats`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch DBT stats');
  return res.json();
}

export async function fetchDbtTransactions(token: string, params?: { status_filter?: string; scheme_id?: number }) {
  const query = new URLSearchParams();
  if (params?.status_filter) query.append('status_filter', params.status_filter);
  if (params?.scheme_id) query.append('scheme_id', params.scheme_id.toString());
  const res = await fetch(`${API_BASE}/api/swd/dbt/transactions?${query.toString()}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch DBT transactions');
  return res.json();
}

export async function processSingleDbt(beneficiaryId: number, token: string, simulateFailure = false) {
  const res = await fetch(`${API_BASE}/api/swd/dbt/process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      beneficiary_id: beneficiaryId,
      remarks: simulateFailure ? "Simulated Bank CBS timeout" : "Simulated Individual DBT Disbursement",
      simulate_failure: simulateFailure
    })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Simulated payment processing failed');
  }
  return res.json();
}

export async function processBatchDbt(beneficiaryIds: number[], token: string, failIds: number[] = []) {
  const res = await fetch(`${API_BASE}/api/swd/dbt/batch-process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      beneficiary_ids: beneficiaryIds,
      remarks: "Simulated DBT Batch Disbursement",
      fail_beneficiary_ids: failIds
    })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Batch DBT processing failed');
  }
  return res.json();
}

export function getBatchDbtReportUrl(batchReference?: string): string {
  return batchReference 
    ? `${API_BASE}/api/swd/dbt/batch-report?batch_reference=${batchReference}`
    : `${API_BASE}/api/swd/dbt/batch-report`;
}

export async function devLogin(email: string, password: string) {
  const res = await fetch(`${API_BASE}/api/swd/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  return res.json();
}

export interface UserProfileData {
  id?: number;
  citizen_id?: string;
  email?: string;
  full_name?: string;
  role?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  address?: string;
  district?: string;
  taluk?: string;
  pin_code?: string;
  state?: string;
  annual_income?: number;
  caste_category?: string;
  disability_percentage?: number;
  bank_account_number?: string;
  bank_ifsc?: string;
  is_active?: boolean;
}

export interface CitizenRegisterData {
  full_name: string;
  email: string;
  phone: string;
  password: string;
  confirm_password?: string;
  date_of_birth?: string;
  gender?: string;
  address?: string;
  district?: string;
  taluk?: string;
  pin_code?: string;
  caste_category?: string;
  annual_income?: number;
}

export async function registerCitizen(data: CitizenRegisterData): Promise<UserProfileData> {
  const res = await fetch(`${API_BASE}/api/swd/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    if (err.detail && Array.isArray(err.detail)) {
      throw new Error(err.detail.map((d: any) => d.msg || d.message).join(', '));
    }
    throw new Error(err.detail || 'Citizen registration failed. Please verify the input values.');
  }
  return res.json();
}

export async function fetchUserProfile(token: string): Promise<UserProfileData> {
  const res = await fetch(`${API_BASE}/api/swd/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch user profile');
  return res.json();
}

export async function updateUserProfile(data: Partial<UserProfileData>, token: string): Promise<UserProfileData> {
  const res = await fetch(`${API_BASE}/api/swd/auth/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to update profile');
  }
  return res.json();
}


// ----------------- Smart Scheme Finder Types & API -----------------
export interface SmartFinderQuestionnaire {
  age?: number;
  district?: string;
  taluk?: string;
  gender?: string;
  caste_category?: string;
  annual_income?: number;
  occupation?: string;
  education_level?: string;
  is_farmer?: boolean;
  is_student?: boolean;
  is_woman?: boolean;
  disability_status?: string;
  disability_percentage?: number;
  marital_status?: string;
}

export interface SmartFinderMatchItem {
  scheme_id: number;
  scheme_code: string;
  scheme_name: string;
  category_id: number;
  category_name: string;
  description: string;
  benefit_summary: string;
  benefit_amount?: number;
  eligibility_summary: string;
  documents_required: string[];
  status: string;
  verification_status: string;
  match_status: 'Potential Match' | 'Check Requirements' | 'Not Matched';
  match_score: number;
  why_matched: string[];
  missing_requirements: string[];
  has_application_form: boolean;
  official_url?: string;
  disclaimer: string;
}

export interface SmartFinderResponse {
  total_matches: number;
  potential_match_count: number;
  check_requirements_count: number;
  results: SmartFinderMatchItem[];
  disclaimer: string;
}

export interface SmartFinderOptions {
  districts: string[];
  social_categories: string[];
  occupations: string[];
  education_levels: string[];
}

export async function fetchFinderOptions(): Promise<SmartFinderOptions> {
  const res = await fetch(`${API_BASE}/api/swd/finder/options`);
  if (!res.ok) throw new Error('Failed to load questionnaire options');
  return res.json();
}

export async function matchSmartSchemes(questionnaire: SmartFinderQuestionnaire): Promise<SmartFinderResponse> {
  const res = await fetch(`${API_BASE}/api/swd/finder/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(questionnaire)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to match schemes with questionnaire');
  }
  return res.json();
}


// ----------------- Offices API -----------------
export interface Office {
  id: number;
  name: string;
  office_type: string;
  district: string;
  taluk: string;
  address: string;
  contact_number: string;
  email: string;
  working_hours: string;
  services_offered: string;
  latitude: number;
  longitude: number;
  map_link: string;
  is_active: boolean;
  verification_status: string;
  distance_km?: number;
  created_at: string;
  updated_at: string;
}

export async function fetchOffices(params?: { district?: string; taluk?: string; search?: string }): Promise<Office[]> {
  const query = new URLSearchParams();
  if (params?.district) query.append("district", params.district);
  if (params?.taluk) query.append("taluk", params.taluk);
  if (params?.search) query.append("search", params.search);
  const res = await fetch(`${API_BASE}/api/swd/offices?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to load welfare offices");
  return res.json();
}

export async function fetchNearbyOffices(latitude: number, longitude: number, radiusKm: number = 25.0): Promise<Office[]> {
  const res = await fetch(`${API_BASE}/api/swd/offices/nearby?latitude=${latitude}&longitude=${longitude}&radius_km=${radiusKm}`);
  if (!res.ok) throw new Error("Failed to load nearby welfare offices");
  return res.json();
}

// ----------------- Grievances API -----------------
export interface Grievance {
  id: number;
  grievance_number: string;
  citizen_id: string;
  citizen_name: string;
  category: string;
  subject: string;
  description: string;
  status: string;
  officer_response?: string;
  resolved_by?: string;
  resolved_at?: string;
  created_at: string;
  updated_at: string;
}

export async function fetchGrievances(params?: { citizen_id?: string; status_filter?: string }, authToken?: string): Promise<Grievance[]> {
  const query = new URLSearchParams();
  if (params?.citizen_id) query.append("citizen_id", params.citizen_id);
  if (params?.status_filter) query.append("status_filter", params.status_filter);
  const token = authToken || (typeof window !== 'undefined' ? localStorage.getItem('ns_swd_token') : '');
  const headers: Record<string, string> = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}/api/swd/grievances?${query.toString()}`, { headers });
  if (!res.ok) throw new Error("Failed to fetch grievances");
  return res.json();
}

export async function submitGrievance(data: { citizen_id: string; citizen_name: string; category: string; subject: string; description: string }, authToken?: string): Promise<Grievance> {
  const token = authToken || (typeof window !== 'undefined' ? localStorage.getItem('ns_swd_token') : '');
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}/api/swd/grievances`, {
    method: "POST",
    headers,
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to submit grievance");
  }
  return res.json();
}

export async function resolveGrievance(grievanceId: number, data: { status: string; officer_response: string }, authToken?: string): Promise<Grievance> {
  const token = authToken || (typeof window !== 'undefined' ? localStorage.getItem('ns_swd_token') : '');
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}/api/swd/grievances/${grievanceId}/resolve`, {
    method: "PUT",
    headers,
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to update grievance");
  }
  return res.json();
}

// ----------------- Notifications API -----------------
export interface NotificationItem {
  id: number;
  user_id: string;
  title: string;
  message: string;
  is_read: boolean;
  notification_type: string;
  created_at: string;
}

export async function fetchNotifications(userId: string, token?: string): Promise<NotificationItem[]> {
  const tok = token || localStorage.getItem('ns_swd_token');
  const headers: Record<string, string> = {};
  if (tok) headers['Authorization'] = `Bearer ${tok}`;
  const res = await fetch(`${API_BASE}/api/swd/notifications/${userId}`, { headers });
  if (!res.ok) return [];
  return res.json();
}

export async function markNotificationRead(id: number, token?: string): Promise<void> {
  const tok = token || localStorage.getItem('ns_swd_token');
  const headers: Record<string, string> = {};
  if (tok) headers['Authorization'] = `Bearer ${tok}`;
  await fetch(`${API_BASE}/api/swd/notifications/${id}/read`, { method: "PATCH", headers });
}

// ----------------- Dynamic Forms & Three Portals API -----------------
export interface DynamicFormField {
  id: number;
  form_id: number;
  field_name: string;
  field_label: string;
  field_type: string;
  placeholder?: string;
  help_text?: string;
  is_required: boolean;
  display_order: number;
  options_json?: string[] | any;
  validation_rules_json?: any;
  conditional_visibility_json?: any;
}

export interface DynamicFormDefinition {
  id: number;
  scheme_id: number;
  version: number;
  title: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  fields: DynamicFormField[];
}

export async function fetchSchemeDynamicForm(schemeId: number): Promise<DynamicFormDefinition | null> {
  const res = await fetch(`${API_BASE}/api/swd/schemes/${schemeId}/form`);
  if (!res.ok) return null;
  return res.json();
}

export async function saveSchemeDynamicForm(
  schemeId: number,
  formData: {
    title: string;
    description?: string;
    fields: Array<{
      field_name: string;
      field_label: string;
      field_type: string;
      placeholder?: string;
      help_text?: string;
      is_required: boolean;
      display_order?: number;
      options_json?: any;
      validation_rules_json?: any;
      conditional_visibility_json?: any;
    }>;
  },
  token: string
): Promise<DynamicFormDefinition> {
  const res = await fetch(`${API_BASE}/api/swd/schemes/${schemeId}/form`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(formData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to save scheme application form configuration');
  }
  return res.json();
}

export interface SchemeBreakdown {
  scheme_id: number;
  scheme_code: string;
  scheme_name: string;
  application_mode: string;
  total_applications: number;
  submitted: number;
  under_review: number;
  documents_required: number;
  approved: number;
  rejected: number;
}

export interface CategoryStats {
  category_id: number;
  category_code: string;
  category_name: string;
  description: string;
  icon: string;
  total_applications: number;
  new_applications: number;
  under_review: number;
  documents_required: number;
  approved: number;
  rejected: number;
  schemes: SchemeBreakdown[];
}

export async function fetchCategoryApplicationStats(token?: string): Promise<CategoryStats[]> {
  const headers: HeadersInit = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}/api/swd/admin/categories/stats`, { headers });
  if (!res.ok) throw new Error("Failed to load category application stats");
  return res.json();
}

export interface PlatformUser {
  id: number;
  citizen_id: string;
  email: string;
  full_name: string;
  role: string;
  phone?: string;
  district?: string;
  taluk?: string;
  is_active: boolean;
  created_at: string;
}

export async function fetchPlatformUsers(token: string, roleFilter?: string, search?: string): Promise<PlatformUser[]> {
  const query = new URLSearchParams();
  if (roleFilter) query.append("role_filter", roleFilter);
  if (search) query.append("search", search);
  const res = await fetch(`${API_BASE}/api/swd/admin/users?${query.toString()}`, {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) throw new Error("Failed to load platform users");
  return res.json();
}

export async function updateUserRole(token: string, userId: number, role: string): Promise<any> {
  const res = await fetch(`${API_BASE}/api/swd/admin/users/${userId}/role?role=${role}`, {
    method: "PUT",
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) throw new Error("Failed to update user role");
  return res.json();
}

export async function toggleUserStatus(token: string, userId: number, isActive: boolean): Promise<any> {
  const res = await fetch(`${API_BASE}/api/swd/admin/users/${userId}/status?is_active=${isActive}`, {
    method: "PUT",
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) throw new Error("Failed to update user status");
  return res.json();
}

export async function fetchAuditLogs(token: string, limit: number = 50): Promise<any[]> {
  const res = await fetch(`${API_BASE}/api/swd/admin/audit-logs?limit=${limit}`, {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) return [];
  return res.json();
}


export async function markAllNotificationsRead(userId: string, token?: string): Promise<void> {
  const tok = token || localStorage.getItem('ns_swd_token');
  const headers: Record<string, string> = {};
  if (tok) headers['Authorization'] = `Bearer ${tok}`;
  await fetch(`${API_BASE}/api/swd/notifications/${userId}/mark-all-read`, { method: "POST", headers });
}

// ----------------- PDF Receipt Download -----------------
export function getReceiptDownloadUrl(applicationId: number): string {
  return `${API_BASE}/api/swd/applications/${applicationId}/receipt`;
}

export async function downloadApplicationReceipt(applicationId: number, token?: string): Promise<{ success: boolean; filename?: string; error?: string }> {
  const tok = token || (typeof window !== 'undefined' ? localStorage.getItem('ns_swd_token') : null);
  if (!tok) {
    return { success: false, error: 'Authentication token is required to download receipt. Please log in.' };
  }

  const url = `${API_BASE}/api/swd/applications/${applicationId}/receipt`;
  try {
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${tok}`
      }
    });

    if (!res.ok) {
      let errorDetail = `Failed to download receipt (HTTP ${res.status})`;
      try {
        const errorJson = await res.json();
        if (errorJson && errorJson.detail) {
          errorDetail = errorJson.detail;
        }
      } catch {
        // Response was not JSON
      }
      return { success: false, error: errorDetail };
    }

    // Extract filename from Content-Disposition header if available
    let filename = `Receipt_Application_${applicationId}.pdf`;
    const disposition = res.headers.get('Content-Disposition');
    if (disposition && disposition.includes('filename=')) {
      const match = disposition.match(/filename=["']?([^"';]+)["']?/);
      if (match && match[1]) {
        filename = match[1].trim();
      }
    }

    const blob = await res.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);

    return { success: true, filename };
  } catch (err: any) {
    return { success: false, error: err.message || 'Network error while downloading receipt' };
  }
}


export async function logoutUser(token: string): Promise<any> {
  const res = await fetch(`${API_BASE}/api/v1/swd/auth/logout`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return res.json().catch(() => ({}));
}

export async function publishAnnouncement(data: { title: string; message: string; announcement_type?: string; target_role?: string }, token: string) {
  const res = await fetch(`${API_BASE}/api/swd/admin/announcements`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to publish announcement');
  }
  return res.json();
}
