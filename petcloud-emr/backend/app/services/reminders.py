from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from app.core.deps import get_accessible_pets
from app.models import Pet, User
from app.schemas import ReminderItem


def _to_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    return value


def _within_days(target_date, days: int) -> bool:
    if not target_date:
        return False
    today = datetime.utcnow().date()
    return today <= target_date <= today + timedelta(days=days)


def get_upcoming_reminders(db: Session, user: User, days: int = 30) -> List[ReminderItem]:
    pets: List[Pet] = get_accessible_pets(db, user)
    reminders: List[ReminderItem] = []
    for pet in pets:
        for vaccine in pet.vaccines:
            due = _to_date(vaccine.next_due)
            if due and _within_days(due, days):
                reminders.append(
                    ReminderItem(
                        pet_id=pet.id,
                        pet_name=pet.name,
                        type="vaccine",
                        title=f"疫苗提醒：{vaccine.vaccine_name}",
                        due_date=due,
                        description=f"批次 {vaccine.batch_no or '未知'}，计划日期 {due.isoformat()}",
                    )
                )
        for deworm in pet.dewormings:
            due = _to_date(deworm.given_at) + timedelta(days=deworm.cycle_days)
            if _within_days(due, days):
                reminders.append(
                    ReminderItem(
                        pet_id=pet.id,
                        pet_name=pet.name,
                        type="deworming",
                        title=f"驱虫提醒：{deworm.drug_name}",
                        due_date=due,
                        description=f"上次日期 {deworm.given_at.isoformat()}，周期 {deworm.cycle_days} 天",
                    )
                )
    reminders.sort(key=lambda item: (item.due_date or datetime.max.date()))
    return reminders
