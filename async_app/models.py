from datetime import datetime


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, select
from sqlalchemy.orm import relationship
from .database.base import Base, Manager
from .database.connector import db_conn
from .services.encryption import make_password, check_password


class User(Base, Manager):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    email = Column(String(100), nullable=True)
    posts = relationship("Post", back_populates="user")
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    def __str__(self):
        return f"User: {self.id} ({self.username})"

    @classmethod
    async def create_user(cls, **kwargs):
        password = kwargs.get("password")
        # ----------
        kwargs["password"] = make_password(password)
        # ----------
        return await super().create(**kwargs)

    @classmethod
    async def get_valid_user(self, username: str, password: str) -> "User":
        user = await User.get(username=username)
        if user:
            if check_password(password, user.password):
                return user




class Post(Base, Manager):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(Text())
    created = Column(DateTime(), default=datetime.now)
    user_id = Column(ForeignKey("users.id", ondelete="cascade"))

    user = relationship("User", back_populates='posts')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"
