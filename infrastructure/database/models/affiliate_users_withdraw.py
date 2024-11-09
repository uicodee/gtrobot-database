from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class AffiliateUsersWithdraw(BaseModel):
    __tablename__ = 'affiliate_users_withdraw'

    user_id: Mapped[float] = mapped_column(Numeric)
    user_sum: Mapped[float] = mapped_column(Numeric)
    wallet_address: Mapped[str] = mapped_column(Text)
    withdraw_time: Mapped[int] = mapped_column(Numeric)
    is_confirmed: Mapped[bool] = mapped_column(Numeric, default=False)
