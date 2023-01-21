from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class User(UserCreate):
    id: int
    name: str
    public_key: str
    private_key: str

    @property
    def address(self):
        return f"10.0.0.{self.id}/32"


class UserList(BaseModel):
    __root__: List[User]


class UserPeerConfiguration(BaseModel):
    configuration: str
