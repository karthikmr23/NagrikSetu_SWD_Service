import sys

filepath = r'C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\App.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace openSchemeApplication definition
old_open_app = """  async function openSchemeApplication(scheme: api.Scheme) {
    // 1. Unauthenticated Visitor Flow: Preserve pending scheme and redirect to Citizen Sign In with clear notice
    if (!token) {
      setSelectedScheme(scheme);
      setPendingSchemeForApply(scheme);
      try {
        sessionStorage.setItem('swd_pending_scheme_apply', JSON.stringify(scheme));
      } catch (e) {
        console.error('Failed to save pending scheme to sessionStorage:', e);
      }
      setCitizenLoginNotice('Please sign in with your Citizen account to apply for this scheme.');
      setActiveTab('sign-in-select');
      return;
    }

    // 2. Administrative Users Restriction: Keep logged in, do not redirect or switch roles, show friendly explanation
    if (userRole !== 'CITIZEN') {
      const roleTitle = (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN')
        ? 'Platform Administrator'
        : 'Government Welfare Officer';
      setAdminApplyNoticeModal(
        `Notice: Scheme applications can only be submitted through a Citizen account. As an authenticated ${roleTitle}, you have administrative and scrutiny permissions only. To submit a welfare scheme application as a beneficiary, please sign in with a registered Citizen account.`
      );
      return;
    }

    // 3. Authenticated Citizen: Directly proceed to Scheme Application Form
    setSelectedScheme(scheme);
    setDynamicFormData({});
    setLoadingSchemeForm(true);
    setActiveTab('apply');
    try {
      const formDef = await api.fetchSchemeDynamicForm(scheme.id);
      setSchemeDynamicForm(formDef);
    } catch (err) {
      console.error('Failed to load scheme dynamic form', err);
      setSchemeDynamicForm(null);
    } finally {
      setLoadingSchemeForm(false);
    }
  }"""

new_open_app = """  async function navigateToSchemeApplication(scheme: api.Scheme) {
    setSelectedScheme(scheme);
    setDynamicFormData({});
    setLoadingSchemeForm(true);
    setActiveTab('apply');
    try {
      const formDef = await api.fetchSchemeDynamicForm(scheme.id);
      setSchemeDynamicForm(formDef);
    } catch (err) {
      console.error('Failed to load scheme dynamic form', err);
      setSchemeDynamicForm(null);
    } finally {
      setLoadingSchemeForm(false);
    }
  }

  async function openSchemeApplication(scheme: api.Scheme) {
    // 1. Unauthenticated Visitor Flow: Preserve pending scheme and redirect to Citizen Sign In with clear notice
    if (!token) {
      setSelectedScheme(scheme);
      setPendingSchemeForApply(scheme);
      try {
        sessionStorage.setItem('swd_pending_scheme_apply', JSON.stringify(scheme));
      } catch (e) {
        console.error('Failed to save pending scheme to sessionStorage:', e);
      }
      setCitizenLoginNotice('Please sign in with your Citizen account to apply for this scheme.');
      setActiveTab('sign-in-select');
      return;
    }

    // 2. Administrative Users Restriction: Keep logged in, do not redirect or switch roles, show friendly explanation
    if (userRole !== 'CITIZEN') {
      const roleTitle = (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN')
        ? 'Platform Administrator'
        : 'Government Welfare Officer';
      setAdminApplyNoticeModal(
        `Notice: Scheme applications can only be submitted through a Citizen account. As an authenticated ${roleTitle}, you have administrative and scrutiny permissions only. To submit a welfare scheme application as a beneficiary, please sign in with a registered Citizen account.`
      );
      return;
    }

    // 3. Authenticated Citizen: Directly proceed to Scheme Application Form
    await navigateToSchemeApplication(scheme);
  }"""

if old_open_app not in text:
    print('ERROR: old_open_app not found')
    sys.exit(1)
text = text.replace(old_open_app, new_open_app, 1)

# Now in useEffect, handlePortalLogin, handleDedicatedLogin, and handleLogin:
# Replace openSchemeApplication(parsedScheme) / openSchemeApplication(restoredScheme) with navigateToSchemeApplication(...)

# 1. In useEffect:
old_eff = """            openSchemeApplication(parsedScheme);"""
new_eff = """            navigateToSchemeApplication(parsedScheme);"""
if old_eff not in text:
    print('ERROR: old_eff not found')
    sys.exit(1)
text = text.replace(old_eff, new_eff, 1)

# 2. In handlePortalLogin:
old_portal = """        if (restoredScheme) {
          openSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }"""
new_portal = """        if (restoredScheme) {
          navigateToSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }"""
if old_portal not in text:
    print('ERROR: old_portal not found')
    sys.exit(1)
text = text.replace(old_portal, new_portal, 1)

# 3. In handleDedicatedLogin:
if old_portal not in text:
    print('ERROR: second old_portal not found')
    sys.exit(1)
text = text.replace(old_portal, new_portal, 1)

# 4. In handleLogin:
if old_portal not in text:
    print('ERROR: third old_portal not found')
    sys.exit(1)
text = text.replace(old_portal, new_portal, 1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: navigateToSchemeApplication implemented and wired to all login handlers!')
