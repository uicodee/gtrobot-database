from sqlalchemy import Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserWithdrawals(BaseModel):
    __tablename__ = "user_withdrawals"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    sum: Mapped[float] = mapped_column(Numeric)
    method: Mapped[str] = mapped_column(Text)
    cryptocurrency: Mapped[str] = mapped_column(Text)
    cryptocurrency_sum: Mapped[float] = mapped_column(Numeric)
    wallet_address: Mapped[str] = mapped_column(Text)
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_transactions.id")
    )
    moderated_at: Mapped[int] = mapped_column(Integer)
    is_accepted: Mapped[bool] = mapped_column(Integer, default=False)
