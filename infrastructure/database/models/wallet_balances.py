from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class WalletBalances(BaseModel):
    __tablename__ = "wallet_balances"

    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallet.id"))
    balance: Mapped[float] = mapped_column(Numeric)
