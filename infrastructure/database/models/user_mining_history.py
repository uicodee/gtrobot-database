from .base import BaseModel
from sqlalchemy import Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserMiningHistory(BaseModel):
    __tablename__ = "user_mining_history"

    mining_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_history.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    mining_date: Mapped[int] = mapped_column(Integer)
    mining_type: Mapped[str] = mapped_column(Text, default="regular")
    end_message_sent: Mapped[bool] = mapped_column(Boolean, default=False)
