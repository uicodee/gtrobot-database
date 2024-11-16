from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserOrders(BaseModel):
    __tablename__ = "user_orders"

    wallet_address: Mapped[str] = mapped_column(Text)
    symbol: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(BigInteger)
    order_id: Mapped[str] = mapped_column(Text)
    order_time: Mapped[int] = mapped_column(Integer)
    order_amount: Mapped[float] = mapped_column(Numeric)
    is_spot_order: Mapped[bool] = mapped_column(Integer, default=True)
    is_market: Mapped[bool] = mapped_column(Integer, default=True)
