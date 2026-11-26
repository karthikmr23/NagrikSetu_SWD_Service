import React, { useState, useEffect } from 'react';
import { 
  HeartHandshake, ExternalLink, Bell, Building, Building2, Download, MessageSquare, Sparkles, Landmark, Search, Shield, Filter, CheckCircle2, 
  AlertCircle, FileText, Check, X, ChevronRight, Calendar, User, 
  MapPin, RefreshCw, Send, LogOut, LogIn, UserPlus, Phone, Award,
  HelpCircle, Eye, EyeOff, ArrowLeft, Upload, FileCheck, Users, DollarSign,
  Layers, Clock, AlertTriangle, ArrowRight, BookOpen, CheckCircle
} from 'lucide-react';
import './style.css';
import * as api from './services/api';
import { SmartSchemeFinderView } from './components/SmartSchemeFinderView';
import { WelfareMap } from './components/WelfareMap';
import { GovernmentWelfareAdminPortal } from './components/GovernmentWelfareAdminPortal';
import { PlatformAdminPortal } from './components/PlatformAdminPortal';
import { DynamicFormRenderer } from './components/DynamicFormRenderer';

export default function App() {
  // Navigation State
  const [activeTab, setActiveTab] = useState<
    'swd-home' | 'schemes' | 'scheme-detail' | 'eligibility' | 'apply' | 
    'citizen-dashboard' | 'my-applications' | 'tracking' | 'citizen-profile' |
    'citizen-register' |
    'admin-dashboard' | 'admin-schemes' | 'admin-applications' | 
    'admin-beneficiaries' | 'admin-dbt' | 'admin-reports' | 'smart-finder' | 'sign-in-select' | 
    'grievance' | 'my-grievances' | 'notifications-view' | 'office-locator' |
    'gov-welfare-admin' | 'platform-admin'
  >(() => {
    try {
      const hasPending = sessionStorage.getItem('swd_pending_scheme_apply');
      const hasToken = localStorage.getItem('ns_swd_token');
      if (hasPending && !hasToken) {
        return 'sign-in-select';
      }
    } catch {}
    return 'swd-home';
  });

  // Auth State
  const [token, setToken] = useState<string>(localStorage.getItem('ns_swd_token') || '');
  const [userRole, setUserRole] = useState<string>(localStorage.getItem('ns_swd_role') || '');
  const [citizenId, setCitizenId] = useState<string>(localStorage.getItem('ns_swd_citizen_id') || '');
  const [userName, setUserName] = useState<string>(localStorage.getItem('ns_swd_name') || '');
  const [showLoginModal, setShowLoginModal] = useState<boolean>(false);
  const [loginRoleMode, setLoginRoleMode] = useState<'CITIZEN' | 'ADMIN'>('CITIZEN');
  const [loginEmail, setLoginEmail] = useState<string>('citizen@example.com');
  const [loginPassword, setLoginPassword] = useState<string>('CitizenPass@2026');
  const [authError, setAuthError] = useState<string>('');

  // Password visibility & form toggle state
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState<boolean>(false);
  const [loginLoading, setLoginLoading] = useState<boolean>(false);

  // Dedicated Three-Portal Gateway Login States
  const [activeGatewayCard, setActiveGatewayCard] = useState<'NONE' | 'CITIZEN' | 'WELFARE' | 'PLATFORM'>('NONE');
  const [citizenLoginEmail, setCitizenLoginEmail] = useState<string>('');
  const [citizenLoginPassword, setCitizenLoginPassword] = useState<string>('');
  const [welfareLoginUser, setWelfareLoginUser] = useState<string>('');
  const [welfareLoginPassword, setWelfareLoginPassword] = useState<string>('');
  const [platformLoginUser, setPlatformLoginUser] = useState<string>('');
  const [platformLoginPassword, setPlatformLoginPassword] = useState<string>('');
  const [citizenAuthError, setCitizenAuthError] = useState<string>('');
  const [welfareAuthError, setWelfareAuthError] = useState<string>('');
  const [platformAuthError, setPlatformAuthError] = useState<string>('');
  const [pendingSchemeForApply, setPendingSchemeForApply] = useState<api.Scheme | null>(() => {
    try {
      const saved = sessionStorage.getItem('swd_pending_scheme_apply');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [citizenLoginNotice, setCitizenLoginNotice] = useState<string>(() => {
    return sessionStorage.getItem('swd_pending_scheme_apply')
      ? 'Please sign in with your Citizen account to apply for this scheme.'
      : '';
  });
  const [adminApplyNoticeModal, setAdminApplyNoticeModal] = useState<string | null>(null);

  // Dedicated Citizen Registration Form State
  const [regFullName, setRegFullName] = useState<string>('');
  const [regEmail, setRegEmail] = useState<string>('');
  const [regPhone, setRegPhone] = useState<string>('');
  const [regPassword, setRegPassword] = useState<string>('');
  const [regConfirmPassword, setRegConfirmPassword] = useState<string>('');
  const [regDob, setRegDob] = useState<string>('');
  const [regGender, setRegGender] = useState<string>('Male');
  const [regAddress, setRegAddress] = useState<string>('');
  const [regDistrict, setRegDistrict] = useState<string>('Bengaluru Urban');
  const [regTaluk, setRegTaluk] = useState<string>('Bengaluru North');
  const [regPinCode, setRegPinCode] = useState<string>('560001');
  const [regCategory, setRegCategory] = useState<string>('SC');
  const [regIncome, setRegIncome] = useState<number>(180000);
  const [regLoading, setRegLoading] = useState<boolean>(false);
  const [regError, setRegError] = useState<string>('');
  const [regSuccessMsg, setRegSuccessMsg] = useState<string>('');

  // Notifications State
  const [notifications, setNotifications] = useState<api.NotificationItem[]>([]);
  const [showNotificationsDropdown, setShowNotificationsDropdown] = useState<boolean>(false);

  // Offices State
  const [offices, setOffices] = useState<api.Office[]>([]);
  const [officeDistrictFilter, setOfficeDistrictFilter] = useState<string>('');
  const [officeTalukFilter, setOfficeTalukFilter] = useState<string>('');
  const [officeSearchQuery, setOfficeSearchQuery] = useState<string>('');
  const [officeLoading, setOfficeLoading] = useState<boolean>(false);
  const [userGpsLocation, setUserGpsLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [gpsStatus, setGpsStatus] = useState<'idle' | 'locating' | 'success' | 'denied' | 'error'>('idle');
  const [gpsStatusMsg, setGpsStatusMsg] = useState<string>('');
  const [isGpsActive, setIsGpsActive] = useState<boolean>(false);
  const [selectedOfficeId, setSelectedOfficeId] = useState<number | null>(null);

  // Grievance State
  const [grievanceActiveSubTab, setGrievanceActiveSubTab] = useState<'track' | 'submit'>('track');
  const [grievances, setGrievances] = useState<api.Grievance[]>([]);
  const [grievanceCategory, setGrievanceCategory] = useState<string>('APPLICATION_DELAY');
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

  // Data State
  const [categories, setCategories] = useState<api.SchemeCategory[]>([]);
  const [schemes, setSchemes] = useState<api.Scheme[]>([]);
  const [selectedScheme, setSelectedScheme] = useState<api.Scheme | null>(null);
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | undefined>(undefined);
  const [selectedBeneficiaryFilter, setSelectedBeneficiaryFilter] = useState<string>('');
  const [selectedDeptFilter, setSelectedDeptFilter] = useState<string>('');
  const [beneficiaryOptions, setBeneficiaryOptions] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  // Eligibility Checker State
  const [eligIncome, setEligIncome] = useState<number>(180000);
  const [eligCaste, setEligCaste] = useState<string>('SC');
  const [eligState, setEligState] = useState<string>('Karnataka');
  const [eligEducation, setEligEducation] = useState<string>('Undergraduate');
  const [eligAge, setEligAge] = useState<number>(21);
  const [eligDisability, setEligDisability] = useState<number>(0);
  const [eligGender, setEligGender] = useState<string>('Female');
  const [eligInstitutionalDelivery, setEligInstitutionalDelivery] = useState<string>('');
  const [eligMaritalStatus, setEligMaritalStatus] = useState<string>('Unmarried');
  const [eligSpouseSC, setEligSpouseSC] = useState<string>('');
  const [eligRationCard, setEligRationCard] = useState<string>('');
  const [eligDomesticMeter, setEligDomesticMeter] = useState<string>('');
  const [eligCooperativeMember, setEligCooperativeMember] = useState<string>('');
  const [eligibilityResult, setEligibilityResult] = useState<any | null>(null);

  // Smart Scheme Finder State
  const [finderAge, setFinderAge] = useState<number | ''>(25);
  const [finderDistrict, setFinderDistrict] = useState<string>('Bengaluru Urban');
  const [finderTaluk, setFinderTaluk] = useState<string>('');
  const [finderGender, setFinderGender] = useState<string>('Female');
  const [finderCategory, setFinderCategory] = useState<string>('SC');
  const [finderIncome, setFinderIncome] = useState<number | ''>(120000);
  const [finderOccupation, setFinderOccupation] = useState<string>('Student');
  const [finderEducation, setFinderEducation] = useState<string>('Undergraduate');
  const [finderIsFarmer, setFinderIsFarmer] = useState<boolean>(false);
  const [finderIsStudent, setFinderIsStudent] = useState<boolean>(true);
  const [finderIsWoman, setFinderIsWoman] = useState<boolean>(true);
  const [finderDisabilityStatus, setFinderDisabilityStatus] = useState<string>('No');
  const [finderDisabilityPct, setFinderDisabilityPct] = useState<number | ''>(0);
  const [finderMaritalStatus, setFinderMaritalStatus] = useState<string>('Unmarried');
  
  const [finderLoading, setFinderLoading] = useState<boolean>(false);
  const [finderError, setFinderError] = useState<string>('');
  const [finderResults, setFinderResults] = useState<api.SmartFinderResponse | null>(null);
  const [finderCategoryFilter, setFinderCategoryFilter] = useState<string>('ALL');
  const [finderSearchQuery, setFinderSearchQuery] = useState<string>('');
  const [finderDetailItem, setFinderDetailItem] = useState<api.SmartFinderMatchItem | null>(null);
  const [finderHasSearched, setFinderHasSearched] = useState<boolean>(false);

  // Application Submission State
  const [applyFullName, setApplyFullName] = useState<string>('');
  const [applyPhone, setApplyPhone] = useState<string>('9845012345');
  const [applyDistrict, setApplyDistrict] = useState<string>('Bengaluru Urban');
  const [applyBankAcc, setApplyBankAcc] = useState<string>('SBIN0040123991');
  const [applyIfsc, setApplyIfsc] = useState<string>('SBIN0040123');
  const [applySuccessMsg, setApplySuccessMsg] = useState<string>('');
  const [applyCategory, setApplyCategory] = useState<string>('SC');
  const [applyConsent, setApplyConsent] = useState<boolean>(false);
  const [schemeDynamicForm, setSchemeDynamicForm] = useState<api.DynamicFormDefinition | null>(null);
  const [dynamicFormData, setDynamicFormData] = useState<Record<string, any>>({});
  const [loadingSchemeForm, setLoadingSchemeForm] = useState<boolean>(false);

  // Citizen & Admin Lists
  const [myApplications, setMyApplications] = useState<api.Application[]>([]);
  const [selectedApp, setSelectedApp] = useState<api.Application | null>(null);
  const [adminStats, setAdminStats] = useState<any | null>(null);
  const [adminApplications, setAdminApplications] = useState<api.Application[]>([]);
  const [beneficiaries, setBeneficiaries] = useState<api.Beneficiary[]>([]);
  const [adminStatusFilter, setAdminStatusFilter] = useState<string>('');

  // Simulated DBT System State
  const [dbtStats, setDbtStats] = useState<any | null>(null);
  const [dbtTransactions, setDbtTransactions] = useState<any[]>([]);
  const [dbtStatusFilter, setDbtStatusFilter] = useState<string>('');
  const [selectedBeneficiaryIds, setSelectedBeneficiaryIds] = useState<number[]>([]);
  const [dbtBatchConfirmModal, setDbtBatchConfirmModal] = useState<boolean>(false);
  const [dbtSimulateFailureToggle, setDbtSimulateFailureToggle] = useState<boolean>(false);
  const [dbtProcessingMsg, setDbtProcessingMsg] = useState<string>('');
  const [lastBatchResult, setLastBatchResult] = useState<any | null>(null);
  const [homeTrackAppNumber, setHomeTrackAppNumber] = useState<string>('');
  const [homeTrackResult, setHomeTrackResult] = useState<any | null>(null);
  const [homeTrackError, setHomeTrackError] = useState<string>('');

  // Admin Action Modal
  const [actionModalApp, setActionModalApp] = useState<api.Application | null>(null);
  const [actionRemarks, setActionRemarks] = useState<string>('');
  const [actionType, setActionType] = useState<'APPROVE' | 'REJECT' | 'REQUEST_INFO'>('APPROVE');
  const [actionSanctionAmount, setActionSanctionAmount] = useState<number>(25000);

  // File Upload State for Tracking View
  const [selectedDocFile, setSelectedDocFile] = useState<File | null>(null);
  const [selectedDocCode, setSelectedDocCode] = useState<string>('SUPPLEMENTARY_DOC');
  const [uploadLoading, setUploadLoading] = useState<boolean>(false);

  // New Scheme Creation State (Admin)
  const [newSchemeCode, setNewSchemeCode] = useState<string>('');
  const [newSchemeName, setNewSchemeName] = useState<string>('');
  const [newSchemeDept, setNewSchemeDept] = useState<string>('Social Welfare Department');
  const [newSchemeAuthority, setNewSchemeAuthority] = useState<string>('NagrikSetu — Social Welfare Department');
  const [newSchemeDesc, setNewSchemeDesc] = useState<string>('');
  const [newSchemeBenefit, setNewSchemeBenefit] = useState<string>('');
  const [newSchemeAmount, setNewSchemeAmount] = useState<number>(10000);
  const [newSchemeElig, setNewSchemeElig] = useState<string>('');
  const [newSchemeInstructions, setNewSchemeInstructions] = useState<string>('');
  const [newSchemeCatId, setNewSchemeCatId] = useState<number>(1);
  const [newSchemeStartDate, setNewSchemeStartDate] = useState<string>('2026-01-01');
  const [newSchemeEndDate, setNewSchemeEndDate] = useState<string>('2026-12-31');
  const [createSchemeMsg, setCreateSchemeMsg] = useState<string>('');

  // Citizen Profile State
  const [userProfile, setUserProfile] = useState<api.UserProfileData | null>(null);
  const [isEditingProfile, setIsEditingProfile] = useState<boolean>(false);
  const [profileEditForm, setProfileEditForm] = useState<Partial<api.UserProfileData>>({});
  const [profileSaveMsg, setProfileSaveMsg] = useState<string>('');
  const [profileSaveError, setProfileSaveError] = useState<string>('');
  const [profileLoading, setProfileLoading] = useState<boolean>(false);

  // Initial Data Load
  useEffect(() => {
    loadInitialData();
    if (token) {
      if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') {
        setActiveTab('platform-admin');
        loadAdminData(token);
      } else if (['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole)) {
        setActiveTab('gov-welfare-admin');
        loadAdminData(token);
      } else if (userRole === 'CITIZEN') {
        loadMyApplications();
        loadProfileData(token);
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            const parsedScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
            navigateToSchemeApplication(parsedScheme);
          }
        } catch (e) {
          console.error('Failed to restore pending scheme application:', e);
        }
      }
    }
  }, []);

  async function loadProfileData(authToken?: string) {
    const t = authToken || token;
    if (!t) return;
    try {
      setProfileLoading(true);
      const data = await api.fetchUserProfile(t);
      setUserProfile(data);
      setProfileEditForm(data);
      if (data.full_name) {
        setUserName(data.full_name);
        setApplyFullName(data.full_name);
      }
      if (data.phone) setApplyPhone(data.phone);
      if (data.district) setApplyDistrict(data.district);
      if (data.caste_category) setApplyCategory(data.caste_category);
    } catch (err: any) {
      console.error('Error fetching profile:', err);
    } finally {
      setProfileLoading(false);
    }
  }

  async function handleCitizenRegisterSubmit(e: React.FormEvent) {
    e.preventDefault();
    setRegError('');
    setRegSuccessMsg('');

    // Front-end validations
    if (!regFullName.trim() || regFullName.trim().length < 2) {
      setRegError('Please enter your full legal name (at least 2 characters).');
      return;
    }
    if (!regEmail.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(regEmail.trim())) {
      setRegError('Please enter a valid email address.');
      return;
    }
    const cleanPhone = regPhone.replace(/\D/g, '');
    if (cleanPhone.length < 10) {
      setRegError('Please enter a valid 10-digit mobile number.');
      return;
    }
    if (!regPassword || regPassword.length < 6) {
      setRegError('Password must be at least 6 characters in length.');
      return;
    }
    if (regPassword !== regConfirmPassword) {
      setRegError('Password and Confirm Password do not match.');
      return;
    }

    try {
      setRegLoading(true);
      const res = await api.registerCitizen({
        full_name: regFullName.trim(),
        email: regEmail.trim(),
        phone: cleanPhone,
        password: regPassword,
        confirm_password: regConfirmPassword,
        date_of_birth: regDob || undefined,
        gender: regGender || undefined,
        address: regAddress.trim() || undefined,
        district: regDistrict || undefined,
        taluk: regTaluk || undefined,
        pin_code: regPinCode || undefined,
      });
      setRegSuccessMsg(`Registration successful! Your Citizen ID is ${res.citizen_id}. You can now proceed to log in.`);
      setLoginEmail(regEmail.trim());
      setLoginPassword('');
    } catch (err: any) {
      setRegError(err.message || 'Registration failed. Please try again.');
    } finally {
      setRegLoading(false);
    }
  }

  async function handlePortalLogin(portal: 'CITIZEN' | 'WELFARE' | 'PLATFORM', e: React.FormEvent) {
    e.preventDefault();
    setCitizenAuthError('');
    setWelfareAuthError('');
    setPlatformAuthError('');

    let identifier = '';
    let password = '';

    if (portal === 'CITIZEN') {
      identifier = citizenLoginEmail.trim();
      password = citizenLoginPassword;
      if (!identifier) { setCitizenAuthError('Email or Citizen ID is required.'); return; }
      if (!password) { setCitizenAuthError('Password is required.'); return; }
    } else if (portal === 'WELFARE') {
      identifier = welfareLoginUser.trim();
      password = welfareLoginPassword;
      if (!identifier) { setWelfareAuthError('Username or official email is required.'); return; }
      if (!password) { setWelfareAuthError('Password is required.'); return; }
    } else if (portal === 'PLATFORM') {
      identifier = platformLoginUser.trim();
      password = platformLoginPassword;
      if (!identifier) { setPlatformAuthError('Username or admin email is required.'); return; }
      if (!password) { setPlatformAuthError('Password is required.'); return; }
    }

    try {
      setLoginLoading(true);
      const res = await api.devLogin(identifier, password);
      
      // Role enforcement check between selected portal and server token role
      const userR = (res.role || '').toUpperCase();
      if (portal === 'CITIZEN' && userR !== 'CITIZEN') {
        throw new Error('Administrative accounts cannot sign in through Citizen Portal. Please use your authorized Admin Portal.');
      }
      if (portal === 'WELFARE' && !['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userR)) {
        throw new Error('Access denied: Government Welfare Admin credentials required.');
      }
      if (portal === 'PLATFORM' && !['PLATFORM_ADMIN', 'SWD_ADMIN'].includes(userR)) {
        throw new Error('Access denied: Platform Super Admin credentials required.');
      }

      setToken(res.access_token);
      setUserRole(res.role);
      setCitizenId(res.citizen_id);
      setUserName(res.name);
      localStorage.setItem('ns_swd_token', res.access_token);
      localStorage.setItem('ns_swd_role', res.role);
      localStorage.setItem('ns_swd_citizen_id', res.citizen_id);
      localStorage.setItem('ns_swd_name', res.name);

      if (userR === 'SWD_ADMIN' || userR === 'PLATFORM_ADMIN') {
        setActiveTab('platform-admin');
        loadAdminData(res.access_token);
      } else if (['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userR)) {
        setActiveTab('gov-welfare-admin');
        loadAdminData(res.access_token);
      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          navigateToSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }
    } catch (err: any) {
      let msg = err.message || 'Authentication failed. Please verify credentials.';
      if (msg.includes('Failed to fetch') || msg.includes('NetworkError') || msg.includes('Load failed')) {
        msg = 'Unable to connect to SWD backend service at http://localhost:8005. Please check network connectivity or contact system administration.';
      }
      if (portal === 'CITIZEN') setCitizenAuthError(msg);
      else if (portal === 'WELFARE') setWelfareAuthError(msg);
      else if (portal === 'PLATFORM') setPlatformAuthError(msg);
    } finally {
      setLoginLoading(false);
    }
  }

  async function handleDedicatedLogin(e: React.FormEvent) {
    e.preventDefault();
    setAuthError('');
    if (!loginEmail.trim()) {
      setAuthError('Email address is required.');
      return;
    }
    if (!loginPassword) {
      setAuthError('Password is required.');
      return;
    }
    try {
      setLoginLoading(true);
      const res = await api.devLogin(loginEmail.trim(), loginPassword);
      setToken(res.access_token);
      setUserRole(res.role);
      setCitizenId(res.citizen_id);
      setUserName(res.name);
      localStorage.setItem('ns_swd_token', res.access_token);
      localStorage.setItem('ns_swd_role', res.role);
      localStorage.setItem('ns_swd_citizen_id', res.citizen_id);
      localStorage.setItem('ns_swd_name', res.name);

      if (res.role === 'SWD_ADMIN' || res.role === 'PLATFORM_ADMIN') {
        setActiveTab('platform-admin');
        loadAdminData(res.access_token);
      } else if (res.role === 'WELFARE_OFFICER' || res.role === 'ADMINISTRATOR') {
        setActiveTab('gov-welfare-admin');
        loadAdminData(res.access_token);
      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          navigateToSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }
    } catch (err: any) {
      setAuthError(err.message || 'Invalid email or password. Please try again.');
    } finally {
      setLoginLoading(false);
    }
  }

  async function handleSaveProfile(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;
    setProfileSaveMsg('');
    setProfileSaveError('');
    try {
      setProfileLoading(true);
      const updated = await api.updateUserProfile({
        full_name: profileEditForm.full_name,
        phone: profileEditForm.phone,
        district: profileEditForm.district,
        state: profileEditForm.state,
        annual_income: profileEditForm.annual_income ? Number(profileEditForm.annual_income) : undefined,
        caste_category: profileEditForm.caste_category,
        disability_percentage: profileEditForm.disability_percentage !== undefined ? Number(profileEditForm.disability_percentage) : undefined,
        bank_account_number: profileEditForm.bank_account_number,
        bank_ifsc: profileEditForm.bank_ifsc
      }, token);
      setUserProfile(updated);
      setProfileEditForm(updated);
      if (updated.full_name) {
        setUserName(updated.full_name);
        localStorage.setItem('ns_swd_user_name', updated.full_name);
      }
      setIsEditingProfile(false);
      setProfileSaveMsg('Profile updated and persisted successfully to database!');
    } catch (err: any) {
      setProfileSaveError(err.message || 'Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  }

  function handleCancelEditProfile() {
    if (userProfile) {
      setProfileEditForm(userProfile);
    }
    setIsEditingProfile(false);
    setProfileSaveMsg('');
    setProfileSaveError('');
  }

  async function loadInitialData() {
    try {
      setLoading(true);
      const [cats, scs, bens] = await Promise.all([
        api.fetchCategories().catch(() => []),
        api.fetchSchemes().catch(() => []),
        api.fetchBeneficiaryCategories().catch(() => [])
      ]);
      setCategories(cats);
      setSchemes(scs);
      setBeneficiaryOptions(bens);
      if (scs.length > 0 && !selectedScheme) {
        setSelectedScheme(scs[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setAuthError('');
    try {
      const res = await api.devLogin(loginEmail, loginPassword);
      setToken(res.access_token);
      setUserRole(res.role);
      setCitizenId(res.citizen_id);
      setUserName(res.name);
      localStorage.setItem('ns_swd_token', res.access_token);
      localStorage.setItem('ns_swd_role', res.role);
      localStorage.setItem('ns_swd_citizen_id', res.citizen_id);
      localStorage.setItem('ns_swd_name', res.name);
      setShowLoginModal(false);

      if (res.role === 'SWD_ADMIN' || res.role === 'PLATFORM_ADMIN') {
        setActiveTab('platform-admin');
        loadAdminData(res.access_token);
      } else if (res.role === 'WELFARE_OFFICER' || res.role === 'ADMINISTRATOR') {
        setActiveTab('gov-welfare-admin');
        loadAdminData(res.access_token);
      } else {
        loadMyApplications(res.citizen_id, res.access_token);
        loadProfileData(res.access_token);
        loadNotifications(res.citizen_id);
        loadGrievances(res.citizen_id);

        let restoredScheme: api.Scheme | null = null;
        try {
          const savedPending = sessionStorage.getItem('swd_pending_scheme_apply');
          if (savedPending) {
            restoredScheme = JSON.parse(savedPending);
            sessionStorage.removeItem('swd_pending_scheme_apply');
            setPendingSchemeForApply(null);
            setCitizenLoginNotice('');
          }
        } catch (e) {
          console.error('Error restoring pending scheme:', e);
        }

        if (restoredScheme) {
          navigateToSchemeApplication(restoredScheme);
        } else {
          setActiveTab('swd-home');
        }
      }
    } catch (err: any) {
      setAuthError(err.message || 'Authentication failed. Please verify credentials.');
    }
  }

  async function handleLogout() {
    if (token) {
      try {
        await api.logoutUser(token);
      } catch (err) {
        console.error('Logout invalidation note:', err);
      }
    }
    setToken('');
    setUserRole('');
    setCitizenId('');
    setUserName('');
    localStorage.clear();
    setActiveTab('swd-home');
  }

  async function loadNotifications(citId?: string) {
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
      setIsGpsActive(false);
    } catch (e) {
      console.error(e);
    } finally {
      setOfficeLoading(false);
    }
  }

  async function handleFindNearbyOffices(radiusKm: number = 25.0) {
    if (!navigator.geolocation) {
      setGpsStatus('error');
      setGpsStatusMsg('Geolocation is not supported by your browser. Please select your District below.');
      return;
    }

    setGpsStatus('locating');
    setGpsStatusMsg('Detecting your location...');
    setOfficeLoading(true);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        setUserGpsLocation({ latitude: lat, longitude: lon });
        setGpsStatus('success');
        setGpsStatusMsg(`Location detected: ${lat.toFixed(4)}° N, ${lon.toFixed(4)}° E. Searching within 25 km radius...`);
        try {
          const nearby = await api.fetchNearbyOffices(lat, lon, radiusKm);
          setOffices(nearby);
          setIsGpsActive(true);
          setOfficeDistrictFilter('');
          setOfficeTalukFilter('');
          setOfficeSearchQuery('');
          if (nearby.length > 0) {
            setSelectedOfficeId(nearby[0].id);
          } else {
            setSelectedOfficeId(null);
          }
        } catch (err: any) {
          console.error(err);
          setGpsStatus('error');
          setGpsStatusMsg('Unable to retrieve nearby offices from server. Please select your District.');
        } finally {
          setOfficeLoading(false);
        }
      },
      (err) => {
        setOfficeLoading(false);
        setGpsStatus('denied');
        if (err.code === 1) {
          setGpsStatusMsg('Location permission denied. Please grant permission or choose your District and Taluk manually.');
        } else {
          setGpsStatusMsg('Location detection timed out or unavailable. Please use the manual District & Taluk filter below.');
        }
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
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
      setGrievanceSuccessMsg(`Grievance registered successfully: ${newGrv.grievance_number}`);
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

  async function downloadReceiptPdf(appId: number) {
    try {
      const res = await api.downloadApplicationReceipt(appId, token);
      if (!res.success) {
        alert(res.error || 'Failed to download receipt');
      }
    } catch (err: any) {
      alert(err.message || 'An error occurred while downloading the receipt');
    }
  }

  async function loadAdminData(authToken?: string) {
    const t = authToken || token;
    if (!t) return;
    try {
      const [stats, apps, bens] = await Promise.all([
        api.fetchAdminDashboard(t).catch(() => null),
        api.fetchAdminApplications(t).catch(() => []),
        api.fetchBeneficiaries(t).catch(() => [])
      ]);
      setAdminStats(stats);
      setAdminApplications(apps);
      setBeneficiaries(bens);
    } catch (e) {
      console.error(e);
    }
  }

  async function loadDbtData(authToken?: string) {
    const t = authToken || token;
    if (!t) return;
    try {
      setLoading(true);
      const [stats, txs, bens] = await Promise.all([
        api.fetchDbtDashboardStats(t).catch(() => null),
        api.fetchDbtTransactions(t).catch(() => []),
        api.fetchBeneficiaries(t).catch(() => [])
      ]);
      setDbtStats(stats);
      setDbtTransactions(txs);
      setBeneficiaries(bens);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function handleSingleSimulatedDbt(beneficiaryId: number, simulateFailure = false) {
    if (!token) return;
    try {
      setLoading(true);
      setDbtProcessingMsg('');
      const res = await api.processSingleDbt(beneficiaryId, token, simulateFailure);
      setDbtProcessingMsg(`Simulated Payment Processed! Reference: ${res.transaction_reference} | Status: ${res.status}`);
      await loadDbtData(token);
    } catch (e: any) {
      alert(e.message || 'Payment simulation failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleBatchDbtSubmit() {
    if (!token || selectedBeneficiaryIds.length === 0) return;
    try {
      setLoading(true);
      setDbtProcessingMsg('');
      const failIds = dbtSimulateFailureToggle && selectedBeneficiaryIds.length > 1 ? [selectedBeneficiaryIds[0]] : [];
      const res = await api.processBatchDbt(selectedBeneficiaryIds, token, failIds);
      setLastBatchResult(res);
      setDbtBatchConfirmModal(false);
      setSelectedBeneficiaryIds([]);
      setDbtProcessingMsg(`Batch Processed: ${res.batch_reference} (${res.successful_count} Succeeded, ${res.failed_count} Failed)`);
      await loadDbtData(token);
    } catch (e: any) {
      alert(e.message || 'Batch DBT execution failed');
    } finally {
      setLoading(false);
    }
  }

  async function loadMyApplications(citId?: string, authToken?: string) {
    const cid = citId || citizenId;
    const t = authToken || token;
    if (!t || !cid) return;
    try {
      const apps = await api.fetchCitizenApplications(cid, t);
      setMyApplications(apps);
    } catch (e) {
      console.error(e);
    }
  }

  function openSmartFinder() {
    setFinderError('');
    // Prefill from userProfile if logged in, without mutating userProfile
    if (userProfile) {
      if (userProfile.district) setFinderDistrict(userProfile.district);
      if (userProfile.taluk) setFinderTaluk(userProfile.taluk);
      if (userProfile.gender) {
        setFinderGender(userProfile.gender);
        if (['female', 'woman'].includes(userProfile.gender.toLowerCase())) {
          setFinderIsWoman(true);
        }
      }
      if (userProfile.caste_category) setFinderCategory(userProfile.caste_category);
      if (userProfile.annual_income !== undefined && userProfile.annual_income !== null) {
        setFinderIncome(Number(userProfile.annual_income));
      }
      if (userProfile.date_of_birth) {
        const birthYear = new Date(userProfile.date_of_birth).getFullYear();
        const currentYear = new Date().getFullYear();
        if (currentYear > birthYear) setFinderAge(currentYear - birthYear);
      }
      if (userProfile.disability_percentage) {
        setFinderDisabilityPct(Number(userProfile.disability_percentage));
        setFinderDisabilityStatus(Number(userProfile.disability_percentage) > 0 ? 'Yes' : 'No');
      }
    }
    setActiveTab('smart-finder');
  }

  async function handleSmartFinderSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFinderLoading(true);
    setFinderError('');
    try {
      const questionnaire: api.SmartFinderQuestionnaire = {
        age: finderAge !== '' ? Number(finderAge) : undefined,
        district: finderDistrict || undefined,
        taluk: finderTaluk || undefined,
        gender: finderGender || undefined,
        caste_category: finderCategory || undefined,
        annual_income: finderIncome !== '' ? Number(finderIncome) : undefined,
        occupation: finderOccupation || undefined,
        education_level: finderEducation || undefined,
        is_farmer: finderIsFarmer,
        is_student: finderIsStudent,
        is_woman: finderIsWoman,
        disability_status: finderDisabilityStatus,
        disability_percentage: finderDisabilityPct !== '' ? Number(finderDisabilityPct) : undefined,
        marital_status: finderMaritalStatus || undefined
      };
      const res = await api.matchSmartSchemes(questionnaire);
      setFinderResults(res);
      setFinderHasSearched(true);
    } catch (err: any) {
      setFinderError(err.message || 'Failed to match schemes. Please verify the questionnaire inputs.');
    } finally {
      setFinderLoading(false);
    }
  }

  async function runEligibilityCheck(schemeId: number) {
    try {
      setLoading(true);
      const payload: Record<string, any> = {
        annual_income: eligIncome,
        caste_category: eligCaste,
        residence_state: eligState,
        education_level: eligEducation,
        age: eligAge,
        disability_percentage: eligDisability,
        gender: eligGender,
        is_woman: eligGender.toLowerCase() === 'female'
      };

      if (eligInstitutionalDelivery !== '') {
        payload.institutional_delivery = eligInstitutionalDelivery === 'true';
      }
      if (eligMaritalStatus) {
        payload.marital_status = eligMaritalStatus;
      }
      if (eligSpouseSC !== '') {
        payload.intercaste_spouse_sc = eligSpouseSC === 'true';
      }
      if (eligRationCard) {
        payload.ration_card_type = eligRationCard;
      }
      if (eligDomesticMeter !== '') {
        payload.domestic_meter_connection = eligDomesticMeter === 'true';
      }
      if (eligCooperativeMember !== '') {
        payload.cooperative_member = eligCooperativeMember === 'true';
      }

      const res = await api.checkEligibility(schemeId, payload);
      setEligibilityResult(res);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function navigateToSchemeApplication(scheme: api.Scheme) {
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
  }

  async function handleApplicationSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedScheme) return;
    if (!token) {
      setLoginRoleMode('CITIZEN');
      setShowLoginModal(true);
      return;
    }
    if (!applyConsent) {
      alert('Please accept the Declaration & Consent before submitting.');
      return;
    }
    try {
      setLoading(true);
      const payload = {
        citizen_id: citizenId,
        citizen_name: applyFullName,
        citizen_phone: applyPhone,
        annual_income: eligIncome,
        caste_category: applyCategory,
        residence_district: applyDistrict,
        disability_percentage: eligDisability,
        bank_account_number: applyBankAcc,
        bank_ifsc: applyIfsc,
        application_data_json: dynamicFormData
      };
      const createdApp = await api.submitApplication(selectedScheme.id, payload, token);
      setApplySuccessMsg(`Application Registered: ${createdApp.application_number}`);
      setSelectedApp(createdApp);
      await loadMyApplications();
      setTimeout(() => {
        setActiveTab('tracking');
      }, 1200);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdminActionSubmit() {
    if (!actionModalApp || !token) return;
    try {
      if (actionType === 'REQUEST_INFO') {
        await api.requestAdminInformation(actionModalApp.id, actionRemarks, token);
      } else {
        await api.recordAdminDecision(
          actionModalApp.id,
          actionType === 'APPROVE' ? 'APPROVED' : 'REJECTED',
          actionRemarks,
          actionType === 'APPROVE' ? actionSanctionAmount : undefined,
          token
        );
      }
      setActionModalApp(null);
      setActionRemarks('');
      loadAdminData(token);
    } catch (err: any) {
      alert(err.message);
    }
  }

  async function handleDocumentUploadSubmit() {
    if (!selectedApp || !selectedDocFile || !token) return;
    try {
      setUploadLoading(true);
      await api.uploadDocument(selectedApp.id, selectedDocCode, selectedDocFile, token);
      const refreshed = await api.fetchApplicationDetails(selectedApp.id, token);
      setSelectedApp(refreshed);
      setSelectedDocFile(null);
      await loadMyApplications();
      alert('Document uploaded and linked to application successfully!');
    } catch (err: any) {
      alert(err.message);
    } finally {
      setUploadLoading(false);
    }
  }

  async function handleCreateScheme(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;
    try {
      const payload = {
        scheme_code: newSchemeCode,
        name: newSchemeName,
        category_id: newSchemeCatId,
        department: newSchemeDept,
        administering_authority: newSchemeAuthority,
        description: newSchemeDesc,
        benefit_summary: newSchemeBenefit,
        benefit_amount: newSchemeAmount,
        benefit_type: 'DIRECT_BENEFIT_TRANSFER',
        eligibility_summary: newSchemeElig,
        application_instructions: newSchemeInstructions,
        application_start_date: newSchemeStartDate,
        application_end_date: newSchemeEndDate,
        status: 'PUBLISHED'
      };
      const res = await fetch(`http://localhost:8004/api/swd/schemes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to create scheme');
      }
      setCreateSchemeMsg(`Scheme "${newSchemeName}" successfully created and published!`);
      const updated = await api.fetchSchemes();
      setSchemes(updated);
      setNewSchemeCode('');
      setNewSchemeName('');
      setNewSchemeDesc('');
      setNewSchemeBenefit('');
      setNewSchemeElig('');
      setNewSchemeInstructions('');
    } catch (err: any) {
      alert(err.message);
    }
  }

  return (
    <div className="nagriksetu-app">
      {/* 1. TOP OFFICIAL GOVERNMENT BANNER */}
      <div className="top-gov-banner">
        <div className="top-gov-left">
          <span className="top-gov-flag"></span>
          <span>NagrikSetu &bull; Social Welfare Department (SWD) Microservice &bull; Scheme Information & Application Assistance</span>
        </div>
        <div>
          <span>Public Helplines: 1902 / 080-22261789 &bull; Web Accessibility & Alignment Best Practices</span>
        </div>
      </div>

      {/* 2. DEDICATED SOCIAL WELFARE DEPARTMENT HEADER */}
      <header className="portal-header">
        <div className="brand-section" onClick={() => setActiveTab('swd-home')}>
          <div className="brand-emblem" style={{ background: 'var(--navy-dark)' }}>
            <HeartHandshake size={24} color="#ea580c" />
          </div>
          <div className="brand-text-block">
            <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.25rem' }}>
              NagrikSetu &bull; Social Welfare Department
            </h1>
            <span className="brand-subtext" style={{ color: '#64748b' }}>
              Public Welfare Scheme Discovery & Citizen Assistance Microservice
            </span>
          </div>
        </div>

        {/* SWD Specific Navigation Bar */}
        <nav className="header-nav-links">
          {!token ? (
            /* PUBLIC / UNAUTHENTICATED NAVIGATION */
            <>
              <button 
                className={`nav-link-btn ${activeTab === 'swd-home' ? 'active' : ''}`}
                onClick={() => setActiveTab('swd-home')}
              >
                Home
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' || activeTab === 'scheme-detail' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Welfare Schemes
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'eligibility' ? 'active' : ''}`}
                onClick={() => setActiveTab('eligibility')}
              >
                Eligibility Checker
              </button>
              <button
                className={`nav-link-btn ${activeTab === 'smart-finder' ? 'active' : ''}`}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: activeTab === 'smart-finder' ? '#ea580c' : '#0f2444', fontWeight: 600 }}
                onClick={openSmartFinder}
              >
                <Sparkles size={14} color="#ea580c" /> Smart Scheme Finder
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'office-locator' ? 'active' : ''}`}
                onClick={() => { setActiveTab('office-locator'); loadOffices(); }}
              >
                <Building2 size={14} style={{ display: 'inline', marginRight: '4px' }} /> Office Locator
              </button>

              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginLeft: '0.5rem' }}>
                <button 
                  className={`btn-header-navy ${activeTab === 'sign-in-select' ? 'active' : ''}`}
                  style={{ fontWeight: 700, padding: '0.5rem 1.1rem', backgroundColor: 'var(--navy-dark)', color: '#ffffff', borderRadius: '6px', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
                  onClick={() => {
                    setCitizenAuthError('');
                    setWelfareAuthError('');
                    setPlatformAuthError('');
                    setActiveTab('sign-in-select');
                  }}
                >
                  <LogIn size={15} /> Sign In
                </button>
              </div>
            </>
          ) : userRole === 'CITIZEN' ? (
            /* EXACT 9 PRIMARY CITIZEN NAVIGATION OPTIONS */
            <>
              {/* 1. Home */}
              <button 
                className={`nav-link-btn ${activeTab === 'swd-home' ? 'active' : ''}`}
                onClick={() => setActiveTab('swd-home')}
              >
                Home
              </button>

              {/* 2. Welfare Schemes */}
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' || activeTab === 'scheme-detail' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Welfare Schemes
              </button>

              {/* 3. Eligibility Checker */}
              <button 
                className={`nav-link-btn ${activeTab === 'eligibility' ? 'active' : ''}`}
                onClick={() => setActiveTab('eligibility')}
              >
                Eligibility Checker
              </button>

              {/* 4. Smart Scheme Finder */}
              <button
                className={`nav-link-btn ${activeTab === 'smart-finder' ? 'active' : ''}`}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: activeTab === 'smart-finder' ? '#ea580c' : '#0f2444', fontWeight: 600 }}
                onClick={openSmartFinder}
              >
                <Sparkles size={14} color="#ea580c" /> Smart Scheme Finder
              </button>

              {/* 5. My Applications (Tracking is strictly inside this page) */}
              <button 
                className={`nav-link-btn ${activeTab === 'my-applications' || activeTab === 'tracking' ? 'active' : ''}`}
                onClick={() => { setActiveTab('my-applications'); loadMyApplications(); }}
              >
                My Applications
              </button>

              {/* 6. Grievances (Consolidated: New Submission + Tracking) */}
              <button 
                className={`nav-link-btn ${activeTab === 'grievance' || activeTab === 'my-grievances' ? 'active' : ''}`}
                onClick={() => { setActiveTab('grievance'); loadGrievances(); }}
              >
                Grievances
              </button>

              {/* 7. Office Locator */}
              <button 
                className={`nav-link-btn ${activeTab === 'office-locator' ? 'active' : ''}`}
                onClick={() => { setActiveTab('office-locator'); loadOffices(); }}
              >
                Office Locator
              </button>

              {/* 8. Notifications */}
              <button 
                className={`nav-link-btn ${activeTab === 'notifications-view' ? 'active' : ''}`}
                onClick={() => { setActiveTab('notifications-view'); loadNotifications(); }}
                style={{ position: 'relative' }}
              >
                Notifications
                {notifications.filter(n => !n.is_read).length > 0 && (
                  <span style={{
                    marginLeft: '5px',
                    background: '#ea580c',
                    color: '#ffffff',
                    borderRadius: '10px',
                    padding: '1px 6px',
                    fontSize: '0.68rem',
                    fontWeight: 700
                  }}>
                    {notifications.filter(n => !n.is_read).length}
                  </span>
                )}
              </button>

              {/* 9. My Profile */}
              <button 
                className={`nav-link-btn ${activeTab === 'citizen-profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('citizen-profile')}
              >
                My Profile
              </button>

              {/* Profile & Header Action Controls: Citizen Dashboard Shortcut + Notification Bell + User Badge */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginLeft: '0.5rem' }}>
                {/* Visible Citizen Dashboard Shortcut */}
                <button
                  type="button"
                  className={`btn-header-orange ${activeTab === 'citizen-dashboard' ? 'active' : ''}`}
                  style={{
                    backgroundColor: activeTab === 'citizen-dashboard' ? 'var(--navy-dark)' : '#ea580c',
                    color: '#ffffff',
                    padding: '0.38rem 0.75rem',
                    fontSize: '0.78rem',
                    fontWeight: 700,
                    borderRadius: '6px',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    border: 'none',
                    cursor: 'pointer'
                  }}
                  onClick={() => { setActiveTab('citizen-dashboard'); loadMyApplications(); }}
                  title="Open Citizen Dashboard"
                >
                  <User size={13} /> Dashboard
                </button>
                <div style={{ position: 'relative' }}>
                  <button
                    type="button"
                    onClick={() => {
                      setShowNotificationsDropdown(!showNotificationsDropdown);
                      if (!showNotificationsDropdown) loadNotifications();
                    }}
                    style={{
                      position: 'relative',
                      background: '#f1f5f9',
                      border: '1px solid #cbd5e1',
                      borderRadius: '50%',
                      width: '32px',
                      height: '32px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: 'pointer',
                      color: 'var(--navy-dark)'
                    }}
                    title="View Quick Notifications"
                  >
                    <Bell size={16} />
                    {notifications.filter(n => !n.is_read).length > 0 && (
                      <span style={{
                        position: 'absolute',
                        top: '-3px',
                        right: '-3px',
                        background: '#ea580c',
                        color: '#ffffff',
                        borderRadius: '50%',
                        width: '16px',
                        height: '16px',
                        fontSize: '0.65rem',
                        fontWeight: 800,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        {notifications.filter(n => !n.is_read).length}
                      </span>
                    )}
                  </button>
                  {showNotificationsDropdown && (
                    <div style={{
                      position: 'absolute',
                      right: 0,
                      top: '40px',
                      width: '320px',
                      background: '#ffffff',
                      border: '1px solid var(--line)',
                      borderRadius: '8px',
                      boxShadow: '0 10px 25px rgba(0,0,0,0.15)',
                      zIndex: 1000,
                      overflow: 'hidden'
                    }}>
                      <div style={{ padding: '0.75rem 1rem', background: 'var(--navy-dark)', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ fontWeight: 700, fontSize: '0.82rem' }}>Notifications ({notifications.filter(n => !n.is_read).length} unread)</div>
                        {notifications.some(n => !n.is_read) && (
                          <button type="button" onClick={handleMarkAllRead} style={{ background: 'transparent', border: 'none', color: '#fed7aa', fontSize: '0.72rem', cursor: 'pointer', textDecoration: 'underline' }}>Mark all read</button>
                        )}
                      </div>
                      <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                        {notifications.length === 0 ? (
                          <div style={{ padding: '1.5rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.8rem' }}>No notifications yet.</div>
                        ) : (
                          notifications.map(n => (
                            <div key={n.id} style={{ padding: '0.75rem 1rem', borderBottom: '1px solid #f1f5f9', backgroundColor: n.is_read ? '#ffffff' : '#f8fafc', cursor: 'pointer' }} onClick={() => !n.is_read && handleMarkOneRead(n.id)}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.2rem' }}>
                                <span style={{ fontWeight: 700, fontSize: '0.78rem', color: 'var(--navy-dark)' }}>{n.title}</span>
                                <span style={{ fontSize: '0.65rem', color: '#94a3b8' }}>{new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                              </div>
                              <p style={{ fontSize: '0.73rem', color: '#475569', margin: 0, lineHeight: 1.4 }}>{n.message}</p>
                            </div>
                          ))
                        )}
                      </div>
                      <div style={{ padding: '0.5rem', textAlign: 'center', background: '#f8fafc', borderTop: '1px solid #f1f5f9' }}>
                        <button 
                          style={{ background: 'transparent', border: 'none', color: 'var(--blue)', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}
                          onClick={() => { setShowNotificationsDropdown(false); setActiveTab('notifications-view'); }}
                        >
                          View Full Notifications Page &rarr;
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--navy-dark)' }}>{userName}</div>
                  <div style={{ fontSize: '0.68rem', color: '#15803d', fontWeight: 600 }}>Citizen</div>
                </div>

                {/* 11. Logout */}
                <button 
                  className="nav-link-btn"
                  style={{ padding: '0.4rem 0.65rem', border: '1px solid var(--line)', borderRadius: '6px', display: 'inline-flex', alignItems: 'center', gap: '0.3rem', color: '#b91c1c' }}
                  onClick={handleLogout}
                  title="Log Out of SWD"
                >
                  <LogOut size={15} /> Logout
                </button>
              </div>
            </>
          ) : ['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole) ? (
            /* WELFARE ADMIN HEADER NAV */
            <>
              <button 
                className={`nav-link-btn ${activeTab === 'gov-welfare-admin' ? 'active' : ''}`}
                onClick={() => setActiveTab('gov-welfare-admin')}
                style={{ color: '#0284c7', fontWeight: 700 }}
              >
                Welfare Admin Portal
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Scheme Catalogue
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'office-locator' ? 'active' : ''}`}
                onClick={() => { setActiveTab('office-locator'); loadOffices(); }}
              >
                Office Locator
              </button>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: 'auto' }}>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--navy-dark)' }}>{userName}</div>
                  <div style={{ fontSize: '0.7rem', color: '#0284c7', fontWeight: 600 }}>Government Welfare Admin</div>
                </div>
                <button 
                  className="nav-link-btn"
                  style={{ padding: '0.4rem 0.65rem', border: '1px solid var(--line)', borderRadius: '6px', display: 'inline-flex', alignItems: 'center', gap: '0.3rem', color: '#b91c1c' }}
                  onClick={handleLogout}
                  title="Log Out"
                >
                  <LogOut size={15} /> Logout
                </button>
              </div>
            </>
          ) : (
            /* PLATFORM ADMIN HEADER NAV */
            <>
              <button 
                className={`nav-link-btn ${activeTab === 'platform-admin' ? 'active' : ''}`}
                onClick={() => setActiveTab('platform-admin')}
                style={{ color: '#7c3aed', fontWeight: 700 }}
              >
                Platform Admin Portal
              </button>
              <button 
                className={`nav-link-btn ${activeTab === 'schemes' ? 'active' : ''}`}
                onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
              >
                Schemes View
              </button>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: 'auto' }}>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--navy-dark)' }}>{userName}</div>
                  <div style={{ fontSize: '0.7rem', color: '#7c3aed', fontWeight: 600 }}>Platform Admin</div>
                </div>
                <button 
                  className="nav-link-btn"
                  style={{ padding: '0.4rem 0.65rem', border: '1px solid var(--line)', borderRadius: '6px', display: 'inline-flex', alignItems: 'center', gap: '0.3rem', color: '#b91c1c' }}
                  onClick={handleLogout}
                  title="Log Out"
                >
                  <LogOut size={15} /> Logout
                </button>
              </div>
            </>
          )}
        </nav>
      </header>

      {/* 3. DEDICATED SOCIAL WELFARE DEPARTMENT LANDING PAGE (NO OTHER DEPARTMENTS) */}
      {activeTab === 'swd-home' && (
        <div>
          {/* SWD HERO SECTION */}
          <section className="swd-hero-container">
            <div className="swd-hero-banner" style={{ background: 'linear-gradient(135deg, #0f2444 0%, #173d69 60%, #1e4a7d 100%)' }}>
              <div className="swd-hero-badge" style={{ backgroundColor: 'rgba(234, 88, 12, 0.25)', borderColor: '#ea580c' }}>
                <HeartHandshake size={14} color="#ea580c" />
                <span>DIRECT BENEFIT TRANSFER & WELFARE SERVICES PLATFORM</span>
              </div>

              <h2 className="swd-hero-title">
                Social Welfare Department
              </h2>
              <h3 className="swd-hero-subtitle" style={{ color: '#fed7aa' }}>
                Karnataka Social Welfare & Direct Benefit Transfer
              </h3>
              <p className="swd-hero-desc" style={{ maxWidth: '780px' }}>
                Access social pensions, student scholarships, disability assistance, and welfare schemes. Check eligibility and apply online.
              </p>

              <div className="swd-hero-actions">
                <button
                  className="hero-btn-orange"
                  style={{ backgroundColor: '#ea580c', borderColor: '#ea580c', display: 'inline-flex', alignItems: 'center', gap: '0.45rem' }}
                  onClick={openSmartFinder}
                >
                  <Sparkles size={16} /> Scheme Finder
                </button>
                <button 
                  className="hero-btn-orange"
                  onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}
                >
                  <Search size={16} /> Browse Schemes
                </button>
                <button 
                  className="hero-btn-navy"
                  style={{ backgroundColor: '#ffffff', color: '#0f2444', fontWeight: 700 }}
                  onClick={() => setActiveTab('eligibility')}
                >
                  <CheckCircle2 size={16} color="#15803d" /> Check Eligibility
                </button>
                {!token ? (
                  <button 
                    className="hero-btn-green"
                    onClick={() => {
                      setCitizenAuthError('');
                      setWelfareAuthError('');
                      setPlatformAuthError('');
                      setActiveTab('sign-in-select');
                    }}
                  >
                    <LogIn size={16} /> Sign In
                  </button>
                ) : (
                  <button 
                    className="hero-btn-green"
                    onClick={() => {
                      if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') setActiveTab('platform-admin');
                      else if (['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole)) setActiveTab('gov-welfare-admin');
                      else setActiveTab('citizen-dashboard');
                    }}
                  >
                    <User size={16} /> My Dashboard
                  </button>
                )}
              </div>
            </div>
          </section>

          {/* SWD CORE FUNCTIONAL PILLARS (DEPARTMENTAL FOCUS ONLY) */}
          <section className="section-wrapper">
            <div className="services-section-header">
              <div className="services-tag">&bull; SCHEME CATEGORIES &bull;</div>
              <h3 className="services-title">
                Welfare Categories
              </h3>
              <p className="services-desc">
                Explore government welfare schemes by category.
              </p>
            </div>

            <div className="streams-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem' }}>
              {/* Category 5: Flagship Guarantee Schemes */}
              <div className="stream-card" style={{ borderColor: '#fed7aa' }}>
                <span className="stream-badge" style={{ backgroundColor: '#fed7aa', color: '#c2410c' }}>5 Flagship Guarantees</span>
                <div className="stream-icon amber">
                  <Award size={20} />
                </div>
                <h4 className="stream-title">Flagship Guarantees</h4>
                <p className="stream-summary">
                  Gruha Lakshmi, Gruha Jyothi, Anna Bhagya, and Yuva Nidhi flagship citizen welfare guarantees.
                </p>
                <div className="stream-schemes-box">
                  <div className="stream-schemes-title">Featured Schemes:</div>
                  <ul className="stream-schemes-list">
                    <li><Check size={12} color="#16a34a" /> Gruha Lakshmi (₹2,000/mo)</li>
                    <li><Check size={12} color="#16a34a" /> Gruha Jyothi (200 Units)</li>
                    <li><Check size={12} color="#16a34a" /> Anna Bhagya & Yuva Nidhi</li>
                  </ul>
                </div>
                <button 
                  className="btn-stream-action"
                  onClick={() => { setSelectedCategoryId(5); setActiveTab('schemes'); api.fetchSchemes({ category_id: 5 }).then(setSchemes); }}
                >
                  <span>View Schemes</span> <ChevronRight size={14} />
                </button>
              </div>

              {/* Category 6: Women, Children & Maternal Care */}
              <div className="stream-card" style={{ borderColor: '#fed7aa' }}>
                <span className="stream-badge" style={{ backgroundColor: '#fed7aa', color: '#c2410c' }}>7 Active Schemes</span>
                <div className="stream-icon peach">
                  <HeartHandshake size={20} />
                </div>
                <h4 className="stream-title">Women & Child Welfare</h4>
                <p className="stream-summary">
                  Udyogini enterprise loans, Bhagyalakshmi bonds, Matru Poorna meals, Thayi Bhagya, and Madilu post-natal kits.
                </p>
                <div className="stream-schemes-box">
                  <div className="stream-schemes-title">Featured Schemes:</div>
                  <ul className="stream-schemes-list">
                    <li><Check size={12} color="#16a34a" /> Udyogini & Bhagyalakshmi</li>
                    <li><Check size={12} color="#16a34a" /> Matru Poorna & Madilu Kit</li>
                    <li><Check size={12} color="#16a34a" /> Santhwana & Dhanashree</li>
                  </ul>
                </div>
                <button 
                  className="btn-stream-action"
                  onClick={() => { setSelectedCategoryId(6); setActiveTab('schemes'); api.fetchSchemes({ category_id: 6 }).then(setSchemes); }}
                >
                  <span>View Schemes</span> <ChevronRight size={14} />
                </button>
              </div>

              {/* Category 7: Agriculture & Rural Livelihoods */}
              <div className="stream-card" style={{ borderColor: '#fed7aa' }}>
                <span className="stream-badge" style={{ backgroundColor: '#fed7aa', color: '#c2410c' }}>7 Active Schemes</span>
                <div className="stream-icon green">
                  <Landmark size={20} />
                </div>
                <h4 className="stream-title">Agriculture & Rural</h4>
                <p className="stream-summary">
                  Raitha Vidya Nidhi scholarships, Ganga Kalyana borewells, Krishi Bhagya farm ponds, and Yeshasvini healthcare.
                </p>
                <div className="stream-schemes-box">
                  <div className="stream-schemes-title">Featured Schemes:</div>
                  <ul className="stream-schemes-list">
                    <li><Check size={12} color="#16a34a" /> Raitha Vidya Nidhi (₹11k)</li>
                    <li><Check size={12} color="#16a34a" /> Ganga Kalyana Borewells</li>
                    <li><Check size={12} color="#16a34a" /> Yeshasvini Health Cover</li>
                  </ul>
                </div>
                <button 
                  className="btn-stream-action"
                  onClick={() => { setSelectedCategoryId(7); setActiveTab('schemes'); api.fetchSchemes({ category_id: 7 }).then(setSchemes); }}
                >
                  <span>View Schemes</span> <ChevronRight size={14} />
                </button>
              </div>

              {/* Category 8: Education, Youth & Startups */}
              <div className="stream-card" style={{ borderColor: '#fed7aa' }}>
                <span className="stream-badge" style={{ backgroundColor: '#fed7aa', color: '#c2410c' }}>5 Active Schemes</span>
                <div className="stream-icon blue">
                  <BookOpen size={20} />
                </div>
                <h4 className="stream-title">Education & Startups</h4>
                <p className="stream-summary">
                  Arivu loans, Vidyasiri food stipends, Dr. Ambedkar Overseas scholarships, and ELEVATE startup innovation grants.
                </p>
                <div className="stream-schemes-box">
                  <div className="stream-schemes-title">Featured Schemes:</div>
                  <ul className="stream-schemes-list">
                    <li><Check size={12} color="#16a34a" /> Arivu Education Loans</li>
                    <li><Check size={12} color="#16a34a" /> Vidyasiri Food Stipends</li>
                    <li><Check size={12} color="#16a34a" /> ELEVATE Startup Grants</li>
                  </ul>
                </div>
                <button 
                  className="btn-stream-action"
                  onClick={() => { setSelectedCategoryId(8); setActiveTab('schemes'); api.fetchSchemes({ category_id: 8 }).then(setSchemes); }}
                >
                  <span>View Schemes</span> <ChevronRight size={14} />
                </button>
              </div>

              {/* Category 9: Labour, Housing & Social Security */}
              <div className="stream-card" style={{ borderColor: '#fed7aa' }}>
                <span className="stream-badge" style={{ backgroundColor: '#fed7aa', color: '#c2410c' }}>7 Active Schemes</span>
                <div className="stream-icon orange">
                  <Shield size={20} />
                </div>
                <h4 className="stream-title">Labour & Housing</h4>
                <p className="stream-summary">
                  KBOCWWB pensions, Gig Workers insurance, Swavalambi Sarathi cabs, Basava Vasati pucca houses, and Gruha Arogya.
                </p>
                <div className="stream-schemes-box">
                  <div className="stream-schemes-title">Featured Schemes:</div>
                  <ul className="stream-schemes-list">
                    <li><Check size={12} color="#16a34a" /> KBOCWWB & Gig Insurance</li>
                    <li><Check size={12} color="#16a34a" /> Swavalambi Sarathi Cabs</li>
                    <li><Check size={12} color="#16a34a" /> Basava & Ambedkar Housing</li>
                  </ul>
                </div>
                <button 
                  className="btn-stream-action"
                  onClick={() => { setSelectedCategoryId(9); setActiveTab('schemes'); api.fetchSchemes({ category_id: 9 }).then(setSchemes); }}
                >
                  <span>View Schemes</span> <ChevronRight size={14} />
                </button>
              </div>
            </div>

            {/* QUICK CIVIC PORTAL ACCESS TRIO */}
            <div className="civic-trio-grid" style={{ marginTop: '2rem' }}>
              <div className="civic-card" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('eligibility')}>
                <div className="civic-card-icon blue"><CheckCircle2 size={20} /></div>
                <div>
                  <h5 className="civic-card-title">SWD Rules & Eligibility Engine</h5>
                  <p className="civic-card-desc">Deterministic verification of income, domicile, category, and age rules against official department criteria without bias.</p>
                </div>
              </div>

              <div className="civic-card" style={{ cursor: 'pointer' }} onClick={() => {
                if (token && userRole === 'CITIZEN') setActiveTab('my-applications');
                else {
                  setCitizenAuthError('');
                  setActiveTab('sign-in-select');
                }
              }}>
                <div className="civic-card-icon green"><FileText size={20} /></div>
                <div>
                  <h5 className="civic-card-title">Dossier Tracking & Uploads</h5>
                  <p className="civic-card-desc">Track status transitions (SUBMITTED &rarr; UNDER_REVIEW &rarr; APPROVED), upload revenue certificates, and view DBT sanction orders.</p>
                </div>
              </div>

              <div className="civic-card" style={{ cursor: 'pointer' }} onClick={() => {
                if (token && userRole === 'CITIZEN') setActiveTab('citizen-dashboard');
                else if (token && (userRole === 'GOVERNMENT_WELFARE_ADMIN' || userRole === 'WELFARE_OFFICER' || userRole === 'ADMINISTRATOR')) setActiveTab('gov-welfare-admin');
                else if (token && (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN')) setActiveTab('platform-admin');
                else {
                  setCitizenAuthError('');
                  setActiveTab('sign-in-select');
                }
              }}>
                <div className="civic-card-icon orange"><Shield size={20} /></div>
                <div>
                  <h5 className="civic-card-title">Application & Beneficiary Services</h5>
                  <p className="civic-card-desc">Access application updates, approval information, beneficiary details, and welfare assistance services through one transparent portal.</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* 4. MAIN CONTENT ROUTED VIEWS */}
      <main className="section-wrapper">
        {/* VIEW: CITIZEN DASHBOARD */}
        {activeTab === 'citizen-dashboard' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Portal Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  The <strong>Citizen Dashboard</strong> is reserved exclusively for registered citizens. Administrative officers must access their designated Administrative portals.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                  <button className="btn-orange" onClick={() => setActiveTab('sign-in-select')}>Sign In</button>
                </div>
              </div>
            </div>
          ) : (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Citizen Dashboard</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Welcome, {userName} (Citizen ID: {citizenId})</p>
              </div>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                <button className="btn-secondary" onClick={() => setActiveTab('citizen-profile')}>View Profile</button>
                <button className="btn-orange" onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}>Apply for New Scheme</button>
              </div>
            </div>

            {/* Quick Citizen Stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '0.85rem', marginBottom: '1.5rem' }}>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Total Applications</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--navy-dark)' }}>{myApplications.length}</div>
                <div style={{ fontSize: '0.7rem', color: '#64748b' }}>All Submitted Applications</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Pending</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#3b82f6' }}>
                  {myApplications.filter(a => a.status === 'SUBMITTED').length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#3b82f6' }}>Awaiting Scrutiny</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Under Review</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#d97706' }}>
                  {myApplications.filter(a => a.status === 'UNDER_REVIEW' || a.status === 'MORE_INFORMATION_REQUIRED').length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#d97706' }}>Officer In-Progress</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Approved</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#15803d' }}>
                  {myApplications.filter(a => a.status === 'APPROVED').length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#15803d' }}>Sanctioned for Benefit</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Rejected</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#b91c1c' }}>
                  {myApplications.filter(a => a.status === 'REJECTED').length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#b91c1c' }}>Ineligible / Closed</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Total Grievances</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#6b21a8' }}>
                  {grievances.length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#6b21a8' }}>Reported Issues</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Awaiting Resolution</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#ea580c' }}>
                  {grievances.filter(g => g.status !== 'RESOLVED').length}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#ea580c' }}>Pending Officer Action</div>
              </div>
            </div>

            {/* My Active Applications Table */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h4 style={{ color: 'var(--navy-dark)' }}>My Welfare Applications</h4>
              <button className="btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }} onClick={() => loadMyApplications()}>
                <RefreshCw size={12} /> Refresh
              </button>
            </div>

            {myApplications.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <AlertCircle size={32} color="#94a3b8" style={{ margin: '0 auto 0.5rem auto' }} />
                <p style={{ color: '#64748b', fontSize: '0.9rem' }}>You have not submitted any welfare scheme applications yet.</p>
                <button className="btn-orange" style={{ marginTop: '0.75rem' }} onClick={() => { setActiveTab('schemes'); api.fetchSchemes().then(setSchemes); }}>
                  Explore & Apply for Schemes
                </button>
              </div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Application Number</th>
                    <th>Citizen Name</th>
                    <th>District</th>
                    <th>Status</th>
                    <th>Submitted On</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {myApplications.map(app => (
                    <tr key={app.id}>
                      <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{app.application_number}</td>
                      <td>{app.citizen_name}</td>
                      <td>{app.residence_district}</td>
                      <td><span className={`status-badge ${app.status}`}>{app.status.replace('_', ' ')}</span></td>
                      <td>{app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
                            onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                          >
                            Track &rarr;
                          </button>
                          <button 
                            className="btn-orange" 
                            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                            onClick={() => downloadReceiptPdf(app.id)}
                            title="Download Receipt"
                          >
                            <Download size={13} /> Receipt
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          )
        )}

                {/* VIEW: CITIZEN PROFILE */}
        {activeTab === 'citizen-profile' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Access Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Citizen profiles can only be accessed by authenticated citizens.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Citizen Profile</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Your verified profile for scheme eligibility and DBT.</p>
              </div>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                {!isEditingProfile ? (
                  <button className="btn-orange" onClick={() => {
                    if (userProfile) setProfileEditForm(userProfile);
                    setIsEditingProfile(true);
                    setProfileSaveMsg('');
                    setProfileSaveError('');
                  }}>
                    Edit Profile
                  </button>
                ) : (
                  <button className="btn-secondary" onClick={handleCancelEditProfile}>
                    Cancel
                  </button>
                )}
                <button className="btn-secondary" onClick={() => setActiveTab('citizen-dashboard')}>&larr; Back</button>
              </div>
            </div>

            {profileSaveMsg && (
              <div style={{ padding: '0.75rem 1rem', background: '#dcfce7', border: '1px solid #86efac', color: '#166534', borderRadius: '6px', marginBottom: '1rem', fontSize: '0.85rem' }}>
                <CheckCircle size={16} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'text-bottom' }} />
                {profileSaveMsg}
              </div>
            )}

            {profileSaveError && (
              <div style={{ padding: '0.75rem 1rem', background: '#fee2e2', border: '1px solid #fca5a5', color: '#991b1b', borderRadius: '6px', marginBottom: '1rem', fontSize: '0.85rem' }}>
                <AlertCircle size={16} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'text-bottom' }} />
                {profileSaveError}
              </div>
            )}

            {isEditingProfile ? (
              <form onSubmit={handleSaveProfile} className="swd-form-card">
                <div className="swd-form-section-header">
                  <User size={18} color="#ea580c" />
                  <div>
                    <h4 className="swd-form-section-title">Edit Citizen Profile</h4>
                    <p className="swd-form-section-desc">Keep your official citizen registry details and DBT bank information up to date.</p>
                  </div>
                </div>

                <div className="form-grid-2" style={{ marginBottom: '1.5rem' }}>
                  <div className="form-group">
                    <label className="form-label">
                      <span>Full Legal Name</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.full_name || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, full_name: e.target.value })} 
                      required 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Contact Phone</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.phone || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, phone: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">District</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.district || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, district: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">State</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.state || 'Karnataka'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, state: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Annual Family Income (INR)</label>
                    <input 
                      type="number" 
                      className="form-input" 
                      value={profileEditForm.annual_income !== undefined ? profileEditForm.annual_income : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, annual_income: Number(e.target.value) })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Caste / Category</label>
                    <select 
                      className="form-input form-select" 
                      value={profileEditForm.caste_category || 'SC'} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, caste_category: e.target.value })}
                    >
                      <option value="SC">Scheduled Caste (SC)</option>
                      <option value="ST">Scheduled Tribe (ST)</option>
                      <option value="OBC">Other Backward Class (OBC)</option>
                      <option value="Minority">Minority</option>
                      <option value="General">General</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Disability Percentage (%)</label>
                    <input 
                      type="number" 
                      className="form-input" 
                      value={profileEditForm.disability_percentage !== undefined ? profileEditForm.disability_percentage : ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, disability_percentage: Number(e.target.value) })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Bank Account Number (DBT)</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.bank_account_number || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_account_number: e.target.value })} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Bank IFSC</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={profileEditForm.bank_ifsc || ''} 
                      onChange={(e) => setProfileEditForm({ ...profileEditForm, bank_ifsc: e.target.value })} 
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '1rem', borderTop: '1px solid var(--line)', paddingTop: '1.25rem', alignItems: 'center' }}>
                  <button type="submit" className="btn-orange" style={{ minWidth: '160px', height: '44px' }} disabled={profileLoading}>
                    {profileLoading ? 'Saving Changes...' : 'Save Changes'}
                  </button>
                  <button type="button" className="btn-secondary" style={{ height: '44px' }} onClick={handleCancelEditProfile} disabled={profileLoading}>
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem' }}>
                <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                    <h4 style={{ color: 'var(--navy-dark)', margin: 0 }}>
                      Demographic & Identity Attributes
                    </h4>
                    <button className="btn-secondary" style={{ padding: '0.25rem 0.65rem', fontSize: '0.75rem' }} onClick={() => {
                      if (userProfile) setProfileEditForm(userProfile);
                      setIsEditingProfile(true);
                    }}>
                      Edit Profile
                    </button>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', fontSize: '0.85rem' }}>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Citizen Platform ID</label>
                      <strong>{userProfile?.citizen_id || citizenId}</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Full Name</label>
                      <strong>{userProfile?.full_name || userName}</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Permanent State Domicile</label>
                      <strong>{userProfile?.state || 'Karnataka'} (Verified)</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>District</label>
                      <strong>{userProfile?.district || 'Bengaluru Urban'}</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Social Category / Caste</label>
                      <strong>{userProfile?.caste_category || 'Scheduled Caste (SC)'}</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Annual Family Income</label>
                      <strong>₹{(userProfile?.annual_income ?? 180000).toLocaleString('en-IN')} (Revenue Certified)</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Disability Status</label>
                      <strong>{userProfile?.disability_percentage ? `${userProfile.disability_percentage}%` : 'None (0%)'}</strong>
                    </div>
                    <div>
                      <label style={{ color: '#64748b', fontSize: '0.75rem', display: 'block' }}>Contact Phone</label>
                      <strong>{userProfile?.phone || 'Not Provided'}</strong>
                    </div>
                  </div>
                </div>

                <div style={{ background: '#f8fafc', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                  <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem' }}>Direct Benefit Transfer (DBT) Seeding</h4>
                  <div style={{ fontSize: '0.82rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    <div>
                      <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>Bank Account Number</span>
                      <strong>{userProfile?.bank_account_number || 'SBIN0040123991'}</strong>
                    </div>
                    <div>
                      <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>Bank IFSC</span>
                      <strong>{userProfile?.bank_ifsc || 'SBIN0040123'}</strong>
                    </div>
                    <div>
                      <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>Aadhaar Seeding Status</span>
                      <span className="status-badge APPROVED" style={{ display: 'inline-block', marginTop: '0.25rem' }}>
                        <CheckCircle size={12} style={{ display: 'inline', marginRight: '4px' }} />
                        Aadhaar Bridge Linked & Active
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          )
        )}

        
        {/* VIEW: ONE PAGE AUTHENTICATION GATEWAY WITH THREE SEPARATE CARDS */}
        {activeTab === 'sign-in-select' && (
          <div className="swd-view-container" style={{ maxWidth: '1180px', margin: '0 auto', padding: '2rem 1rem' }}>
            <div className="swd-view-header" style={{ textAlign: 'center', justifyContent: 'center', marginBottom: '2rem' }}>
              <div>
                <h2 style={{ fontSize: '1.65rem', color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>
                  Select Authentication Gateway
                </h2>
                <p style={{ fontSize: '0.9rem', color: '#64748b', maxWidth: '720px', margin: '0 auto' }}>
                  Choose the portal you want to access.
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.75rem', alignItems: 'stretch' }}>
              
              {/* CARD 1: CITIZEN PORTAL */}
              <div style={{
                background: '#ffffff',
                border: '2px solid #ea580c',
                borderRadius: '12px',
                padding: '1.75rem',
                boxShadow: '0 4px 16px rgba(234, 88, 12, 0.08)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', marginBottom: '1rem' }}>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '10px',
                      backgroundColor: '#fff7ed',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <User size={26} color="#ea580c" />
                    </div>
                    <div>
                      <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', margin: 0, fontWeight: 700 }}>
                        Citizen Portal
                      </h3>
                      <span style={{ fontSize: '0.75rem', color: '#ea580c', fontWeight: 600 }}>Public Citizen Access</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.82rem', color: '#475569', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    Access welfare schemes, check eligibility, track applications and manage your profile.
                  </p>

                  {/* PENDING SCHEME APPLICATION NOTICE BANNER */}
                  {citizenLoginNotice && (
                    <div style={{
                      backgroundColor: '#eff6ff',
                      border: '1px solid #93c5fd',
                      borderRadius: '8px',
                      padding: '0.85rem 1rem',
                      marginBottom: '1rem',
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.65rem'
                    }}>
                      <AlertCircle size={20} color="#1d4ed8" style={{ marginTop: '0.1rem', flexShrink: 0 }} />
                      <div style={{ flex: 1, fontSize: '0.82rem', color: '#1e3a8a', lineHeight: 1.5 }}>
                        <strong>{citizenLoginNotice}</strong>
                        {pendingSchemeForApply && (
                          <div style={{ marginTop: '0.25rem', fontSize: '0.78rem', color: '#2563eb' }}>
                            Target Scheme: <strong>{pendingSchemeForApply.name}</strong>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* CITIZEN LOGIN FORM */}
                  <div style={{ background: '#fffaf5', border: '1px solid #fed7aa', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>
                    <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--navy-dark)', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      <LogIn size={15} color="#ea580c" /> Citizen Sign In
                    </div>

                    {citizenAuthError && (
                      <div style={{ backgroundColor: '#fee2e2', border: '1px solid #fca5a5', color: '#b91c1c', padding: '0.5rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', marginBottom: '0.75rem' }}>
                        {citizenAuthError}
                      </div>
                    )}

                    <form onSubmit={(e) => handlePortalLogin('CITIZEN', e)}>
                      <div style={{ marginBottom: '0.75rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Registered Email / Citizen ID
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="Enter registered email or ID"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={citizenLoginEmail}
                          onChange={e => setCitizenLoginEmail(e.target.value)}
                        />
                      </div>

                      <div style={{ marginBottom: '0.85rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Password
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Enter password"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={citizenLoginPassword}
                          onChange={e => setCitizenLoginPassword(e.target.value)}
                        />
                      </div>

                      <button
                        type="submit"
                        className="btn-orange"
                        style={{ width: '100%', padding: '0.65rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                        disabled={loginLoading}
                      >
                        <LogIn size={15} /> {loginLoading ? 'Authenticating...' : 'Sign In as Citizen'}
                      </button>
                    </form>
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem' }}>
                  <button
                    type="button"
                    className="btn-secondary"
                    style={{ width: '100%', padding: '0.65rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                    onClick={() => {
                      setRegError('');
                      setRegSuccessMsg('');
                      setActiveTab('citizen-register');
                    }}
                  >
                    <UserPlus size={15} /> Register as New Citizen
                  </button>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textAlign: 'center', marginTop: '0.5rem' }}>
                    Open to all residents of Karnataka.
                  </div>
                </div>
              </div>


              {/* CARD 2: GOVERNMENT WELFARE ADMIN */}
              <div style={{
                background: '#ffffff',
                border: '2px solid #0284c7',
                borderRadius: '12px',
                padding: '1.75rem',
                boxShadow: '0 4px 16px rgba(2, 132, 199, 0.08)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', marginBottom: '1rem' }}>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '10px',
                      backgroundColor: '#f0f9ff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <Building2 size={26} color="#0284c7" />
                    </div>
                    <div>
                      <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', margin: 0, fontWeight: 700 }}>
                        Government Welfare Admin
                      </h3>
                      <span style={{ fontSize: '0.75rem', color: '#0284c7', fontWeight: 600 }}>Welfare Officer Access</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.82rem', color: '#475569', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    Review applications, manage assigned grievances and support welfare services.
                  </p>

                  {/* WELFARE ADMIN LOGIN FORM */}
                  <div style={{ background: '#f8fafc', border: '1px solid #bae6fd', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>
                    <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--navy-dark)', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      <Building2 size={15} color="#0284c7" /> Welfare Admin Sign In
                    </div>

                    {welfareAuthError && (
                      <div style={{ backgroundColor: '#fee2e2', border: '1px solid #fca5a5', color: '#b91c1c', padding: '0.5rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', marginBottom: '0.75rem' }}>
                        {welfareAuthError}
                      </div>
                    )}

                    <form onSubmit={(e) => handlePortalLogin('WELFARE', e)}>
                      <div style={{ marginBottom: '0.75rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Officer Username / Email
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="Enter officer username or email"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={welfareLoginUser}
                          onChange={e => setWelfareLoginUser(e.target.value)}
                        />
                      </div>

                      <div style={{ marginBottom: '0.85rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Password
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Enter password"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={welfareLoginPassword}
                          onChange={e => setWelfareLoginPassword(e.target.value)}
                        />
                      </div>

                      <button
                        type="submit"
                        className="btn-header-navy"
                        style={{ width: '100%', padding: '0.65rem', fontSize: '0.85rem', backgroundColor: '#0284c7', borderColor: '#0284c7', color: '#ffffff', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                        disabled={loginLoading}
                      >
                        <Building2 size={15} /> {loginLoading ? 'Authenticating...' : 'Sign In as Welfare Admin'}
                      </button>
                    </form>
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: '#64748b' }}>
                    Role: <strong>GOVERNMENT_WELFARE_ADMIN</strong>
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                    Access restricted to authorized SWD officers.
                  </div>
                </div>
              </div>


              {/* CARD 3: PLATFORM ADMIN */}
              <div style={{
                background: '#ffffff',
                border: '2px solid #0f2444',
                borderRadius: '12px',
                padding: '1.75rem',
                boxShadow: '0 4px 16px rgba(15, 36, 68, 0.08)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', marginBottom: '1rem' }}>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '10px',
                      backgroundColor: '#f1f5f9',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <Shield size={26} color="#0f2444" />
                    </div>
                    <div>
                      <h3 style={{ fontSize: '1.2rem', color: 'var(--navy-dark)', margin: 0, fontWeight: 700 }}>
                        Platform Admin
                      </h3>
                      <span style={{ fontSize: '0.75rem', color: '#0f2444', fontWeight: 600 }}>Platform Administration</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.82rem', color: '#475569', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    Monitor platform activity, records, users and system operations.
                  </p>

                  {/* PLATFORM ADMIN LOGIN FORM */}
                  <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>
                    <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--navy-dark)', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      <Shield size={15} color="#0f2444" /> Platform Admin Sign In
                    </div>

                    {platformAuthError && (
                      <div style={{ backgroundColor: '#fee2e2', border: '1px solid #fca5a5', color: '#b91c1c', padding: '0.5rem 0.75rem', borderRadius: '6px', fontSize: '0.75rem', marginBottom: '0.75rem' }}>
                        {platformAuthError}
                      </div>
                    )}

                    <form onSubmit={(e) => handlePortalLogin('PLATFORM', e)}>
                      <div style={{ marginBottom: '0.75rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Super-Admin Username / Email
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="Enter admin username or email"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={platformLoginUser}
                          onChange={e => setPlatformLoginUser(e.target.value)}
                        />
                      </div>

                      <div style={{ marginBottom: '0.85rem' }}>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.2rem' }}>
                          Password
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Enter password"
                          className="filter-input"
                          style={{ width: '100%', fontSize: '0.82rem', padding: '0.5rem' }}
                          value={platformLoginPassword}
                          onChange={e => setPlatformLoginPassword(e.target.value)}
                        />
                      </div>

                      <button
                        type="submit"
                        className="btn-header-navy"
                        style={{ width: '100%', padding: '0.65rem', fontSize: '0.85rem', backgroundColor: 'var(--navy-dark)', color: '#ffffff', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                        disabled={loginLoading}
                      >
                        <Shield size={15} /> {loginLoading ? 'Authenticating...' : 'Sign In as Platform Admin'}
                      </button>
                    </form>
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: '#64748b' }}>
                    Role: <strong>PLATFORM_ADMIN</strong>
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                    System governance and security administration.
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

{/* VIEW: CITIZEN REGISTRATION (SEPARATE DEDICATED PAGE) */}
        {activeTab === 'citizen-register' && (
          <div className="swd-view-container" style={{ maxWidth: '820px', margin: '0 auto' }}>
            <div className="swd-view-header">
              <div>
                <h2>Citizen Registration</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Register for the NagrikSetu Social Welfare Department to apply for welfare schemes, track DBT disbursements, and maintain your citizen registry profile.
                </p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>
                &larr; Back
              </button>
            </div>

            {regSuccessMsg ? (
              <div style={{ background: '#ffffff', padding: '2rem', borderRadius: '8px', border: '1px solid #86efac', textAlign: 'center' }}>
                <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: '#dcfce7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem auto' }}>
                  <CheckCircle size={28} color="#16a34a" />
                </div>
                <h3 style={{ color: 'var(--navy-dark)', marginBottom: '0.5rem' }}>Registration Successful!</h3>
                <p style={{ color: '#166534', fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
                  {regSuccessMsg}
                </p>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
                  <button 
                    className="btn-orange" 
                    onClick={() => {
                      setRegSuccessMsg('');
                      setCitizenAuthError('');
                      setActiveTab('sign-in-select');
                    }}
                  >
                    Proceed to Citizen Sign In &rarr;
                  </button>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>
                    Browse Schemes
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ background: '#ffffff', padding: '2rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                {regError && (
                  <div style={{ backgroundColor: '#fee2e2', border: '1px solid #fca5a5', color: '#b91c1c', padding: '0.85rem 1rem', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <AlertCircle size={18} />
                    <span>{regError}</span>
                  </div>
                )}

                <form onSubmit={handleCitizenRegisterSubmit}>
                  {/* Section 1: Required Account Credentials */}
                  <div className="swd-form-section" style={{ marginBottom: '1.25rem' }}>
                    <div className="swd-form-section-header">
                      <User size={18} color="#ea580c" />
                      <div>
                        <h4 className="swd-form-section-title">1. Account Credentials & Login Details</h4>
                        <p className="swd-form-section-desc">Required for citizen authentication and scheme application submission.</p>
                      </div>
                    </div>
                    
                    <div className="form-grid-2">
                      <div className="form-group form-grid-full">
                        <label className="form-label">
                          <span>Full Legal Name</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="text" 
                          required 
                          placeholder="e.g. Anand Kumar Nayak" 
                          className="form-input" 
                          value={regFullName}
                          onChange={e => setRegFullName(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Email Address</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="email" 
                          required 
                          placeholder="anand@example.com" 
                          className="form-input" 
                          value={regEmail}
                          onChange={e => setRegEmail(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Mobile Number (10 digits)</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <input 
                          type="tel" 
                          required 
                          maxLength={10}
                          placeholder="9845012345" 
                          className="form-input" 
                          value={regPhone}
                          onChange={e => setRegPhone(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Password (min 6 characters)</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <div style={{ position: 'relative' }}>
                          <input 
                            type={showPassword ? "text" : "password"} 
                            required 
                            minLength={6}
                            placeholder="Create strong password" 
                            className="form-input" 
                            style={{ paddingRight: '2.5rem' }}
                            value={regPassword}
                            onChange={e => setRegPassword(e.target.value)}
                          />
                          <button 
                            type="button" 
                            onClick={() => setShowPassword(!showPassword)}
                            style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                            title={showPassword ? "Hide password" : "Show password"}
                          >
                            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>

                      <div className="form-group">
                        <label className="form-label">
                          <span>Confirm Password</span>
                          <span className="form-label-required">*</span>
                        </label>
                        <div style={{ position: 'relative' }}>
                          <input 
                            type={showConfirmPassword ? "text" : "password"} 
                            required 
                            minLength={6}
                            placeholder="Re-enter password" 
                            className="form-input" 
                            style={{ paddingRight: '2.5rem' }}
                            value={regConfirmPassword}
                            onChange={e => setRegConfirmPassword(e.target.value)}
                          />
                          <button 
                            type="button" 
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                            title={showConfirmPassword ? "Hide password" : "Show password"}
                          >
                            {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Section 2: Demographic & Domicile Details */}
                  <div className="swd-form-section" style={{ marginBottom: '1.5rem' }}>
                    <div className="swd-form-section-header">
                      <Building2 size={18} color="#2563eb" />
                      <div>
                        <h4 className="swd-form-section-title">2. Citizen Demographics & Welfare Profile</h4>
                        <p className="swd-form-section-desc">Used to accelerate scheme eligibility evaluation and taluk administration.</p>
                      </div>
                    </div>

                    <div className="form-grid-3">
                      <div className="form-group">
                        <label className="form-label">Date of Birth</label>
                        <input 
                          type="date" 
                          className="form-input" 
                          value={regDob}
                          onChange={e => setRegDob(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">Gender</label>
                        <select 
                          className="form-input form-select" 
                          value={regGender}
                          onChange={e => setRegGender(e.target.value)}
                        >
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Transgender">Transgender</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>

                      <div className="form-group">
                        <label className="form-label">District (Karnataka)</label>
                        <input 
                          type="text" 
                          className="form-input" 
                          value={regDistrict}
                          onChange={e => setRegDistrict(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">Taluk</label>
                        <input 
                          type="text" 
                          placeholder="e.g. Bengaluru North"
                          className="form-input" 
                          value={regTaluk}
                          onChange={e => setRegTaluk(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label className="form-label">PIN Code</label>
                        <input 
                          type="text" 
                          maxLength={6}
                          placeholder="e.g. 560001"
                          className="form-input" 
                          value={regPinCode}
                          onChange={e => setRegPinCode(e.target.value)}
                        />
                      </div>

                      <div className="form-group form-grid-full">
                        <label className="form-label">Residential Address</label>
                        <input 
                          type="text" 
                          placeholder="Door / Flat No, Street, Locality"
                          className="form-input" 
                          value={regAddress}
                          onChange={e => setRegAddress(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  <div style={{ background: '#f8fafc', padding: '0.85rem 1rem', borderRadius: '6px', border: '1px solid var(--line)', marginBottom: '1.5rem', fontSize: '0.78rem', color: '#64748b' }}>
                    <Shield size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'text-bottom', color: '#ea580c' }} />
                    <strong>Security Notice:</strong> Citizen accounts are secured with strong cryptographic password encryption. Official administrative roles cannot be created via public registration.
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ fontSize: '0.85rem', color: '#475569' }}>
                      Already have an account?{' '}
                      <button 
                        type="button" 
                        className="nav-link-btn" 
                        style={{ color: '#ea580c', fontWeight: 700, padding: 0, textDecoration: 'underline' }}
                        onClick={() => {
                          setCitizenAuthError('');
                          setActiveTab('sign-in-select');
                        }}
                      >
                        Sign In here
                      </button>
                    </div>

                    <div style={{ display: 'flex', gap: '0.75rem' }}>
                      <button 
                        type="button" 
                        className="btn-secondary" 
                        onClick={() => setActiveTab('swd-home')}
                        disabled={regLoading}
                      >
                        Cancel
                      </button>
                      <button 
                        type="submit" 
                        className="btn-orange" 
                        disabled={regLoading}
                      >
                        {regLoading ? 'Registering...' : 'Create Citizen Account'}
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            )}
          </div>
        )}


        {/* VIEW: SMART SCHEME FINDER */}
        {activeTab === 'smart-finder' && (
          <SmartSchemeFinderView
            userProfile={userProfile}
            token={token}
            onBackToHome={() => setActiveTab('swd-home')}
            onApplyScheme={(scheme) => {
              openSchemeApplication(scheme);
            }}
          />
        )}

        {/* VIEW: SCHEME CATALOGUE */}
        {activeTab === 'schemes' && (
          <div className="swd-view-container" style={{ width: '100%', maxWidth: '100%', boxSizing: 'border-box', overflowX: 'hidden' }}>
            <div className="swd-view-header" style={{ marginBottom: '1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.85rem' }}>
              <div style={{ flex: '1 1 280px', minWidth: 0 }}>
                <h2>Welfare Scheme Catalogue</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '0.2rem' }}>Explore government welfare schemes, departmental criteria, and Direct Benefit Transfer (DBT) entitlements.</p>
              </div>
              <button className="btn-orange" style={{ flexShrink: 0 }} onClick={() => setActiveTab('eligibility')}>
                Smart Eligibility Checker
              </button>
            </div>

            {/* COMPACT & VISUALLY ORGANIZED FILTER BAR */}
            <div style={{
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '10px',
              padding: '0.85rem 1rem',
              marginBottom: '1.25rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem',
              width: '100%',
              boxSizing: 'border-box'
            }}>
              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'center', width: '100%' }}>
                <div style={{ position: 'relative', flex: '1 1 240px', minWidth: '200px', maxWidth: '100%' }}>
                  <Search size={15} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }} />
                  <input 
                    type="text" 
                    placeholder="Search schemes by name, keyword or benefit..." 
                    className="filter-input" 
                    style={{ width: '100%', paddingLeft: '2.2rem', paddingRight: '0.75rem', height: '38px', fontSize: '0.82rem', boxSizing: 'border-box' }}
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value);
                      api.fetchSchemes({ 
                        category_id: selectedCategoryId, 
                        search: e.target.value,
                        beneficiary_category: selectedBeneficiaryFilter || undefined,
                        department: selectedDeptFilter || undefined
                      }).then(setSchemes);
                    }}
                  />
                </div>
                <select 
                  className="filter-select"
                  style={{ flex: '1 1 180px', minWidth: '150px', maxWidth: '100%', height: '38px', fontSize: '0.82rem', boxSizing: 'border-box' }}
                  value={selectedCategoryId || ''}
                  onChange={(e) => {
                    const val = e.target.value ? Number(e.target.value) : undefined;
                    setSelectedCategoryId(val);
                    api.fetchSchemes({ 
                      category_id: val, 
                      search: searchQuery,
                      beneficiary_category: selectedBeneficiaryFilter || undefined,
                      department: selectedDeptFilter || undefined
                    }).then(setSchemes);
                  }}
                >
                  <option value="">All Categories ({categories.length})</option>
                  {categories.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
                <select 
                  className="filter-select"
                  style={{ flex: '1 1 180px', minWidth: '150px', maxWidth: '100%', height: '38px', fontSize: '0.82rem', boxSizing: 'border-box' }}
                  value={selectedBeneficiaryFilter}
                  onChange={(e) => {
                    const val = e.target.value;
                    setSelectedBeneficiaryFilter(val);
                    api.fetchSchemes({ 
                      category_id: selectedCategoryId, 
                      search: searchQuery,
                      beneficiary_category: val || undefined,
                      department: selectedDeptFilter || undefined
                    }).then(setSchemes);
                  }}
                >
                  <option value="">All Beneficiary Groups ({beneficiaryOptions.length})</option>
                  {beneficiaryOptions.map((b, idx) => (
                    <option key={idx} value={b}>{b}</option>
                  ))}
                </select>
                {(selectedCategoryId || selectedBeneficiaryFilter || searchQuery) && (
                  <button 
                    className="btn-secondary" 
                    style={{ padding: '0.45rem 0.85rem', height: '38px', fontSize: '0.78rem', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '0.35rem', boxSizing: 'border-box' }}
                    onClick={() => {
                      setSelectedCategoryId(undefined);
                      setSelectedBeneficiaryFilter('');
                      setSearchQuery('');
                      api.fetchSchemes().then(setSchemes);
                    }}
                  >
                    <X size={14} /> Clear Filters
                  </button>
                )}
              </div>

              {/* ACTIVE FILTER & RESULT COUNT BAR */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', color: '#64748b', borderTop: '1px solid #e2e8f0', paddingTop: '0.5rem', flexWrap: 'wrap', gap: '0.4rem' }}>
                <span style={{ fontWeight: 600, color: 'var(--navy-dark)' }}>
                  Showing {schemes.length} of 35 Welfare Schemes
                </span>
                <span style={{ fontSize: '0.74rem', color: '#94a3b8' }}>
                  {schemes.length === 35 ? 'Displaying full catalogue' : 'Filtered results'}
                </span>
              </div>
            </div>

            {/* REDESIGNED COMPACT SCHEME CARDS */}
            <div className="schemes-list-grid" style={{ width: '100%', boxSizing: 'border-box' }}>
              {schemes.map(s => {
                const categoryBadge = (s.category && typeof s.category === 'object' && s.category.name)
                  ? s.category.name
                  : (s.benefit_type ? s.benefit_type.replace(/_/g, ' ') : null);

                // Department short name helper
                const deptMapping: Record<string, string> = {
                  "Directorate for the Empowerment of Differently Abled and Senior Citizens": "Disabilities & Senior Citizens",
                  "Karnataka State Women's Development Corporation (KSWDC)": "Women's Development (KSWDC)",
                  "Department of Electronics, IT, Bt and S&T, Government of Karnataka": "Electronics, IT & Bt",
                  "Skill Development, Entrepreneurship and Livelihood Department": "Skill Development & Livelihood",
                  "Food, Civil Supplies and Consumer Affairs Department": "Food & Civil Supplies",
                  "Revenue Department (Social Security and Pensions), Government of Karnataka": "Revenue (Social Security)"
                };
                let shortDept = s.department || "Social Welfare";
                if (deptMapping[shortDept]) {
                  shortDept = deptMapping[shortDept];
                } else {
                  shortDept = shortDept.replace(/, Government of Karnataka/g, '')
                    .replace(/Department of /g, '')
                    .replace(/ Department/g, '')
                    .trim();
                }

                // Clean 2-line max short description
                const shortDesc = s.description || s.benefit_summary || "Government welfare assistance provided under Karnataka State social security rules.";

                return (
                  <div key={s.id} className="scheme-item-card" style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', boxSizing: 'border-box' }}>
                    {/* Top Row: Department Label & Subtle Category Badge */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem', marginBottom: '0.5rem', width: '100%' }}>
                      <span style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: '1 1 auto', minWidth: 0 }} title={s.department}>
                        {shortDept}
                      </span>
                      {categoryBadge && (
                        <span style={{
                          fontSize: '0.66rem',
                          fontWeight: 600,
                          backgroundColor: '#f1f5f9',
                          color: 'var(--navy-dark)',
                          padding: '0.15rem 0.5rem',
                          borderRadius: '12px',
                          border: '1px solid #e2e8f0',
                          flexShrink: 0,
                          maxWidth: '55%',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }} title={categoryBadge}>
                          {categoryBadge}
                        </span>
                      )}
                    </div>

                    {/* Prominent Scheme Title */}
                    <h4 style={{
                      fontSize: '0.96rem',
                      fontWeight: 700,
                      lineHeight: 1.35,
                      color: 'var(--navy-dark)',
                      marginBottom: '0.45rem',
                      minHeight: '2.7em',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                      wordBreak: 'break-word'
                    }} title={s.name}>
                      {s.name}
                    </h4>

                    {/* Short Description (max 2 lines) */}
                    <p style={{
                      fontSize: '0.78rem',
                      color: '#64748b',
                      lineHeight: 1.45,
                      marginBottom: '0.9rem',
                      flexGrow: 1,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                      wordBreak: 'break-word'
                    }}>
                      {shortDesc}
                    </p>

                    {/* Single Primary Action: View Details */}
                    <div style={{ marginTop: 'auto', paddingTop: '0.5rem', borderTop: '1px solid #f1f5f9', width: '100%', boxSizing: 'border-box' }}>
                      <button 
                        className="btn-primary"
                        style={{
                          width: '100%',
                          padding: '0.5rem 0.75rem',
                          fontSize: '0.82rem',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '0.4rem',
                          borderRadius: '6px',
                          boxSizing: 'border-box'
                        }}
                        onClick={() => { setSelectedScheme(s); setActiveTab('scheme-detail'); }}
                      >
                        <span>View Details</span>
                        <ChevronRight size={14} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* VIEW: SCHEME DETAIL */}
        {activeTab === 'scheme-detail' && selectedScheme && (
          <div className="swd-view-container" style={{ width: '100%', maxWidth: '100%', boxSizing: 'border-box', overflowX: 'hidden' }}>
            <div className="swd-view-header" style={{ marginBottom: '1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
              <div style={{ flex: '1 1 300px', minWidth: 0 }}>
                <h2 style={{ wordBreak: 'break-word', fontSize: '1.25rem', lineHeight: 1.3 }}>{selectedScheme.name}</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b', marginTop: '0.25rem' }}>
                  Administering Authority: {selectedScheme.administering_authority || selectedScheme.department}
                </p>
              </div>
              <button 
                className="btn-secondary" 
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', padding: '0.45rem 0.85rem', whiteSpace: 'nowrap', flexShrink: 0 }}
                onClick={() => setActiveTab('schemes')}
              >
                <ArrowLeft size={14} /> Back to Scheme Catalogue
              </button>
            </div>

            {/* SCHEME DETAIL TWO-COLUMN WORKFLOW LAYOUT */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
              {/* Left Column: Comprehensive Scheme Information */}
              <div>
                {/* 1. Official Full Scheme Name & Department */}
                <div style={{ background: '#fff', border: '1px solid var(--line)', borderRadius: '8px', padding: '1.25rem', marginBottom: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span className="status-badge APPROVED" style={{ fontSize: '0.68rem', fontWeight: 600 }}>
                      {selectedScheme.status || 'ACTIVE'}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>
                      Code: {selectedScheme.scheme_code || 'KAR-SWD'}
                    </span>
                  </div>
                  <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.5rem' }}>
                    {selectedScheme.name}
                  </h3>
                  <p style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.5, margin: 0 }}>
                    <strong>Responsible Department:</strong> {selectedScheme.department}
                  </p>
                </div>

                {/* 2. Scheme Overview */}
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.45rem', fontSize: '0.95rem', fontWeight: 700 }}>
                  Scheme Overview & Objective
                </h4>
                <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                  {selectedScheme.description || 'Comprehensive state social welfare scheme assisting eligible citizens with direct financial or material support.'}
                </p>

                {/* 3. Benefits & Direct Benefit Transfer */}
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.45rem', fontSize: '0.95rem', fontWeight: 700 }}>
                  Benefits & Entitlements
                </h4>
                <div style={{ backgroundColor: '#ecfdf5', padding: '1rem', borderRadius: '8px', border: '1px solid #a7f3d0', marginBottom: '1.25rem' }}>
                  <p style={{ fontWeight: 600, color: '#065f46', fontSize: '0.88rem', margin: 0 }}>
                    {selectedScheme.benefit_summary || 'Standard government assistance and financial subsidies.'}
                  </p>
                  {selectedScheme.benefit_amount ? (
                    <p style={{ fontSize: '0.8rem', color: '#047857', marginTop: '0.35rem', margin: 0 }}>
                      Direct Benefit Transfer (DBT): ₹{Number(selectedScheme.benefit_amount).toLocaleString('en-IN')} (Directly disbursed to Aadhaar-seeded bank account)
                    </p>
                  ) : null}
                </div>

                {/* 4. Eligibility Criteria */}
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.45rem', fontSize: '0.95rem', fontWeight: 700 }}>
                  Eligibility Criteria
                </h4>
                <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '1.25rem' }}>
                  <p style={{ fontSize: '0.84rem', color: '#334155', lineHeight: 1.6, margin: 0 }}>
                    {selectedScheme.eligibility_summary || 'Standard departmental criteria apply for domicile, income ceiling, and targeted social category.'}
                  </p>
                </div>

                {/* 5. Required Documents */}
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.45rem', fontSize: '0.95rem', fontWeight: 700 }}>
                  Required Documents
                </h4>
                {selectedScheme.documents && selectedScheme.documents.length > 0 ? (
                  <ul style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.25rem', paddingLeft: '1.2rem' }}>
                    {selectedScheme.documents.map((doc: any, i: number) => (
                      <li key={i} style={{ marginBottom: '0.35rem' }}>
                        <strong style={{ color: 'var(--navy-dark)' }}>{doc.document_name || doc.document_code}</strong>: {doc.description || 'Mandatory official supporting document'}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                    Aadhaar card, revenue income certificate, caste certificate (if applicable), domicile proof, and bank passbook copy.
                  </p>
                )}

                {/* 6. Application Procedure */}
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.45rem', fontSize: '0.95rem', fontWeight: 700 }}>
                  Application Procedure & Instructions
                </h4>
                <p style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.6, margin: 0 }}>
                  {selectedScheme.application_instructions || 'Complete the online application form with verified supporting documents. Scrutiny and scrutiny status updates are accessible in real-time through your citizen portal.'}
                </p>
              </div>

              {/* Right Column: Key Official Details & Action Buttons */}
              <div>
                <div style={{ backgroundColor: '#f8fafc', padding: '1.25rem', borderRadius: '8px', border: '1px solid var(--line)', position: 'sticky', top: '1rem' }}>
                  <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem', fontSize: '0.95rem', fontWeight: 700 }}>
                    Quick Information
                  </h4>
                  <div style={{ fontSize: '0.8rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    <div><strong>Scheme Code:</strong> {selectedScheme.scheme_code || 'KAR-SWD'}</div>
                    <div><strong>Target Group:</strong> {selectedScheme.beneficiary_categories || 'General Karnataka Citizens'}</div>
                    <div><strong>Application Start:</strong> {selectedScheme.application_start_date || 'Open'}</div>
                    <div><strong>Application End:</strong> {selectedScheme.application_end_date || 'Open Throughout Year'}</div>
                    <div><strong>Verification:</strong> <span className="status-badge APPROVED">{selectedScheme.verification_status || 'VERIFIED'}</span></div>
                    {selectedScheme.official_url && (
                      <div>
                        <strong>Official Portal:</strong> <br />
                        <a href={selectedScheme.official_url} target="_blank" rel="noreferrer" style={{ color: 'var(--blue)', wordBreak: 'break-all' }}>
                          {selectedScheme.official_url} ↗
                        </a>
                      </div>
                    )}
                    <div style={{ marginTop: '0.5rem', padding: '0.6rem', background: '#fffbeb', border: '1px solid #fde68a', borderRadius: '6px', fontSize: '0.72rem', color: '#92400e', lineHeight: 1.4 }}>
                      Direct Benefit Transfer guarantees direct disbursement into beneficiary accounts upon approval.
                    </div>
                  </div>

                  {/* Primary Actions Moved Here */}
                  <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                    <button 
                      className="btn-primary" 
                      style={{
                        padding: '0.65rem 1rem',
                        fontSize: '0.85rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.45rem',
                        borderRadius: '6px'
                      }}
                      onClick={() => { setActiveTab('eligibility'); runEligibilityCheck(selectedScheme.id); }}
                    >
                      <CheckCircle2 size={16} /> Check Eligibility
                    </button>
                    <button 
                      className="btn-orange" 
                      style={{
                        padding: '0.65rem 1rem',
                        fontSize: '0.85rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.45rem',
                        borderRadius: '6px'
                      }}
                      onClick={() => selectedScheme && openSchemeApplication(selectedScheme)}
                    >
                      <FileText size={16} /> Apply Now
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW: ELIGIBILITY CHECKER */}
        {activeTab === 'eligibility' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Eligibility Assessment</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Rule-based verification against official department criteria.</p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>&larr; Back to Catalogue</button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.5rem' }}>
              {/* Profile Inputs */}
              <div style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem' }}>Enter Citizen Profile Attributes</h4>
                
                <div style={{ marginBottom: '0.85rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Target Scheme</label>
                  <select 
                    className="filter-select" 
                    style={{ width: '100%' }}
                    value={selectedScheme?.id || schemes[0]?.id || ''}
                    onChange={(e) => {
                      const sc = schemes.find(x => x.id === Number(e.target.value));
                      if (sc) setSelectedScheme(sc);
                    }}
                  >
                    {schemes.map(s => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>

                <div style={{ marginBottom: '0.85rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Annual Family Income (₹)</label>
                  <input type="number" className="filter-input" style={{ width: '100%' }} value={eligIncome} onChange={e => setEligIncome(Number(e.target.value))} />
                </div>

                <div style={{ marginBottom: '0.85rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Caste / Social Category</label>
                  <select className="filter-select" style={{ width: '100%' }} value={eligCaste} onChange={e => setEligCaste(e.target.value)}>
                    <option value="SC">Scheduled Caste (SC)</option>
                    <option value="ST">Scheduled Tribe (ST)</option>
                    <option value="Cat-1">Category-1</option>
                    <option value="2A">Category 2A</option>
                    <option value="2B">Category 2B</option>
                    <option value="3A">Category 3A</option>
                    <option value="3B">Category 3B</option>
                    <option value="General">General Merit</option>
                  </select>
                </div>

                <div style={{ marginBottom: '0.85rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>State of Permanent Domicile</label>
                  <select className="filter-select" style={{ width: '100%' }} value={eligState} onChange={e => setEligState(e.target.value)}>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Other">Other State</option>
                  </select>
                </div>

                <div style={{ marginBottom: '0.85rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Education Level</label>
                  <select className="filter-select" style={{ width: '100%' }} value={eligEducation} onChange={e => setEligEducation(e.target.value)}>
                    <option value="Post-Matric">Post-Matric (PUC / Diploma)</option>
                    <option value="Undergraduate">Undergraduate (Degree / BE / BCom)</option>
                    <option value="Postgraduate">Postgraduate</option>
                    <option value="School">SSLC / High School</option>
                  </select>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem', marginBottom: '0.85rem' }}>
                  <div>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Gender</label>
                    <select className="filter-select" style={{ width: '100%' }} value={eligGender} onChange={e => setEligGender(e.target.value)}>
                      <option value="Female">Female</option>
                      <option value="Male">Male</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Marital Status</label>
                    <select className="filter-select" style={{ width: '100%' }} value={eligMaritalStatus} onChange={e => setEligMaritalStatus(e.target.value)}>
                      <option value="Unmarried">Unmarried</option>
                      <option value="Married">Married</option>
                      <option value="Widowed">Widowed</option>
                      <option value="Divorced">Divorced</option>
                    </select>
                  </div>
                </div>

                {/* Scheme-Specific Dynamic Question Fields */}
                {selectedScheme?.name?.toLowerCase().includes('madilu') && (
                  <div style={{ marginBottom: '0.85rem', padding: '0.65rem', background: '#eff6ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#1e40af' }}>
                      Delivery in a Public Healthcare Institution? *
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%', borderColor: '#3b82f6' }} 
                      value={eligInstitutionalDelivery} 
                      onChange={e => setEligInstitutionalDelivery(e.target.value)}
                    >
                      <option value="">-- Please Select (Required) --</option>
                      <option value="true">Yes, delivered in Government Hospital / CHC</option>
                      <option value="false">No, home delivery or private facility</option>
                    </select>
                  </div>
                )}

                {selectedScheme?.name?.toLowerCase().includes('inter-caste') && (
                  <div style={{ marginBottom: '0.85rem', padding: '0.65rem', background: '#eff6ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#1e40af' }}>
                      Does either spouse belong to Scheduled Caste (SC)? *
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%', borderColor: '#3b82f6' }} 
                      value={eligSpouseSC} 
                      onChange={e => setEligSpouseSC(e.target.value)}
                    >
                      <option value="">-- Please Select (Required) --</option>
                      <option value="true">Yes, one spouse belongs to SC</option>
                      <option value="false">No, neither spouse belongs to SC</option>
                    </select>
                  </div>
                )}

                {selectedScheme?.name?.toLowerCase().includes('anna bhagya') && (
                  <div style={{ marginBottom: '0.85rem', padding: '0.65rem', background: '#eff6ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#1e40af' }}>
                      Ration Card Type *
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%', borderColor: '#3b82f6' }} 
                      value={eligRationCard} 
                      onChange={e => setEligRationCard(e.target.value)}
                    >
                      <option value="">-- Please Select (Required) --</option>
                      <option value="bpl">BPL (Below Poverty Line) Card</option>
                      <option value="antyodaya">Antyodaya Anna Yojana (AAY) Card</option>
                      <option value="apl">APL Card / No Ration Card</option>
                    </select>
                  </div>
                )}

                {selectedScheme?.name?.toLowerCase().includes('gruha jyothi') && (
                  <div style={{ marginBottom: '0.85rem', padding: '0.65rem', background: '#eff6ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#1e40af' }}>
                      Domestic Electricity Connection (Avg &lt;= 200 units/month)? *
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%', borderColor: '#3b82f6' }} 
                      value={eligDomesticMeter} 
                      onChange={e => setEligDomesticMeter(e.target.value)}
                    >
                      <option value="">-- Please Select (Required) --</option>
                      <option value="true">Yes, domestic meter with avg &lt;= 200 units</option>
                      <option value="false">No / Commercial / Over 200 units</option>
                    </select>
                  </div>
                )}

                {selectedScheme?.name?.toLowerCase().includes('yeshasvini') && (
                  <div style={{ marginBottom: '0.85rem', padding: '0.65rem', background: '#eff6ff', borderRadius: '6px', border: '1px solid #bfdbfe' }}>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem', color: '#1e40af' }}>
                      Member of Recognized Rural/Urban Cooperative Society (&gt;= 3 months)? *
                    </label>
                    <select 
                      className="filter-select" 
                      style={{ width: '100%', borderColor: '#3b82f6' }} 
                      value={eligCooperativeMember} 
                      onChange={e => setEligCooperativeMember(e.target.value)}
                    >
                      <option value="">-- Please Select (Required) --</option>
                      <option value="true">Yes, active cooperative society member</option>
                      <option value="false">No, not a cooperative society member</option>
                    </select>
                  </div>
                )}

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem', marginBottom: '1rem' }}>
                  <div>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Age</label>
                    <input type="number" className="filter-input" style={{ width: '100%' }} value={eligAge} onChange={e => setEligAge(Number(e.target.value))} />
                  </div>
                  <div>
                    <label style={{ fontSize: '0.78rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Disability (%)</label>
                    <input type="number" className="filter-input" style={{ width: '100%' }} value={eligDisability} onChange={e => setEligDisability(Number(e.target.value))} />
                  </div>
                </div>

                <button 
                  className="btn-orange" 
                  style={{ width: '100%' }}
                  onClick={() => selectedScheme && runEligibilityCheck(selectedScheme.id)}
                >
                  Check Eligibility
                </button>
              </div>

              {/* Assessment Results */}
              <div>
                {eligibilityResult ? (
                  <div>
                    <div style={{ 
                      padding: '1.25rem', 
                      borderRadius: '8px', 
                      marginBottom: '1.25rem',
                      backgroundColor: eligibilityResult.preliminary_status === 'LIKELY_ELIGIBLE' ? '#ecfdf5' : eligibilityResult.preliminary_status === 'NOT_ELIGIBLE' ? '#fef2f2' : '#fffbeb',
                      border: `1px solid ${eligibilityResult.preliminary_status === 'LIKELY_ELIGIBLE' ? '#a7f3d0' : eligibilityResult.preliminary_status === 'NOT_ELIGIBLE' ? '#fecaca' : '#fde68a'}`
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                        {eligibilityResult.preliminary_status === 'LIKELY_ELIGIBLE' && <CheckCircle size={20} color="#16a34a" />}
                        {eligibilityResult.preliminary_status === 'NOT_ELIGIBLE' && <X size={20} color="#dc2626" />}
                        {eligibilityResult.preliminary_status === 'INSUFFICIENT_INFORMATION' && <HelpCircle size={20} color="#d97706" />}
                        <h4 style={{ 
                          color: eligibilityResult.preliminary_status === 'LIKELY_ELIGIBLE' ? '#065f46' : eligibilityResult.preliminary_status === 'NOT_ELIGIBLE' ? '#991b1b' : '#92400e',
                          fontSize: '1.05rem'
                        }}>
                          Preliminary Result: {eligibilityResult.preliminary_status.replace('_', ' ')}
                        </h4>
                      </div>
                      <p style={{ fontSize: '0.85rem', color: '#334155', marginBottom: '0.6rem' }}>{eligibilityResult.summary_explanation}</p>
                      
                      {/* MANDATORY DISCLAIMER */}
                      <div style={{ fontSize: '0.75rem', fontStyle: 'italic', color: '#64748b', borderTop: '1px solid rgba(0,0,0,0.08)', paddingTop: '0.4rem' }}>
                        &bull; {eligibilityResult.disclaimer}
                      </div>
                    </div>

                    <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.6rem' }}>Rule Evaluation Breakdown</h4>
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>Criterion / Rule</th>
                          <th>Requirement</th>
                          <th>Your Value</th>
                          <th>Result</th>
                        </tr>
                      </thead>
                      <tbody>
                        {eligibilityResult.satisfied_criteria.map((c: any, i: number) => (
                          <tr key={`sat-${i}`}>
                            <td>{c.description}</td>
                            <td>{c.operator} {c.expected}</td>
                            <td>{String(c.actual_value)}</td>
                            <td><span className="status-badge APPROVED">SATISFIED</span></td>
                          </tr>
                        ))}
                        {eligibilityResult.unmet_criteria.map((c: any, i: number) => (
                          <tr key={`unmet-${i}`}>
                            <td>{c.description}</td>
                            <td>{c.operator} {c.expected}</td>
                            <td>{String(c.actual_value)}</td>
                            <td><span className="status-badge REJECTED">UNMET</span></td>
                          </tr>
                        ))}
                        {eligibilityResult.unknown_criteria.map((c: any, i: number) => (
                          <tr key={`unk-${i}`}>
                            <td>{c.description}</td>
                            <td>{c.operator} {c.expected}</td>
                            <td>Missing</td>
                            <td><span className="status-badge MORE_INFORMATION_REQUIRED">UNKNOWN</span></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>

                    {eligibilityResult.preliminary_status === 'LIKELY_ELIGIBLE' && (
                      <div style={{ marginTop: '1.25rem' }}>
                        <button className="btn-orange" onClick={() => selectedScheme && openSchemeApplication(selectedScheme)}>
                          Apply for Scheme &rarr;
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{ textAlign: 'center', padding: '3rem 1rem', color: '#94a3b8' }}>
                    <AlertCircle size={36} style={{ margin: '0 auto 0.75rem auto', color: '#cbd5e1' }} />
                    <p>Select a scheme on the left and click "Check Eligibility" to evaluate preliminary criteria.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* VIEW: APPLICATION FORM */}
        {activeTab === 'apply' && selectedScheme && (
          !token ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #bfdbfe', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(37, 99, 235, 0.08)' }}>
                <AlertCircle size={52} color="#2563eb" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#1e3a8a', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>Citizen Authentication Required</h3>
                <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Please sign in with your Citizen account to apply for <strong>{selectedScheme.name}</strong>. Your selected scheme will open immediately after signing in.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>Browse Schemes</button>
                  <button className="btn-orange" onClick={() => {
                    setCitizenLoginNotice('Please sign in with your Citizen account to apply for this scheme.');
                    try {
                      sessionStorage.setItem('swd_pending_scheme_apply', JSON.stringify(selectedScheme));
                    } catch {}
                    setPendingSchemeForApply(selectedScheme);
                    setActiveTab('sign-in-select');
                  }}>Citizen Sign In</button>
                </div>
              </div>
            </div>
          ) : userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '540px', margin: '0 auto', background: '#fff', border: '1px solid #fed7aa', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(234, 88, 12, 0.08)' }}>
                <Shield size={52} color="#ea580c" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#9a3412', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>Citizen Account Required for Scheme Applications</h3>
                <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Scheme applications can only be submitted through a Citizen account. As an administrative officer, you can review and scrutinize applications in your portal.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>Return to Catalogue</button>
                  <button className="btn-orange" onClick={() => {
                    if (userRole === 'PLATFORM_ADMIN' || userRole === 'SWD_ADMIN') {
                      setActiveTab('platform-admin');
                    } else {
                      setActiveTab('gov-welfare-admin');
                    }
                  }}>Open Admin Portal</button>
                </div>
              </div>
            </div>
          ) : (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Apply: {selectedScheme.name}</h2>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('schemes')}>&larr; Cancel</button>
            </div>

            {applySuccessMsg && (
              <div style={{ backgroundColor: '#ecfdf5', color: '#065f46', padding: '1rem', borderRadius: '8px', marginBottom: '1.25rem' }}>
                <CheckCircle size={18} style={{ display: 'inline', marginRight: '0.5rem' }} />
                {applySuccessMsg}
              </div>
            )}

            {/* EXTERNAL PORTAL & OFFICIAL ROUTING GUIDANCE BANNER */}
            {selectedScheme.official_url && (
              <div style={{
                backgroundColor: '#eff6ff',
                border: '1px solid #bfdbfe',
                borderRadius: '8px',
                padding: '1rem 1.25rem',
                marginBottom: '1.5rem',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.85rem'
              }}>
                <ExternalLink size={20} color="#1d4ed8" style={{ marginTop: '0.15rem', flexShrink: 0 }} />
                <div style={{ flex: 1, fontSize: '0.85rem', color: '#1e3a8a', lineHeight: 1.5 }}>
                  <div style={{ fontWeight: 700, marginBottom: '0.25rem' }}>
                    Official Government Channel & Assisted Submission
                  </div>
                  <div style={{ marginBottom: '0.5rem' }}>
                    {selectedScheme.application_instructions || 'This scheme is administered through designated Karnataka department portals or field offices. You may submit your verification dossier directly through NagrikSetu SWD or complete registration on the designated portal.'}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '0.8rem', color: '#4b5563' }}>Authorized Official Portal:</span>
                    <a
                      href={selectedScheme.official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: '#1d4ed8',
                        fontWeight: 600,
                        textDecoration: 'underline',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      {selectedScheme.official_url} ↗
                    </a>
                  </div>
                </div>
              </div>
            )}

            <form onSubmit={handleApplicationSubmit}>
              {/* SECTION 1: CITIZEN REGISTRY & DIRECT BENEFIT TRANSFER PROFILE */}
              <div className="swd-form-section">
                <div className="swd-form-section-header">
                  <User size={18} color="#ea580c" />
                  <div>
                    <h3 className="swd-form-section-title">1. Citizen Identity & Direct Benefit Transfer Profile</h3>
                    <p className="swd-form-section-desc">
                      Pre-filled from your authenticated citizen account. Used to verify Aadhaar seeding and disburse benefits.
                    </p>
                  </div>
                </div>

                <div className="form-grid-2">
                  <div className="form-group">
                    <label className="form-label">
                      <span>Applicant Full Name</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyFullName} 
                      onChange={e => setApplyFullName(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Mobile Phone Number</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="tel" 
                      required 
                      className="form-input" 
                      value={applyPhone} 
                      onChange={e => setApplyPhone(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Permanent Residence District</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyDistrict} 
                      onChange={e => setApplyDistrict(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Social Category</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <select 
                      className="form-input form-select" 
                      value={applyCategory} 
                      onChange={e => setApplyCategory(e.target.value)}
                    >
                      <option value="General">General</option>
                      <option value="SC">SC</option>
                      <option value="ST">ST</option>
                      <option value="OBC">OBC</option>
                      <option value="Category 1">Category 1</option>
                      <option value="Category 2A">Category 2A</option>
                      <option value="Category 2B">Category 2B</option>
                      <option value="Category 3A">Category 3A</option>
                      <option value="Category 3B">Category 3B</option>
                      <option value="Minority">Minority</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Aadhaar-Seeded Bank Account Number</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyBankAcc} 
                      onChange={e => setApplyBankAcc(e.target.value)} 
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">
                      <span>Bank IFSC Code</span>
                      <span className="form-label-required">*</span>
                    </label>
                    <input 
                      type="text" 
                      required 
                      className="form-input" 
                      value={applyIfsc} 
                      onChange={e => setApplyIfsc(e.target.value)} 
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 2: SCHEME-SPECIFIC REQUIREMENTS & DOSSIER */}
              <div className="swd-form-section" style={{ border: '1px solid #bfdbfe' }}>
                <div className="swd-form-section-header">
                  <Award size={18} color="#2563eb" />
                  <div>
                    <h3 className="swd-form-section-title" style={{ color: '#1e3a8a' }}>
                      2. {schemeDynamicForm ? schemeDynamicForm.title : `${selectedScheme.name} — Specific Requirements`}
                    </h3>
                    <p className="swd-form-section-desc">
                      Official statutory criteria and application details required by the administering department.
                    </p>
                  </div>
                </div>

                {loadingSchemeForm ? (
                  <div style={{ textAlign: 'center', padding: '2rem 1.5rem', color: '#64748b' }}>
                    Loading scheme-specific requirements and fields...
                  </div>
                ) : schemeDynamicForm && schemeDynamicForm.fields && schemeDynamicForm.fields.length > 0 ? (
                  <DynamicFormRenderer 
                    fields={schemeDynamicForm.fields}
                    formData={dynamicFormData}
                    onChange={(name, val) => setDynamicFormData(prev => ({ ...prev, [name]: val }))}
                  />
                ) : (
                  <div style={{ fontSize: '0.84rem', color: '#64748b', fontStyle: 'italic', padding: '1rem', background: '#f8fafc', borderRadius: '6px' }}>
                    Standard applicant verification applies for this welfare service.
                  </div>
                )}
              </div>

              {/* SECTION 3: STATUTORY DECLARATION & CONSENT */}
              <div className="swd-declaration-box">
                <label>
                  <input 
                    type="checkbox" 
                    required 
                    checked={applyConsent} 
                    onChange={e => setApplyConsent(e.target.checked)} 
                  />
                  <span>
                    <strong>Declaration & Consent:</strong> I hereby declare that the particulars provided above are authentic to the best of my knowledge and match my official revenue records. I authorize NagrikSetu SWD to authenticate my Aadhaar bank seeding for Direct Benefit Transfer.
                  </span>
                </label>
              </div>

              <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center" }}>
                <button 
                  type="submit" 
                  className="btn-orange" 
                  style={{ minWidth: '180px', height: '44px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}
                  disabled={loading || !applyConsent}
                >
                  {loading ? "Submitting Application..." : "Confirm & Submit Application"}
                </button>
                <button 
                  type="button" 
                  className="btn-secondary" 
                  style={{ height: '44px' }}
                  onClick={() => setActiveTab('schemes')}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
          )
        )}

        {/* VIEW: CITIZEN MY APPLICATIONS */}
        {activeTab === 'my-applications' && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Access Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Only authenticated <strong>Citizens</strong> can view their application portfolio.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>My Applications</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Track submitted applications, reviewer remarks, and DBT status.</p>
              </div>
              <button className="btn-secondary" onClick={() => loadMyApplications()}>
                <RefreshCw size={14} /> Refresh Portfolio
              </button>
            </div>

            {myApplications.length === 0 ? (
              <p style={{ color: '#94a3b8', textAlign: 'center', padding: '2rem' }}>No applications registered yet. Browse the scheme catalogue to apply.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Citizen Name</th>
                    <th>District</th>
                    <th>Status</th>
                    <th>Submitted On</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {myApplications.map(app => (
                    <tr key={app.id}>
                      <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{app.application_number}</td>
                      <td>{app.citizen_name}</td>
                      <td>{app.residence_district}</td>
                      <td><span className={`status-badge ${app.status}`}>{app.status.replace('_', ' ')}</span></td>
                      <td>{app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '0.35rem 0.65rem', fontWeight: 600 }}
                            onClick={() => { setSelectedApp(app); setActiveTab('tracking'); }}
                          >
                            Track Application &rarr;
                          </button>
                          <button 
                            className="btn-orange" 
                            style={{ padding: '0.35rem 0.65rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}
                            onClick={() => downloadReceiptPdf(app.id)}
                            title="Download Receipt"
                          >
                            <Download size={13} /> Receipt
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          )
        )}

        {/* VIEW: APPLICATION TRACKING & TIMELINE & DOCUMENT UPLOAD */}
        {activeTab === 'tracking' && selectedApp && (
          !token || userRole !== 'CITIZEN' ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Citizen Tracking Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  Detailed citizen dossier tracking is reserved for authenticated citizens. Administrative officers should use the scrutiny queue.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                </div>
              </div>
            </div>
          ) : (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Application Tracking: {selectedApp.application_number}</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Status: <span className={`status-badge ${selectedApp.status}`}>{selectedApp.status.replace('_', ' ')}</span></p>
              </div>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                <button 
                  className="btn-orange" 
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.85rem' }}
                  onClick={() => downloadReceiptPdf(selectedApp.id)}
                >
                  <Download size={15} /> Download Receipt
                </button>
                <button className="btn-secondary" onClick={() => setActiveTab('my-applications')}>&larr; Back to My Applications</button>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.5rem' }}>
              {/* Left Column: Details & Upload */}
              <div>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem' }}>Application Details</h4>
                <div style={{ fontSize: '0.82rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
                  <div><strong>Applicant:</strong> {selectedApp.citizen_name}</div>
                  <div><strong>Phone:</strong> {selectedApp.citizen_phone}</div>
                  <div><strong>Caste Category:</strong> {selectedApp.caste_category}</div>
                  <div><strong>Annual Income:</strong> ₹{Number(selectedApp.annual_income).toLocaleString('en-IN')}</div>
                  <div><strong>Bank Account:</strong> {selectedApp.bank_account_number ? selectedApp.bank_account_number.replace(/\d(?=\d{4})/g, "X") : 'Not provided'} ({selectedApp.bank_ifsc || 'N/A'})</div>
                  {selectedApp.admin_remarks && (
                    <div style={{ backgroundColor: '#fffbeb', padding: '0.75rem', borderRadius: '6px', border: '1px solid #fde68a', marginTop: '0.5rem' }}>
                      <strong>Official Reviewer Note:</strong> {selectedApp.admin_remarks}
                    </div>
                  )}
                </div>

                {/* Upload Documents (FR-SWD-015) */}
                <div style={{ background: '#f8fafc', padding: '1.15rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                  <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.65rem' }}>Upload Supporting Document</h4>
                  <p style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.85rem' }}>Max file size: 5 MB (PDF, JPG, PNG).</p>
                  
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.25rem' }}>Document Type</label>
                    <select className="filter-select" style={{ width: '100%' }} value={selectedDocCode} onChange={e => setSelectedDocCode(e.target.value)}>
                      <option value="INCOME_CERT">Revenue Income Certificate (RD Number)</option>
                      <option value="CASTE_CERT">Caste Certificate</option>
                      <option value="MARKSHEET">Marks Card / Passing Certificate</option>
                      <option value="BANK_PASSBOOK">Bank Passbook Copy</option>
                      <option value="SUPPLEMENTARY_DOC">Other Supporting Document</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: '0.85rem' }}>
                    <input 
                      type="file" 
                      accept=".pdf,.jpg,.jpeg,.png"
                      onChange={e => setSelectedDocFile(e.target.files ? e.target.files[0] : null)}
                      style={{ fontSize: '0.8rem' }}
                    />
                  </div>

                  <button className="btn-primary" style={{ width: '100%' }} onClick={handleDocumentUploadSubmit} disabled={!selectedDocFile || uploadLoading}>
                    {uploadLoading ? 'Uploading...' : 'Upload Supporting Document'}
                  </button>
                </div>
              </div>

              {/* Right Column: History Timeline */}
              <div>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem' }}>Application Progress & History</h4>
                {selectedApp.history && selectedApp.history.length > 0 ? (
                  <div style={{ borderLeft: '2px solid #e2e8f0', paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.15rem' }}>
                    {selectedApp.history.map((h: any, i: number) => (
                      <div key={i} style={{ position: 'relative' }}>
                        <div style={{ position: 'absolute', left: '-1.65rem', top: '0.2rem', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: 'var(--accent-saffron)' }} />
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{new Date(h.created_at).toLocaleString()} &bull; Actor: {h.changed_by}</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--navy-dark)' }}>{h.action_type}: {h.to_status}</div>
                        {h.remarks && <p style={{ fontSize: '0.8rem', color: '#475569', marginTop: '0.2rem' }}>{h.remarks}</p>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: '#94a3b8', fontSize: '0.82rem' }}>Application registered. Awaiting initial administrative verification.</p>
                )}

                {/* Uploaded Documents List */}
                <h4 style={{ color: 'var(--navy-dark)', marginTop: '2rem', marginBottom: '0.65rem' }}>Submitted Documents</h4>
                {selectedApp.documents && selectedApp.documents.length > 0 ? (
                  <ul style={{ listStyle: 'none' }}>
                    {selectedApp.documents.map((d: any) => (
                      <li key={d.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#334155', padding: '0.4rem 0', borderBottom: '1px solid #f1f5f9' }}>
                        <FileText size={14} color="#64748b" />
                        <span><strong>{d.document_code}</strong>: {d.file_name} ({Math.round(d.file_size_bytes/1024)} KB)</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>No documents uploaded yet.</p>
                )}
              </div>
            </div>
          </div>
          )
        )}

        {/* VIEW: ADMIN DASHBOARD */}
        {activeTab === 'admin-dashboard' && adminStats && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Admin Command Center</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Scheme metrics and application review workflows.</p>
              </div>
              <div style={{ display: 'flex', gap: '0.6rem' }}>
                <button className="btn-secondary" onClick={() => setActiveTab('admin-schemes')}>Schemes</button>
                <button className="btn-secondary" onClick={() => setActiveTab('admin-beneficiaries')}>Beneficiaries</button>
                <button className="btn-orange" onClick={() => setActiveTab('admin-applications')}>Review Queue</button>
              </div>
            </div>

            {/* Metrics Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Total Schemes</div>
                <div style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--navy-dark)' }}>{adminStats.total_schemes}</div>
                <div style={{ fontSize: '0.72rem', color: '#16a34a' }}>{adminStats.published_schemes} Published</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Total Applications</div>
                <div style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--navy-dark)' }}>{adminStats.total_applications}</div>
                <div style={{ fontSize: '0.72rem', color: '#d97706' }}>{adminStats.under_review_applications} Under Review</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Approved Beneficiaries</div>
                <div style={{ fontSize: '1.65rem', fontWeight: 800, color: '#15803d' }}>{adminStats.total_beneficiaries}</div>
                <div style={{ fontSize: '0.72rem', color: '#15803d' }}>DBT Mandates Active</div>
              </div>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Disbursed Grants</div>
                <div style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--accent-saffron)' }}>
                  ₹{(adminStats.total_sanctioned_amount / 100000).toFixed(2)}L
                </div>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Aadhaar Bridge Direct</div>
              </div>
            </div>

            {/* Recent Submissions Queue */}
            <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem' }}>Recent Applications Inflow</h4>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Application No</th>
                  <th>Citizen Name</th>
                  <th>Annual Income</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {adminStats.recent_applications.map((app: any) => (
                  <tr key={app.id}>
                    <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{app.application_number}</td>
                    <td>{app.citizen_name}</td>
                    <td>₹{Number(app.annual_income).toLocaleString('en-IN')}</td>
                    <td>{app.caste_category}</td>
                    <td><span className={`status-badge ${app.status}`}>{app.status}</span></td>
                    <td>
                      <button 
                        className="btn-secondary" 
                        style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }}
                        onClick={() => { setActionModalApp(app); }}
                      >
                        Review / Action
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* VIEW: ADMIN SCHEMES MANAGEMENT */}
        {activeTab === 'admin-schemes' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>SWD Scheme Management Portal</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Create, update, and manage social welfare scheme parameters.</p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('admin-dashboard')}>&larr; Back</button>
            </div>

            {createSchemeMsg && (
              <div style={{ backgroundColor: '#ecfdf5', color: '#065f46', padding: '0.85rem', borderRadius: '6px', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
                <CheckCircle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
                {createSchemeMsg}
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.5rem' }}>
              {/* Scheme Creation Form */}
              <div style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem' }}>Create New Welfare Scheme</h4>
                <form onSubmit={handleCreateScheme}>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Scheme Unique Code</label>
                    <input type="text" required placeholder="e.g. KAR-SWD-GRANT-2026" className="filter-input" style={{ width: '100%' }} value={newSchemeCode} onChange={e => setNewSchemeCode(e.target.value)} />
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Scheme Title / Name</label>
                    <input type="text" required placeholder="Full scheme name" className="filter-input" style={{ width: '100%' }} value={newSchemeName} onChange={e => setNewSchemeName(e.target.value)} />
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Welfare Category</label>
                    <select className="filter-select" style={{ width: '100%' }} value={newSchemeCatId} onChange={e => setNewSchemeCatId(Number(e.target.value))}>
                      {categories.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Benefit Ceiling Amount (₹)</label>
                    <input type="number" required className="filter-input" style={{ width: '100%' }} value={newSchemeAmount} onChange={e => setNewSchemeAmount(Number(e.target.value))} />
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Benefit Summary</label>
                    <input type="text" required placeholder="e.g. ₹15,000 one-time grant via DBT" className="filter-input" style={{ width: '100%' }} value={newSchemeBenefit} onChange={e => setNewSchemeBenefit(e.target.value)} />
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Description & Objectives</label>
                    <textarea required placeholder="Detailed objective of scheme..." className="filter-input" style={{ width: '100%', minHeight: '60px' }} value={newSchemeDesc} onChange={e => setNewSchemeDesc(e.target.value)} />
                  </div>
                  <div style={{ marginBottom: '0.65rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Eligibility Criteria Text</label>
                    <textarea required placeholder="Criteria requirements..." className="filter-input" style={{ width: '100%', minHeight: '50px' }} value={newSchemeElig} onChange={e => setNewSchemeElig(e.target.value)} />
                  </div>
                  <div style={{ marginBottom: '0.85rem' }}>
                    <label style={{ fontSize: '0.75rem', fontWeight: 600, display: 'block', marginBottom: '0.2rem' }}>Application Instructions</label>
                    <input type="text" required placeholder="Instructions for applicants..." className="filter-input" style={{ width: '100%' }} value={newSchemeInstructions} onChange={e => setNewSchemeInstructions(e.target.value)} />
                  </div>
                  <button type="submit" className="btn-orange" style={{ width: '100%' }}>
                    Save & Publish Scheme
                  </button>
                </form>
              </div>

              {/* Current Schemes List */}
              <div>
                <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.85rem' }}>Existing Schemes ({schemes.length})</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxHeight: '550px', overflowY: 'auto' }}>
                  {schemes.map(s => (
                    <div key={s.id} style={{ background: '#ffffff', padding: '1rem', borderRadius: '8px', border: '1px solid var(--line)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--blue)' }}>{s.scheme_code}</span>
                        <span className="status-badge APPROVED">{s.status}</span>
                      </div>
                      <h5 style={{ color: 'var(--navy-dark)', fontSize: '0.9rem', marginBottom: '0.25rem' }}>{s.name}</h5>
                      <p style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.4rem' }}>{s.benefit_summary}</p>
                      <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Window: {s.application_start_date} to {s.application_end_date}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW: ADMIN APPLICATIONS REVIEW */}
        {activeTab === 'admin-applications' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Application Review Queue</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Application scrutiny, document verification, and sanction orders.</p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('admin-dashboard')}>&larr; Back</button>
            </div>

            <div className="filter-bar">
              <select 
                className="filter-select"
                value={adminStatusFilter}
                onChange={e => {
                  setAdminStatusFilter(e.target.value);
                  api.fetchAdminApplications(token, { statusFilter: e.target.value || undefined }).then(setAdminApplications);
                }}
              >
                <option value="">All Statuses</option>
                <option value="SUBMITTED">SUBMITTED</option>
                <option value="UNDER_REVIEW">UNDER_REVIEW</option>
                <option value="MORE_INFORMATION_REQUIRED">MORE_INFORMATION_REQUIRED</option>
                <option value="APPROVED">APPROVED</option>
                <option value="REJECTED">REJECTED</option>
              </select>
            </div>

            <table className="data-table">
              <thead>
                <tr>
                  <th>Application No</th>
                  <th>Citizen Name</th>
                  <th>District</th>
                  <th>Income</th>
                  <th>Duplicate Flag</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {adminApplications.map(app => (
                  <tr key={app.id}>
                    <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{app.application_number}</td>
                    <td>{app.citizen_name}</td>
                    <td>{app.residence_district}</td>
                    <td>₹{Number(app.annual_income).toLocaleString('en-IN')}</td>
                    <td>
                      {app.is_duplicate_suspect ? (
                        <span style={{ color: '#b91c1c', fontWeight: 600, fontSize: '0.75rem' }}>Suspect Flagged</span>
                      ) : (
                        <span style={{ color: '#16a34a', fontSize: '0.75rem' }}>Clear</span>
                      )}
                    </td>
                    <td><span className={`status-badge ${app.status}`}>{app.status}</span></td>
                    <td>
                      <button 
                        className="btn-orange" 
                        style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }}
                        onClick={() => setActionModalApp(app)}
                      >
                        Scrutiny Action &rarr;
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* VIEW: ADMIN BENEFICIARY REGISTRY */}
        {activeTab === 'admin-beneficiaries' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Beneficiary Ledger</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Approved beneficiaries and DBT records.</p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button className="btn-orange" onClick={() => { setActiveTab('admin-dbt'); loadDbtData(); }}>
                  Go to Simulated DBT Console &rarr;
                </button>
                <button className="btn-secondary" onClick={() => setActiveTab('admin-dashboard')}>&larr; Back</button>
              </div>
            </div>

            <table className="data-table">
              <thead>
                <tr>
                  <th>Beneficiary Code</th>
                  <th>Citizen Name</th>
                  <th>Sanctioned Amount</th>
                  <th>Disbursement Mode</th>
                  <th>Status</th>
                  <th>Sanction Date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {beneficiaries.map(b => (
                  <tr key={b.id}>
                    <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{b.beneficiary_code}</td>
                    <td>{b.citizen_name}</td>
                    <td style={{ fontWeight: 700, color: '#15803d' }}>₹{Number(b.sanctioned_amount).toLocaleString('en-IN')}</td>
                    <td>{b.disbursement_mode}</td>
                    <td><span className="status-badge APPROVED">{b.status}</span></td>
                    <td>{new Date(b.sanctioned_at).toLocaleDateString()}</td>
                    <td>
                      <button 
                        className="btn-orange" 
                        style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}
                        onClick={() => { setActiveTab('admin-dbt'); loadDbtData(); }}
                      >
                        Process DBT &rarr;
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* VIEW: SIMULATED DIRECT BENEFIT TRANSFER (DBT) PAYMENT SYSTEM */}
        {activeTab === 'admin-dbt' && (
          <div className="swd-view-container">
            {/* DEMO NOTICE CALLOUT */}
            <div style={{
              backgroundColor: '#fffbeb',
              border: '2px solid #f59e0b',
              borderRadius: '8px',
              padding: '1rem 1.25rem',
              marginBottom: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.85rem'
            }}>
              <AlertTriangle size={24} color="#d97706" />
              <div>
                <strong style={{ color: '#92400e', fontSize: '0.9rem', display: 'block' }}>
                  DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED.
                </strong>
                <p style={{ color: '#b45309', fontSize: '0.78rem', margin: 0 }}>
                  This payment console simulates the Direct Benefit Transfer engine, generates transaction references, tests atomic batch disbursements, and records audit ledgers in MySQL without connecting to live banking networks.
                </p>
              </div>
            </div>

            <div className="swd-view-header">
              <div>
                <h2>DBT Console</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Simulated batch disbursements with duplicate payment checks.</p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <a 
                  href={api.getBatchDbtReportUrl()} 
                  target="_blank" 
                  rel="noreferrer"
                  className="btn-secondary"
                  style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
                >
                  <FileText size={14} /> Download CSV Report
                </a>
                <button className="btn-secondary" onClick={() => setActiveTab('admin-dashboard')}>&larr; Back</button>
              </div>
            </div>

            {/* DBT KPI DASHBOARD CARDS */}
            {dbtStats && (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gap: '1rem',
                marginBottom: '1.75rem'
              }}>
                <div className="admin-stat-card">
                  <div className="stat-label">Total Approved Beneficiaries</div>
                  <div className="stat-val">{dbtStats.total_approved_beneficiaries}</div>
                  <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>Eligible for DBT</div>
                </div>
                <div className="admin-stat-card">
                  <div className="stat-label">Simulated Disbursed (INR)</div>
                  <div className="stat-val" style={{ color: '#15803d' }}>
                    ₹{Number(dbtStats.total_simulated_disbursed).toLocaleString('en-IN')}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.25rem' }}>
                    Remaining Budget: ₹{Number(dbtStats.remaining_budget).toLocaleString('en-IN')}
                  </div>
                </div>
                <div className="admin-stat-card">
                  <div className="stat-label">Successful Transactions</div>
                  <div className="stat-val" style={{ color: '#16a34a' }}>{dbtStats.successful_transactions}</div>
                  <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '0.25rem' }}>Simulated Payment Successful</div>
                </div>
                <div className="admin-stat-card">
                  <div className="stat-label">Failed / Pending</div>
                  <div className="stat-val" style={{ color: '#dc2626' }}>
                    {dbtStats.failed_transactions} / {dbtStats.pending_transactions}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#dc2626', marginTop: '0.25rem' }}>Simulated Payment Failed / Pending</div>
                </div>
              </div>
            )}

            {dbtProcessingMsg && (
              <div style={{
                backgroundColor: '#eff6ff',
                border: '1px solid #bfdbfe',
                color: '#1e40af',
                padding: '0.75rem 1rem',
                borderRadius: '6px',
                fontSize: '0.82rem',
                marginBottom: '1.25rem',
                fontWeight: 600
              }}>
                {dbtProcessingMsg}
              </div>
            )}

            {/* BATCH ACTION BAR */}
            <div style={{
              background: '#ffffff',
              border: '1px solid var(--line)',
              borderRadius: '8px',
              padding: '1rem',
              marginBottom: '1.5rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--navy-dark)' }}>
                  Selected for Batch DBT: {selectedBeneficiaryIds.length} Beneficiaries
                </span>
                {selectedBeneficiaryIds.length > 0 && (
                  <span style={{ fontSize: '0.8rem', color: '#15803d', fontWeight: 600 }}>
                    (Total: ₹{beneficiaries
                      .filter(b => selectedBeneficiaryIds.includes(b.id))
                      .reduce((acc, curr) => acc + Number(curr.sanctioned_amount), 0)
                      .toLocaleString('en-IN')})
                  </span>
                )}
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  className="btn-secondary"
                  disabled={beneficiaries.length === 0}
                  onClick={() => {
                    if (selectedBeneficiaryIds.length === beneficiaries.length) {
                      setSelectedBeneficiaryIds([]);
                    } else {
                      setSelectedBeneficiaryIds(beneficiaries.map(b => b.id));
                    }
                  }}
                >
                  {selectedBeneficiaryIds.length === beneficiaries.length ? 'Deselect All' : 'Select All Beneficiaries'}
                </button>
                <button
                  className="btn-orange"
                  disabled={selectedBeneficiaryIds.length === 0}
                  onClick={() => setDbtBatchConfirmModal(true)}
                >
                  Process Selected Batch DBT &rarr;
                </button>
              </div>
            </div>

            {/* SECTION 1: BENEFICIARIES PENDING / AVAILABLE FOR SIMULATED DBT */}
            <div style={{ marginBottom: '2rem' }}>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '0.75rem', color: 'var(--navy-dark)' }}>
                1. Eligible Approved Beneficiary Roll
              </h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th style={{ width: '40px' }}>Select</th>
                    <th>Beneficiary Code</th>
                    <th>Citizen Name</th>
                    <th>Sanctioned Amount</th>
                    <th>Disbursement Mode</th>
                    <th>Payment Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {beneficiaries.map(b => {
                    const isSelected = selectedBeneficiaryIds.includes(b.id);
                    const tx = dbtTransactions.find(t => t.beneficiary_id === b.id && t.status === 'SUCCESSFUL');
                    return (
                      <tr key={b.id} style={{ backgroundColor: isSelected ? '#f0fdf4' : 'inherit' }}>
                        <td>
                          <input 
                            type="checkbox" 
                            checked={isSelected}
                            onChange={(e) => {
                              if (e.target.checked) setSelectedBeneficiaryIds([...selectedBeneficiaryIds, b.id]);
                              else setSelectedBeneficiaryIds(selectedBeneficiaryIds.filter(id => id !== b.id));
                            }}
                          />
                        </td>
                        <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{b.beneficiary_code}</td>
                        <td>{b.citizen_name}</td>
                        <td style={{ fontWeight: 700, color: '#15803d' }}>₹{Number(b.sanctioned_amount).toLocaleString('en-IN')}</td>
                        <td>SIMULATED_AADHAAR_BRIDGE</td>
                        <td>
                          {tx ? (
                            <span style={{ color: '#16a34a', fontWeight: 600, fontSize: '0.75rem' }}>
                              Simulated Payment Successful ({tx.transaction_reference})
                            </span>
                          ) : (
                            <span style={{ color: '#d97706', fontWeight: 600, fontSize: '0.75rem' }}>
                              Simulated Transaction Pending
                            </span>
                          )}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.35rem' }}>
                            <button
                              className="btn-orange"
                              style={{ padding: '0.25rem 0.55rem', fontSize: '0.72rem' }}
                              disabled={!!tx}
                              onClick={() => handleSingleSimulatedDbt(b.id, false)}
                              title={tx ? "Already Disbursed" : "Simulate Payment Success"}
                            >
                              {tx ? "Paid" : "Pay (Success)"}
                            </button>
                            <button
                              className="btn-secondary"
                              style={{ padding: '0.25rem 0.55rem', fontSize: '0.72rem', color: '#dc2626' }}
                              disabled={!!tx}
                              onClick={() => handleSingleSimulatedDbt(b.id, true)}
                              title="Simulate CBS Failure Test"
                            >
                              Simulate Fail
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* SECTION 2: SIMULATED TRANSACTION HISTORY */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--navy-dark)' }}>
                  2. Simulated DBT Transaction Ledger & Audit Trail
                </h3>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <select
                    className="filter-select"
                    value={dbtStatusFilter}
                    onChange={(e) => {
                      setDbtStatusFilter(e.target.value);
                      api.fetchDbtTransactions(token, { status_filter: e.target.value || undefined }).then(setDbtTransactions);
                    }}
                  >
                    <option value="">All Transaction States</option>
                    <option value="SUCCESSFUL">SUCCESSFUL</option>
                    <option value="FAILED">FAILED</option>
                    <option value="PENDING">PENDING</option>
                  </select>
                </div>
              </div>

              <table className="data-table">
                <thead>
                  <tr>
                    <th>Tx Reference</th>
                    <th>Batch ID</th>
                    <th>Beneficiary / Citizen</th>
                    <th>Scheme Name</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Processed Time (UTC)</th>
                    <th>Remarks</th>
                  </tr>
                </thead>
                <tbody>
                  {dbtTransactions.length === 0 ? (
                    <tr>
                      <td colSpan={8} style={{ textAlign: 'center', padding: '1.5rem', color: '#64748b' }}>
                        No simulated transactions recorded yet.
                      </td>
                    </tr>
                  ) : (
                    dbtTransactions.map(tx => (
                      <tr key={tx.id}>
                        <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{tx.transaction_reference}</td>
                        <td style={{ fontSize: '0.75rem', fontFamily: 'monospace' }}>{tx.batch_reference || 'INDIVIDUAL'}</td>
                        <td>{tx.beneficiary_name}</td>
                        <td>{tx.scheme_name}</td>
                        <td style={{ fontWeight: 700, color: tx.status === 'SUCCESSFUL' ? '#15803d' : '#dc2626' }}>
                          ₹{Number(tx.amount).toLocaleString('en-IN')}
                        </td>
                        <td>
                          {tx.status === 'SUCCESSFUL' ? (
                            <span className="status-badge APPROVED">Simulated Payment Successful</span>
                          ) : tx.status === 'FAILED' ? (
                            <span className="status-badge REJECTED">Simulated Payment Failed</span>
                          ) : (
                            <span className="status-badge UNDER_REVIEW">Simulated Transaction Pending</span>
                          )}
                        </td>
                        <td style={{ fontSize: '0.75rem' }}>{new Date(tx.processed_at).toLocaleString()}</td>
                        <td style={{ fontSize: '0.72rem', maxWidth: '200px' }}>{tx.remarks}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* VIEW: DISTRICT & TALUK WELFARE OFFICE LOCATOR / GPS WELFARE CENTRE LOCATOR */}
        {activeTab === 'office-locator' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Welfare Centres</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Find Social Welfare Department centres within 25 km.
                </p>
              </div>
              <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>
                &larr; Back
              </button>
            </div>

            {/* GPS Controls Banner */}
            <div style={{
              background: '#f8fafc',
              border: '1px solid var(--line)',
              borderRadius: '8px',
              padding: '1rem 1.25rem',
              marginBottom: '1.25rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <button 
                    className="btn-primary" 
                    style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', padding: '0.5rem 1rem' }}
                    onClick={() => handleFindNearbyOffices(25.0)}
                    disabled={officeLoading}
                  >
                    <MapPin size={15} /> Use My Current Location
                  </button>

                  <button 
                    className="btn-secondary" 
                    style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', padding: '0.5rem 0.85rem' }}
                    onClick={() => {
                      if (userGpsLocation) {
                        handleFindNearbyOffices(25.0);
                      } else {
                        loadOffices();
                      }
                    }}
                    disabled={officeLoading}
                  >
                    <RefreshCw size={14} className={officeLoading ? 'animate-spin' : ''} /> Refresh Search
                  </button>

                  <button 
                    className="btn-secondary" 
                    style={{ fontSize: '0.82rem', padding: '0.5rem 0.85rem' }}
                    onClick={() => {
                      setUserGpsLocation(null);
                      setIsGpsActive(false);
                      setGpsStatus('idle');
                      setGpsStatusMsg('');
                      setOfficeDistrictFilter('');
                      setOfficeTalukFilter('');
                      setOfficeSearchQuery('');
                      loadOffices();
                    }}
                  >
                    Clear Filters
                  </button>
                </div>

                <div style={{ fontSize: '0.78rem', color: '#64748b' }}>
                  Radius: <strong style={{ color: '#0f172a' }}>25 km</strong>
                </div>
              </div>

              {/* GPS Status Indicator */}
              {gpsStatusMsg && (
                <div style={{
                  padding: '0.55rem 0.85rem',
                  borderRadius: '6px',
                  fontSize: '0.78rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  backgroundColor: gpsStatus === 'locating' ? '#eff6ff' : gpsStatus === 'success' ? '#f0fdf4' : '#fef2f2',
                  color: gpsStatus === 'locating' ? '#1d4ed8' : gpsStatus === 'success' ? '#15803d' : '#b91c1c',
                  border: `1px solid ${gpsStatus === 'locating' ? '#bfdbfe' : gpsStatus === 'success' ? '#bbf7d0' : '#fecaca'}`
                }}>
                  {gpsStatus === 'locating' && <RefreshCw size={14} className="animate-spin" />}
                  {gpsStatus === 'success' && <CheckCircle size={14} />}
                  {(gpsStatus === 'denied' || gpsStatus === 'error') && <AlertCircle size={14} />}
                  <span>{gpsStatusMsg}</span>
                </div>
              )}
            </div>

            {/* Interactive OpenStreetMap Leaflet Map */}
            <WelfareMap 
              userLocation={userGpsLocation} 
              offices={offices} 
              selectedOfficeId={selectedOfficeId} 
              onSelectOffice={(off) => setSelectedOfficeId(off.id)}
            />

            {/* Manual Fallback Filter Bar */}
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.78rem', color: '#64748b', marginBottom: '0.4rem', fontWeight: 600 }}>
                Manual Filter / Alternative Search:
              </div>
              <div className="filter-bar" style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'center' }}>
                <input 
                  type="text" 
                  placeholder="Search office name, address, or service..." 
                  className="filter-input" 
                  style={{ flex: '1 1 240px' }}
                  value={officeSearchQuery}
                  onChange={(e) => {
                    setOfficeSearchQuery(e.target.value);
                    loadOffices(officeDistrictFilter || undefined, officeTalukFilter || undefined, e.target.value || undefined);
                  }}
                />
                <select 
                  className="filter-select"
                  style={{ flex: '0 1 200px' }}
                  value={officeDistrictFilter}
                  onChange={(e) => {
                    const dist = e.target.value;
                    setOfficeDistrictFilter(dist);
                    setOfficeTalukFilter('');
                    loadOffices(dist || undefined, undefined, officeSearchQuery || undefined);
                  }}
                >
                  <option value="">All Districts (Karnataka)</option>
                  <option value="Bengaluru Urban">Bengaluru Urban</option>
                  <option value="Mysuru">Mysuru</option>
                  <option value="Dharwad">Dharwad</option>
                  <option value="Belagavi">Belagavi</option>
                  <option value="Kalaburagi">Kalaburagi</option>
                  <option value="Dakshina Kannada">Dakshina Kannada</option>
                </select>

                {officeDistrictFilter && (
                  <select 
                    className="filter-select"
                    style={{ flex: '0 1 200px' }}
                    value={officeTalukFilter}
                    onChange={(e) => {
                      const tlk = e.target.value;
                      setOfficeTalukFilter(tlk);
                      loadOffices(officeDistrictFilter, tlk || undefined, officeSearchQuery || undefined);
                    }}
                  >
                    <option value="">All Taluks</option>
                    {officeDistrictFilter === 'Bengaluru Urban' && (
                      <>
                        <option value="Bengaluru North">Bengaluru North</option>
                        <option value="Bengaluru South">Bengaluru South</option>
                        <option value="Bengaluru East">Bengaluru East</option>
                      </>
                    )}
                    {officeDistrictFilter === 'Mysuru' && (
                      <>
                        <option value="Mysuru">Mysuru</option>
                        <option value="Nanjangud">Nanjangud</option>
                      </>
                    )}
                    {officeDistrictFilter === 'Dharwad' && (
                      <>
                        <option value="Dharwad">Dharwad</option>
                        <option value="Hubballi Urban">Hubballi Urban</option>
                      </>
                    )}
                    {officeDistrictFilter === 'Belagavi' && (
                      <option value="Belagavi">Belagavi</option>
                    )}
                    {officeDistrictFilter === 'Kalaburagi' && (
                      <option value="Kalaburagi">Kalaburagi</option>
                    )}
                    {officeDistrictFilter === 'Dakshina Kannada' && (
                      <option value="Mangaluru">Mangaluru</option>
                    )}
                  </select>
                )}
              </div>
            </div>

            {/* Office Cards Header & Count */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#334155' }}>
                {isGpsActive ? `Verified Welfare Centres within 25 km (${offices.length})` : `All Verified Welfare Centres (${offices.length})`}
              </span>
              {isGpsActive && (
                <span style={{ fontSize: '0.72rem', background: '#eff6ff', color: '#1d4ed8', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                  ⚡ Sorted Nearest to Farthest
                </span>
              )}
            </div>

            {/* Office Cards Grid */}
            {officeLoading ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>Searching verified Welfare Centres...</div>
            ) : offices.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <MapPin size={36} style={{ color: '#94a3b8', margin: '0 auto 0.75rem' }} />
                <h4 style={{ fontSize: '1.1rem', color: '#0f172a', marginBottom: '0.35rem' }}>No Welfare Centres Found</h4>
                <p style={{ color: '#64748b', fontSize: '0.85rem' }}>
                  No verified Welfare Centres were found within 25 km of your current location.
                </p>
                <div style={{ marginTop: '1rem' }}>
                  <button 
                    className="btn-secondary" 
                    onClick={() => {
                      setUserGpsLocation(null);
                      setIsGpsActive(false);
                      loadOffices();
                    }}
                  >
                    View All Karnataka Offices
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.25rem' }}>
                {offices.map(off => (
                  <div 
                    key={off.id} 
                    onClick={() => setSelectedOfficeId(off.id)}
                    style={{
                      background: '#ffffff',
                      border: selectedOfficeId === off.id ? '2px solid #ea580c' : '1px solid var(--line)',
                      borderRadius: '10px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      boxShadow: selectedOfficeId === off.id ? '0 4px 14px rgba(234,88,12,0.15)' : '0 2px 8px rgba(0,0,0,0.04)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                        <span style={{
                          backgroundColor: off.office_type.includes('District') ? '#eff6ff' : '#f0fdf4',
                          color: off.office_type.includes('District') ? '#1d4ed8' : '#15803d',
                          fontWeight: 700,
                          fontSize: '0.72rem',
                          padding: '0.2rem 0.5rem',
                          borderRadius: '4px'
                        }}>
                          {off.office_type}
                        </span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          {off.distance_km !== undefined && (
                            <span style={{
                              backgroundColor: '#fff7ed',
                              color: '#ea580c',
                              fontWeight: 700,
                              fontSize: '0.72rem',
                              padding: '0.2rem 0.5rem',
                              borderRadius: '4px',
                              border: '1px solid #ffedd5'
                            }}>
                              ⚡ {off.distance_km} km away
                            </span>
                          )}
                          <span style={{ fontSize: '0.72rem', color: '#16a34a', fontWeight: 600 }}>
                            &bull; {off.verification_status}
                          </span>
                        </div>
                      </div>

                      <h4 style={{ fontSize: '1.05rem', color: 'var(--navy-dark)', marginBottom: '0.4rem' }}>
                        {off.name}
                      </h4>
                      <p style={{ fontSize: '0.8rem', color: '#64748b', display: 'flex', alignItems: 'flex-start', gap: '0.4rem', marginBottom: '0.75rem' }}>
                        <MapPin size={15} style={{ flexShrink: 0, marginTop: '2px', color: '#ea580c' }} />
                        <span>{off.address}</span>
                      </p>

                      <div style={{ fontSize: '0.78rem', color: '#334155', display: 'flex', flexDirection: 'column', gap: '0.35rem', marginBottom: '0.85rem' }}>
                        <div><strong>Contact:</strong> {off.contact_number}</div>
                        <div><strong>Official Email:</strong> {off.email}</div>
                        <div><strong>Hours:</strong> {off.working_hours}</div>
                        <div style={{ marginTop: '0.25rem', background: '#f8fafc', padding: '0.4rem 0.6rem', borderRadius: '4px', fontSize: '0.75rem' }}>
                          <strong>Services:</strong> {off.services_offered}
                        </div>
                      </div>
                    </div>

                    <div style={{ borderTop: '1px solid var(--line)', paddingTop: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                        Taluk: <strong>{off.taluk}</strong> &bull; District: <strong>{off.district}</strong>
                      </span>
                      <button 
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedOfficeId(off.id);
                        }}
                        className="btn-secondary" 
                        style={{ fontSize: '0.75rem', padding: '0.3rem 0.65rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                      >
                        View On Map 🗺️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* VIEW: CONSOLIDATED CITIZEN GRIEVANCES (SUBMISSION & STATUS TRACKING) */}
        {(activeTab === 'grievance' || activeTab === 'my-grievances') && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Citizen Grievance Redressal Portal</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Submit complaints, track ticket investigation status, review official responses, and inspect resolution history.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <button 
                  className="btn-secondary" 
                  onClick={() => loadGrievances()} 
                  title="Refresh Tickets"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.82rem' }}
                >
                  <RefreshCw size={14} /> Refresh
                </button>
                <button 
                  className="btn-secondary" 
                  onClick={() => setActiveTab('citizen-dashboard')}
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.82rem' }}
                >
                  &larr; Dashboard
                </button>
              </div>
            </div>

            {/* Sub-tab Navigation Banner */}
            <div className="grievance-tabs-banner" style={{ display: 'flex', borderBottom: '2px solid var(--line)', marginBottom: '1.5rem', gap: '1rem', flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={() => { setGrievanceActiveSubTab('track'); loadGrievances(); }}
                style={{
                  padding: '0.65rem 1.25rem',
                  background: 'none',
                  border: 'none',
                  borderBottom: grievanceActiveSubTab === 'track' ? '3px solid #ea580c' : '3px solid transparent',
                  color: grievanceActiveSubTab === 'track' ? '#ea580c' : '#475569',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem'
                }}
              >
                <FileCheck size={16} /> My Grievances & Status Tracking ({grievances.length})
              </button>
              <button
                type="button"
                onClick={() => setGrievanceActiveSubTab('submit')}
                style={{
                  padding: '0.65rem 1.25rem',
                  background: 'none',
                  border: 'none',
                  borderBottom: grievanceActiveSubTab === 'submit' ? '3px solid #ea580c' : '3px solid transparent',
                  color: grievanceActiveSubTab === 'submit' ? '#ea580c' : '#475569',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem'
                }}
              >
                <MessageSquare size={16} /> Register New Complaint
              </button>
            </div>

            {/* TAB 1: MY SUBMITTED GRIEVANCES & STATUS TRACKING */}
            {grievanceActiveSubTab === 'track' && (
              <div>
                {grievances.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '3.5rem 1.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                    <p style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1rem' }}>No grievances submitted yet.</p>
                    <button className="btn-orange" onClick={() => setGrievanceActiveSubTab('submit')}>
                      Register Your First Complaint
                    </button>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {grievances.map(g => {
                      const formatDateReadable = (isoStr?: string) => {
                        if (!isoStr) return 'N/A';
                        try {
                          // Handle ISO string stored in UTC (e.g. 2026-11-24T17:10:01)
                          const utcIso = isoStr.endsWith('Z') || isoStr.includes('+') ? isoStr : isoStr + 'Z';
                          const d = new Date(utcIso);
                          const dateStr = d.toLocaleDateString('en-GB', {
                            timeZone: 'Asia/Kolkata',
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric'
                          });
                          const timeStr = d.toLocaleTimeString('en-US', {
                            timeZone: 'Asia/Kolkata',
                            hour: 'numeric',
                            minute: '2-digit',
                            hour12: true
                          });
                          return `${dateStr} • ${timeStr}`;
                        } catch {
                          return isoStr;
                        }
                      };

                      const getStatusBadge = (status: string) => {
                        const s = (status || '').toUpperCase();
                        let badgeClass = 'status-badge SUBMITTED';
                        let label = 'Submitted';

                        if (s === 'RESOLVED') {
                          badgeClass = 'status-badge RESOLVED';
                          label = 'Resolved';
                        } else if (s === 'UNDER_REVIEW' || s === 'UNDER_INVESTIGATION') {
                          badgeClass = 'status-badge UNDER_REVIEW';
                          label = 'Under Review';
                        } else if (s === 'AWAITING_INFORMATION' || s === 'MORE_INFORMATION_REQUIRED') {
                          badgeClass = 'status-badge AWAITING_INFORMATION';
                          label = 'Awaiting Information';
                        } else if (s === 'REJECTED') {
                          badgeClass = 'status-badge REJECTED';
                          label = 'Rejected';
                        }

                        return <span className={badgeClass}>{label}</span>;
                      };

                      return (
                        <div key={g.id} style={{ background: '#ffffff', padding: '1.25rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
                              <span style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: '0.88rem', color: 'var(--navy-dark)', background: '#f8fafc', padding: '3px 8px', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                                {g.grievance_number}
                              </span>
                              <span style={{ fontSize: '0.74rem', color: '#475569', background: '#f1f5f9', padding: '3px 8px', borderRadius: '4px', fontWeight: 600 }}>
                                {(g.category || 'GENERAL').replace(/_/g, ' ')}
                              </span>
                            </div>
                            <div>
                              {getStatusBadge(g.status)}
                            </div>
                          </div>
                          
                          <h4 style={{ fontSize: '0.98rem', fontWeight: 700, color: 'var(--navy-dark)', marginBottom: '0.45rem' }}>
                            {g.subject}
                          </h4>
                          <p style={{ fontSize: '0.84rem', color: '#334155', marginBottom: '0.85rem', lineHeight: 1.55 }}>
                            {g.description}
                          </p>
                          
                          {g.officer_response ? (
                            <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '0.85rem 1rem', borderRadius: '6px', fontSize: '0.83rem', color: '#166534', marginTop: '0.65rem' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontWeight: 700, marginBottom: '0.35rem' }}>
                                <CheckCircle size={15} style={{ color: '#16a34a' }} />
                                <span>Official Response &bull; Officer: {g.resolved_by || 'Jurisdictional Social Welfare Officer'}</span>
                              </div>
                              <p style={{ margin: 0, color: '#15803d', lineHeight: 1.5 }}>
                                {g.officer_response}
                              </p>
                            </div>
                          ) : (
                            <div style={{ fontSize: '0.78rem', color: '#64748b', background: '#f8fafc', border: '1px solid #e2e8f0', padding: '0.65rem 0.85rem', borderRadius: '6px', marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                              <Clock size={14} style={{ color: '#94a3b8' }} />
                              <span>Status: Assigned to Jurisdictional Social Welfare Officer. Official review in progress.</span>
                            </div>
                          )}

                          {/* Resolution history / Activity timeline */}
                          <div style={{ marginTop: '0.85rem', paddingTop: '0.75rem', borderTop: '1px solid #f1f5f9', fontSize: '0.75rem', color: '#64748b' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                                <Calendar size={13} style={{ color: '#94a3b8' }} />
                                <span><strong>Submitted:</strong> {formatDateReadable(g.created_at)}</span>
                              </div>
                              {g.updated_at && (
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                                  <Clock size={13} style={{ color: '#94a3b8' }} />
                                  <span><strong>Last Updated:</strong> {formatDateReadable(g.updated_at)}</span>
                                </div>
                              )}
                            </div>
                            {g.resolved_at && (
                              <div style={{ marginTop: '0.35rem', color: '#166534', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                                <Check size={13} style={{ color: '#16a34a' }} />
                                <span><strong>Resolution Recorded:</strong> {formatDateReadable(g.resolved_at)}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: REGISTER NEW GRIEVANCE */}
            {grievanceActiveSubTab === 'submit' && (
              <div style={{ maxWidth: '780px', margin: '0 auto' }}>
                <div style={{ background: '#ffffff', padding: '1.75rem', borderRadius: '8px', border: '1px solid var(--line)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                  <h4 style={{ color: 'var(--navy-dark)', marginBottom: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem' }}>
                    Register New Grievance Ticket
                  </h4>

                  {grievanceSuccessMsg && (
                    <div style={{ backgroundColor: '#ecfdf5', color: '#065f46', padding: '0.85rem 1rem', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <CheckCircle size={18} />
                        <span>{grievanceSuccessMsg}</span>
                      </div>
                      <button 
                        className="btn-orange" 
                        style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
                        onClick={() => { setGrievanceActiveSubTab('track'); loadGrievances(); }}
                      >
                        Track Ticket &rarr;
                      </button>
                    </div>
                  )}

                  {grievanceErrorMsg && (
                    <div style={{ backgroundColor: '#fee2e2', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '6px', fontSize: '0.82rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <AlertCircle size={16} />
                      <span>{grievanceErrorMsg}</span>
                    </div>
                  )}

                  <form onSubmit={async (e) => {
                    await handleGrievanceSubmit(e);
                    setGrievanceActiveSubTab('track');
                  }}>
                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Grievance Category <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <select 
                        className="filter-select" 
                        style={{ width: '100%' }}
                        value={grievanceCategory}
                        onChange={e => setGrievanceCategory(e.target.value)}
                      >
                        <option value="APPLICATION_DELAY">Application delay</option>
                        <option value="REJECTION_DISPUTE">Application rejection dispute</option>
                        <option value="DOCUMENT_ISSUE">Document-related issue</option>
                        <option value="SCHEME_INFO_ISSUE">Scheme information issue</option>
                        <option value="TECHNICAL_ISSUE">Technical issue</option>
                        <option value="OTHER">Other</option>
                      </select>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Subject / Brief Summary <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <input 
                        type="text" 
                        required 
                        placeholder="e.g. Verification delay for post-matric hostel application" 
                        className="filter-input" 
                        style={{ width: '100%' }}
                        value={grievanceSubject}
                        onChange={e => setGrievanceSubject(e.target.value)}
                      />
                    </div>

                    <div style={{ marginBottom: '1.25rem' }}>
                      <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                        Detailed Complaint / Explanation <span style={{ color: '#dc2626' }}>*</span>
                      </label>
                      <textarea 
                        required 
                        placeholder="Please specify scheme name, application reference number, and exact issue faced..." 
                        className="filter-input" 
                        style={{ width: '100%', minHeight: '120px' }}
                        value={grievanceDesc}
                        onChange={e => setGrievanceDesc(e.target.value)}
                      />
                    </div>

                    <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                      <button 
                        type="button" 
                        className="btn-secondary"
                        onClick={() => {
                          setGrievanceSubject('');
                          setGrievanceDesc('');
                          setGrievanceErrorMsg('');
                        }}
                      >
                        Clear
                      </button>
                      <button 
                        type="submit" 
                        className="btn-orange" 
                        style={{ padding: '0.65rem 1.5rem', fontWeight: 700 }}
                        disabled={grievanceLoading}
                      >
                        {grievanceLoading ? 'Submitting Grievance...' : 'Submit Grievance Ticket'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        {/* VIEW: CITIZEN NOTIFICATIONS (FULL VIEW) */}
        {activeTab === 'notifications-view' && (
          <div className="swd-view-container">
            <div className="swd-view-header">
              <div>
                <h2>Notifications</h2>
                <p style={{ fontSize: '0.82rem', color: '#64748b' }}>
                  Direct updates on application status changes, DBT disbursements, and official announcements.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                {notifications.some(n => !n.is_read) && (
                  <button className="btn-orange" onClick={handleMarkAllRead}>
                    Mark All as Read
                  </button>
                )}
                <button className="btn-secondary" onClick={() => loadNotifications()}>
                  <RefreshCw size={14} /> Refresh
                </button>
                <button className="btn-secondary" onClick={() => setActiveTab('citizen-dashboard')}>
                  &larr; Back to Dashboard
                </button>
              </div>
            </div>

            {notifications.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3.5rem 1.5rem', background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)' }}>
                <p style={{ color: '#64748b', fontSize: '0.9rem' }}>No notifications found.</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {notifications.map(n => (
                  <div 
                    key={n.id} 
                    style={{ 
                      background: '#ffffff', 
                      padding: '1.25rem', 
                      borderRadius: '8px', 
                      border: n.is_read ? '1px solid var(--line)' : '2px solid #ea580c',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                      cursor: 'pointer',
                      transition: 'border-color 0.15s'
                    }}
                    onClick={() => {
                      if (!n.is_read) handleMarkOneRead(n.id);
                      // Smart deep navigation based on notification context
                      const t = (n.title + ' ' + n.message).toLowerCase();
                      if (t.includes('application') || t.includes('swd-app-') || t.includes('sanction') || t.includes('document')) {
                        setActiveTab('my-applications');
                        loadMyApplications();
                      } else if (t.includes('grievance') || t.includes('complaint')) {
                        setActiveTab('grievance');
                        setGrievanceActiveSubTab('track');
                        loadGrievances();
                      } else if (t.includes('scheme') || t.includes('welfare')) {
                        setActiveTab('schemes');
                        api.fetchSchemes().then(setSchemes);
                      }
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {!n.is_read && (
                          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#ea580c' }} />
                        )}
                        <h4 style={{ fontSize: '0.95rem', color: 'var(--navy-dark)', margin: 0 }}>{n.title}</h4>
                        {!n.is_read && (
                          <span style={{ fontSize: '0.65rem', background: '#ffedd5', color: '#c2410c', padding: '1px 6px', borderRadius: '4px', fontWeight: 700 }}>NEW</span>
                        )}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                          {new Date(n.created_at).toLocaleString()}
                        </span>
                        <span style={{ fontSize: '0.72rem', color: '#ea580c', fontWeight: 600 }}>View Details &rarr;</span>
                      </div>
                    </div>
                    <p style={{ fontSize: '0.82rem', color: '#475569', margin: '0.4rem 0 0', lineHeight: 1.5 }}>
                      {n.message}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* VIEW: GOVERNMENT WELFARE ADMIN PORTAL (PORTAL 2) */}
        {activeTab === 'gov-welfare-admin' && (
          !token || !['GOVERNMENT_WELFARE_ADMIN', 'WELFARE_OFFICER', 'ADMINISTRATOR'].includes(userRole) ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #fee2e2', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(239, 68, 68, 0.08)' }}>
                <Shield size={52} color="#dc2626" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#991b1b', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Access Restricted</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  The <strong>Government Welfare Admin Dashboard</strong> is strictly restricted to authorized Welfare Officers and Department Administrators. Citizens and unauthenticated sessions cannot access this portal.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                  <button className="btn-orange" onClick={() => { setActiveTab('sign-in-select'); }}>
                    Welfare Officer Login
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <GovernmentWelfareAdminPortal 
              token={token}
              userName={userName}
              userRole={userRole}
              onLogout={handleLogout}
              onViewReceipt={(appId) => downloadReceiptPdf(appId)}
            />
          )
        )}

        {/* VIEW: PLATFORM ADMIN PORTAL (PORTAL 3) */}
        {activeTab === 'platform-admin' && (
          !token || !['PLATFORM_ADMIN', 'SWD_ADMIN'].includes(userRole) ? (
            <div className="swd-view-container" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
              <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: '1px solid #f3e8ff', borderRadius: '12px', padding: '2.5rem 2rem', boxShadow: '0 8px 24px rgba(124, 58, 237, 0.08)' }}>
                <Shield size={52} color="#7c3aed" style={{ marginBottom: '1rem' }} />
                <h3 style={{ color: '#5b21b6', marginBottom: '0.75rem', fontSize: '1.25rem', fontWeight: 700 }}>403 Forbidden — Platform Admin Only</h3>
                <p style={{ fontSize: '0.88rem', color: '#64748b', marginBottom: '1.75rem', lineHeight: 1.6 }}>
                  The <strong>Platform Admin Dashboard</strong> is exclusively reserved for Platform Super Administrators. Welfare Officers and Citizens are prohibited from accessing platform configuration, user access management, and system audit logs.
                </p>
                <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
                  <button className="btn-secondary" onClick={() => setActiveTab('swd-home')}>Return Home</button>
                  <button className="btn-primary" onClick={() => { setActiveTab('sign-in-select'); }}>
                    Platform Admin Login
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <PlatformAdminPortal 
              token={token}
              userName={userName}
              onLogout={handleLogout}
            />
          )
        )}

      </main>

      {/* ADMINISTRATIVE USER APPLY RESTRICTION MODAL */}
      {adminApplyNoticeModal && (
        <div className="modal-overlay" style={{ zIndex: 9999 }}>
          <div className="modal-content" style={{ maxWidth: '520px', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <div style={{
                width: '44px',
                height: '44px',
                borderRadius: '8px',
                backgroundColor: '#fff7ed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <Shield size={24} color="#ea580c" />
              </div>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--navy-dark)', margin: 0, fontWeight: 700 }}>
                  Citizen Application Only
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#ea580c', fontWeight: 600 }}>Administrative Access Restriction</span>
              </div>
            </div>

            <p style={{ fontSize: '0.86rem', color: '#475569', lineHeight: 1.6, marginBottom: '1.5rem' }}>
              {adminApplyNoticeModal}
            </p>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                className="btn-primary"
                style={{ padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
                onClick={() => setAdminApplyNoticeModal(null)}
              >
                Understood
              </button>
            </div>
          </div>
        </div>
      )}

      {/* BATCH DBT CONFIRMATION MODAL */}
      {dbtBatchConfirmModal && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '520px' }}>
            <div className="modal-header">
              <h3>Confirm Simulated Batch DBT Disbursement</h3>
              <button className="close-btn" onClick={() => setDbtBatchConfirmModal(false)}>&times;</button>
            </div>

            <div style={{
              backgroundColor: '#fffbeb',
              border: '1px solid #fcd34d',
              padding: '0.75rem',
              borderRadius: '6px',
              fontSize: '0.78rem',
              color: '#92400e',
              marginBottom: '1rem'
            }}>
              <strong>NOTICE:</strong> DEMO MODE — SIMULATED DBT TRANSACTIONS. NO REAL MONEY IS TRANSFERRED.
            </div>

            <div style={{ fontSize: '0.85rem', marginBottom: '1.25rem', lineHeight: 1.6 }}>
              <div><strong>Selected Beneficiaries:</strong> {selectedBeneficiaryIds.length} applicants</div>
              <div>
                <strong>Total Batch Disbursement:</strong>{' '}
                <span style={{ color: '#15803d', fontWeight: 700 }}>
                  ₹{beneficiaries
                    .filter(b => selectedBeneficiaryIds.includes(b.id))
                    .reduce((acc, curr) => acc + Number(curr.sanctioned_amount), 0)
                    .toLocaleString('en-IN')}
                </span>
              </div>
              <div><strong>Execution Mode:</strong> Simulated Aadhaar Payment Bridge (APB)</div>
            </div>

            <div style={{ marginBottom: '1.25rem', background: '#f8fafc', padding: '0.75rem', borderRadius: '6px' }}>
              <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input 
                  type="checkbox" 
                  checked={dbtSimulateFailureToggle} 
                  onChange={e => setDbtSimulateFailureToggle(e.target.checked)} 
                />
                <span>Simulate Partial Failure (Test unseeded Aadhaar CBS bank rejection for first applicant)</span>
              </label>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
              <button className="btn-secondary" onClick={() => setDbtBatchConfirmModal(false)}>Cancel</button>
              <button className="btn-orange" onClick={handleBatchDbtSubmit} disabled={loading}>
                {loading ? 'Processing Simulation...' : 'Confirm & Execute Batch DBT'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ADMIN ACTION MODAL */}
      {actionModalApp && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Scrutinize Application: {actionModalApp.application_number}</h3>
              <button className="close-btn" onClick={() => setActionModalApp(null)}>&times;</button>
            </div>

            <div style={{ fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              <div><strong>Applicant:</strong> {actionModalApp.citizen_name} ({actionModalApp.citizen_phone})</div>
              <div><strong>Declared Income:</strong> ₹{Number(actionModalApp.annual_income).toLocaleString('en-IN')}</div>
              <div><strong>Social Category:</strong> {actionModalApp.caste_category}</div>
              {actionModalApp.is_duplicate_suspect && (
                <div style={{ color: '#dc2626', marginTop: '0.4rem' }}>
                  <strong>Duplicate Warning:</strong> {actionModalApp.duplicate_reason}
                </div>
              )}
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Select Review Decision / Status</label>
              <select className="filter-select" style={{ width: '100%' }} value={actionType} onChange={e => setActionType(e.target.value as any)}>
                <option value="APPROVE">Approve & Issue Sanction Mandate (APPROVED)</option>
                <option value="REJECT">Reject Application (REJECTED)</option>
                <option value="REQUEST_INFO">Request Supplementary Information / Document (Awaiting Documents)</option>
                <option value="UNDER_REVIEW">Mark Application In Scrutiny (Under Review)</option>
                <option value="CORRECTION_REQUIRED">Mark Correction Required by Citizen</option>
              </select>
            </div>

            {actionType === 'APPROVE' && (
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Sanction Amount (₹)</label>
                <input type="number" className="filter-input" style={{ width: '100%' }} value={actionSanctionAmount} onChange={e => setActionSanctionAmount(Number(e.target.value))} />
              </div>
            )}

            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, display: 'block', marginBottom: '0.35rem' }}>Official Remarks / Justification</label>
              <textarea 
                className="filter-input" 
                style={{ width: '100%', minHeight: '80px' }} 
                required
                value={actionRemarks}
                onChange={e => setActionRemarks(e.target.value)}
                placeholder="Enter mandatory decision reason or specific documents requested..."
              />
            </div>

            <div style={{ display: 'flex', gap: '0.85rem', justifyContent: 'flex-end' }}>
              <button className="btn-secondary" onClick={() => setActionModalApp(null)}>Cancel</button>
              <button className="btn-orange" onClick={handleAdminActionSubmit} disabled={!actionRemarks.trim()}>
                Confirm Decision
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 5. DEDICATED SOCIAL WELFARE DEPARTMENT FOOTER */}
      <footer className="portal-footer">
        <div className="footer-content">
          <div>
            <h4 style={{ color: '#ffffff', fontSize: '1rem', marginBottom: '0.35rem' }}>
              NagrikSetu &bull; Social Welfare Department
            </h4>
            <p style={{ color: '#94a3b8', fontSize: '0.78rem', maxWidth: '600px' }}>
              Unified citizen welfare scheme discovery, eligibility assessment, and direct benefit transfer facilitation.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '2rem', fontSize: '0.78rem' }}>
            <div>
              <strong style={{ color: '#f8fafc' }}>Official References</strong>
              <div style={{ marginTop: '0.35rem' }}>
                <a 
                  href="https://ssp.postmatric.karnataka.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  style={{ color: '#93c5fd', textDecoration: 'none' }}
                >
                  State Scholarship Portal (SSP) &rarr;
                </a>
              </div>
              <div style={{ marginTop: '0.25rem' }}>
                <a 
                  href="https://dbtbharat.gov.in" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  style={{ color: '#93c5fd', textDecoration: 'none' }}
                >
                  Direct Benefit Transfer (DBT) &rarr;
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          &copy; 2026 NagrikSetu Platform
        </div>
      </footer>
    </div>
  );
}