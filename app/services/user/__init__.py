from typing import Type

from app.services.user.base import BaseUserService
from app.services.user.json import JsonUserServiceImpl

UserService: Type[BaseUserService] = JsonUserServiceImpl
