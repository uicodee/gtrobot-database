from .base import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserSymbols(BaseModel):
    __tablename__ = "user_symbols"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    symbol_id: Mapped[int] = mapped_column(Integer, ForeignKey("symbols.id"))
    tx_value: Mapped[int] = mapped_column(Integer, default=500000)
