from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class PrescriptionBase(BaseModel):
    drug_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    days: Optional[int] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionRead(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True


class MedicalRecordBase(BaseModel):
    visit_date: date
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    clinic_id: Optional[int] = None
    attachments: List[str] = []


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    id: int
    pet_id: int
    vet_id: Optional[int] = None

    class Config:
        orm_mode = True


class MedicalRecordDetail(MedicalRecordRead):
    prescriptions: List[PrescriptionRead] = []
