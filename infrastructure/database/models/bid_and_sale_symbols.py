from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class BidAndSaleSymbols(BaseModel):
    __tablename__ = "bid_and_sale_symbols"

    name: Mapped[str] = mapped_column(Text, unique=True)
