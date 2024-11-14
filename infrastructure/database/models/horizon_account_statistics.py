from .base import BaseModel
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class HorizonAccountStatistics(BaseModel):
    __tablename__ = "horizon_account_statistics"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    last_sync_timestamp: Mapped[int] = mapped_column(Integer)
    last_tap_timestamp: Mapped[int] = mapped_column(Integer)
    last_boost_timestamp: Mapped[int] = mapped_column(Integer)
    boost_attempts: Mapped[int] = mapped_column(Integer)
    boost_taps: Mapped[int] = mapped_column(Integer)
    distance: Mapped[float] = mapped_column(Float)
    delta: Mapped[float] = mapped_column(Float)
    speed: Mapped[float] = mapped_column(Float)
    referrals_count: Mapped[int] = mapped_column(Integer)
    is_banned: Mapped[bool] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Integer)
    is_premium: Mapped[bool] = mapped_column(Integer)
