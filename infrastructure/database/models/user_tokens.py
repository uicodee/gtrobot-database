from sqlalchemy import Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserTokens(BaseModel):
    __tablename__ = "user_tokens"

    user_id: Mapped[int] = mapped_column(BigInteger)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("subscription_orders.query_id"), unique=True, nullable=True
    )
    days: Mapped[int] = mapped_column(Integer)
    date: Mapped[int] = mapped_column(Integer)
