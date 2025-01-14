from .base import BaseModel
from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class SignalsUsers(BaseModel):
    __tablename__ = "signals_users"

    user_id: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Integer, default=True)
