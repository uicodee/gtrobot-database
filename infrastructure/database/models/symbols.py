from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Symbols(BaseModel):
    __tablename__ = "symbols"

    name: Mapped[str] = mapped_column(Text, unique=True)
