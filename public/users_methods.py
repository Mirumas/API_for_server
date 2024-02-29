from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from starlette import status
from models.models import *
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from public.db import engine_s

users_router = APIRouter(prefix='/api/users')
info_router = APIRouter(prefix='/api/users/info')


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()


def coder_passwd(cod: str):
    return cod * 2


@users_router.get("/{id}", response_model=Main_User)
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    else:
        return user


@users_router.get("/", response_model=Optional[list[Main_User]])
def get_user_db(db: Session = Depends(get_session)):
    users = db.query(User).all()
    if users is None:
        return JSONResponse(status_code=404, content={"message": " Пользователь не найден"})
    return users


@users_router.post("/", response_model=Main_User, status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True)],
                db: Session = Depends(get_session)):
    try:
        user = User(name=item.name)

        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")


@users_router.put("/", response_model=Main_User)
def edit_user_(item: Annotated[Main_User, Body(embed=True)],
               db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == item.id).first()

    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = item.name
    try:
        db.commit()
        db.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user


@users_router.delete("/{id}", response_class=JSONResponse)
def delete_user(id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        db.delete(user)
        db.commit()
    except HTTPException:
        return JSONResponse(content={'message': f'Произошла ошибка при удалении объекта'})
    return JSONResponse(content={'message': f'Пользователь удалён {id}'})


@info_router.post("/{id}", response_model=Main_Info, status_code=status.HTTP_201_CREATED)
def create_info(item: Annotated[Main_Info, Body(embed=True)],
                db: Session = Depends(get_session),
                user: User = Depends(get_user)):
    try:
        info = Info(inf=item.inf)
        info = Info(age=item.age)
        info.user_id = user.id
        info.user = user
        if info is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        db.add(info)
        db.commit()
        db.refresh(info)
        return info
    except Exception:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {info}")
