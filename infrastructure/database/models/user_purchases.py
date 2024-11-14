from .base import BaseModel
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserPurchases(BaseModel):
    __tablename__ = "user_purchases"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    purchase_id: Mapped[int] = mapped_column(Integer, unique=True)
    purchase_sum: Mapped[float] = mapped_column(Numeric)
    current_pps_level: Mapped[int] = mapped_column(Integer, default=1)
    transaction_id: Mapped[int] = mapped_column(Integer)
