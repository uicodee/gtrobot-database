from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Referrals(BaseModel):
    __tablename__ = "referrals"

    user_id: Mapped[int] = mapped_column(Integer)
    referral_user_id: Mapped[int] = mapped_column(Integer)
    referral_username: Mapped[str] = mapped_column(String)
    referral_reg_data: Mapped[int] = mapped_column(Integer)
