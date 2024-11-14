from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class LeaderboardsData(BaseModel):
    __tablename__ = "leaderboards_data"

    leaderboard_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leaderboard_ids.id")
    )
    position: Mapped[int] = mapped_column(Integer)
    withdrawal_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_withdrawals.id"))
    name: Mapped[str] = mapped_column(Text)
    earnings: Mapped[float] = mapped_column(Numeric)
    views: Mapped[int] = mapped_column(Integer)
    sales: Mapped[int] = mapped_column(Integer)
    registered_at: Mapped[int] = mapped_column(Integer)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
