from sqlalchemy import Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Videos(BaseModel):
    __tablename__ = "videos"

    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_videos.id"))
    title: Mapped[str] = mapped_column(Text)
    thumbnail: Mapped[str] = mapped_column(Text)
    duration: Mapped[float] = mapped_column(Numeric)
    video_url: Mapped[str] = mapped_column(Text)
    view_count: Mapped[int] = mapped_column(Integer)
    like_count: Mapped[int] = mapped_column(Integer)
    comment_count: Mapped[int] = mapped_column(Integer)
    current_cpm_level: Mapped[int] = mapped_column(
        Integer, ForeignKey("cpm_levels.id"), default=1
    )
    new_views: Mapped[int] = mapped_column(Integer, default=0)
    transaction_id: Mapped[int] = mapped_column(Integer)
