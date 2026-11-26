import os
import zipfile
import shutil

src_dir = r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final"
delivery_dir = r"C:\Users\karth\OneDrive\Documents\SWD_FINAL_DELIVERY"
zip_filename = "SWD_FINAL.zip"
root_folder = "SWD_FINAL"

os.makedirs(delivery_dir, exist_ok=True)
dest_zip = os.path.join(delivery_dir, zip_filename)

exclude_dirs = {
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    ".git",
    ".vscode",
    ".idea"
}

exclude_files = {
    "NagrikSetu_SWD_FINAL.zip",
    "SWD_FINAL.zip",
    "test_swd.db"
}

print(f"Packaging {src_dir} into {dest_zip} with root folder '{root_folder}/'...")

count = 0
with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for f in files:
            if f in exclude_files or f.endswith(".pyc") or f.endswith(".log"):
                continue

            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, src_dir)
            arc_name = os.path.join(root_folder, rel_path).replace("\\", "/")
            z.write(full_path, arc_name)
            count += 1

size_mb = os.path.getsize(dest_zip) / (1024 * 1024)
print(f"Successfully packaged {count} files into {dest_zip} ({size_mb:.2f} MB)")

# Verify clean-room extraction test
extract_test_dir = os.path.join(delivery_dir, "CLEAN_ROOM_TEST_EXTRACT")
if os.path.exists(extract_test_dir):
    shutil.rmtree(extract_test_dir)
os.makedirs(extract_test_dir, exist_ok=True)

with zipfile.ZipFile(dest_zip, "r") as z:
    z.extractall(extract_test_dir)

extracted_root = os.path.join(extract_test_dir, root_folder)
if os.path.exists(extracted_root) and os.path.exists(os.path.join(extracted_root, "backend")) and os.path.exists(os.path.join(extracted_root, "frontend")):
    print("Clean-room extraction verification: PASS (SWD_FINAL root directory confirmed)")
else:
    print("Clean-room extraction verification: FAIL")

# Cleanup clean-room test
shutil.rmtree(extract_test_dir)
print("Clean-room test folder cleaned up.")
