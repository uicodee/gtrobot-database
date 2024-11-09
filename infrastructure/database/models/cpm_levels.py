from .base import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class CPMLevels(BaseModel):
    __tablename__ = "cpm_levels"

    min_views: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
