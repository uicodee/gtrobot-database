import time
from typing import List, Dict

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import SignalsUsers, Pairs, XAUUSDSignals


class SignalsDAO(BaseDAO[SignalsUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(SignalsUsers, session)

    async def get_active_signal_users(self, pair: str, timeframe: str) -> List[int]:
        result = await self.session.execute(
            select(SignalsUsers.user_id)
            .join(Pairs, Pairs.user_id == SignalsUsers.user_id)
            .where(
                SignalsUsers.is_active == 1,
                Pairs.pair == pair,
                Pairs.timeframe == timeframe,
            )
        )
        return list(set(row[0] for row in result.fetchall()))

    async def get_active_forex_signal_users(self, pair: str) -> List[int]:
        result = await self.session.execute(
            select(SignalsUsers.user_id)
            .join(Pairs, Pairs.user_id == SignalsUsers.user_id)
            .where(SignalsUsers.is_active == 1, Pairs.pair == pair)
        )
        return list(set(row[0] for row in result.fetchall()))

    async def get_all_active_signal_users(self) -> List[Dict[str, int]]:
        result = await self.session.execute(
            select(SignalsUsers.user_id).where(SignalsUsers.is_active == 1)
        )
        return [{"user_id": row[0]} for row in result.fetchall()]

    async def get_all_signal_users(self) -> List[int]:
        result = await self.session.execute(select(SignalsUsers.user_id))
        return [row[0] for row in result.fetchall()]

    async def get_signals_users(self, user_id: int) -> List[str]:
        result = await self.session.execute(
            select(Pairs.pair).where(Pairs.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

    async def get_last_xauusd_signal_types(self) -> Dict[str, float]:
        subquery = (
            select(XAUUSDSignals.timestamp)
            .where(XAUUSDSignals.is_entry == 1)
            .order_by(XAUUSDSignals.timestamp.desc())
            .limit(1)
        )
        result = await self.session.execute(
            select(XAUUSDSignals.type, XAUUSDSignals.price)
            .where(XAUUSDSignals.timestamp >= subquery)
            .order_by(XAUUSDSignals.timestamp)
        )
        signals = {}
        for row in result.fetchall():
            signals[row[0]] = row[1]
        return signals

    async def signals_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(SignalsUsers).where(SignalsUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def signals_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(SignalsUsers.is_active).where(SignalsUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def update_user_signal_active_status(self, user_id, is_active) -> None:
        await self.session.execute(
            update(SignalsUsers)
            .where(SignalsUsers.user_id == user_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def set_user_signal_profile(self, user_id):
        await self.session.execute(
            insert(SignalsUsers).values(user_id=user_id)
        )
        await self.session.commit()

    async def set_user_signal_data(self, user_id, pair, timeframes):
        await self.session.execute(
            insert(Pairs).values(user_id=user_id, pair=pair, timeframe=timeframes)
        )
        await self.session.commit()

    async def set_xauusd_signal(self, signal_type, price, is_entry, timestamp: int = None):
        if timestamp is None:
            timestamp = int(time.time())

        await self.session.execute(
            insert(XAUUSDSignals).values(type=signal_type, price=price, is_entry=is_entry, timestamp=timestamp)
        )
        await self.session.commit()

    async def del_user_signal_pair(self, user_id: int, pair: str):
        await self.session.execute(
            delete(Pairs).where(Pairs.user_id == user_id, Pairs.pair == pair)
        )
        await self.session.commit()

    async def del_all_xauusd_signals(self):
        await self.session.execute(
            delete(XAUUSDSignals)
        )
        await self.session.commit()
