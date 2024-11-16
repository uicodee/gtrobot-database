from .base import BaseModel
from sqlalchemy import Integer, Numeric, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class UserEarnings(BaseModel):
    __tablename__ = "user_earnings"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    mining_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_history.id"))
    earning: Mapped[float] = mapped_column(Numeric)
    earning_date: Mapped[int] = mapped_column(Integer)
