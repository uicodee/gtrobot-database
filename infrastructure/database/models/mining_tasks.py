from .base import BaseModel
from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class MiningTasks(BaseModel):
    __tablename__ = 'mining_tasks'

    task_text: Mapped[str] = mapped_column(Text)
    task_link: Mapped[str] = mapped_column(Text)
    task_group_id: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
