from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.database.models import BaseModel


class ReplyMessages(BaseModel):
    __tablename__ = 'reply_messages'

    user_id: Mapped[int] = mapped_column(Integer)
    original_message_id: Mapped[int] = mapped_column(Integer)
    copy_message_id: Mapped[int] = mapped_column(Integer)
    reply_date: Mapped[int] = mapped_column(Integer)
    is_admin_reply: Mapped[bool] = mapped_column(Boolean, default=False)
