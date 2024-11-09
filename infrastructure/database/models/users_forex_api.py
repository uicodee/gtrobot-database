from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UsersForexAPI(BaseModel):
    __tablename__ = 'users_forex_api'

    user_id: Mapped[int] = mapped_column(Integer)
    user_login: Mapped[int] = mapped_column(Integer)
    user_password: Mapped[str] = mapped_column(Text)
    user_server: Mapped[str] = mapped_column(Text)
