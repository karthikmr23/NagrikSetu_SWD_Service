portal_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\GovernmentWelfareAdminPortal.tsx"

with open(portal_path, "r", encoding="utf-8") as f:
    content = f.read()

old_import = """import { 
  Building2, Users, FileText, CheckCircle2, Clock, 
  AlertCircle, ChevronRight, Search, Filter, Eye, RefreshCw, 
  Check, X, AlertTriangle, ArrowLeft, Download, Shield
} from 'lucide-react';"""

new_import = """import { 
  Building2, Users, FileText, CheckCircle2, Clock, 
  AlertCircle, ChevronRight, Search, Filter, Eye, RefreshCw, 
  Check, X, AlertTriangle, ArrowLeft, Download, Shield, Bell, Send
} from 'lucide-react';"""

content = content.replace(old_import, new_import, 1)

with open(portal_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated lucide-react imports in GovernmentWelfareAdminPortal.tsx")
