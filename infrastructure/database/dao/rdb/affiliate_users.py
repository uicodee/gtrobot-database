from typing import List

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    AffiliateUsers,
    AffiliateUsersHistory,
    AffiliateUsersWithdraw,
)


class AffiliateUsersDAO(BaseDAO[AffiliateUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(AffiliateUsers, session)

    async def get_affiliate_users_profile(self, user_id: int) -> dict:
        result = await self.session.execute(
            select(
                AffiliateUsers.user_name,
                AffiliateUsers.user_last_name,
                AffiliateUsers.user_number,
                AffiliateUsers.user_rating,
            ).where(AffiliateUsers.user_id == user_id)
        )
        dict_keys = ["user_name", "user_last_name", "user_number", "user_rating"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_affiliate_user_usdt_balance(self, user_id: int) -> float:
        result = await self.session.execute(
            select(AffiliateUsers.usdt_balance).where(AffiliateUsers.user_id == user_id)
        )
        return result.scalar()

    async def get_affiliate_user_history(self, user_id: int) -> List[dict]:
        result = await self.session.execute(
            select(
                AffiliateUsersHistory.user_id,
                AffiliateUsersHistory.user_earnings,
                AffiliateUsersHistory.promo_code,
                AffiliateUsersHistory.buyer_id,
                AffiliateUsersHistory.purchase_time,
            ).where(AffiliateUsersHistory.user_id == user_id)
        )
        dict_keys = [
            "user_id",
            "user_earnings",
            "promo_code",
            "buyer_id",
            "purchase_time",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_affiliate_user_withdraws(self, user_id: int) -> List[dict]:
        result = await self.session.execute(
            select(
                AffiliateUsersWithdraw.user_id,
                AffiliateUsersWithdraw.user_sum,
                AffiliateUsersWithdraw.wallet_address,
                AffiliateUsersWithdraw.withdraw_time,
                AffiliateUsersWithdraw.is_confirmed,
            ).where(AffiliateUsersWithdraw.user_id == user_id)
        )
        dict_keys = [
            "user_id",
            "user_sum",
            "wallet_address",
            "withdraw_time",
            "is_confirmed",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_affiliate_user_withdraw_data(
        self, user_id: int, withdraw_id: int
    ) -> dict:
        result = await self.session.execute(
            select(
                AffiliateUsersWithdraw.user_id,
                AffiliateUsersWithdraw.user_sum,
                AffiliateUsersWithdraw.wallet_address,
                AffiliateUsersWithdraw.withdraw_time,
                AffiliateUsersWithdraw.is_confirmed,
            ).where(
                AffiliateUsersWithdraw.user_id == user_id,
                AffiliateUsersWithdraw.id == withdraw_id,
            )
        )
        dict_keys = [
            "user_id",
            "user_sum",
            "wallet_address",
            "withdraw_time",
            "is_confirmed",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_active_affiliate_users_data(self) -> List[dict]:
        result = await self.session.execute(
            select(
                AffiliateUsers.user_id,
                AffiliateUsers.user_name,
                AffiliateUsers.user_last_name,
                AffiliateUsers.user_number,
                AffiliateUsers.user_rating,
            ).where(AffiliateUsers.is_active == 1)
        )
        dict_keys = [
            "user_id",
            "user_name",
            "user_last_name",
            "user_number",
            "user_rating",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def affiliate_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AffiliateUsers).where(AffiliateUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def affiliate_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AffiliateUsers.is_active).where(AffiliateUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def update_user_withdraw_usdt_request(self, user_id, withdraw_id, status):
        await self.session.execute(
            update(AffiliateUsersWithdraw)
            .where(AffiliateUsersWithdraw.user_id == user_id)
            .where(AffiliateUsersWithdraw.id == withdraw_id)
            .values(is_confirmed=status)
        )
        await self.session.commit()

    async def update_affiliate_user_usdt_balances(self, user_id, usdt_bonus):
        await self.session.execute(
            update(AffiliateUsers)
            .where(AffiliateUsers.user_id == user_id)
            .values(usdt_balance=AffiliateUsers.usdt_balance + usdt_bonus)
        )
        await self.session.commit()

    async def update_affiliate_user_status(self, user_id, is_active):
        await self.session.execute(
            update(AffiliateUsers)
            .where(AffiliateUsers.user_id == user_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def set_affiliate_user(
        self, user_id: int, user_name: str, user_last_name: str, user_number: str
    ):
        await self.session.execute(
            insert(AffiliateUsers).values(
                user_id=user_id,
                user_name=user_name,
                user_last_name=user_last_name,
                user_number=user_number,
            )
        )
        await self.session.commit()

    async def set_new_affiliate_user_income(
        self, user_id: int, user_earnings: int, promo_code: str, buyer_id: int
    ):
        await self.session.execute(
            insert(AffiliateUsersHistory).values(
                user_id=user_id,
                user_earnings=user_earnings,
                promo_code=promo_code,
                buyer_id=buyer_id,
            )
        )
        await self.session.commit()

    async def set_new_affiliate_user_withdraw(
        self, user_id: int, user_sum: int, wallet_address: str
    ):
        result = await self.session.execute(
            insert(AffiliateUsersWithdraw).values(
                user_id=user_id,
                user_sum=user_sum,
                wallet_address=wallet_address,
            )
        )
        await self.session.commit()

        return result.lastrowid
