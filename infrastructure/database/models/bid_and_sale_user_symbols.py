from .base import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class BidAndSaleUserSymbols(BaseModel):
    __tablename__ = "bid_and_sale_user_symbols"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bid_and_sale_users.user_id")
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bid_and_sale_symbols.id")
    )
    tx_value: Mapped[int] = mapped_column(Integer, default=500000)
