from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import SubscriptionOrders


class SubscriptionOrdersDAO(BaseDAO[SubscriptionOrders]):
    def __init__(self, session: AsyncSession):
        super().__init__(SubscriptionOrders, session)

    async def set_subscription_order(self, query_id: int, user_id: int, currency: str, total_amount: float,
                                     invoice_payload: str, shipping_option_id: str = None) -> int:
        stmt = insert(SubscriptionOrders).values(
            query_id=query_id,
            user_id=user_id,
            currency=currency,
            total_amount=total_amount,
            invoice_payload=invoice_payload,
            shipping_option_id=shipping_option_id
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.inserted_primary_key[0]

    async def del_subscription_order(self, subscription_order_id: int):
        await self.session.execute(
            delete(SubscriptionOrders).where(SubscriptionOrders.id == subscription_order_id)
        )
        await self.session.commit()
