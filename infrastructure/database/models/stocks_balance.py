from .base import BaseModel
from sqlalchemy import Integer, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class StocksBalance(BaseModel):
    __tablename__ = "stocks_balance"

    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallet.id"))
    stock: Mapped[str] = mapped_column(Text)
    balance: Mapped[float] = mapped_column(Float)
    quote: Mapped[float] = mapped_column(Float)
