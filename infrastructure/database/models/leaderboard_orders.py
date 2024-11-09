from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class LeaderboardOrders(BaseModel):
    __tablename__ = 'leaderboard_orders'

    position_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)
