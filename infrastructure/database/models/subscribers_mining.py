from .base import BaseModel
from sqlalchemy import Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class SubscribersMining(BaseModel):
    __tablename__ = 'subscribers_mining'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    start_date: Mapped[int] = mapped_column(Integer)
    end_date: Mapped[int] = mapped_column(Integer)
    subscription: Mapped[str] = mapped_column(Text)
    end_message_sent: Mapped[bool] = mapped_column(Boolean, default=False)
