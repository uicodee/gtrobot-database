from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UsersExchange(BaseModel):
    __tablename__ = "users_exchange"

    user_id: Mapped[int] = mapped_column(Integer)
    user_buy_usdt: Mapped[float] = mapped_column(Numeric, default=0.0)
    user_buy_usdt_date: Mapped[str] = mapped_column(String)
    user_request_number: Mapped[int] = mapped_column(Integer, default=0)
