from fastapi import APIRouter
from starlette import status

from app.services.user import JsonUserService
from app.services.wireguard import WireguardService

router = APIRouter()


@router.post("/wireguard/restart", status_code=status.HTTP_200_OK)
async def update():
    user_service = await JsonUserService.new()
    await WireguardService.update_configuration(users=user_service.users)
    WireguardService.restart_wireguard_service()
