from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class MiningUsers(BaseModel):
    __tablename__ = "mining_users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    referral_code: Mapped[str] = mapped_column(Text)
    balance: Mapped[float] = mapped_column(Numeric, default=0)
    daily_mining_balance: Mapped[float] = mapped_column(Numeric, default=0)
    crypto_currency: Mapped[str] = mapped_column(Text, default="btc")
    user_profile_photo: Mapped[str] = mapped_column(Text, nullable=True)
    registration_date: Mapped[int] = mapped_column(Integer)
