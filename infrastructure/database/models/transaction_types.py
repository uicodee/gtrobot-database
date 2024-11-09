from .base import BaseModel
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column


class TransactionTypes(BaseModel):
    __tablename__ = "transaction_types"

    type_name: Mapped[str] = mapped_column(Text)
