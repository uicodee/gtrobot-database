from .base import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class BidAndSaleUsers(BaseModel):
    __tablename__ = "bid_and_sale_sale_users"

    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    is_active: Mapped[bool] = mapped_column(Integer, default=True)
