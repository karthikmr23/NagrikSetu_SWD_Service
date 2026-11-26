import zipfile
import os

zip_path = "NagrikSetu_SWD_Final.zip"
exclude_dirs = {"node_modules", ".pytest_cache", "__pycache__", ".git", "dist"}

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk("."):
        # filter dirs in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f == zip_path or f.endswith(".pyc"):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ".")
            z.write(full_path, rel_path)

print(f"Archive successfully generated at {os.path.abspath(zip_path)} with size {os.path.getsize(zip_path)} bytes.")
