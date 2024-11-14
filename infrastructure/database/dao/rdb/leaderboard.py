import time
from typing import List, Dict, Optional

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    LeaderboardUsers, LeaderboardOrders, LeaderboardIDs,
    LeaderboardsData, LeaderboardPositions, ClosedLeaderboardOrders
)


class LeaderboardDAO(BaseDAO[LeaderboardUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(LeaderboardUsers, session)

    async def get_auto_order_leaderboard_users(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                LeaderboardUsers.encrypted_uid,
                LeaderboardUsers.nick_name,
                LeaderboardUsers.is_new_profile,
            )
        )
        dict_keys = ['encrypted_uid', 'nick_name', 'is_new_profile']
        user_data = [dict(zip(dict_keys, data)) for data in result.fetchall()]
        return user_data

    async def get_leaderboard_nick_name(self, encrypted_uid: str) -> Optional[str]:
        result = await self.session.execute(
            select(LeaderboardUsers.nick_name).where(LeaderboardUsers.encrypted_uid == encrypted_uid)
        )
        nick_name = result.scalar()
        return nick_name

    async def get_leaderboard_position(self, position_id: int) -> Dict[str, float]:
        result = await self.session.execute(
            select(
                LeaderboardPositions.encrypted_uid,
                LeaderboardPositions.symbol,
                LeaderboardPositions.entry_price,
                LeaderboardPositions.mark_price,
                LeaderboardPositions.amount,
                LeaderboardPositions.leverage,
                LeaderboardPositions.update_time_stamp,
            ).where(LeaderboardPositions.id == position_id)
        )

        dict_keys = ['encrypted_uid', 'symbol', 'entry_price', 'mark_price', 'amount', 'leverage', 'update_time_stamp']
        position_data = dict(zip(dict_keys, result.fetchone())) if result.fetchone() else {}
        return position_data

    async def get_leaderboard_users(self, period_type: str) -> Dict[str, str]:
        result = await self.session.execute(
            select(LeaderboardUsers.nick_name, LeaderboardUsers.encrypted_uid)
            .where(LeaderboardUsers.period_type == period_type)
            .order_by(LeaderboardUsers.rank)
        )

        users = {user[0]: user[1] for user in result.fetchall()}
        return users

    async def get_leaderboard_user_positions(self, encrypted_uid: str) -> List[Dict[str, float]]:
        result = await self.session.execute(
            select(
                LeaderboardPositions.symbol,
                LeaderboardPositions.entry_price,
                LeaderboardPositions.mark_price,
                LeaderboardPositions.amount,
                LeaderboardPositions.leverage
            ).where(
                LeaderboardPositions.encrypted_uid == encrypted_uid,
                LeaderboardPositions.is_active_position == True
            )
        )
        return [{'symbol': row[0], 'entry_price': row[1], 'mark_price': row[2], 'amount': row[3], 'leverage': row[4]} for row in result.fetchall()]

    async def get_leaderboard_user_position(self, position_id: int) -> List[Dict[str, float]]:
        result = await self.session.execute(
            select(
                LeaderboardPositions.encrypted_uid,
                LeaderboardPositions.symbol,
                LeaderboardPositions.entry_price,
                LeaderboardPositions.mark_price,
                LeaderboardPositions.amount,
                LeaderboardPositions.leverage
            ).where(LeaderboardPositions.id == position_id)
        )
        dict_keys = ['encrypted_uid', 'symbol', 'entry_price', 'mark_price', 'amount', 'leverage']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_inactive_leaderboard_user_positions(self, period_type: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                LeaderboardPositions.id,
                LeaderboardPositions.symbol,
                LeaderboardPositions.entry_price,
                LeaderboardPositions.mark_price,
                LeaderboardPositions.amount,
                LeaderboardPositions.leverage
            ).where(
                LeaderboardPositions.period_type == period_type,
                LeaderboardPositions.is_active_position == False
            )
        )
        dict_keys = ['position_id', 'symbol', 'entry_price', 'mark_price', 'amount', 'leverage']
        return [dict(zip(dict_keys, map(str, row))) for row in result.fetchall()]

    async def get_not_posted_leaderboard_positions(self) -> List[Dict[str, float]]:
        result = await self.session.execute(
            select(
                LeaderboardPositions.id,
                LeaderboardPositions.encrypted_uid,
                LeaderboardPositions.symbol,
                LeaderboardPositions.entry_price,
                LeaderboardPositions.mark_price,
                LeaderboardPositions.amount,
                LeaderboardPositions.leverage,
                LeaderboardPositions.update_time_stamp,
                LeaderboardPositions.period_type
            ).where(
                LeaderboardPositions.is_active_position == True,
                LeaderboardPositions.is_posted == False
            )
        )
        dict_keys = ['position_id', 'encrypted_uid', 'symbol', 'entry_price', 'mark_price', 'amount', 'leverage', 'update_time_stamp', 'period_type']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def leaderboard_user_exists_with_period(self, encrypted_uid: str, period_type: int) -> bool:
        result = await self.session.execute(
            select(LeaderboardUsers).where(
                LeaderboardUsers.encrypted_uid == encrypted_uid,
                LeaderboardUsers.period_type == period_type
            )
        )
        return result.fetchone() is not None

    async def leaderboard_user_position_exists(self, encrypted_uid: str, entry_price: float, update_time_stamp: int, period_type: int) -> bool:
        result = await self.session.execute(
            select(LeaderboardPositions).where(
                LeaderboardPositions.encrypted_uid == encrypted_uid,
                LeaderboardPositions.entry_price == entry_price,
                LeaderboardPositions.update_time_stamp == update_time_stamp,
                LeaderboardPositions.period_type == period_type
            )
        )
        return result.fetchone() is not None

    async def leaderboard_position_exists(self, position_id: int) -> bool:
        result = await self.session.execute(
            select(LeaderboardPositions).where(LeaderboardPositions.id == position_id)
        )
        return result.fetchone() is not None

    async def leaderboard_user_exists(self, encrypted_uid: str) -> bool:
        result = await self.session.execute(
            select(LeaderboardUsers).where(LeaderboardUsers.encrypted_uid == encrypted_uid)
        )
        return result.fetchone() is not None

    async def similar_position_exists(self, encrypted_uid: str, entry_price: float, symbol: str, period_type: int) -> bool:
        current_time = int(time.time()) - 300
        result = await self.session.execute(
            select(LeaderboardPositions).where(
                LeaderboardPositions.encrypted_uid == encrypted_uid,
                ((LeaderboardPositions.entry_price - entry_price).abs() / entry_price * 100 < 2) |
                (LeaderboardPositions.update_time_stamp > current_time),
                LeaderboardPositions.symbol == symbol,
                LeaderboardPositions.period_type == period_type
            )
        )
        return result.fetchone() is not None

    async def update_all_leaderboard_user_positions(self, period_type: int, is_active_position: bool = False):
        await self.session.execute(
            update(LeaderboardPositions)
            .where(LeaderboardPositions.period_type == period_type)
            .values(is_active_position=is_active_position)
        )
        await self.session.commit()

    async def update_all_leaderboard_users(self, period_type: int, is_active_user: bool = False):
        await self.session.execute(
            update(LeaderboardUsers)
            .where(LeaderboardUsers.period_type == period_type)
            .values(is_active_user=is_active_user)
        )
        await self.session.commit()

    async def update_rank_leaderboard_user(self, encrypted_uid: str, rank: int, is_active_user: bool, period_type: int):
        await self.session.execute(
            update(LeaderboardUsers)
            .where(
                LeaderboardUsers.encrypted_uid == encrypted_uid,
                LeaderboardUsers.period_type == period_type
            )
            .values(rank=rank, is_active_user=is_active_user)
        )
        await self.session.commit()

    async def update_leaderboard_user_position(
        self, encrypted_uid: str, entry_price: float, mark_price: float,
        update_time_stamp: int, is_active_position: bool, period_type: int
    ):
        await self.session.execute(
            update(LeaderboardPositions)
            .where(
                LeaderboardPositions.encrypted_uid == encrypted_uid,
                LeaderboardPositions.entry_price == entry_price,
                LeaderboardPositions.update_time_stamp == update_time_stamp,
                LeaderboardPositions.period_type == period_type
            )
            .values(is_active_position=is_active_position, mark_price=mark_price)
        )
        await self.session.commit()

    async def update_is_posted_leaderboard_position(self, position_id: int, is_posted: bool = True):
        await self.session.execute(
            update(LeaderboardPositions)
            .where(LeaderboardPositions.id == position_id)
            .values(is_posted=is_posted)
        )
        await self.session.commit()

    async def delete_all_inactive_leaderboard_user_positions(self, period_type: int):
        await self.session.execute(
            delete(LeaderboardPositions)
            .where(
                LeaderboardPositions.is_active_position == False,
                LeaderboardPositions.period_type == period_type
            )
        )
        await self.session.commit()

    async def delete_all_inactive_leaderboard_users(self, period_type: int):
        await self.session.execute(
            delete(LeaderboardUsers)
            .where(
                LeaderboardUsers.is_active_user == False,
                LeaderboardUsers.period_type == period_type
            )
        )
        await self.session.commit()
