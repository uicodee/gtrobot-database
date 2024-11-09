from .base import BaseModel
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class CPMRewards(BaseModel):
    __tablename__ = "cpm_rewards"

    cpm_level_id: Mapped[int] = mapped_column(Integer, ForeignKey("cpm_levels.id"))
    video_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("video_types.id"))
    reward: Mapped[float] = mapped_column(Numeric)
