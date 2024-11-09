from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class BalanceHistory(BaseModel):
    __tablename__ = "balance_history"

    user_id: Mapped[int] = mapped_column(Integer)
    balance: Mapped[float] = mapped_column(Numeric)
    crypto_currency: Mapped[str] = mapped_column(String)
    balance_date: Mapped[int] = mapped_column(Integer)
