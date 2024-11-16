from sqlalchemy import Integer, Boolean, Float, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class KlinesUsers(BaseModel):
    __tablename__ = "klines_users"

    user_id: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    short_value: Mapped[float] = mapped_column(Float, default=0.0)
    long_value: Mapped[float] = mapped_column(Float, default=0.0)
