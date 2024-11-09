from .base import BaseModel
from sqlalchemy import Integer, Text, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class UserWithdraws(BaseModel):
    __tablename__ = 'user_withdraws'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    withdraw_source_currency: Mapped[str] = mapped_column(Text)
    withdraw_source_amount: Mapped[float] = mapped_column(Numeric)
    withdraw_currency: Mapped[str] = mapped_column(Text, default='USDT')
    withdraw_amount: Mapped[float] = mapped_column(Numeric)
    withdraw_address: Mapped[str] = mapped_column(Text)
    withdraw_date: Mapped[int] = mapped_column(Integer)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
