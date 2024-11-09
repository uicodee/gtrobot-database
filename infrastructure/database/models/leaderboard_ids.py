from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class LeaderboardIDs(BaseModel):
    __tablename__ = "leaderboard_ids"

    level: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(Text)
