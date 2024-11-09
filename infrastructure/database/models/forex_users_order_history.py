from sqlalchemy import Numeric, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ForexUsersOrderHistory(BaseModel):
    __tablename__ = "forex_users_order_history"

    user_id: Mapped[int] = mapped_column(Integer)
    order_type: Mapped[str] = mapped_column(Text)
    order_symbol: Mapped[str] = mapped_column(Text)
    order_volume: Mapped[float] = mapped_column(Numeric)
    order_tp_price: Mapped[float] = mapped_column(Numeric)
    order_sl_price: Mapped[float] = mapped_column(Numeric)
    order_price: Mapped[float] = mapped_column(Numeric)
    order_date: Mapped[int] = mapped_column(Integer)
    order_ticket: Mapped[int] = mapped_column(Integer)
    signal_id: Mapped[int] = mapped_column(Integer)
