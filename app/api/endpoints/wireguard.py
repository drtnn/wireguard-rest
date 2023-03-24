from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from app.api.deps import authentication_scheme
from app.services.user import UserService
from app.services.wireguard import WireguardService

router = APIRouter()


@router.post("/wireguard/restart", status_code=status.HTTP_200_OK)
async def update(authentication: HTTPAuthorizationCredentials = Depends(authentication_scheme)):
    user_service = await UserService.new()
    await WireguardService.update_configuration(users=user_service.users)
    WireguardService.restart_wireguard_service()
