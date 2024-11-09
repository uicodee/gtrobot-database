from .base import BaseModel
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserVideos(BaseModel):
    __tablename__ = "user_videos"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    video_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("video_types.id"))
    video_id: Mapped[str] = mapped_column(Text, unique=True)
    stopped_at: Mapped[int] = mapped_column(Integer)
    moderated_at: Mapped[int] = mapped_column(Integer)
    is_accepted: Mapped[bool] = mapped_column(Integer, default=False)
