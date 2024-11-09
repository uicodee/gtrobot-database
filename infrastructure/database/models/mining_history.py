from .base import BaseModel
from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class MiningHistory(BaseModel):
    __tablename__ = "mining_history"

    start_date: Mapped[int] = mapped_column(Integer)
    end_date: Mapped[int] = mapped_column(Integer)
    mining_type: Mapped[str] = mapped_column(Text, default="regular")
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
