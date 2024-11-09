from sqlalchemy import Integer, String, Numeric, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class Profiles(BaseModel):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    user_last_name: Mapped[str] = mapped_column(String, nullable=False)
    user_num: Mapped[str] = mapped_column(String, nullable=False)
    user_rating: Mapped[int] = mapped_column(Integer, default=1)
    user_doge_balance: Mapped[float] = mapped_column(Numeric, default=0.0)
    user_ton_balance: Mapped[float] = mapped_column(Numeric, default=0.0)
    user_gtu_balance: Mapped[float] = mapped_column(Numeric, default=0.0)
    is_request: Mapped[bool] = mapped_column(Boolean, default=False)
    is_terms_of_use: Mapped[bool] = mapped_column(Boolean, default=False)
    invite_link_id: Mapped[int] = mapped_column(Integer, default=0)
    invite_link: Mapped[str] = mapped_column(String, nullable=True)
