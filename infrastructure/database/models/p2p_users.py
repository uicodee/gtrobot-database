from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class P2PUsers(BaseModel):
    __tablename__ = "p2p_users"

    user_id: Mapped[int] = mapped_column(BigInteger)
    profit_percent: Mapped[float] = mapped_column(Numeric, default=0)
    is_active: Mapped[bool] = mapped_column(Integer, default=True)
    is_active_exchanges: Mapped[bool] = mapped_column(Integer, default=True)
    exchanges: Mapped[str] = mapped_column(Text, default="0123")
