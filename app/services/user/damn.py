from typing import Dict

from app.models.user import User
from app.services.user.base import BaseUserService

cached_users: Dict[int, User] = {}


class DamnUserServiceImpl(BaseUserService):
    async def load_users(self) -> Dict[int, User]:
        return cached_users

    async def dump_users(self):
        global cached_users
        cached_users = self.users_by_id
