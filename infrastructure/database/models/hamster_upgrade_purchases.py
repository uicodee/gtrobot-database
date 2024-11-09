from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class HamsterUpgradePurchases(BaseModel):
    __tablename__ = "hamster_upgrade_purchases"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_accounts.id"))
    upgrade_id: Mapped[str] = mapped_column(Text)
    upgrade_name: Mapped[str] = mapped_column(Text)
    upgrade_level: Mapped[int] = mapped_column(Integer)
    upgrade_section: Mapped[str] = mapped_column(Text)
    upgrade_price: Mapped[float] = mapped_column(Numeric)
    date: Mapped[int] = mapped_column(Integer)
