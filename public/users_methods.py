from fastapi import APIRouter, Body
from models.models import User, UserDB, Response
from typing import Union, Annotated
import random
import string

users_router = APIRouter()

users_database = [UserDB(FirstName='Ilya', LastName='Bob', Nickname='Shama', user_id=1, password='qwerty'),
                  UserDB(FirstName='Maksim', LastName='Sob', Nickname='Aka', user_id=2, password='qazwsx'),
                  UserDB(FirstName='Bill', LastName='De', Nickname='Baron', user_id=3, password='123456'),
                  UserDB(FirstName='Mikhail ', LastName='Vladimirovich ', Nickname='Krug', user_id=4, password='222001')]


def generate_password():
    result = ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(5, 50)))
    return result


def find_user(user_id: int) -> Union[UserDB, None]:
    for user in users_database:
        if user.user_id == user_id:
            return user
    return None


@users_router.get("/api/users", response_model=Union[list[User], None])
def get_users():
    return users_database


@users_router.get("/api/users/{user_id}", response_model=Union[User, Response])
def get_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        print(user)
        return user


@users_router.post("/api/users", response_model=Union[User, Response])
def create_user(item: Annotated[User, Body(embed=True, description="Создание нового пользователя")]):
    user = UserDB(FirstName=item.FirstName, LastName=item.LastName, Nickname=item.Nickname, user_id=item.user_id, password=generate_password())
    users_database.append(user)
    return user


@users_router.put("/api/users", response_model=Union[User, Response])
def edit_user(item: Annotated[User, Body(embed=True, description="Редактирование пользователя")]):
    user = find_user(item.user_id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        user.user_id = item.user_id
        user.FirstName = item.FirstName
        user.LastName = item.LastName
        user.Nickname = item.Nickname
        return user


@users_router.delete("/api/users/{user_id}", response_model=Union[list[User], None])
def delete_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        return Response(message="Пользователь не найден")
    else:
        users_database.remove(user)
        return users_database
