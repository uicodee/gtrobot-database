from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import KlinesUsers, KlinesPairs


class KlinesDAO(BaseDAO[KlinesUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(KlinesUsers, session)

    async def get_active_klines_users(self, pair: str) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                KlinesUsers.user_id,
                KlinesPairs.bid_value,
                KlinesPairs.sale_value,
                KlinesPairs.pair
            ).join(KlinesPairs, KlinesPairs.user_id == KlinesUsers.user_id)
            .where(KlinesUsers.is_active == 1, KlinesPairs.pair == pair)
        )
        dict_keys = ['user_id', 'long_value', 'short_value', 'pair']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_active_klines_user_data(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(KlinesUsers.user_id).where(KlinesUsers.is_active == 1)
        )
        return [{'user_id': str(row[0])} for row in result.fetchall()]

    async def get_user_kline_pairs(self, user_id: int) -> List[str]:
        result = await self.session.execute(
            select(KlinesPairs.pair).where(KlinesPairs.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

    async def klines_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(KlinesUsers).where(KlinesUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def klines_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(KlinesUsers.is_active).where(KlinesUsers.user_id == user_id)
        )
        return bool(result.scalar())
