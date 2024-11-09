from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class PPSRewards(BaseModel):
    __tablename__ = "pps_rewards"

    pps_level_id: Mapped[int] = mapped_column(Integer, ForeignKey("pps_levels.id"))
    rate: Mapped[float] = mapped_column(Numeric)
    bonus_rate: Mapped[float] = mapped_column(Numeric)
    bonus_rate_min_price: Mapped[float] = mapped_column(Numeric)
