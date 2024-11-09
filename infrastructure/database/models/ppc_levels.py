from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class PPCLevels(BaseModel):
    __tablename__ = "ppc_levels"

    min_clicks: Mapped[int] = mapped_column(Integer)
