import zipfile
import os

zip_filename = "NagrikSetu_SWD_FINAL.zip"
root_folder_name = "NagrikSetu_SWD_FINAL"
base_dir = os.path.dirname(os.path.abspath(__file__))

exclude_dirs = {
    "node_modules", 
    ".pytest_cache", 
    "__pycache__", 
    ".git", 
    "dist", 
    ".vscode", 
    ".idea"
}

exclude_files = {
    zip_filename,
    "NagrikSetu_SWD_Final.zip",
    ".env"  # preserve .env.example, exclude live .env credentials
}

zip_filepath = os.path.join(base_dir, zip_filename)

with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(base_dir):
        # Filter directories in-place to prune excluded trees
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for f in files:
            if f in exclude_files or f.endswith(".pyc") or f.endswith(".log"):
                continue
            
            full_path = os.path.join(root, f)
            rel_from_base = os.path.relpath(full_path, base_dir)
            # Prefix with the required root folder name: NagrikSetu_SWD_FINAL/
            archive_path = os.path.join(root_folder_name, rel_from_base).replace("\\", "/")
            z.write(full_path, archive_path)

size_bytes = os.path.getsize(zip_filepath)
print(f"Archive successfully generated at: {zip_filepath}")
print(f"File size: {size_bytes} bytes ({size_bytes / (1024*1024):.2f} MB)")
