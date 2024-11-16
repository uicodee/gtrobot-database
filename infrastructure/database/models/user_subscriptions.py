from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserSubscriptions(BaseModel):
    __tablename__ = "user_subscriptions"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    subscription: Mapped[str] = mapped_column(Text)
    purchase_date: Mapped[int] = mapped_column(Integer)
    end_subscription_date: Mapped[int] = mapped_column(Integer)
    order_id: Mapped[str] = mapped_column(Text, nullable=True)
    token_id: Mapped[str] = mapped_column(Text, nullable=True)
