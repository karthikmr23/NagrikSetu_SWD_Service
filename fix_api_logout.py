with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\services\api.ts", "r", encoding="utf-8") as f:
    text = f.read()

bad_func = '''export async function logoutUser(token: string): Promise<any> {
  const res = await fetch(${API_BASE_URL}/auth/logout, {
    method: 'POST',
    headers: {
      Authorization: Bearer 
    }
  });
  return res.json().catch(() => ({}));
}'''

good_func = '''export async function logoutUser(token: string): Promise<any> {
  const res = await fetch(`${API_BASE}/api/v1/swd/auth/logout`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return res.json().catch(() => ({}));
}'''

if bad_func in text:
    text = text.replace(bad_func, good_func)
    with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\services\api.ts", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed logoutUser in api.ts")
else:
    print("bad_func not found")
