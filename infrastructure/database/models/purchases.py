from .base import BaseModel
from sqlalchemy import Integer, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class Purchases(BaseModel):
    __tablename__ = "purchases"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=True)
    provider: Mapped[str] = mapped_column(Text)
    tariff_plan: Mapped[str] = mapped_column(Text)
    total_amount: Mapped[int] = mapped_column(Integer)
    promo_code: Mapped[str] = mapped_column(Text, nullable=True)
    referral_user: Mapped[int] = mapped_column(Integer, nullable=True)
    purchase_time: Mapped[int] = mapped_column(Integer)
    is_purchase: Mapped[bool] = mapped_column(Integer, default=True)
