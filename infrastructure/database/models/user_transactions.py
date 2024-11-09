from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserTransactions(BaseModel):
    __tablename__ = "user_transactions"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Numeric)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_types.id"))
    on_holding: Mapped[bool] = mapped_column(Integer, default=True)
