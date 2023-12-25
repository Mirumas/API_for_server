import uuid
from fastapi.responses import JSONResponse, FileResponse
import hashlib
from fastapi import APIRouter, Body
from models.models import User, UserDB, Response
from typing import Union, Annotated

users_router = APIRouter()

users_database = [UserDB(FirstName='Ilya', LastName='Bob', Nickname='Shama', id=1, password='qwerty'),
                  UserDB(FirstName='Maksim', LastName='Sob', Nickname='Aka', id=2, password='qazwsx'),
                  UserDB(FirstName='Bill', LastName='De', Nickname='Baron', id=3, password='123456'),
                  UserDB(FirstName='Mikhail ', LastName='Vladimirovich ', Nickname='Krug', id=4, password='222001')]


def coder_password(cod: str):
    result = cod * 2


def find_user(user_id: int) -> Union[UserDB, None]:
    for user in users_database:
        if user.id == user_id:
            return user
    return None


@users_router.get("/api/users", response_model=Union[list[User], None])
def get_users():
    return users_database


@users_router.get("/api/users/{id}", response_model=Union[User, Response])
def get_user(id: int):
    user = find_user(id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        print(user)
        return user


@users_router.post("/api/users", response_model=Union[User, Response])
def create_user(item: Annotated[User, Body(embed=True, description="Создание нового пользователя")]):
    user = UserDB(name=item.name, id=item.id, password=coder_password(item.name))
    users_database.append(user)
    return user


@users_router.put("/api/users", response_model=Union[User, Response])
def edit_user(item: Annotated[User, Body(embed=True, description="Редактирование пользователя")]):
    user = find_user(item.id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        user.id = item.id
        user.name = item.name
        return user


@users_router.delete("/api/users/{id}", response_model=Union[list[User], None])
def delete_user(id: int):
    user = find_user(id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        users_database.remove(user)
        return users_database
