from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserExchanges(BaseModel):
    __tablename__ = 'user_exchanges'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    from_currency: Mapped[str] = mapped_column(Text)
    to_currency: Mapped[str] = mapped_column(Text)
    from_balance: Mapped[float] = mapped_column(Numeric)
    to_balance: Mapped[float] = mapped_column(Numeric)
    exchange_date: Mapped[int] = mapped_column(Integer)
