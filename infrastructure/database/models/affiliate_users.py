from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class AffiliateUsers(BaseModel):
    __tablename__ = "affiliate_users"

    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    user_name: Mapped[str] = mapped_column(Text)
    user_last_name: Mapped[str] = mapped_column(Text)
    user_number: Mapped[str] = mapped_column(Text)
    usdt_balance: Mapped[float] = mapped_column(Numeric, default=0)
    user_rating: Mapped[float] = mapped_column(Numeric, default=1)
    is_active: Mapped[bool] = mapped_column(Numeric, default=True)
