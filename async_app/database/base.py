from typing_extensions import Self
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import declarative_base

from .connector import db_conn

Base = declarative_base()


class Manager:

    @classmethod
    async def create(cls, **kwargs) -> Self:
        obj = cls(**kwargs)
        async with db_conn.session as session:
            session.add(obj)  # Добавляем объект в его таблицу.
            await session.commit()  # Подтверждаем.
            await session.refresh(obj)  # Обновляем атрибуты у объекта, чтобы получить его primary key.
        return obj

    @classmethod
    async def get(cls, **kwargs):
        async with db_conn.session as session:
            query = select(cls)
            for key, value in kwargs.items():
                query = query.where(getattr(cls, key) == value)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def filter(cls, **kwargs):
        async with db_conn.session as session:
            result = await session.execute(
                select(cls).filter_by(**kwargs)
            )
            return result.scalars()

    @classmethod
    async def all(cls) -> Sequence[Self]:
        async with db_conn.session as session:
            result = await session.execute(select(cls))
            return result.scalars().all()