from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class ForexUsers(BaseModel):
    __tablename__ = 'forex_users'

    user_id: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
