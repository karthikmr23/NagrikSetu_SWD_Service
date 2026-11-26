import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

def save_uploaded_document(upload_file: UploadFile, citizen_id: str, doc_code: str) -> dict:
    filename = upload_file.filename or "unknown"
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension '.{ext}'. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Secure storage directory
    target_dir = os.path.join(settings.UPLOAD_DIR, citizen_id)
    os.makedirs(target_dir, exist_ok=True)

    safe_filename = f"{doc_code}_{uuid.uuid4().hex[:8]}.{ext}"
    target_path = os.path.join(target_dir, safe_filename)

    # Stream file to disk and measure size
    file_size = 0
    with open(target_path, "wb") as buffer:
        for chunk in upload_file.file:
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE_BYTES:
                buffer.close()
                if os.path.exists(target_path):
                    os.remove(target_path)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
                )
            buffer.write(chunk)

    return {
        "file_name": filename,
        "file_path": target_path,
        "file_type": upload_file.content_type or f"application/{ext}",
        "file_size_bytes": file_size
    }
