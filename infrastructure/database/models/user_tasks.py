from .base import BaseModel
from sqlalchemy import Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserTasks(BaseModel):
    __tablename__ = "user_tasks"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_tasks.id"))
    completion_date: Mapped[int] = mapped_column(Integer)
