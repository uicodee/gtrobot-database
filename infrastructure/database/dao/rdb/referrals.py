from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import Referrals


class ReferralsDAO(BaseDAO[Referrals]):
    def __init__(self, session: AsyncSession):
        super().__init__(Referrals, session)

    async def get_user_referral(self, user_id: int) -> List[dict]:
        result = await self.session.execute(
            select(
                Referrals.referral_user_id,
                Referrals.referral_username,
                Referrals.referral_reg_data
            ).where(Referrals.user_id == user_id)
        )
        dict_keys = ['referral_user_id', 'referral_username', 'referral_reg_data']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_user_referrer(self, user_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(Referrals.user_id).where(Referrals.referral_user_id == user_id)
        )
        return result.scalar()

    async def get_referrer_user(self, user_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(Referrals.user_id).where(Referrals.referral_user_id == user_id)
        )
        return result.scalar()

