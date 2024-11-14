import typing
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    promo_code: Optional[str] = None
    bonus_days: Optional[int] = 0
    discount: Optional[float] = 0
    is_demo: Optional[bool] = False
    demo_days: Optional[int] = 0


class Subscription(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    stars_price: Optional[int] = None
    usd_price: Optional[float] = None
    subscription_days: Optional[int] = None
    services: Optional[list[int]] = None


class Root(BaseModel):
    user: User = None
    subscriptions: typing.List[Subscription] = None
