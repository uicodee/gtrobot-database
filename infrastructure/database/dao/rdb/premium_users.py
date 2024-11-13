from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import PremiumUsers


class PremiumUsersDAO(BaseDAO[PremiumUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(PremiumUsers, session)

    async def get_premium_user_data(self, user_id: int) -> dict:
        result = await self.session.execute(
            select(
                PremiumUsers.tariff_plan,
                PremiumUsers.name,
                PremiumUsers.username,
                PremiumUsers.subscription_date,
                PremiumUsers.subscription_days,
                PremiumUsers.bonus_days,
                PremiumUsers.is_demo_subscription
            ).where(PremiumUsers.user_id == user_id)
        )
        dict_keys = ['tariff_plan', 'name', 'username', 'subscription_date',
                     'subscription_days', 'bonus_days', 'is_demo_subscription']
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_all_premium_users_data(self) -> List[dict]:
        result = await self.session.execute(
            select(
                PremiumUsers.user_id,
                PremiumUsers.tariff_plan,
                PremiumUsers.name,
                PremiumUsers.username,
                PremiumUsers.subscription_date,
                PremiumUsers.subscription_days,
                PremiumUsers.bonus_days
            )
        )
        dict_keys = ['user_id', 'tariff_plan', 'name', 'username', 'subscription_date', 'subscription_days', 'bonus_days']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def premium_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(PremiumUsers).where(PremiumUsers.user_id == user_id)
        )
        return result.fetchone() is not None
