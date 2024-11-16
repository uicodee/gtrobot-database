from sqlalchemy import BigInteger, Integer, Text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Accounts(BaseModel):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(BigInteger)
    referral_token: Mapped[str] = mapped_column(Text)
    account_name: Mapped[str] = mapped_column(String, default="NoName")
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)
    bot_name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_error: Mapped[bool] = mapped_column(Boolean)
    date: Mapped[int] = mapped_column(Integer)
