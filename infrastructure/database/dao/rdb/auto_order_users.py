from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    AutoOrderUsers,
    LeaderboardUsers,
    LeaderboardOrders,
    AutoOrderUsersOrders,
    Positions,
    ClosedLeaderboardOrders,
)


class AutoOrderUsersDAO(BaseDAO[AutoOrderUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(AutoOrderUsers, session)

    async def get_all_auto_order_users(self) -> List[int]:
        result = await self.session.execute(select(AutoOrderUsers.user_id))
        return [row[0] for row in result.fetchall()]

    async def get_active_auto_order_users_with_uid(
        self, encrypted_uid: str
    ) -> List[int]:
        result = await self.session.execute(
            select(AutoOrderUsers.user_id)
            .join(LeaderboardUsers, LeaderboardUsers.user_id == AutoOrderUsers.user_id)
            .where(
                AutoOrderUsers.is_active == 1,
                LeaderboardUsers.encrypted_uid == encrypted_uid,
            )
        )
        return [row[0] for row in result.fetchall()]

    async def get_auto_order_leaderboard_orders(self, user_id: int) -> List[int]:
        result = await self.session.execute(
            select(LeaderboardOrders.position_id).where(
                LeaderboardOrders.user_id == user_id
            )
        )
        return [row[0] for row in result.fetchall()]

    async def get_leaderboard_users_data(self, user_id: int) -> List[dict]:
        result = await self.session.execute(
            select(LeaderboardUsers.encrypted_uid, LeaderboardUsers.nick_name).where(
                LeaderboardUsers.user_id == user_id
            )
        )
        dict_keys = ["encrypted_uid", "nick_name"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_user_orders_history_data(
        self, user_id: int, is_market: int = 1
    ) -> List[dict]:
        result = await self.session.execute(
            select(
                AutoOrderUsersOrders.user_name,
                AutoOrderUsersOrders.entry_price,
                AutoOrderUsersOrders.symbol,
                AutoOrderUsersOrders.is_short,
                AutoOrderUsersOrders.order_amount,
                AutoOrderUsersOrders.stop,
                AutoOrderUsersOrders.take_profit,
                AutoOrderUsersOrders.leverage,
                AutoOrderUsersOrders.is_spot_order,
                AutoOrderUsersOrders.order_status,
            ).where(
                AutoOrderUsersOrders.user_id == user_id,
                AutoOrderUsersOrders.is_market == is_market,
                AutoOrderUsersOrders.is_spot_order == "0",
                AutoOrderUsersOrders.order_status.in_(["profit", "nonprofit"]),
            )
        )
        dict_keys = [
            "user_name",
            "entry_price",
            "symbol",
            "is_short",
            "order_amount",
            "stop",
            "take_profit",
            "leverage",
            "is_spot_order",
            "order_status",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_new_order(self) -> List[dict]:
        result = await self.session.execute(
            select(
                LeaderboardOrders.id,
                LeaderboardOrders.position_id,
                LeaderboardOrders.user_id,
            ).limit(1)
        )
        dict_keys = ["id", "position_id", "user_id"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_closed_leaderboard_orders(self) -> List[dict]:
        result = await self.session.execute(
            select(
                ClosedLeaderboardOrders.id,
                ClosedLeaderboardOrders.position_id,
                ClosedLeaderboardOrders.user_id,
                ClosedLeaderboardOrders.amount,
                ClosedLeaderboardOrders.symbol,
                ClosedLeaderboardOrders.entry_price,
                ClosedLeaderboardOrders.mark_price,
                ClosedLeaderboardOrders.leverage,
            ).limit(1)
        )
        dict_keys = [
            "id",
            "position_id",
            "user_id",
            "amount",
            "symbol",
            "entry_price",
            "mark_price",
            "leverage",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_all_auto_order_leaderboard_users(self) -> List[dict]:
        result = await self.session.execute(
            select(LeaderboardUsers.encrypted_uid, LeaderboardUsers.user_id)
        )
        dict_keys = ["encrypted_uid", "user_id"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_auto_order_users_with_unexist_position(self) -> List[dict]:
        result = await self.session.execute(
            select(
                AutoOrderUsers.user_id,
                AutoOrderUsers.api_key,
                AutoOrderUsers.api_secret,
                AutoOrderUsers.api_passphrase,
                AutoOrderUsers.user_exchange,
                AutoOrderUsersOrders.position_id,
                AutoOrderUsersOrders.order_id,
                AutoOrderUsersOrders.is_spot_order,
                AutoOrderUsersOrders.is_market,
                AutoOrderUsersOrders.order_amount,
                AutoOrderUsersOrders.symbol,
                AutoOrderUsersOrders.is_short,
            ).outerjoin(
                AutoOrderUsersOrders,
                AutoOrderUsersOrders.user_id == AutoOrderUsers.user_id,
            )
        )
        dict_keys = [
            "user_id",
            "api_key",
            "api_secret",
            "api_passphrase",
            "user_exchange",
            "position_id",
            "orderId",
            "is_spot_order",
            "is_market",
            "order_amount",
            "symbol",
            "is_short",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_active_auto_order_users(self) -> List[dict]:
        result = await self.session.execute(
            select(
                AutoOrderUsers.user_id,
                AutoOrderUsers.api_key,
                AutoOrderUsers.api_secret,
            ).where(AutoOrderUsers.is_active == 1)
        )
        dict_keys = ["user_id", "api_key", "api_secret"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_users_with_current_position_id(self, position_id: int) -> List[int]:
        result = await self.session.execute(
            select(AutoOrderUsersOrders.user_id).where(
                AutoOrderUsersOrders.position_id == position_id
            )
        )
        return [row[0] for row in result.fetchall()]

    async def get_auto_order_new_positions(self) -> List[dict]:
        result = await self.session.execute(
            select(
                AutoOrderUsers.user_id,
                AutoOrderUsers.api_key,
                AutoOrderUsers.api_secret,
                AutoOrderUsers.api_passphrase,
                AutoOrderUsers.user_exchange,
                AutoOrderUsersOrders.position_id,
                AutoOrderUsersOrders.order_id,
                AutoOrderUsersOrders.is_spot_order,
                AutoOrderUsersOrders.is_market,
                AutoOrderUsersOrders.symbol,
                AutoOrderUsersOrders.order_time,
                AutoOrderUsersOrders.order_status,
                AutoOrderUsersOrders.is_take_profit,
            )
            .join(
                AutoOrderUsersOrders,
                AutoOrderUsersOrders.user_id == AutoOrderUsers.user_id,
            )
            .where(AutoOrderUsersOrders.order_status == "new")
        )
        dict_keys = [
            "user_id",
            "api_key",
            "api_secret",
            "api_passphrase",
            "user_exchange",
            "position_id",
            "orderId",
            "is_spot_order",
            "is_market",
            "symbol",
            "order_time",
            "order_status",
            "is_take_profit",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_user_data(self, user_id: int) -> dict:
        result = await self.session.execute(
            select(
                AutoOrderUsers.api_key,
                AutoOrderUsers.api_secret,
                AutoOrderUsers.api_passphrase,
                AutoOrderUsers.user_exchange,
            ).where(AutoOrderUsers.user_id == user_id)
        )
        dict_keys = ["api_key", "api_secret", "api_passphrase", "user_exchange"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_auto_order_trading_ban_status(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AutoOrderUsers.is_trading_ban).where(
                AutoOrderUsers.user_id == user_id
            )
        )
        return bool(result.scalar())

    async def auto_order_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AutoOrderUsers).where(AutoOrderUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def auto_order_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AutoOrderUsers.is_active).where(AutoOrderUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def auto_order_leaderboard_user_position_exists(
        self, encrypted_uid: str, entry_price: float, update_time_stamp: int
    ) -> bool:
        result = await self.session.execute(
            select(Positions).where(
                Positions.encrypted_uid == encrypted_uid,
                Positions.entry_price == entry_price,
                Positions.update_time_stamp == update_time_stamp,
            )
        )
        return result.fetchone() is not None

    async def get_auto_order_user_nonprofit_positions_count(self, user_id: int) -> int:
        result = await self.session.execute(
            select(AutoOrderUsersOrders.order_status).where(
                AutoOrderUsersOrders.user_id == user_id,
                AutoOrderUsersOrders.is_market == 1,
            )
        )
        statuses = [row[0] for row in result.fetchall()]
        max_nonprofit_count = 0
        current_count = 0

        for status in statuses:
            if status == "nonprofit":
                current_count += 1
                max_nonprofit_count = max(max_nonprofit_count, current_count)
            elif status == "profit":
                current_count = 0

        return max_nonprofit_count
