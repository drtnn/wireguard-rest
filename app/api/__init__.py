from fastapi import APIRouter

from .endpoints.user import router as user_router
from .endpoints.wireguard import router as wireguard_router

router = APIRouter()

router.include_router(user_router, prefix="", tags=["user"])
router.include_router(wireguard_router, prefix="", tags=["wireguard"])
