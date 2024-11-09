from .base import BaseModel
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column


class WinWinUsers(BaseModel):
    __tablename__ = "winwin_users"

    name: Mapped[str] = mapped_column(Text)
    phone_number: Mapped[int] = mapped_column(Integer)
