"""
CLAS means 'CLAS'sification.
"""
import os
import shutil

from fastapi import APIRouter, UploadFile, HTTPException

router = APIRouter()


@router.post(
    "/data/upload/",
    summary="Upload learning data",
    description="Upload learning data to train model",
)
async def learn_data_upload(file: UploadFile):
    _UPLOAD_DIR = "data/learning"

    full_path = os.path.abspath(os.path.join(_UPLOAD_DIR, file.filename))
    if os.name == "nt":
        full_path = full_path.replace("\\", "/")

    # if file already exists
    if os.path.exists(full_path):
        raise HTTPException(status_code=400, detail="File already exists")
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)
