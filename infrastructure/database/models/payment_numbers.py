from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class PaymentNumbers(BaseModel):
    __tablename__ = 'payment_numbers'

    user_id: Mapped[int] = mapped_column(Integer)
    user_number: Mapped[float] = mapped_column(Numeric)
