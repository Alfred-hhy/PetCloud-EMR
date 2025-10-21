from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReminderItem(BaseModel):
    pet_id: int
    pet_name: str
    type: str
    title: str
    due_date: Optional[date]
    description: Optional[str] = None
