const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "services", "api.ts");
let content = fs.readFileSync(filePath, "utf8");

const extraApi = `
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
  created_at: string;
  updated_at: string;
}

export async function fetchOffices(params?: { district?: string; taluk?: string; search?: string }): Promise<Office[]> {
  const query = new URLSearchParams();
  if (params?.district) query.append("district", params.district);
  if (params?.taluk) query.append("taluk", params.taluk);
  if (params?.search) query.append("search", params.search);
  const res = await fetch(\`\${API_BASE}/api/swd/offices?\${query.toString()}\`);
  if (!res.ok) throw new Error("Failed to load welfare offices");
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

export async function fetchGrievances(params?: { citizen_id?: string; status_filter?: string }): Promise<Grievance[]> {
  const query = new URLSearchParams();
  if (params?.citizen_id) query.append("citizen_id", params.citizen_id);
  if (params?.status_filter) query.append("status_filter", params.status_filter);
  const res = await fetch(\`\${API_BASE}/api/swd/grievances?\${query.toString()}\`);
  if (!res.ok) throw new Error("Failed to fetch grievances");
  return res.json();
}

export async function submitGrievance(data: { citizen_id: string; citizen_name: string; category: string; subject: string; description: string }): Promise<Grievance> {
  const res = await fetch(\`\${API_BASE}/api/swd/grievances\`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to submit grievance");
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

export async function fetchNotifications(userId: string): Promise<NotificationItem[]> {
  const res = await fetch(\`\${API_BASE}/api/swd/notifications/\${userId}\`);
  if (!res.ok) return [];
  return res.json();
}

export async function markNotificationRead(id: number): Promise<void> {
  await fetch(\`\${API_BASE}/api/swd/notifications/\${id}/read\`, { method: "PATCH" });
}

export async function markAllNotificationsRead(userId: string): Promise<void> {
  await fetch(\`\${API_BASE}/api/swd/notifications/\${userId}/mark-all-read\`, { method: "POST" });
}

// ----------------- PDF Receipt Download -----------------
export function getReceiptDownloadUrl(applicationId: number): string {
  return \`\${API_BASE}/api/swd/applications/\${applicationId}/receipt\`;
}
`;

fs.writeFileSync(filePath, content + "\n" + extraApi, "utf8");
console.log("Successfully appended new API methods to api.ts");
