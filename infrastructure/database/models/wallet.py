from .base import BaseModel
from sqlalchemy import Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(BaseModel):
    __tablename__ = "wallet"

    address: Mapped[str] = mapped_column(Text)
    last_block_number: Mapped[str] = mapped_column(Text)
    network: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallet.id"))
    is_available_free: Mapped[bool] = mapped_column(Integer, default=False)
    is_personal_wallet: Mapped[bool] = mapped_column(Integer, default=False)
