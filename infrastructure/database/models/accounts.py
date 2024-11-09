from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Accounts(BaseModel):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(Integer)
    referral_token: Mapped[str] = mapped_column(Text)
    account_name: Mapped[str] = mapped_column(Text, default="NoName")
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str] = mapped_column(Text)
    bot_name: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Integer)
    is_error: Mapped[bool] = mapped_column(Integer)
    date: Mapped[int] = mapped_column(Integer)
