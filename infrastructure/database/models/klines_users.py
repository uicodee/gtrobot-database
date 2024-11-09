from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class KlinesUsers(BaseModel):
    __tablename__ = "klines_users"

    user_id: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
