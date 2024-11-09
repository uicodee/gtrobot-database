from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class AdminSettings(BaseModel):
    __tablename__ = 'admin_settings'

    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    exchange_usdt_balance: Mapped[float] = mapped_column(Float)
    request_counter: Mapped[int] = mapped_column(Integer)
