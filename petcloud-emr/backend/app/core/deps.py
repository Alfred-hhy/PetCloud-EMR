from datetime import datetime
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.db import SessionLocal
from app.core.security import decode_access_token
from app.models import AccessGrant, Pet, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ----- 数据库依赖 -----
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----- 用户相关依赖 -----
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证身份，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("user_id"))
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.get(User, user_id)
    if not user:
        raise credentials_exception
    return user


# ----- 权限辅助 -----
def _active_grant_for_pet(db: Session, pet_id: int, user_id: int) -> Optional[AccessGrant]:
    now = datetime.utcnow()
    return (
        db.query(AccessGrant)
        .filter(
            AccessGrant.pet_id == pet_id,
            AccessGrant.grantee_user_id == user_id,
            or_(AccessGrant.expires_at.is_(None), AccessGrant.expires_at > now),
        )
        .first()
    )


def ensure_pet_readable(db: Session, pet: Pet, user: User) -> Pet:
    if pet.owner_id == user.id:
        return pet
    grant = _active_grant_for_pet(db, pet.id, user.id)
    if grant:
        return pet
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="没有权限访问该宠物")


def ensure_pet_writable(db: Session, pet: Pet, user: User) -> Pet:
    if pet.owner_id == user.id:
        return pet
    grant = _active_grant_for_pet(db, pet.id, user.id)
    if grant and grant.scope in {"write", "all"}:
        return pet
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="没有权限修改该宠物")


def ensure_pet_record_permission(db: Session, pet: Pet, user: User) -> Pet:
    grant = _active_grant_for_pet(db, pet.id, user.id)
    if user.role in {"VET", "CLINIC_ADMIN"}:
        if pet.owner_id == user.id or grant:
            return pet
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="需要宠主授权后才能创建病历")
    if grant and grant.scope in {"write", "all"}:
        return pet
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅兽医或被授权用户可创建病历")


def get_pet_or_404(pet_id: int, db: Session) -> Pet:
    pet = db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宠物不存在")
    return pet


def get_accessible_pets(db: Session, user: User) -> list[Pet]:
    now = datetime.utcnow()
    owned = db.query(Pet).filter(Pet.owner_id == user.id).all()
    granted = (
        db.query(Pet)
        .join(AccessGrant, AccessGrant.pet_id == Pet.id)
        .filter(
            AccessGrant.grantee_user_id == user.id,
            or_(AccessGrant.expires_at.is_(None), AccessGrant.expires_at > now),
        )
        .all()
    )
    pet_map = {pet.id: pet for pet in owned}
    for pet in granted:
        pet_map.setdefault(pet.id, pet)
    return list(pet_map.values())
