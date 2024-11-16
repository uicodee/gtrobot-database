from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class Follow(BaseModel):
    __tablename__ = "follow"

    user_id: Mapped[int] = mapped_column(BigInteger)
    wallet_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    info: Mapped[str] = mapped_column(Text, nullable=True)
