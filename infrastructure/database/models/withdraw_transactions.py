from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class WithdrawTransactions(BaseModel):
    __tablename__ = 'withdraw_transactions'

    withdraw_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_withdraws.id'))
    transaction_id: Mapped[str] = mapped_column(Text)
    transaction_date: Mapped[int] = mapped_column(Integer)
