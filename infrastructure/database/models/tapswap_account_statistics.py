from .base import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class TapswapAccountStatistics(BaseModel):
    __tablename__ = "tapswap_account_statistics"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    shares: Mapped[int] = mapped_column(Integer)
    ligue: Mapped[int] = mapped_column(Integer)
    energy_level: Mapped[int] = mapped_column(Integer)
    charge_level: Mapped[int] = mapped_column(Integer)
    boost_energy_count: Mapped[int] = mapped_column(Integer)
    boost_turbo_count: Mapped[int] = mapped_column(Integer)
    stat_taps: Mapped[int] = mapped_column(Integer)
    stat_ref_in: Mapped[int] = mapped_column(Integer)
    stat_ref_out: Mapped[int] = mapped_column(Integer)
    stat_ref_cnt: Mapped[int] = mapped_column(Integer)
    stat_earned: Mapped[int] = mapped_column(Integer)
    stat_reward: Mapped[int] = mapped_column(Integer)
    stat_spent: Mapped[int] = mapped_column(Integer)
    date: Mapped[int] = mapped_column(Integer)
