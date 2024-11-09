from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SocialNetworksLinks(BaseModel):
    __tablename__ = 'social_networks_links'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.user_id'))
    is_profile: Mapped[bool] = mapped_column(Boolean)
    user_link: Mapped[str] = mapped_column(String)
    date: Mapped[int] = mapped_column(Integer)
