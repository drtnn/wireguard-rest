from fastapi import APIRouter

from .user import router as user_router
from .wireguard import router as wireguard_router

router = APIRouter()

router.include_router(user_router, prefix="", tags=["user"])
router.include_router(wireguard_router, prefix="", tags=["wireguard"])
