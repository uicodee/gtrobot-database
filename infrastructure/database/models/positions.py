from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Positions(BaseModel):
    __tablename__ = "positions"

    encrypted_uid: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Numeric)
    symbol: Mapped[str] = mapped_column(String)
    entry_price: Mapped[float] = mapped_column(Numeric)
    mark_price: Mapped[float] = mapped_column(Numeric)
    update_time_stamp: Mapped[int] = mapped_column(Integer)
    leverage: Mapped[int] = mapped_column(Integer)
    is_active_position: Mapped[bool] = mapped_column(Boolean, default=True)
    period_type: Mapped[str] = mapped_column(Text, default="DAILY")
    is_posted: Mapped[bool] = mapped_column(Numeric, default=False)
