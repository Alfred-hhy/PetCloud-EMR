from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.models import AccessGrant, DewormingRecord, FeedingLog, Pet, User, VaccineRecord, WeightLog
from app.schemas import (
    AccessGrantCreate,
    AccessGrantRead,
    DewormingRecordCreate,
    DewormingRecordRead,
    FeedingLogCreate,
    FeedingLogRead,
    PetCreate,
    PetDetail,
    PetRead,
    PetUpdate,
    VaccineRecordCreate,
    VaccineRecordRead,
    WeightLogCreate,
    WeightLogRead,
)

router = APIRouter()


@router.get("/", response_model=List[PetRead])
def list_pets(
    db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)
) -> List[Pet]:
    pets = deps.get_accessible_pets(db, current_user)
    return pets


@router.post("/", response_model=PetRead)
def create_pet(
    pet_in: PetCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Pet:
    owner_id = pet_in.owner_id or current_user.id
    if current_user.role == "OWNER" and owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="宠主只能为自己添加宠物")
    owner = db.get(User, owner_id)
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="指定的主人不存在")
    pet = Pet(owner_id=owner_id, **pet_in.dict(exclude_unset=True, exclude={"owner_id"}))
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/{pet_id}", response_model=PetDetail)
def get_pet(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Pet:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    return pet


@router.put("/{pet_id}", response_model=PetRead)
def update_pet(
    pet_id: int,
    pet_in: PetUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Pet:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_writable(db, pet, current_user)
    update_data = pet_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pet, key, value)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}")
def delete_pet(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    pet = deps.get_pet_or_404(pet_id, db)
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅主人可删除宠物")
    db.delete(pet)
    db.commit()
    return {"message": "宠物已删除"}


@router.post("/{pet_id}/weights", response_model=WeightLogRead)
def create_weight_log(
    pet_id: int,
    item: WeightLogCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> WeightLog:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_writable(db, pet, current_user)
    log = WeightLog(pet_id=pet_id, **item.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/{pet_id}/weights", response_model=List[WeightLogRead])
def list_weight_logs(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[WeightLog]:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    logs = db.query(WeightLog).filter(WeightLog.pet_id == pet_id).order_by(WeightLog.logged_at.desc()).all()
    return logs


@router.post("/{pet_id}/feedings", response_model=FeedingLogRead)
def create_feeding_log(
    pet_id: int,
    item: FeedingLogCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> FeedingLog:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_writable(db, pet, current_user)
    log = FeedingLog(pet_id=pet_id, **item.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/{pet_id}/feedings", response_model=List[FeedingLogRead])
def list_feeding_logs(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[FeedingLog]:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    logs = db.query(FeedingLog).filter(FeedingLog.pet_id == pet_id).order_by(FeedingLog.logged_at.desc()).all()
    return logs


@router.post("/{pet_id}/vaccines", response_model=VaccineRecordRead)
def create_vaccine_record(
    pet_id: int,
    item: VaccineRecordCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> VaccineRecord:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_writable(db, pet, current_user)
    record = VaccineRecord(pet_id=pet_id, **item.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{pet_id}/vaccines", response_model=List[VaccineRecordRead])
def list_vaccine_records(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[VaccineRecord]:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    records = db.query(VaccineRecord).filter(VaccineRecord.pet_id == pet_id).order_by(VaccineRecord.injected_at.desc()).all()
    return records


@router.post("/{pet_id}/dewormings", response_model=DewormingRecordRead)
def create_deworming_record(
    pet_id: int,
    item: DewormingRecordCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> DewormingRecord:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_writable(db, pet, current_user)
    record = DewormingRecord(pet_id=pet_id, **item.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{pet_id}/dewormings", response_model=List[DewormingRecordRead])
def list_deworming_records(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[DewormingRecord]:
    pet = deps.get_pet_or_404(pet_id, db)
    deps.ensure_pet_readable(db, pet, current_user)
    records = db.query(DewormingRecord).filter(DewormingRecord.pet_id == pet_id).order_by(DewormingRecord.given_at.desc()).all()
    return records


@router.post("/{pet_id}/grants", response_model=AccessGrantRead)
def create_or_update_grant(
    pet_id: int,
    grant_in: AccessGrantCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> AccessGrant:
    pet = deps.get_pet_or_404(pet_id, db)
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅主人可管理授权")
    grant = (
        db.query(AccessGrant)
        .filter(AccessGrant.pet_id == pet_id, AccessGrant.grantee_user_id == grant_in.grantee_user_id)
        .first()
    )
    data = grant_in.dict()
    if grant:
        for key, value in data.items():
            setattr(grant, key, value)
    else:
        grant = AccessGrant(pet_id=pet_id, **data)
        db.add(grant)
    db.commit()
    db.refresh(grant)
    return grant


@router.get("/{pet_id}/grants", response_model=List[AccessGrantRead])
def list_grants(
    pet_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[AccessGrant]:
    pet = deps.get_pet_or_404(pet_id, db)
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅主人可查看授权")
    return pet.grants
