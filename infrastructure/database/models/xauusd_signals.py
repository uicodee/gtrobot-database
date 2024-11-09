from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class XAUUSDSignals(BaseModel):
    __tablename__ = 'xauusd_signals'

    type: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric)
    is_entry: Mapped[bool] = mapped_column(Numeric, default=True)
    timestamp: Mapped[int] = mapped_column(Numeric)
