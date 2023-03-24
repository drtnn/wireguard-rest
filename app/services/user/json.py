import json
from typing import Dict

import aiofiles
from pydantic import parse_obj_as

from app.models.user import User, UserList
from app.services.user.base import BaseUserService
from app.settings.main import settings


class JsonUserServiceImpl(BaseUserService):
    users_file_path: str = settings.USERS_FILE_PATH

    async def load_users(self) -> Dict[int, User]:
        async with aiofiles.open(self.users_file_path, encoding="utf-8") as file:
            users = json.loads(await file.read())
        return {user.id: user for user in parse_obj_as(UserList, users).__root__}

    async def dump_users(self):
        user_list = UserList(__root__=self.users)
        async with aiofiles.open(self.users_file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(user_list.dict(), indent=4))
