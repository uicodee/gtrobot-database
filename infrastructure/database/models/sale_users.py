from .base import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class SaleUsers(BaseModel):
    __tablename__ = "sale_users"

    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    is_active: Mapped[bool] = mapped_column(Integer, default=True)
