from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class LeaderboardUsers(BaseModel):
    __tablename__ = "leaderboard_users"

    encrypted_uid: Mapped[str] = mapped_column(String)
    nick_name: Mapped[str] = mapped_column(String, default="No name")
    rank: Mapped[int] = mapped_column(Integer)
    period_type: Mapped[str] = mapped_column(String, default="DAILY")
    is_new_profile: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active_user: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[str] = mapped_column(String)
