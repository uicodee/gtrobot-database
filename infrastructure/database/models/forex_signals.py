from sqlalchemy import Text, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel


class ForexSignals(BaseModel):
    __tablename__ = "forex_signals"

    symbol: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric)
    parent_signal_id: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[int] = mapped_column(Integer)
