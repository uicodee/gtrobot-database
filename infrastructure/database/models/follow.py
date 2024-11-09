from .base import BaseModel
from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column


class Follow(BaseModel):
    __tablename__ = "follow"

    user_id: Mapped[int] = mapped_column(Integer)
    wallet_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    info: Mapped[str] = mapped_column(Text)
