from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class PlatformVideoIDs(BaseModel):
    __tablename__ = "platform_video_ids"

    user_video_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_videos.id"))
    video_id: Mapped[str] = mapped_column(Text, unique=True)
