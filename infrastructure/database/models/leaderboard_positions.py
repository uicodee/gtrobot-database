from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class LeaderboardPositions(BaseModel):
    __tablename__ = "leaderboard_positions"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    position: Mapped[int] = mapped_column(Integer)
