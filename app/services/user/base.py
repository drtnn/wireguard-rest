from abc import abstractmethod, ABC
from typing import List, Dict

from app.models.user import UserCreate, User
from app.services.wireguard import WireguardService


class BaseUserService(ABC):
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

    @abstractmethod
    async def load_users(self) -> Dict[int, User]:
        raise NotImplementedError

    @abstractmethod
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
