const fs = require('fs');
const path = require('path');

const targetPath = path.join(__dirname, 'frontend', 'src', 'App.tsx');
const lines = fs.readFileSync(targetPath, 'utf8').split('\r\n');

// 1. Navigation Button: In top nav, insert Smart Scheme Finder button right next to Eligibility Checker
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("activeTab === 'eligibility'") && lines[i-1] && lines[i-1].includes("<button")) {
    // find closing </button>
    for (let k = i; k < i + 10; k++) {
      if (lines[k].includes("</button>")) {
        const smartFinderBtn = [
          "          <button",
          "            className={`nav-link-btn ${activeTab === 'smart-finder' ? 'active' : ''}`}",
          "            style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: activeTab === 'smart-finder' ? '#ea580c' : '#0f2444', fontWeight: 600 }}",
          "            onClick={openSmartFinder}",
          "          >",
          "            <Sparkles size={14} color=\"#ea580c\" /> Smart Scheme Finder",
          "          </button>"
        ];
        lines.splice(k + 1, 0, ...smartFinderBtn);
        console.log("Inserted Smart Scheme Finder button into top navigation after line", k);
        break;
      }
    }
    break;
  }
}

// 2. Hero Section: Add Smart Scheme Finder hero button right next to Browse Welfare Schemes
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('className="swd-hero-actions"')) {
    const heroFinderBtn = [
      "                <button",
      "                  className=\"hero-btn-orange\"",
      "                  style={{ backgroundColor: '#ea580c', borderColor: '#ea580c', display: 'inline-flex', alignItems: 'center', gap: '0.45rem' }}",
      "                  onClick={openSmartFinder}",
      "                >",
      "                  <Sparkles size={16} /> Smart Scheme Finder &rarr;",
      "                </button>"
    ];
    lines.splice(i + 1, 0, ...heroFinderBtn);
    console.log("Inserted Smart Scheme Finder button into hero actions after line", i);
    break;
  }
}

fs.writeFileSync(targetPath, lines.join('\r\n'), 'utf8');
console.log("SUCCESSFULLY_UPDATED_APP_NAV_AND_HERO");
