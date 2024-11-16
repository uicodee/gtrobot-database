from .base import BaseModel
from sqlalchemy import Integer, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class PersonalWalletAssets(BaseModel):
    __tablename__ = "personal_wallet_assets"

    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallet.id"), nullable=True)
    stock: Mapped[str] = mapped_column(Text, nullable=True)
    balance: Mapped[float] = mapped_column(Float, nullable=True)
