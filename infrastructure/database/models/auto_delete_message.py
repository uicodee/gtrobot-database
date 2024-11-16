from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class AutoDeleteMessage(BaseModel):
    __tablename__ = "autodelete_message"

    user_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(Integer)
    current_time: Mapped[int] = mapped_column(Integer)
