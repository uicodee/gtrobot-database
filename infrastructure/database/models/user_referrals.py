from .base import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserReferrals(BaseModel):
    __tablename__ = "user_referrals"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    referral_user_id: Mapped[int] = mapped_column(Integer, unique=True)
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_transactions.id")
    )
    user_is_active: Mapped[bool] = mapped_column(Integer, default=False)
    active_bonus_transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_transactions.id")
    )
    current_ppc_level: Mapped[int] = mapped_column(Integer, default=1)
