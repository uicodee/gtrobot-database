from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class AffiliateUsersHistory(BaseModel):
    __tablename__ = "affiliate_users_history"

    user_id: Mapped[int] = mapped_column(BigInteger)
    user_earnings: Mapped[float] = mapped_column(Numeric)
    promo_code: Mapped[str] = mapped_column(Text)
    buyer_id: Mapped[float] = mapped_column(Numeric)
    purchase_time: Mapped[int] = mapped_column(Numeric)
