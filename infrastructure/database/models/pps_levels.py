from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class PPSLevels(BaseModel):
    __tablename__ = "pps_levels"

    min_sales: Mapped[int] = mapped_column(Integer)
