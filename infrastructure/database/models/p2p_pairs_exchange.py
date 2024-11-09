from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class P2PPairsExchange(BaseModel):
    __tablename__ = "p2p_pairs_exchange"

    profit: Mapped[float] = mapped_column(Numeric)
    asset: Mapped[str] = mapped_column(Text)
    exchange_buy: Mapped[str] = mapped_column(Text)
    price_buy: Mapped[float] = mapped_column(Numeric)
    exchange_sell: Mapped[str] = mapped_column(Text)
    price_sell: Mapped[float] = mapped_column(Numeric)
    is_post: Mapped[bool] = mapped_column(Numeric, default=False)
