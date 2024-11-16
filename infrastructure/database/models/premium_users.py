from sqlalchemy import String, Boolean, Integer, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class PremiumUsers(BaseModel):
    __tablename__ = "premium_users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    tariff_plan: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    subscription_date: Mapped[str] = mapped_column(String, nullable=True)
    subscription_days: Mapped[int] = mapped_column(Integer, nullable=True)
    is_demo_subscription: Mapped[bool] = mapped_column(Boolean, default=False)
    bonus_days: Mapped[int] = mapped_column(Integer, default=0)
