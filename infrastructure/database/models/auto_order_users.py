from sqlalchemy import Integer, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel


class AutoOrderUsers(BaseModel):
    __tablename__ = "auto_order_users"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    api_key: Mapped[str] = mapped_column(String, nullable=False)
    api_secret: Mapped[str] = mapped_column(String, nullable=False)
    api_passphrase: Mapped[str] = mapped_column(Text)
    user_exchange: Mapped[str] = mapped_column(
        String, default="Binance", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_trading_ban: Mapped[bool] = mapped_column(Boolean, default=False)
