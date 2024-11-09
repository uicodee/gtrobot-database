from .base import BaseModel
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class PositionUsers(BaseModel):
    __tablename__ = "position_users"

    encrypted_uid: Mapped[str] = mapped_column(String)
    nick_name: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)
    period_type: Mapped[str] = mapped_column(Text, default="DAILY")
    is_active_user: Mapped[bool] = mapped_column(Integer, default=True)
