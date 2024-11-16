from sqlalchemy import Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Videos(BaseModel):
    __tablename__ = "videos"

    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_videos.id"))
    title: Mapped[str] = mapped_column(Text, nullable=True)
    thumbnail: Mapped[str] = mapped_column(Text, nullable=True)
    duration: Mapped[float] = mapped_column(Numeric, nullable=True)
    video_url: Mapped[str] = mapped_column(Text, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, nullable=True)
    like_count: Mapped[int] = mapped_column(Integer, nullable=True)
    comment_count: Mapped[int] = mapped_column(Integer, nullable=True)
    current_cpm_level: Mapped[int] = mapped_column(
        Integer, ForeignKey("cpm_levels.id"), default=1
    )
    new_views: Mapped[int] = mapped_column(Integer, default=0)
    transaction_id: Mapped[int] = mapped_column(Integer, nullable=True)
