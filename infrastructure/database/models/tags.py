from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Tags(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(Text)
    locale: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"), nullable=True)
