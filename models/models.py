from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Identity(start=10), primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    info: Mapped["Info"] = relationship(back_populates="user")


class Info(Base):
    __tablename__ = "info"
    id: Mapped[int] = mapped_column(primary_key=True)
    inf: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="info")


class Main_User(BaseModel):
    id: Annotated[int | None, Identity(start=10), Field(default=100, ge=1, lt=200)] = None
    name: str | None = None


class Main_Info(BaseModel):
    id: Annotated[int | None, Identity(start=10), Field(default=100, ge=1, lt=200)] = None
    inf: str | None = None
    age: Annotated[int | None, Field(ge=0, lt=200)]
