from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class HoldingBalances(BaseModel):
    __tablename__ = "holding_balances"

    user_id: Mapped[int] = mapped_column(Integer)
    crypto_currency: Mapped[str] = mapped_column(Text, default="usdt")
    balance: Mapped[float] = mapped_column(Numeric, default=0)
    is_withdrawn: Mapped[bool] = mapped_column(Boolean, default=False)
    holding_date: Mapped[int] = mapped_column(Integer)
