import zipfile, os, shutil, docx, xml.etree.ElementTree as ET

zip_path = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD.zip"
extract_dir = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD_VERIFY_TEMP"

if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir, ignore_errors=True)
os.makedirs(extract_dir, exist_ok=True)

print(f"=== 1. EXTRACTING FROM ZIP: {zip_path} ===")
with zipfile.ZipFile(zip_path, 'r') as zf:
    for name in zf.namelist():
        if "FINAL_REPORTS" in name and name.endswith(".docx"):
            zf.extract(name, extract_dir)
            print("  Extracted:", name)

docx_files = [
    os.path.join(extract_dir, "SWD_FINAL", "FINAL_REPORTS", "01_About_the_Service.docx"),
    os.path.join(extract_dir, "SWD_FINAL", "FINAL_REPORTS", "02_Functional_Requirements.docx"),
    os.path.join(extract_dir, "SWD_FINAL", "FINAL_REPORTS", "03_Problem_Statement_and_Business.docx")
]

target_term = "mukesh"
overall_found = 0

print("\n=== 2. DEEP SCANNING EXTRACTED DOCX FILES ===")

for file_path in docx_files:
    fname = os.path.basename(file_path)
    print(f"\nScanning: {fname}")
    doc = docx.Document(file_path)
    file_matches = []
    
    # A. Check Paragraphs (Body)
    for i, p in enumerate(doc.paragraphs):
        if target_term in p.text.lower():
            file_matches.append(f"Body Paragraph {i}: {p.text[:100]}")
            
    # B. Check Tables
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if target_term in cell.text.lower():
                    file_matches.append(f"Table {t_idx} [R{r_idx}, C{c_idx}]: {cell.text[:100]}")
                    
    # C. Check Headers & Footers across all sections
    for s_idx, section in enumerate(doc.sections):
        for hp in section.header.paragraphs:
            if target_term in hp.text.lower():
                file_matches.append(f"Section {s_idx} Header: {hp.text[:100]}")
        for fp in section.footer.paragraphs:
            if target_term in fp.text.lower():
                file_matches.append(f"Section {s_idx} Footer: {fp.text[:100]}")
        if section.different_first_page_header_footer:
            first_header = section.first_page_header
            for fhp in first_header.paragraphs:
                if target_term in fhp.text.lower():
                    file_matches.append(f"Section {s_idx} First Page Header: {fhp.text[:100]}")
            first_footer = section.first_page_footer
            for ffp in first_footer.paragraphs:
                if target_term in ffp.text.lower():
                    file_matches.append(f"Section {s_idx} First Page Footer: {ffp.text[:100]}")

    # D. Check Core Document Properties (Metadata)
    core = doc.core_properties
    meta_fields = {
        'title': core.title,
        'author': core.author,
        'subject': core.subject,
        'keywords': core.keywords,
        'comments': core.comments,
        'category': core.category,
        'last_modified_by': core.last_modified_by
    }
    for field, val in meta_fields.items():
        if val and target_term in str(val).lower():
            file_matches.append(f"Metadata {field}: {val}")
            
    # E. Check Raw Underlying XML (document.xml, core.xml, app.xml, header/footer XMLs)
    with zipfile.ZipFile(file_path, 'r') as inner_zip:
        for inner_name in inner_zip.namelist():
            if inner_name.endswith('.xml') or inner_name.endswith('.rels'):
                xml_content = inner_zip.read(inner_name).decode('utf-8', errors='ignore')
                if target_term in xml_content.lower():
                    file_matches.append(f"Underlying XML part ({inner_name}): matched")

    print(f"  Result for {fname}: {len(file_matches)} occurrence(s) found.")
    if file_matches:
        for m in file_matches:
            print("    -> [MATCH]:", m)
        overall_found += len(file_matches)
    else:
        print("    -> [VERIFIED CLEAN]: 0 occurrences across body, tables, headers, footers, metadata & raw XML.")

shutil.rmtree(extract_dir, ignore_errors=True)

print(f"\n=== OVERALL AUDIT SUMMARY ===")
print(f"Total occurrences of '{target_term}' across all extracted ZIP reports: {overall_found}")
assert overall_found == 0, "Failed: target term found in extracted zip!"
print("CONFIRMED: ALL THREE DOCX REPORTS IN THE FINAL ZIP ARE 100% CLEAN!")
