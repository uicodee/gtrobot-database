from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class ReferralActivities(BaseModel):
    __tablename__ = "referral_activities"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user_referrals.referral_user_id")
    )
    url: Mapped[str] = mapped_column(Text)
    remote_addr: Mapped[str] = mapped_column(Text)
