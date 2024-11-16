from sqlalchemy import Integer, Numeric, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UsersExchange(BaseModel):
    __tablename__ = "users_exchange"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_buy_usdt: Mapped[float] = mapped_column(Numeric, default=0.0, nullable=True)
    user_buy_usdt_date: Mapped[str] = mapped_column(String, nullable=True)
    user_request_number: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
