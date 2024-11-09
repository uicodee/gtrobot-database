from .base import BaseModel
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column


class Requests(BaseModel):
    __tablename__ = "requests"

    type: Mapped[str] = mapped_column(Text)
    source_id: Mapped[int] = mapped_column(Integer)
