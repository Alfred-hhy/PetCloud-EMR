from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .user import UserRead


class PetBase(BaseModel):
    name: str
    species: Optional[str] = None
    breed: Optional[str] = None
    sex: Optional[str] = None
    birthday: Optional[date] = None
    color: Optional[str] = None
    chip_id: Optional[str] = None
    avatar_url: Optional[str] = None


class PetCreate(PetBase):
    owner_id: Optional[int] = None


class PetUpdate(PetBase):
    name: Optional[str] = None


class PetRead(PetBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AccessGrantBase(BaseModel):
    grantee_user_id: int
    scope: str = Field(regex="^(read|write|all)$", default="read")
    expires_at: Optional[datetime] = None


class AccessGrantCreate(AccessGrantBase):
    pass


class AccessGrantRead(AccessGrantBase):
    id: int

    class Config:
        orm_mode = True


class WeightLogBase(BaseModel):
    logged_at: date
    weight_kg: float


class WeightLogCreate(WeightLogBase):
    pass


class WeightLogRead(WeightLogBase):
    id: int

    class Config:
        orm_mode = True


class FeedingLogBase(BaseModel):
    logged_at: date
    food: str
    amount: Optional[str] = None
    notes: Optional[str] = None


class FeedingLogCreate(FeedingLogBase):
    pass


class FeedingLogRead(FeedingLogBase):
    id: int

    class Config:
        orm_mode = True


class VaccineRecordBase(BaseModel):
    vaccine_name: str
    batch_no: Optional[str] = None
    dose_number: Optional[int] = None
    injected_at: date
    next_due: Optional[date] = None


class VaccineRecordCreate(VaccineRecordBase):
    pass


class VaccineRecordRead(VaccineRecordBase):
    id: int

    class Config:
        orm_mode = True


class DewormingRecordBase(BaseModel):
    drug_name: str
    given_at: date
    cycle_days: int = Field(gt=0)


class DewormingRecordCreate(DewormingRecordBase):
    pass


class DewormingRecordRead(DewormingRecordBase):
    id: int

    class Config:
        orm_mode = True


class PetDetail(PetRead):
    owner: Optional[UserRead]
    grants: List[AccessGrantRead] = []
    weight_logs: List[WeightLogRead] = []
    feeding_logs: List[FeedingLogRead] = []
    vaccines: List[VaccineRecordRead] = []
    dewormings: List[DewormingRecordRead] = []

    class Config:
        orm_mode = True
