import React, { useState } from 'react';
import { 
  Sparkles, Search, Filter, CheckCircle2, AlertCircle, FileText, 
  Check, X, ChevronRight, User, MapPin, RefreshCw, Eye, ArrowRight,
  Shield, HelpCircle, AlertTriangle, Info, BookOpen
} from 'lucide-react';
import * as api from '../services/api';

interface SmartSchemeFinderProps {
  userProfile: api.UserProfileData | null;
  onApplyScheme: (scheme: api.Scheme) => void;
  onBackToHome: () => void;
  token?: string;
}

export const SmartSchemeFinderView: React.FC<SmartSchemeFinderProps> = ({
  userProfile,
  onApplyScheme,
  onBackToHome,
  token
}) => {
  // Questionnaire Inputs (Default initialized, prefilled from userProfile if available)
  const [age, setAge] = useState<number | ''>(() => {
    if (userProfile?.date_of_birth) {
      const birthYear = new Date(userProfile.date_of_birth).getFullYear();
      const curYear = new Date().getFullYear();
      if (curYear > birthYear) return curYear - birthYear;
    }
    return 24;
  });
  const [district, setDistrict] = useState<string>(userProfile?.district || 'Bengaluru Urban');
  const [taluk, setTaluk] = useState<string>(userProfile?.taluk || '');
  const [gender, setGender] = useState<string>(userProfile?.gender || 'Male');
  const [casteCategory, setCasteCategory] = useState<string>(userProfile?.caste_category || 'General');
  const [annualIncome, setAnnualIncome] = useState<number | ''>(
    userProfile?.annual_income !== undefined && userProfile?.annual_income !== null 
      ? Number(userProfile.annual_income) 
      : 180000
  );
  const [occupation, setOccupation] = useState<string>('Student');
  const [educationLevel, setEducationLevel] = useState<string>('Professional / Engineering / Medical');
  const [isFarmer, setIsFarmer] = useState<boolean>(false);
  const [isStudent, setIsStudent] = useState<boolean>(true);
  const [isWoman, setIsWoman] = useState<boolean>(
    userProfile?.gender ? ['female', 'woman'].includes(userProfile.gender.toLowerCase()) : false
  );
  const [disabilityStatus, setDisabilityStatus] = useState<string>(
    userProfile?.disability_percentage && Number(userProfile.disability_percentage) > 0 ? 'Yes' : 'No'
  );
  const [disabilityPercentage, setDisabilityPercentage] = useState<number | ''>(
    userProfile?.disability_percentage ? Number(userProfile.disability_percentage) : 0
  );
  const [maritalStatus, setMaritalStatus] = useState<string>('Unmarried');

  // UI & Search State
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [results, setResults] = useState<api.SmartFinderResponse | null>(null);
  const [hasSearched, setHasSearched] = useState<boolean>(false);
  const [categoryFilter, setCategoryFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedModalScheme, setSelectedModalScheme] = useState<api.SmartFinderMatchItem | null>(null);

  const districtsList = [
    "Bagalkote", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
    "Bidar", "Chamarajanagar", "Chikkaballapura", "Chikkamagaluru", "Chitradurga",
    "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
    "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
    "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir"
  ];

  const socialCategoriesList = [
    "General", "SC", "ST", "OBC", "Category 1", "Category 2A",
    "Category 2B", "Category 3A", "Category 3B", "Minority", "Other", "Prefer not to disclose"
  ];

  const occupationsList = [
    "Student", "Farmer", "Unemployed", "Employed",
    "Self-employed", "Construction worker", "Gig worker", "Other"
  ];

  const educationLevelsList = [
    "Below 10th", "10th / SSLC", "12th / PUC", "Diploma / ITI",
    "Undergraduate", "Postgraduate", "Professional / Engineering / Medical", "Other"
  ];

  // Quick occupation change handler to smartly update farmer/student checkboxes
  const handleOccupationChange = (newOcc: string) => {
    setOccupation(newOcc);
    if (newOcc === 'Student') {
      setIsStudent(true);
      setIsFarmer(false);
    } else if (newOcc === 'Farmer') {
      setIsFarmer(true);
      setIsStudent(false);
    } else {
      setIsStudent(false);
      setIsFarmer(false);
    }
  };

  const handleGenderChange = (newGender: string) => {
    setGender(newGender);
    if (['female', 'woman'].includes(newGender.toLowerCase())) {
      setIsWoman(true);
    } else {
      setIsWoman(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const q: api.SmartFinderQuestionnaire = {
        age: age !== '' ? Number(age) : undefined,
        district: district || undefined,
        taluk: taluk || undefined,
        gender: gender || undefined,
        caste_category: casteCategory || undefined,
        annual_income: annualIncome !== '' ? Number(annualIncome) : undefined,
        occupation: occupation || undefined,
        education_level: educationLevel || undefined,
        is_farmer: isFarmer,
        is_student: isStudent,
        is_woman: isWoman,
        disability_status: disabilityStatus,
        disability_percentage: disabilityPercentage !== '' ? Number(disabilityPercentage) : undefined,
        marital_status: maritalStatus || undefined
      };
      const res = await api.matchSmartSchemes(q);
      setResults(res);
      setHasSearched(true);
    } catch (err: any) {
      setError(err.message || 'Failed to match welfare schemes. Please review questionnaire answers.');
    } finally {
      setLoading(false);
    }
  };

  // Filter schemes based on Category tabs & Search query
  const filteredSchemes = (results?.results || []).filter(item => {
    // 1. Category Filter
    if (categoryFilter !== 'ALL') {
      const catLower = item.category_name.toLowerCase();
      if (categoryFilter === 'Education' && !catLower.includes('education') && !catLower.includes('scholarship')) return false;
      if (categoryFilter === 'Women & Children' && !catLower.includes('women') && !catLower.includes('child')) return false;
      if (categoryFilter === 'Agriculture' && !catLower.includes('agriculture') && !catLower.includes('rural')) return false;
      if (categoryFilter === 'Employment' && !catLower.includes('labour') && !catLower.includes('startup') && !catLower.includes('youth')) return false;
      if (categoryFilter === 'Social Security' && !catLower.includes('social security') && !catLower.includes('disability') && !catLower.includes('harmony')) return false;
      if (categoryFilter === 'Housing' && !catLower.includes('housing') && !item.scheme_name.toLowerCase().includes('nivas') && !item.scheme_name.toLowerCase().includes('vasati')) return false;
      if (categoryFilter === 'Health' && !catLower.includes('health') && !item.scheme_name.toLowerCase().includes('arogya') && !item.scheme_name.toLowerCase().includes('yeshasvini')) return false;
    }

    // 2. Search Query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchName = item.scheme_name.toLowerCase().includes(q);
      const matchDesc = item.description.toLowerCase().includes(q);
      const matchCat = item.category_name.toLowerCase().includes(q);
      const matchBenefit = item.benefit_summary.toLowerCase().includes(q);
      if (!matchName && !matchDesc && !matchCat && !matchBenefit) return false;
    }

    return true;
  });

  return (
    <div className="swd-view-container" style={{ maxWidth: '1120px', margin: '0 auto' }}>
      {/* Header */}
      <div className="swd-view-header">
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: '#ea580c', fontWeight: 700, fontSize: '0.82rem', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.25rem' }}>
            <Sparkles size={16} /> Scheme Finder
          </div>
          <h2 style={{ color: 'var(--navy-dark)', margin: 0 }}>Smart Scheme Finder</h2>
          <p style={{ fontSize: '0.88rem', color: '#64748b', marginTop: '0.2rem' }}>
            Find schemes matching your profile.
          </p>
        </div>
        <button className="btn-secondary" onClick={onBackToHome}>
          &larr; Back
        </button>
      </div>

      {/* Profile prefill info pill */}
      {token && userProfile ? (
        <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.82rem', color: '#166534', display: 'flex', alignItems: 'center' }}>
          <div>
            Logged in as <strong>{userProfile.full_name || 'Citizen'}</strong>. Questionnaire prefilled from your account without altering your saved profile.
          </div>
        </div>
      ) : (
        <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.82rem', color: '#1e40af', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Info size={16} />
          <span><strong>Guest Mode:</strong> Explore scheme matches freely. Sign in when you are ready to apply.</span>
        </div>
      )}

      {/* Main Questionnaire Card */}
      <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid var(--line)', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.03)', marginBottom: '1.75rem' }}>
        <h3 style={{ color: 'var(--navy-dark)', fontSize: '1rem', borderBottom: '1px solid var(--line)', paddingBottom: '0.5rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <User size={18} color="#ea580c" /> Profile Details
        </h3>

        {error && (
          <div style={{ background: '#fee2e2', border: '1px solid #fca5a5', color: '#991b1b', padding: '0.85rem 1rem', borderRadius: '6px', fontSize: '0.85rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Row 1: Demographics */}
          <div className="finder-grid-4">
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Age (Years)
              </label>
              <input 
                type="number" 
                min={0} 
                max={120} 
                className="filter-input" 
                style={{ width: '100%' }}
                value={age}
                onChange={e => setAge(e.target.value !== '' ? Number(e.target.value) : '')}
                placeholder="e.g. 25"
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                District (Karnataka)
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={district}
                onChange={e => setDistrict(e.target.value)}
              >
                {districtsList.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Taluk (Optional)
              </label>
              <input 
                type="text" 
                className="filter-input" 
                style={{ width: '100%' }}
                value={taluk}
                onChange={e => setTaluk(e.target.value)}
                placeholder="e.g. Bengaluru North"
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Gender
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={gender}
                onChange={e => handleGenderChange(e.target.value)}
              >
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Transgender">Transgender</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          {/* Row 2: Social Category & Economic */}
          <div className="finder-grid-3">
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Social Category
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={casteCategory}
                onChange={e => setCasteCategory(e.target.value)}
              >
                {socialCategoriesList.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Annual Family Income (INR)
              </label>
              <input 
                type="number" 
                min={0}
                className="filter-input" 
                style={{ width: '100%' }}
                value={annualIncome}
                onChange={e => setAnnualIncome(e.target.value !== '' ? Number(e.target.value) : '')}
                placeholder="e.g. 150000"
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Occupation
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={occupation}
                onChange={e => handleOccupationChange(e.target.value)}
              >
                {occupationsList.map(occ => (
                  <option key={occ} value={occ}>{occ}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Row 3: Education & Status Flags */}
          <div className="finder-grid-3">
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Education Level
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={educationLevel}
                onChange={e => setEducationLevel(e.target.value)}
              >
                {educationLevelsList.map(edu => (
                  <option key={edu} value={edu}>{edu}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Disability Status
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={disabilityStatus}
                onChange={e => {
                  setDisabilityStatus(e.target.value);
                  if (e.target.value === 'Yes' && (!disabilityPercentage || disabilityPercentage === 0)) {
                    setDisabilityPercentage(40);
                  } else if (e.target.value === 'No') {
                    setDisabilityPercentage(0);
                  }
                }}
              >
                <option value="No">No Disability</option>
                <option value="Yes">Persons with Disability (Divyangjan)</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--navy-dark)', marginBottom: '0.25rem' }}>
                Marital Status
              </label>
              <select 
                className="filter-input" 
                style={{ width: '100%' }}
                value={maritalStatus}
                onChange={e => setMaritalStatus(e.target.value)}
              >
                <option value="Unmarried">Unmarried</option>
                <option value="Married">Married</option>
                <option value="Widowed / Single Parent">Widowed / Single Parent</option>
                <option value="Separated / Divorced">Separated / Divorced</option>
              </select>
            </div>
          </div>

          {/* Checkboxes row for explicit clarity */}
          <div style={{ background: '#f8fafc', padding: '0.85rem 1rem', borderRadius: '6px', border: '1px solid var(--line)', marginBottom: '1.5rem', display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 600, color: '#334155' }}>
              <input 
                type="checkbox" 
                checked={isStudent} 
                onChange={e => setIsStudent(e.target.checked)} 
              />
              Are you currently a student?
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 600, color: '#334155' }}>
              <input 
                type="checkbox" 
                checked={isFarmer} 
                onChange={e => setIsFarmer(e.target.checked)} 
              />
              Are you an agricultural farmer / landholder?
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 600, color: '#334155' }}>
              <input 
                type="checkbox" 
                checked={isWoman} 
                onChange={e => setIsWoman(e.target.checked)} 
              />
              Are you a woman or girl child applicant?
            </label>
          </div>

          {/* Action Row */}
          <div className="finder-actions-row">
            <div style={{ fontSize: '0.78rem', color: '#64748b' }}>
              * Results are evaluated against scheme eligibility rules.
            </div>
            <div className="finder-button-group">
              <button 
                type="button" 
                className="btn-secondary"
                style={{ minWidth: '110px' }}
                onClick={() => {
                  if (userProfile) {
                    if (userProfile.date_of_birth) {
                      const birthYear = new Date(userProfile.date_of_birth).getFullYear();
                      const curYear = new Date().getFullYear();
                      if (curYear > birthYear) setAge(curYear - birthYear);
                    } else {
                      setAge(24);
                    }
                    setDistrict(userProfile.district || 'Bengaluru Urban');
                    setTaluk(userProfile.taluk || '');
                    setGender(userProfile.gender || 'Male');
                    setCasteCategory(userProfile.caste_category || 'General');
                    setAnnualIncome(
                      userProfile.annual_income !== undefined && userProfile.annual_income !== null 
                        ? Number(userProfile.annual_income) 
                        : 180000
                    );
                    setOccupation('Student');
                    setEducationLevel('Professional / Engineering / Medical');
                    setIsFarmer(false);
                    setIsStudent(true);
                    setIsWoman(
                      userProfile.gender ? ['female', 'woman'].includes(userProfile.gender.toLowerCase()) : false
                    );
                    setDisabilityStatus(
                      userProfile.disability_percentage && Number(userProfile.disability_percentage) > 0 ? 'Yes' : 'No'
                    );
                    setDisabilityPercentage(
                      userProfile.disability_percentage ? Number(userProfile.disability_percentage) : 0
                    );
                    setMaritalStatus('Unmarried');
                  } else {
                    setAge(28);
                    setDistrict('Bengaluru Urban');
                    setTaluk('Bengaluru South');
                    setGender('Male');
                    setCasteCategory('General');
                    setAnnualIncome(180000);
                    setOccupation('Student');
                    setEducationLevel('Professional / Engineering / Medical');
                    setIsFarmer(false);
                    setIsStudent(true);
                    setIsWoman(false);
                    setDisabilityStatus('No');
                    setDisabilityPercentage(0);
                    setMaritalStatus('Unmarried');
                  }
                  setResults(null);
                  setHasSearched(false);
                  setError('');
                }}
              >
                Reset
              </button>
              <button 
                type="submit" 
                className="btn-orange" 
                disabled={loading}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', minWidth: '180px', justifyContent: 'center' }}
              >
                {loading ? 'Searching...' : 'Find Schemes'}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* MATCH RESULTS SECTION */}
      {hasSearched && results && (
        <div style={{ marginTop: '2rem' }}>
          {/* Statutory Department Notice */}
          <div style={{ background: '#fffbeb', border: '1px solid #fef08a', padding: '0.85rem 1.15rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.82rem', color: '#854d0e', display: 'flex', alignItems: 'flex-start', gap: '0.6rem' }}>
            <AlertTriangle size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong>Notice:</strong> {results.disclaimer}
            </div>
          </div>

          {/* Results Summary & Filter Tabs */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
            <div>
              <h3 style={{ color: 'var(--navy-dark)', fontSize: '1.15rem', margin: 0 }}>
                Matched Schemes ({results.potential_match_count} Potential Matches, {results.check_requirements_count} Check Requirements)
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '0.15rem' }}>
                Sorted by eligibility score.
              </p>
            </div>

            {/* Search Input for Recommended Schemes */}
            <div style={{ position: 'relative', width: '280px' }}>
              <Search size={14} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
              <input 
                type="text" 
                placeholder="Search schemes..." 
                className="filter-input"
                style={{ width: '100%', paddingLeft: '2rem', fontSize: '0.8rem' }}
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          {/* Filter Categories Pill Bar */}
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', overflowX: 'auto', paddingBottom: '0.25rem' }}>
            {[
              { id: 'ALL', label: 'All Matches' },
              { id: 'Education', label: 'Education' },
              { id: 'Women & Children', label: 'Women & Children' },
              { id: 'Agriculture', label: 'Agriculture' },
              { id: 'Employment', label: 'Employment' },
              { id: 'Social Security', label: 'Social Security' },
              { id: 'Housing', label: 'Housing' },
              { id: 'Health', label: 'Health' }
            ].map(tab => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setCategoryFilter(tab.id)}
                style={{
                  padding: '0.4rem 0.85rem',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  borderRadius: '20px',
                  border: '1px solid',
                  cursor: 'pointer',
                  backgroundColor: categoryFilter === tab.id ? 'var(--navy-dark)' : '#ffffff',
                  color: categoryFilter === tab.id ? '#ffffff' : '#475569',
                  borderColor: categoryFilter === tab.id ? 'var(--navy-dark)' : '#cbd5e1',
                  transition: 'all 0.15s ease'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Empty State */}
          {filteredSchemes.length === 0 ? (
            <div style={{ background: '#ffffff', border: '1px solid var(--line)', borderRadius: '8px', padding: '3rem 1.5rem', textAlign: 'center' }}>
              <AlertCircle size={36} color="#94a3b8" style={{ margin: '0 auto 0.75rem auto' }} />
              <h4 style={{ color: 'var(--navy-dark)', marginBottom: '0.4rem' }}>No Matching Schemes Found</h4>
              <p style={{ color: '#64748b', fontSize: '0.85rem', maxWidth: '500px', margin: '0 auto 1.25rem auto' }}>
                No schemes matched this filter. Adjust your questionnaire answers or filters.
              </p>
              <button 
                className="btn-orange" 
                onClick={() => {
                  setCategoryFilter('ALL');
                  setSearchQuery('');
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
              >
                Adjust Answers
              </button>
            </div>
          ) : (
            /* Results Cards Grid */
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1.25rem' }}>
              {filteredSchemes.map(item => {
                const isPotentialMatch = item.match_status === 'Potential Match';
                const isCheckReq = item.match_status === 'Check Requirements';

                return (
                  <div 
                    key={item.scheme_id}
                    style={{
                      background: '#ffffff',
                      border: '1px solid',
                      borderColor: isPotentialMatch ? '#86efac' : isCheckReq ? '#fde047' : '#e2e8f0',
                      borderRadius: '8px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      boxShadow: isPotentialMatch ? '0 4px 12px rgba(22, 163, 74, 0.08)' : '0 2px 6px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div>
                      {/* Badge Row */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
                        <span style={{ fontSize: '0.72rem', background: '#f1f5f9', color: '#475569', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                          {item.category_name}
                        </span>

                        {/* Match Indicator */}
                        {isPotentialMatch && (
                          <span style={{ fontSize: '0.72rem', background: '#dcfce7', color: '#15803d', border: '1px solid #bbf7d0', padding: '0.2rem 0.55rem', borderRadius: '4px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                            <CheckCircle2 size={12} /> Potential Match
                          </span>
                        )}
                        {isCheckReq && (
                          <span style={{ fontSize: '0.72rem', background: '#fef9c3', color: '#854d0e', border: '1px solid #fef08a', padding: '0.2rem 0.55rem', borderRadius: '4px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                            <Info size={12} /> Check Requirements
                          </span>
                        )}
                        {!isPotentialMatch && !isCheckReq && (
                          <span style={{ fontSize: '0.72rem', background: '#f1f5f9', color: '#64748b', padding: '0.2rem 0.55rem', borderRadius: '4px', fontWeight: 600 }}>
                            Not Matched
                          </span>
                        )}
                      </div>

                      {/* Scheme Name */}
                      <h4 style={{ color: 'var(--navy-dark)', fontSize: '0.98rem', fontWeight: 700, lineHeight: 1.35, marginBottom: '0.5rem' }}>
                        {item.scheme_name}
                      </h4>

                      {/* Description */}
                      <p style={{ fontSize: '0.8rem', color: '#64748b', lineHeight: 1.5, marginBottom: '0.75rem', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                        {item.description}
                      </p>

                      {/* Verified Benefits */}
                      {item.benefit_summary && (
                        <div style={{ background: '#f8fafc', padding: '0.65rem 0.85rem', borderRadius: '6px', border: '1px solid var(--line)', marginBottom: '0.75rem', fontSize: '0.78rem', color: '#0f2444' }}>
                          <strong style={{ color: '#065f46' }}>Verified Benefit:</strong> {item.benefit_summary}
                        </div>
                      )}

                      {/* Why Matched Explanation Box */}
                      {item.why_matched.length > 0 && (
                        <div style={{ background: '#f0fdf4', border: '1px solid #dcfce7', borderRadius: '6px', padding: '0.65rem 0.85rem', marginBottom: '0.75rem' }}>
                          <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#166534', marginBottom: '0.25rem' }}>
                            Why recommended:
                          </div>
                          <ul style={{ margin: 0, paddingLeft: '1.1rem', fontSize: '0.74rem', color: '#15803d', lineHeight: 1.4 }}>
                            {item.why_matched.map((r, idx) => (
                              <li key={idx}>{r}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Missing or Unverified conditions warning */}
                      {item.missing_requirements.length > 0 && (
                        <div style={{ background: '#fffbeb', border: '1px solid #fef3c7', borderRadius: '6px', padding: '0.65rem 0.85rem', marginBottom: '0.75rem' }}>
                          <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#92400e', marginBottom: '0.2rem' }}>
                            Important Notice:
                          </div>
                          <p style={{ margin: 0, fontSize: '0.74rem', color: '#b45309', lineHeight: 1.35 }}>
                            Some conditions could not be verified. Review requirements before applying.
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Action Buttons Row */}
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', borderTop: '1px solid var(--line)', paddingTop: '0.75rem' }}>
                      <button 
                        type="button" 
                        className="btn-secondary" 
                        style={{ flex: 1, padding: '0.45rem', fontSize: '0.78rem', justifyContent: 'center' }}
                        onClick={() => setSelectedModalScheme(item)}
                      >
                        <Eye size={13} style={{ marginRight: '4px' }} /> View Details
                      </button>

                      {item.has_application_form ? (
                        <button 
                          type="button" 
                          className="btn-orange" 
                          style={{ flex: 1, padding: '0.45rem', fontSize: '0.78rem', justifyContent: 'center' }}
                          onClick={() => {
                            // Convert item to Scheme structure and launch Apply workflow
                            onApplyScheme({
                              id: item.scheme_id,
                              scheme_code: item.scheme_code,
                              name: item.scheme_name,
                              category_id: item.category_id,
                              administering_authority: 'Social Welfare Department',
                              description: item.description,
                              benefit_summary: item.benefit_summary,
                              benefit_amount: item.benefit_amount,
                              eligibility_summary: item.eligibility_summary,
                              application_instructions: 'Complete official application with valid documents.',
                              department: 'Social Welfare Department, Government of Karnataka',
                              benefit_type: 'DIRECT_BENEFIT_TRANSFER',
                              application_start_date: '2026-01-01',
                              application_end_date: '2026-12-31',
                              status: item.status
                            });
                          }}
                        >
                          Apply Now &rarr;
                        </button>
                      ) : (
                        <button 
                          type="button" 
                          disabled 
                          className="btn-secondary" 
                          style={{ flex: 1, padding: '0.45rem', fontSize: '0.74rem', color: '#94a3b8', justifyContent: 'center', cursor: 'not-allowed' }}
                          title="Online application is not currently available for this scheme."
                        >
                          Offline / Walk-in
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* SCHEME DETAILS MODAL */}
      {selectedModalScheme && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(15, 23, 42, 0.6)', backdropFilter: 'blur(3px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: '1rem' }}>
          <div style={{ backgroundColor: '#ffffff', borderRadius: '10px', maxWidth: '640px', width: '100%', maxHeight: '90vh', overflowY: 'auto', padding: '1.75rem', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div>
                <span style={{ fontSize: '0.72rem', background: '#f1f5f9', color: '#475569', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                  {selectedModalScheme.category_name}
                </span>
                <h3 style={{ color: 'var(--navy-dark)', fontSize: '1.15rem', marginTop: '0.4rem', marginBottom: '0.2rem' }}>
                  {selectedModalScheme.scheme_name}
                </h3>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  Scheme Code: <strong>{selectedModalScheme.scheme_code}</strong> &bull; Verification Status: <strong>{selectedModalScheme.verification_status}</strong>
                </div>
              </div>
              <button 
                onClick={() => setSelectedModalScheme(null)}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#94a3b8' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <h5 style={{ fontSize: '0.82rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.35rem' }}>Description</h5>
              <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.5, margin: 0 }}>
                {selectedModalScheme.description}
              </p>
            </div>

            <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '0.85rem', borderRadius: '6px', marginBottom: '1.25rem' }}>
              <h5 style={{ fontSize: '0.82rem', color: '#166534', fontWeight: 700, marginBottom: '0.3rem' }}>Benefit Details</h5>
              <p style={{ fontSize: '0.84rem', color: '#15803d', margin: 0 }}>
                {selectedModalScheme.benefit_summary}
              </p>
              {selectedModalScheme.benefit_amount ? (
                <div style={{ fontSize: '0.78rem', color: '#047857', fontWeight: 600, marginTop: '0.35rem' }}>
                  Maximum Sanction Cap: ₹{Number(selectedModalScheme.benefit_amount).toLocaleString('en-IN')} (Direct Benefit Transfer)
                </div>
              ) : null}
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <h5 style={{ fontSize: '0.82rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.35rem' }}>Eligibility Criteria</h5>
              <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.5, margin: 0 }}>
                {selectedModalScheme.eligibility_summary}
              </p>
            </div>

            {selectedModalScheme.documents_required.length > 0 && (
              <div style={{ marginBottom: '1.25rem' }}>
                <h5 style={{ fontSize: '0.82rem', color: 'var(--navy-dark)', fontWeight: 700, marginBottom: '0.35rem' }}>Required Supporting Documents</h5>
                <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.82rem', color: '#475569', lineHeight: 1.5 }}>
                  {selectedModalScheme.documents_required.map((doc, idx) => (
                    <li key={idx}>{doc}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Official Portal Link (only if verified) */}
            <div style={{ marginBottom: '1.5rem', fontSize: '0.8rem', color: '#64748b' }}>
              <strong>Official Portal Link:</strong>{' '}
              {selectedModalScheme.official_url ? (
                <a href={selectedModalScheme.official_url} target="_blank" rel="noopener noreferrer" style={{ color: '#ea580c', textDecoration: 'underline' }}>
                  {selectedModalScheme.official_url}
                </a>
              ) : (
                <span style={{ color: '#94a3b8' }}>Official link is currently unavailable.</span>
              )}
            </div>

            {/* Modal Actions */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', borderTop: '1px solid var(--line)', paddingTop: '1rem' }}>
              <button className="btn-secondary" onClick={() => setSelectedModalScheme(null)}>
                Close
              </button>
              {selectedModalScheme.has_application_form ? (
                <button 
                  className="btn-orange" 
                  onClick={() => {
                    const item = selectedModalScheme;
                    setSelectedModalScheme(null);
                    onApplyScheme({
                      id: item.scheme_id,
                      scheme_code: item.scheme_code,
                      name: item.scheme_name,
                      category_id: item.category_id,
                      administering_authority: 'Social Welfare Department',
                      description: item.description,
                      benefit_summary: item.benefit_summary,
                      benefit_amount: item.benefit_amount,
                      eligibility_summary: item.eligibility_summary,
                      application_instructions: 'Complete official application with valid documents.',
                      department: 'Social Welfare Department, Government of Karnataka',
                      benefit_type: 'DIRECT_BENEFIT_TRANSFER',
                      application_start_date: '2026-01-01',
                      application_end_date: '2026-12-31',
                      status: item.status
                    });
                  }}
                >
                  Apply Now &rarr;
                </button>
              ) : (
                <div style={{ fontSize: '0.78rem', color: '#94a3b8', alignSelf: 'center' }}>
                  Online application is not currently available for this scheme.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
