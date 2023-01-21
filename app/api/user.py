from fastapi import APIRouter
from starlette import status

from app.models.user import UserList, UserCreate, User, UserPeerConfiguration
from app.services.user import JsonUserService

router = APIRouter()


@router.get("/user", response_model=UserList, status_code=status.HTTP_200_OK)
async def list():
    user_service = await JsonUserService.new()
    return await user_service.list()


@router.get("/user/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def retrieve(id: int):
    user_service = await JsonUserService.new()
    return await user_service.retrieve(id=id)


@router.post("/user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(data: UserCreate):
    user_service = await JsonUserService.new()
    return await user_service.create(user_create=data)


@router.put("/user/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def update(id: int, data: UserCreate):
    user_service = await JsonUserService.new()
    return await user_service.update(id=id, user_update=data)


@router.patch("/user/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def partial_update(id: int, data: UserCreate):
    user_service = await JsonUserService.new()
    return await user_service.update(id=id, user_update=data)


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def partial_update(id: int):
    user_service = await JsonUserService.new()
    return await user_service.delete(id=id)


@router.get("/user/{id}/peer-configuration", response_model=UserPeerConfiguration, status_code=status.HTTP_200_OK)
async def peer_configuration(id: int):
    user_service = await JsonUserService.new()
    configuration = user_service.peer_configuration(id=id)
    return UserPeerConfiguration(configuration=configuration)
