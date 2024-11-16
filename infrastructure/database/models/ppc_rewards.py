from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class PPCRewards(BaseModel):
    __tablename__ = "ppc_rewards"

    ppc_level_id: Mapped[int] = mapped_column(Integer, ForeignKey("ppc_levels.id"))
    rate: Mapped[float] = mapped_column(Numeric)
    bonus_rate: Mapped[float] = mapped_column(Numeric, nullable=True)
    bonus_rate_min_activities: Mapped[int] = mapped_column(Integer, default=5)
