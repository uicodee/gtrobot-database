from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class MiningReferrals(BaseModel):
    __tablename__ = "mining_referrals"

    referrer_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    referral_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    referral_user_name: Mapped[str] = mapped_column(Text, nullable=True)
    referral_date: Mapped[int] = mapped_column(Integer)
