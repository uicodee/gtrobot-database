from .base import BaseModel
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class UserAPI(BaseModel):
    __tablename__ = "user_api"

    user_id: Mapped[int] = mapped_column(Integer)
    api_key: Mapped[str] = mapped_column(String)
    api_secret: Mapped[str] = mapped_column(String)
    api_passphrase: Mapped[str] = mapped_column(Text)
    user_exchange: Mapped[str] = mapped_column(Text, default="Binance")
