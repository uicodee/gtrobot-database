from sqlalchemy import String, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Referrals(BaseModel):
    __tablename__ = "referrals"

    user_id: Mapped[int] = mapped_column(BigInteger)
    referral_user_id: Mapped[int] = mapped_column(BigInteger)
    referral_username: Mapped[str] = mapped_column(String, nullable=True)
    referral_reg_data: Mapped[int] = mapped_column(Numeric)
