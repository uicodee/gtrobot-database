from sqlalchemy import String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class KursPlaceholders(BaseModel):
    __tablename__ = "kurs_placeholders"

    symbol: Mapped[str] = mapped_column(String)
    file_id: Mapped[str] = mapped_column(String)
