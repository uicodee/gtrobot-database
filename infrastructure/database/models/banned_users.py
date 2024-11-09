from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class BannedUsers(BaseModel):
    __tablename__ = "banned_users"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    ban_reason: Mapped[str] = mapped_column(Text)
