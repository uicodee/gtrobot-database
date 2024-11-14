from .base import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class WalletsUsers(BaseModel):
    __tablename__ = "wallets_users"

    user_id: Mapped[int] = mapped_column(Integer)
    wallet_id: Mapped[int] = mapped_column(Integer)
