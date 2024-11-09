from .base import BaseModel
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class HamsterAccountStatistics(BaseModel):
    __tablename__ = "hamster_account_statistics"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    max_taps: Mapped[int] = mapped_column(Integer)
    earn_per_tap: Mapped[int] = mapped_column(Integer)
    earn_passive_per_hour: Mapped[float] = mapped_column(Numeric)
    earn_passive_per_sec: Mapped[float] = mapped_column(Numeric)
    taps_recover_per_sec: Mapped[float] = mapped_column(Numeric)
    balance_coins: Mapped[float] = mapped_column(Numeric)
    referral_count: Mapped[int] = mapped_column(Integer, default=0)
    date: Mapped[int] = mapped_column(Integer)
