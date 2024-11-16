from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UzumPayment(BaseModel):
    __tablename__ = "uzum_payment"

    user_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    last_operation_id: Mapped[str] = mapped_column(Text)
    order_id: Mapped[str] = mapped_column(Text)
    currency_code: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(Text, nullable=True)
    tariff_plan: Mapped[str] = mapped_column(Text)
    total_amount: Mapped[int] = mapped_column(Integer)
    promo_code: Mapped[str] = mapped_column(Text, nullable=True)
    order_opening_time: Mapped[int] = mapped_column(Numeric)
    is_completed: Mapped[bool] = mapped_column(Numeric, default=False)
    transaction_id: Mapped[str] = mapped_column(Text, nullable=True)
