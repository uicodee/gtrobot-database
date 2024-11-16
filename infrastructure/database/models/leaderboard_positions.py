from sqlalchemy import Integer, ForeignKey, String, Numeric, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class LeaderboardPositions(BaseModel):
    __tablename__ = "leaderboard_positions"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    encrypted_uid: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Numeric)
    symbol: Mapped[str] = mapped_column(String)
    entry_price: Mapped[float] = mapped_column(Numeric)
    mark_price: Mapped[float] = mapped_column(Numeric)
    update_time_stamp: Mapped[int] = mapped_column(Integer)
    leverage: Mapped[int] = mapped_column(Integer)
    is_active_position: Mapped[bool] = mapped_column(Boolean, default=True)
    period_type: Mapped[str] = mapped_column(String, default="DAILY")
    position: Mapped[int] = mapped_column(Integer)
    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)
