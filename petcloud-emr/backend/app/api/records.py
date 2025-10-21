import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.models import MedicalRecord, Prescription, User
from app.schemas import (
    MedicalRecordCreate,
    MedicalRecordDetail,
    MedicalRecordRead,
    PrescriptionCreate,
    PrescriptionRead,
)

router = APIRouter()


def _serialize_record(record: MedicalRecord) -> MedicalRecordRead:
    attachments = []
    if record.attachments:
        try:
            attachments = json.loads(record.attachments)
        except json.JSONDecodeError:
            attachments = []
    return MedicalRecordRead(
        id=record.id,
        pet_id=record.pet_id,
        vet_id=record.vet_id,
        clinic_id=record.clinic_id,
        visit_date=record.visit_date,
        chief_complaint=record.chief_complaint,
        diagnosis=record.diagnosis,
        treatment=record.treatment,
        notes=record.notes,
        attachments=attachments,
    )


def _serialize_record_detail(record: MedicalRecord) -> MedicalRecordDetail:
    base = _serialize_record(record)
    return MedicalRecordDetail(
        **base.dict(),
        prescriptions=[
            PrescriptionRead(
                id=pres.id,
                drug_name=pres.drug_name,
                dosage=pres.dosage,
                frequency=pres.frequency,
                days=pres.days,
            )
            for pres in record.prescriptions
        ],
    )


@router.post("/pets/{pet_id}/records", response_model=MedicalRecordRead)
def create_record(
    pet_id: int,
    record_in: MedicalRecordCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> MedicalRecordRead:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_record_permission(db, pet, current_user)
    record = MedicalRecord(
        pet_id=pet_id,
        vet_id=current_user.id,
        clinic_id=record_in.clinic_id,
        visit_date=record_in.visit_date,
        chief_complaint=record_in.chief_complaint,
        diagnosis=record_in.diagnosis,
        treatment=record_in.treatment,
        notes=record_in.notes,
        attachments=json.dumps(record_in.attachments or []),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return _serialize_record(record)


@router.get("/pets/{pet_id}/records", response_model=List[MedicalRecordRead])
def list_records(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[MedicalRecordRead]:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.pet_id == pet_id)
        .order_by(MedicalRecord.visit_date.desc())
        .all()
    )
    return [_serialize_record(record) for record in records]


@router.get("/records/{record_id}", response_model=MedicalRecordDetail)
def get_record(
    record_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> MedicalRecordDetail:
    record = db.get(MedicalRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="病历不存在")
    pet = deps.get_pet_or_404(record.pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    return _serialize_record_detail(record)


@router.post("/records/{record_id}/prescriptions", response_model=PrescriptionRead)
def create_prescription(
    record_id: int,
    item: PrescriptionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> PrescriptionRead:
    record = db.get(MedicalRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="病历不存在")
    pet = deps.get_pet_or_404(record.pet_id, db)
    deps.ensure_pet_record_permission(db, pet, current_user)
    prescription = Prescription(medical_record_id=record_id, **item.dict())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return PrescriptionRead.from_orm(prescription)
