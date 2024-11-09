from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class MiningSubscriptionOrders(BaseModel):
    __tablename__ = 'mining_subscription_orders'

    query_id: Mapped[int] = mapped_column(Integer, unique=True)
    user_id: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(Text)
    total_amount: Mapped[float] = mapped_column(Numeric)
    invoice_payload: Mapped[str] = mapped_column(Text)
    shipping_option_id: Mapped[str] = mapped_column(Text)
    date: Mapped[int] = mapped_column(Integer)
