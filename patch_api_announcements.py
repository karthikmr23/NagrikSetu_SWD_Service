import os

path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\services\api.ts"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

target = """export async function logoutUser(token: string): Promise<any> {
  const res = await fetch(`${API_BASE}/api/v1/swd/auth/logout`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return res.json().catch(() => ({}));
}"""

replacement = """export async function logoutUser(token: string): Promise<any> {
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
}"""

assert target in code, "Target not found in api.ts"
code = code.replace(target, replacement)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("api.ts updated with publishAnnouncement!")
