from sqlalchemy import String, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SubscriptionOrders(BaseModel):
    __tablename__ = "subscription_orders"

    query_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String)
    total_amount: Mapped[float] = mapped_column(Numeric)
    invoice_payload: Mapped[str] = mapped_column(Text)
    shipping_option_id: Mapped[str] = mapped_column(String, nullable=True)
