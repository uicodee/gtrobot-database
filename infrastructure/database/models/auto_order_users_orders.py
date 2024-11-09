from sqlalchemy import Text, Numeric, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class AutoOrderUsersOrders(BaseModel):
    __tablename__ = "auto_order_users_orders"

    user_name: Mapped[str] = mapped_column(Text, nullable=False)
    symbol: Mapped[str] = mapped_column(Text, nullable=False)
    entry_price: Mapped[float] = mapped_column(Numeric, nullable=False)
    is_short: Mapped[bool] = mapped_column(Boolean, nullable=False)
    position_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order_id: Mapped[str] = mapped_column(Text, nullable=False)
    order_time: Mapped[int] = mapped_column(Integer, nullable=False)
    order_amount: Mapped[float] = mapped_column(Numeric, nullable=False)
    stop: Mapped[float] = mapped_column(Numeric)
    take_profit: Mapped[float] = mapped_column(Numeric)
    leverage: Mapped[int] = mapped_column(Integer)
    is_spot_order: Mapped[bool] = mapped_column(Boolean, default=True)
    is_market: Mapped[bool] = mapped_column(Boolean, default=True)
    is_take_profit: Mapped[bool] = mapped_column(Boolean, default=False)
    order_status: Mapped[str] = mapped_column(Text, default="new", nullable=False)
