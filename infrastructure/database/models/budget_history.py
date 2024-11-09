from sqlalchemy import Numeric, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class BudgetHistory(BaseModel):
    __tablename__ = 'budget_history'

    budget: Mapped[float] = mapped_column(Numeric, default=1500)
    budget_type: Mapped[str] = mapped_column(Text, default='regular')
    budget_date: Mapped[int] = mapped_column(Integer)
    