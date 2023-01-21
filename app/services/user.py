import json
from typing import Dict, List

import aiofiles
from pydantic import parse_obj_as

from app.models.user import User, UserCreate, UserList
from app.services.wireguard import WireguardService
from app.settings.main import settings


class BaseUserService:
    users_file_path: str = settings.USERS_FILE_PATH
    users_by_id: Dict[int, User]

    @classmethod
    async def new(cls):
        self = cls()
        await self.__setup_users()
        return self

    async def __setup_users(self):
        if not getattr(self, "users_by_id", None):
            self.users_by_id = await self.load_users()

    @property
    def users(self) -> List[User]:
        return list(self.users_by_id.values())

    @property
    def last_user_id(self) -> int:
        ids = self.users_by_id.keys()
        return max(ids) if ids else 1

    async def load_users(self) -> Dict[int, User]:
        raise NotImplementedError

    async def dump_users(self):
        raise NotImplementedError

    async def list(self) -> List[User]:
        return self.users

    async def retrieve(self, id: int):
        return self.users_by_id[id]

    async def create(self, user_create: UserCreate):
        private_key = WireguardService.generate_private_key()
        public_key = WireguardService.generate_public_key(private_key)
        user = User(
            id=self.last_user_id + 1, name=user_create.name, public_key=public_key, private_key=private_key
        )
        self.users_by_id[user.id] = user

        await self.dump_users()
        await WireguardService.update_configuration(users=self.users)

        return user

    async def update(self, id: int, user_update: UserCreate):
        self.users_by_id[id].name = user_update.name
        await self.dump_users()
        return self.users_by_id[id]

    async def delete(self, id: int):
        del self.users_by_id[id]

        await self.dump_users()
        await WireguardService.update_configuration(users=self.users)

    def peer_configuration(self, id: int) -> str:
        return WireguardService.generate_peer_configuration(user=self.users_by_id[id])


class JsonUserService(BaseUserService):
    async def load_users(self) -> Dict[int, User]:
        async with aiofiles.open(self.users_file_path, encoding="utf-8") as file:
            users = json.loads(await file.read())
        return {user.id: user for user in parse_obj_as(UserList, users).__root__}

    async def dump_users(self):
        user_list = UserList(__root__=self.users)
        async with aiofiles.open(self.users_file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(user_list.dict(), indent=4))
