from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class CoursePlaceholders(BaseModel):
    __tablename__ = "kurs_placeholders"

    symbol: Mapped[str] = mapped_column(String)
    file_id: Mapped[str] = mapped_column(String)
