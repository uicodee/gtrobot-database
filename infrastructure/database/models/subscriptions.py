from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.database.models import BaseModel


class Subscriptions(BaseModel):
    __tablename__ = "subscriptions"

    name: Mapped[str] = mapped_column(String)
    stars_price: Mapped[int] = mapped_column(Integer)
    usd_price: Mapped[float] = mapped_column(Numeric, nullable=True)
    subscription_days: Mapped[int] = mapped_column(Integer)
