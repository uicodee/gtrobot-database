from sqlalchemy import Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel


class UserServices(BaseModel):
    __tablename__ = "user_services"

    user_id: Mapped[int] = mapped_column(BigInteger)
    service: Mapped[int] = mapped_column(Integer)
    token_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_tokens.id"))
