import re

file_path = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\frontend\src\components\SmartSchemeFinderView.tsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # Top subtitle
    ("Intelligent Scheme Matching System", "Scheme Finder"),
    ("Find welfare schemes that may match your profile.", "Find schemes matching your profile."),
    ("&larr; Back to Portal", "&larr; Back"),
    # Prefill banner
    ("<strong>Profile Active:</strong> Logged in as <strong>{userProfile.full_name}</strong>. Available details have been prefilled. Answers changed here will <em>not</em> modify your permanent profile.",
     "Logged in as <strong>{userProfile.full_name}</strong>. Details prefilled. Changes here do not alter your profile."),
    ("<strong>Guest Search Mode:</strong> You can explore scheme recommendations freely. You may sign in or register whenever you decide to submit an official application.",
     "<strong>Guest Mode:</strong> Explore scheme matches freely. Sign in when you are ready to apply."),
    # Card heading
    ("Citizen Questionnaire", "Profile Details"),
    # Buttons
    ("Reset Fields", "Reset"),
    ("<Sparkles size={16} /> Find Matching Schemes", "<Sparkles size={16} /> Find Schemes"),
    ("Searching & Matching Schemes...", "Searching..."),
    # Disclaimer note
    ("* Questionnaire inputs are evaluated against deterministic eligibility rules in real-time.",
     "* Results are evaluated against scheme eligibility rules."),
    # Statutory Notice
    ("<strong>Department Notice & Guidance:</strong> {results.disclaimer}",
     "<strong>Notice:</strong> {results.disclaimer}"),
    # Results headings
    ("Matched Welfare Programs ({results.potential_match_count} Potential Matches &bull; {results.check_requirements_count} Check Requirements)",
     "Matched Schemes ({results.potential_match_count} Potential Matches, {results.check_requirements_count} Check Requirements)"),
    ("Sorted by relevance and eligibility score with most relevant schemes first.",
     "Sorted by eligibility score."),
    ("Search recommended schemes...", "Search schemes..."),
    # Empty state
    ("None of the published welfare schemes strictly matched the criteria for this filter. You can modify your questionnaire answers or clear filters to view other available opportunities.",
     "No schemes matched this filter. Adjust your questionnaire answers or filters."),
    ("Edit Questionnaire & Try Again", "Adjust Answers"),
    # Badges & Buttons
    ("Why this scheme is recommended:", "Why recommended:"),
    ("Some eligibility conditions could not be verified. Please review the scheme requirements before applying.",
     "Some conditions could not be verified. Review requirements before applying.")
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"NOT FOUND: {old[:40]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated SmartSchemeFinderView.tsx")
