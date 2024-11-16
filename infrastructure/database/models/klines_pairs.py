from sqlalchemy import Integer, String, Numeric, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class KlinesPairs(BaseModel):
    __tablename__ = "klines_pairs"

    user_id: Mapped[int] = mapped_column(BigInteger)
    pair: Mapped[str] = mapped_column(String)
    bid_value: Mapped[float] = mapped_column(Numeric, default=500000)
    sale_value: Mapped[float] = mapped_column(Numeric, default=500000)
