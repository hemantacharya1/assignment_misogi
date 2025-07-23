from fastapi import UploadFile
import os
from pathlib import Path

UPLOAD_DIR = Path("data/raw_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    file_path = UPLOAD_DIR / upload_file.filename
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
    return str(file_path)
