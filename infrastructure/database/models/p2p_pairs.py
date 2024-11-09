from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class P2PPairs(BaseModel):
    __tablename__ = 'p2p_pairs'

    profit: Mapped[float] = mapped_column(Numeric)
    asset_buy: Mapped[str] = mapped_column(Text)
    price_buy: Mapped[float] = mapped_column(Numeric)
    payment_buy: Mapped[str] = mapped_column(Text)
    asset_sell: Mapped[str] = mapped_column(Text)
    price_sell: Mapped[float] = mapped_column(Numeric)
    payment_sell: Mapped[str] = mapped_column(Text)
    exchange: Mapped[str] = mapped_column(Text)
    currency: Mapped[str] = mapped_column(Text)
    is_post: Mapped[bool] = mapped_column(Numeric, default=False)
