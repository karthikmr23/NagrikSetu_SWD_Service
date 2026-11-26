const fs = require("fs");
const path = require("path");

const filePath = path.join(__dirname, "frontend", "src", "App.tsx");
let content = fs.readFileSync(filePath, "utf8");

// 1. Update lucide-react imports if needed: ensure Bell, Building, Building2, MapPin, Download, MessageSquare, etc.
if (!content.includes("Bell,") && !content.includes(", Bell")) {
  content = content.replace("import { \n  HeartHandshake,", "import { \n  HeartHandshake, Bell, Building, Building2, Download, MessageSquare, ExternalLink,");
}

// 2. Add activeTab types: 'sign-in-select' | 'grievance' | 'office-locator'
content = content.replace(
  "'admin-reports' | 'smart-finder'",
  "'admin-reports' | 'smart-finder' | 'sign-in-select' | 'grievance' | 'office-locator'"
);

// 3. Add state variables for notifications, offices, grievances, and admin search/filter
const stateInsertAnchor = "  // Data State";
const newStates = `  // Notifications State
  const [notifications, setNotifications] = useState<api.NotificationItem[]>([]);
  const [showNotificationsDropdown, setShowNotificationsDropdown] = useState<boolean>(false);

  // Offices State
  const [offices, setOffices] = useState<api.Office[]>([]);
  const [officeDistrictFilter, setOfficeDistrictFilter] = useState<string>('');
  const [officeTalukFilter, setOfficeTalukFilter] = useState<string>('');
  const [officeSearchQuery, setOfficeSearchQuery] = useState<string>('');
  const [officeLoading, setOfficeLoading] = useState<boolean>(false);

  // Grievance State
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);
  const [grievanceCategory, setGrievanceCategory] = useState<string>('DELAY_IN_SANCTION');
  const [grievanceSubject, setGrievanceSubject] = useState<string>('');
  const [grievanceDesc, setGrievanceDesc] = useState<string>('');
  const [grievanceLoading, setGrievanceLoading] = useState<boolean>(false);
  const [grievanceSuccessMsg, setGrievanceSuccessMsg] = useState<string>('');
  const [grievanceErrorMsg, setGrievanceErrorMsg] = useState<string>('');

  // Admin Application Review Enhanced Filter
  const [adminDistrictFilter, setAdminDistrictFilter] = useState<string>('');
  const [adminSearchQuery, setAdminSearchQuery] = useState<string>('');
  const [adminSchemeFilter, setAdminSchemeFilter] = useState<number | undefined>(undefined);
  const [reviewDecisionMode, setReviewDecisionMode] = useState<string>('APPROVED');
`;

content = content.replace(stateInsertAnchor, newStates + "\n" + stateInsertAnchor);

// 4. Add helper functions for notifications, offices, grievances, PDF download
const helperInsertAnchor = "  async function loadAdminData(authToken?: string) {";
const newHelpers = `  async function loadNotifications(citId?: string) {
    const cid = citId || citizenId;
    if (!cid) return;
    try {
      const data = await api.fetchNotifications(cid);
      setNotifications(data);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleMarkAllRead() {
    if (!citizenId) return;
    try {
      await api.markAllNotificationsRead(citizenId);
      await loadNotifications(citizenId);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleMarkOneRead(id: number) {
    try {
      await api.markNotificationRead(id);
      await loadNotifications(citizenId);
    } catch (e) {
      console.error(e);
    }
  }

  async function loadOffices(district?: string, taluk?: string, search?: string) {
    try {
      setOfficeLoading(true);
      const data = await api.fetchOffices({ district, taluk, search });
      setOffices(data);
    } catch (e) {
      console.error(e);
    } finally {
      setOfficeLoading(false);
    }
  }

  async function loadGrievances(citId?: string) {
    const cid = citId || citizenId;
    if (!cid) return;
    try {
      setGrievanceLoading(true);
      const data = await api.fetchGrievances({ citizen_id: cid });
      setGrievances(data);
    } catch (e) {
      console.error(e);
    } finally {
      setGrievanceLoading(false);
    }
  }

  async function handleGrievanceSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!grievanceSubject.trim() || !grievanceDesc.trim()) {
      setGrievanceErrorMsg('Subject and description are required.');
      return;
    }
    try {
      setGrievanceLoading(true);
      setGrievanceErrorMsg('');
      const newGrv = await api.submitGrievance({
        citizen_id: citizenId,
        citizen_name: userName,
        category: grievanceCategory,
        subject: grievanceSubject.trim(),
        description: grievanceDesc.trim()
      });
      setGrievanceSuccessMsg(\`Grievance registered successfully: \${newGrv.grievance_number}\`);
      setGrievanceSubject('');
      setGrievanceDesc('');
      await loadGrievances(citizenId);
      await loadNotifications(citizenId);
    } catch (err: any) {
      setGrievanceErrorMsg(err.message || 'Failed to submit grievance');
    } finally {
      setGrievanceLoading(false);
    }
  }

  function downloadReceiptPdf(appId: number) {
    const url = api.getReceiptDownloadUrl(appId);
    window.open(url, '_blank');
  }
`;

content = content.replace(helperInsertAnchor, newHelpers + "\n" + helperInsertAnchor);

fs.writeFileSync(filePath, content, "utf8");
console.log("Stage 1 updates applied successfully");
