from .base import BaseModel
from sqlalchemy import Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserPromoCodes(BaseModel):
    __tablename__ = 'user_promo_codes'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    promo_code: Mapped[str] = mapped_column(Text)
    promo_code_sum: Mapped[int] = mapped_column(Integer)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    promo_code_date: Mapped[int] = mapped_column(Integer)
