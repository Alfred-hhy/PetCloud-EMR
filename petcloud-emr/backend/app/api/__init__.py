from fastapi import APIRouter

from . import auth, pets, records, reminders, uploads

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])
api_router.include_router(records.router, tags=["records"])
api_router.include_router(uploads.router, tags=["uploads"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
