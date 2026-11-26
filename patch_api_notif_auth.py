api_ts_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\services\api.ts"

with open(api_ts_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update fetchNotifications to accept optional token or pull from localStorage
old_fetch_notifs = """export async function fetchNotifications(userId: string): Promise<NotificationItem[]> {
  const res = await fetch(`${API_BASE}/api/swd/notifications/${userId}`);
  if (!res.ok) return [];
  return res.json();
}

export async function markNotificationRead(id: number): Promise<void> {
  await fetch(`${API_BASE}/api/swd/notifications/${id}/read`, { method: "PATCH" });
}"""

new_fetch_notifs = """export async function fetchNotifications(userId: string, token?: string): Promise<NotificationItem[]> {
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
}"""

old_mark_all = """export async function markAllNotificationsRead(userId: string): Promise<void> {
  await fetch(`${API_BASE}/api/swd/notifications/${userId}/mark-all-read`, { method: "POST" });
}"""

new_mark_all = """export async function markAllNotificationsRead(userId: string, token?: string): Promise<void> {
  const tok = token || localStorage.getItem('ns_swd_token');
  const headers: Record<string, string> = {};
  if (tok) headers['Authorization'] = `Bearer ${tok}`;
  await fetch(`${API_BASE}/api/swd/notifications/${userId}/mark-all-read`, { method: "POST", headers });
}"""

content = content.replace(old_fetch_notifs, new_fetch_notifs)
content = content.replace(old_mark_all, new_mark_all)

with open(api_ts_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated api.ts with Authorization headers for notifications.")
