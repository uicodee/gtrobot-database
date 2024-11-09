from sqlalchemy import Boolean, BigInteger, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.database.models import BaseModel


class ReplyMessages(BaseModel):
    __tablename__ = "reply_messages"

    user_id: Mapped[int] = mapped_column(BigInteger)
    original_message_id: Mapped[int] = mapped_column(BigInteger)
    copy_message_id: Mapped[int] = mapped_column(BigInteger)
    reply_date: Mapped[int] = mapped_column(Numeric)
    is_admin_reply: Mapped[bool] = mapped_column(Boolean, default=False)
