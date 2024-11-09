from sqlalchemy import Text, Numeric, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class ActivatedUserSections(BaseModel):
    __tablename__ = "activated_user_sections"

    user_id: Mapped[int] = mapped_column(BigInteger)
    section: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[int] = mapped_column(Numeric)
