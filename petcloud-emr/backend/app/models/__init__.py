from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    pets: Mapped[List["Pet"]] = relationship("Pet", back_populates="owner")
    vet_records: Mapped[List["MedicalRecord"]] = relationship("MedicalRecord", back_populates="vet")


class Clinic(Base):
    __tablename__ = "clinics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    records: Mapped[List["MedicalRecord"]] = relationship("MedicalRecord", back_populates="clinic")


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[Optional[str]] = mapped_column(String(100))
    breed: Mapped[Optional[str]] = mapped_column(String(100))
    sex: Mapped[Optional[str]] = mapped_column(String(20))
    birthday: Mapped[Optional[date]] = mapped_column(Date)
    color: Mapped[Optional[str]] = mapped_column(String(100))
    chip_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    owner: Mapped[User] = relationship("User", back_populates="pets")
    grants: Mapped[List["AccessGrant"]] = relationship("AccessGrant", back_populates="pet", cascade="all, delete-orphan")
    records: Mapped[List["MedicalRecord"]] = relationship("MedicalRecord", back_populates="pet", cascade="all, delete-orphan")
    vaccines: Mapped[List["VaccineRecord"]] = relationship("VaccineRecord", back_populates="pet", cascade="all, delete-orphan")
    dewormings: Mapped[List["DewormingRecord"]] = relationship("DewormingRecord", back_populates="pet", cascade="all, delete-orphan")
    weight_logs: Mapped[List["WeightLog"]] = relationship("WeightLog", back_populates="pet", cascade="all, delete-orphan")
    feeding_logs: Mapped[List["FeedingLog"]] = relationship("FeedingLog", back_populates="pet", cascade="all, delete-orphan")


class AccessGrant(Base):
    __tablename__ = "access_grants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    grantee_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    scope: Mapped[str] = mapped_column(String(20), default="read", nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    pet: Mapped[Pet] = relationship("Pet", back_populates="grants")
    grantee: Mapped[User] = relationship("User")

    __table_args__ = (Index("ix_grant_pet_user", "pet_id", "grantee_user_id", unique=True),)


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    vet_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    clinic_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("clinics.id"), index=True)
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    chief_complaint: Mapped[Optional[str]] = mapped_column(Text)
    diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    treatment: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    attachments: Mapped[str] = mapped_column(Text, default="[]", nullable=False)

    pet: Mapped[Pet] = relationship("Pet", back_populates="records")
    vet: Mapped[Optional[User]] = relationship("User", back_populates="vet_records")
    clinic: Mapped[Optional[Clinic]] = relationship("Clinic", back_populates="records")
    prescriptions: Mapped[List["Prescription"]] = relationship(
        "Prescription", back_populates="record", cascade="all, delete-orphan"
    )


class VaccineRecord(Base):
    __tablename__ = "vaccine_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    vaccine_name: Mapped[str] = mapped_column(String(200), nullable=False)
    batch_no: Mapped[Optional[str]] = mapped_column(String(100))
    dose_number: Mapped[Optional[int]] = mapped_column(Integer)
    injected_at: Mapped[date] = mapped_column(Date, nullable=False)
    next_due: Mapped[Optional[date]] = mapped_column(Date)

    pet: Mapped[Pet] = relationship("Pet", back_populates="vaccines")


class DewormingRecord(Base):
    __tablename__ = "deworming_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    drug_name: Mapped[str] = mapped_column(String(200), nullable=False)
    given_at: Mapped[date] = mapped_column(Date, nullable=False)
    cycle_days: Mapped[int] = mapped_column(Integer, nullable=False)

    pet: Mapped[Pet] = relationship("Pet", back_populates="dewormings")


class WeightLog(Base):
    __tablename__ = "weight_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    logged_at: Mapped[date] = mapped_column(Date, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)

    pet: Mapped[Pet] = relationship("Pet", back_populates="weight_logs")


class FeedingLog(Base):
    __tablename__ = "feeding_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"), index=True, nullable=False)
    logged_at: Mapped[date] = mapped_column(Date, nullable=False)
    food: Mapped[str] = mapped_column(String(200), nullable=False)
    amount: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    pet: Mapped[Pet] = relationship("Pet", back_populates="feeding_logs")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medical_record_id: Mapped[int] = mapped_column(Integer, ForeignKey("medical_records.id"), index=True, nullable=False)
    drug_name: Mapped[str] = mapped_column(String(200), nullable=False)
    dosage: Mapped[Optional[str]] = mapped_column(String(200))
    frequency: Mapped[Optional[str]] = mapped_column(String(200))
    days: Mapped[Optional[int]] = mapped_column(Integer)

    record: Mapped[MedicalRecord] = relationship("MedicalRecord", back_populates="prescriptions")
