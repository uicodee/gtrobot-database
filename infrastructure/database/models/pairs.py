from .base import BaseModel
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column


class Pairs(BaseModel):
    __tablename__ = "pairs"

    user_id: Mapped[int] = mapped_column(Integer)
    pair: Mapped[str] = mapped_column(Text, default="BTC/USDT")
    timeframe: Mapped[int] = mapped_column(Integer)
