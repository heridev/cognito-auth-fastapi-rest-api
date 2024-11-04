from fastapi import APIRouter
from .endpoints import contacts, users

router = APIRouter()


router.include_router(contacts.router)
router.include_router(users.router)
