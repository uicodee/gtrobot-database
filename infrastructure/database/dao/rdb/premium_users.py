from typing import List

from sqlalchemy import select, update, insert, delete
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
                PremiumUsers.is_demo_subscription,
            ).where(PremiumUsers.user_id == user_id)
        )
        dict_keys = [
            "tariff_plan",
            "name",
            "username",
            "subscription_date",
            "subscription_days",
            "bonus_days",
            "is_demo_subscription",
        ]
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
                PremiumUsers.bonus_days,
            )
        )
        dict_keys = [
            "user_id",
            "tariff_plan",
            "name",
            "username",
            "subscription_date",
            "subscription_days",
            "bonus_days",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def premium_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(PremiumUsers).where(PremiumUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def update_premium_user_bonus_days(self, user_id: int, bonus_days: int):
        await self.session.execute(
            update(PremiumUsers).where(PremiumUsers.user_id == user_id).values(bonus_days=bonus_days)
        )
        await self.session.commit()

    async def update_premium_user_name(self, user_id: int, name: str, username: str):
        await self.session.execute(
            update(PremiumUsers)
            .where(PremiumUsers.user_id == user_id)
            .values(name=name, username=username)
        )
        await self.session.commit()

    async def update_premium_subscription(self, user_id: int, subscription: str):
        await self.session.execute(
            update(PremiumUsers).where(PremiumUsers.user_id == user_id).values(subscription_date=subscription)
        )
        await self.session.commit()

    async def set_premium_user(self, user_id, tariff_plan=None, subscription_date=None, name=None, username=None,
                               subscription_days=10, bonus_days=0, is_demo_subscription=False):
        await self.session.execute(
            insert(PremiumUsers).values(
                user_id=user_id,
                tariff_plan=tariff_plan,
                subscription_date=subscription_date,
                name=name,
                username=username,
                subscription_days=subscription_days,
                bonus_days=bonus_days,
                is_demo_subscription=is_demo_subscription,
            )
        )

    async def del_premium_user(self, user_id):
        await self.session.execute(delete(PremiumUsers).where(PremiumUsers.user_id == user_id))
        await self.session.commit()
