from datetime import datetime
from xmlrpc.client import DateTime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, select

from .database.base import Base, Manager
from .database.connector import db_conn


class User(Base, Manager):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    email = Column(String(100), nullable=True)

    def __str__(self):
        return f"User: {self.id} ({self.username})"

    @classmethod
    async def create_user(cls, **kwargs):
        password = kwargs.get("password")
        # ----------
        kwargs["password"] = password  # TODO: добавить шифрование пароля
        # ----------
        return await super().create(**kwargs)

    @classmethod
    async def get_valid_user(self, username: str, password: str) -> "User":
        # TODO: добавить проверку с шифрованным паролем.
        query = select(User).where(User.username == username, User.password == password)
        async with db_conn.session as session:
            user = await session.execute(query)
            return user.scalar_one()


class Post(Base, Manager):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(Text())
    created = Column(DateTime(), default=datetime.now)
    user_id = Column(ForeignKey("users.id", ondelete="cascade"))

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"
