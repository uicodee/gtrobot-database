from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import UsersExchange


class UsersExchangeDAO(BaseDAO[UsersExchange]):
    def __init__(self, session: AsyncSession):
        super().__init__(UsersExchange, session)

    async def get_exchange_daily_user_buy_usdt(self, user_id: int) -> Optional[float]:
        result = await self.session.execute(
            select(UsersExchange.user_buy_usdt).where(UsersExchange.user_id == user_id)
        )
        return result.scalar()

    async def get_exchange_daily_user_buy_usdt_date(self, user_id: int) -> Optional[str]:
        result = await self.session.execute(
            select(UsersExchange.user_buy_usdt_date).where(UsersExchange.user_id == user_id)
        )
        return result.scalar()

    async def get_user_request_number(self, user_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(UsersExchange.user_request_number).where(UsersExchange.user_id == user_id)
        )
        return result.scalar()
