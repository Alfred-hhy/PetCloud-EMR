from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field, validator

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

    @validator("expires_at", pre=True)
    def parse_expires_at(cls, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, time.min)
        if isinstance(value, str):
            trimmed = value.strip()
            if not trimmed:
                return None
            for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
                try:
                    return datetime.strptime(trimmed, fmt)
                except ValueError:
                    continue
            try:
                return datetime.fromisoformat(trimmed)
            except ValueError as exc:
                raise ValueError("invalid datetime format") from exc
        return value


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

    @validator("batch_no", "dose_number", "next_due", pre=True)
    def empty_to_none(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            trimmed = value.strip()
            if not trimmed:
                return None
            return trimmed
        return value


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
