from sqlalchemy import Numeric, String, Boolean, Integer
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class PremiumUsers(BaseModel):
    __tablename__ = 'premium_users'

    user_id: Mapped[int] = mapped_column(Numeric, unique=True, nullable=False)
    tariff_plan: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    subscription_date: Mapped[str] = mapped_column(String)
    subscription_days: Mapped[int] = mapped_column(Integer)
    is_demo_subscription: Mapped[bool] = mapped_column(Boolean, default=False)
    bonus_days: Mapped[int] = mapped_column(Integer, default=0)
