import re

app_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add grievanceActiveSubTab state if not present
if "grievanceActiveSubTab" not in content:
    subtab_state = """  // Grievance State
  const [grievanceActiveSubTab, setGrievanceActiveSubTab] = useState<'track' | 'submit'>('track');
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);"""
    content = content.replace("""  // Grievance State
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);""", subtab_state, 1)

# 2. Update post-login redirection in handlePortalLogin
old_portal_cit_redir = """      } else {
        setActiveTab('citizen-dashboard');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadGrievances(res.citizen_id);
      }"""

new_portal_cit_redir = """      } else {
        setActiveTab('swd-home');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);
      }"""

if old_portal_cit_redir in content:
    content = content.replace(old_portal_cit_redir, new_portal_cit_redir, 1)
    print("Updated handlePortalLogin redirection to swd-home")
else:
    print("Warning: old_portal_cit_redir not found in content!")

# 3. Update post-login redirection in handleDedicatedLogin
old_ded_cit_redir = """      } else {
        setActiveTab('citizen-dashboard');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadGrievances(res.citizen_id);
      }"""

# Since handleDedicatedLogin and handleLogin have the same block, let's replace all occurrences:
content = content.replace(old_portal_cit_redir, new_portal_cit_redir)

# Also check handleLogin (modal login)
old_handle_login_redir = """      } else {
        setActiveTab('citizen-dashboard');
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadGrievances(res.citizen_id);
      }"""
content = content.replace(old_handle_login_redir, new_portal_cit_redir)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved login redirection changes.")
