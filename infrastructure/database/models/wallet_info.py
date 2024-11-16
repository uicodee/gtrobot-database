from sqlalchemy import Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class WalletInfo(BaseModel):
    __tablename__ = "wallet_info"

    wallet_id: Mapped[int] = mapped_column(Integer)
    mini_description: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    locale: Mapped[str] = mapped_column(String)
