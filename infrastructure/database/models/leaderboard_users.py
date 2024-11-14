from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class LeaderboardUsers(BaseModel):
    __tablename__ = "leaderboard_users"

    encrypted_uid: Mapped[str] = mapped_column(String)
    nick_name: Mapped[str] = mapped_column(String, default="No name")
    user_id: Mapped[str] = mapped_column(String)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new_profile: Mapped[bool] = mapped_column(Boolean, default=True)
