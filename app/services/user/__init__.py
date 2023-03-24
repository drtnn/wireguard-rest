from typing import Type

from app.services.user.base import BaseUserService
from app.services.user.damn import DamnUserServiceImpl
from app.services.user.json import JsonUserServiceImpl
from app.settings.main import settings

UserService: Type[BaseUserService] = JsonUserServiceImpl
if settings.ENVIRONMENT == "DEVELOPMENT":
    UserService = DamnUserServiceImpl
