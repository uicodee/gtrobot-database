from typing import List, Optional, Dict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import Subscriptions, SubscriptionServices, SubscriptionOrders


class SubscriptionsDAO(BaseDAO[Subscriptions]):
    def __init__(self, session: AsyncSession):
        super().__init__(Subscriptions, session)

    async def get_subscriptions(self) -> List[Subscriptions]:
        async def get_subscription_services(subscription_id: int) -> List[int]:
            service_result = await self.session.execute(
                select(SubscriptionServices.service_id).where(SubscriptionServices.subscription_id == subscription_id)
            )
            return [service_id for service_id in service_result.scalars().all()]

        query_result = await self.session.execute(select(Subscriptions))
        subscriptions = [
            Subscriptions(
                id=row.id,
                name=row.name,
                usd_price=row.usd_price,
                subscription_days=row.subscription_days
            )
            for row in query_result.fetchall()
        ]

        for subscription in subscriptions:
            subscription.services = await get_subscription_services(subscription.id)

        return subscriptions

    async def get_subscription_order(self, query_id: int) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                SubscriptionOrders.query_id,
                SubscriptionOrders.user_id,
                SubscriptionOrders.currency,
                SubscriptionOrders.total_amount,
                SubscriptionOrders.invoice_payload,
                SubscriptionOrders.shipping_option_id,
                SubscriptionOrders.created_at
            ).where(SubscriptionOrders.query_id == query_id)
        )
        dict_keys = [
            'query_id',
            'user_id',
            'currency',
            'total_amount',
            'invoice_payload',
            'shipping_option_id',
            'created_at'
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def is_promo_code_already_used(self, user_id: int, promo_code: str) -> bool:
        search_string = f"%'code': '{promo_code}%'"
        result = await self.session.execute(
            select(func.count()).where(
                SubscriptionOrders.user_id == user_id,
                SubscriptionOrders.invoice_payload.ilike(search_string)
            )
        )
        return result.scalar() > 0
