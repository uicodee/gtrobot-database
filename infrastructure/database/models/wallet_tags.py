from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class WalletTags(BaseModel):
    __tablename__ = "wallet_tags"

    wallet_id: Mapped[int] = mapped_column(Integer)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"))
