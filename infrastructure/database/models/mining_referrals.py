from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class MiningReferrals(BaseModel):
    __tablename__ = "mining_referrals"

    referrer_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    referral_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    referral_user_name: Mapped[str] = mapped_column(Text)
    referral_date: Mapped[int] = mapped_column(Integer)
