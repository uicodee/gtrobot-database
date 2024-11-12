from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String, default="start")
    user_quiz: Mapped[int] = mapped_column(Integer, default=0)
    locale: Mapped[str] = mapped_column(String, default="uz")
