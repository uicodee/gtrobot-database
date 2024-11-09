from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class VideoTypes(BaseModel):
    __tablename__ = "video_types"

    type_name: Mapped[str] = mapped_column(Text)
