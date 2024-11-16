from sqlalchemy import Numeric, String, Boolean, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ClosedLeaderboardOrders(BaseModel):
    __tablename__ = "closed_leaderboard_orders"

    position_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(BigInteger)
    amount: Mapped[float] = mapped_column(Numeric)
    symbol: Mapped[str] = mapped_column(String)
    entry_price: Mapped[float] = mapped_column(Numeric)
    mark_price: Mapped[float] = mapped_column(Numeric)
    leverage: Mapped[float] = mapped_column(Numeric)
    is_posted: Mapped[bool] = mapped_column(Boolean)
