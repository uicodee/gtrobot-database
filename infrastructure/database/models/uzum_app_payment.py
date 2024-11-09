from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UzumAppPayment(BaseModel):
    __tablename__ = "uzum_app_payment"

    phone_number: Mapped[str] = mapped_column(Text)
    plan: Mapped[str] = mapped_column(Text)
    total_amount: Mapped[float] = mapped_column(Numeric)
    transaction_id: Mapped[str] = mapped_column(Text)
    order_opening_time: Mapped[int] = mapped_column(Numeric)
    is_completed: Mapped[bool] = mapped_column(Numeric, default=False)
    provider: Mapped[str] = mapped_column(Text, default="UZUMSUM")
