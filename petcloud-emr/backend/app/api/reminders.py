from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core import deps
from app.schemas import ReminderItem
from app.services.reminders import get_upcoming_reminders

router = APIRouter()


@router.get("/upcoming", response_model=List[ReminderItem])
def upcoming_reminders(
    days: int = Query(30, ge=1, le=365, description="提醒范围（天）"),
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
) -> List[ReminderItem]:
    return get_upcoming_reminders(db, current_user, days=days)
