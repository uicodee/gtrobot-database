from .base import BaseModel
from sqlalchemy import Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserReferrals(BaseModel):
    __tablename__ = "user_referrals"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    referral_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_transactions.id"), nullable=True
    )
    user_is_active: Mapped[bool] = mapped_column(Integer, default=False)
    active_bonus_transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_transactions.id"), nullable=True
    )
    current_ppc_level: Mapped[int] = mapped_column(Integer, default=1)
