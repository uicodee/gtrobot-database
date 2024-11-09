from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SubscriptionServices(BaseModel):
    __tablename__ = "subscription_services"

    subscription_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscriptions.id")
    )
    service_id: Mapped[int] = mapped_column(Integer)
