import os
import zipfile
import tempfile
import shutil

SOURCE_DIR = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final"
OUTPUT_ZIP = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_SAD.zip"

# Directories and extensions to ignore
IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.pytest_cache', 
    'dist', '.venv', 'venv', 'env', '.idea', '.vscode'
}
IGNORE_EXTS = {'.pyc', '.pyo', '.pyd', '.DS_Store', '.log', '.zip'}
IGNORE_FILES = {'PRIVATE_DEMO_CREDENTIALS.txt', 'verified_pre_audit_backup.sql', '.env'}

def package_project():
    print(f"Packaging {SOURCE_DIR} into {OUTPUT_ZIP}...")
    
    file_count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SOURCE_DIR):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if any(file.endswith(ext) for ext in IGNORE_EXTS) or file in IGNORE_FILES:
                    continue
                
                full_path = os.path.join(root, file)
                # Store with SWD_FINAL/ root or relative to source dir
                rel_path = os.path.relpath(full_path, SOURCE_DIR)
                arcname = os.path.join("SWD_FINAL", rel_path)
                zipf.write(full_path, arcname)
                file_count += 1
                
    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"Successfully packaged {file_count} files into {OUTPUT_ZIP} ({size_mb:.2f} MB)")
    
    # Clean-room extraction verification
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Performing clean-room extraction test in: {tmpdir}...")
        with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zipf:
            zipf.extractall(tmpdir)
            extracted_items = os.listdir(tmpdir)
            if "SWD_FINAL" in extracted_items:
                extracted_root = os.path.join(tmpdir, "SWD_FINAL")
                subitems = os.listdir(extracted_root)
                print(f"Extraction verification: PASS (Found root folder 'SWD_FINAL' with items: {subitems})")
            else:
                print(f"Extraction verification: FAIL (Expected 'SWD_FINAL' root directory, got {extracted_items})")

if __name__ == "__main__":
    package_project()
