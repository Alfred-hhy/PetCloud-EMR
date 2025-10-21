import json
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core import deps
from app.core.config import get_settings
from app.models import MedicalRecord, User

router = APIRouter()
settings = get_settings()


@router.post("/records/{record_id}/attachments")
def upload_attachments(
    record_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    record = db.get(MedicalRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="病历不存在")
    pet = deps.get_pet_or_404(record.pet_id, db)
    deps.ensure_pet_record_permission(db, pet, current_user)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    existing = []
    if record.attachments:
        try:
            existing = json.loads(record.attachments)
        except json.JSONDecodeError:
            existing = []

    urls = []
    for file in files:
        suffix = os.path.splitext(file.filename or "")[1]
        filename = f"{uuid.uuid4().hex}{suffix}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        url = f"/uploads/{filename}"
        urls.append(url)
        existing.append(url)

    record.attachments = json.dumps(existing)
    db.add(record)
    db.commit()
    return {"urls": urls}
