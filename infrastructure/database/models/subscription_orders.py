from sqlalchemy import String, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SubscriptionOrders(BaseModel):
    __tablename__ = "subscription_orders"

    query_id: Mapped[int] = mapped_column(Integer, unique=True)
    user_id: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String)
    total_amount: Mapped[float] = mapped_column(Numeric)
    invoice_payload: Mapped[str] = mapped_column(Text)
    shipping_option_id: Mapped[str] = mapped_column(String)
