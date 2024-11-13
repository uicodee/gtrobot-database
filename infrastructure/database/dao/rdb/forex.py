from typing import List, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    ForexUsers,
    UsersForexAPI,
    ForexSignals,
    ForexUsersOrderHistory,
)


class ForexDAO(BaseDAO[ForexUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(ForexUsers, session)

    async def get_forex_user_api(self, user_id: int) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                UsersForexAPI.user_id,
                UsersForexAPI.user_login,
                UsersForexAPI.user_password,
                UsersForexAPI.user_server,
            ).where(UsersForexAPI.user_id == user_id)
        )
        dict_keys = ["user_id", "user_login", "user_password", "user_server"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_last_forex_parent_signal_id(self) -> Optional[int]:
        result = await self.session.execute(
            select(ForexSignals.id)
            .where(ForexSignals.parent_signal_id.is_(None))
            .order_by(ForexSignals.timestamp.desc())
            .limit(1)
        )
        return result.scalar()

    async def get_active_forex_users_data(self) -> List[Dict[str, Optional[str]]]:
        result = await self.session.execute(
            select(
                ForexUsers.user_id,
                UsersForexAPI.user_login,
                UsersForexAPI.user_password,
                UsersForexAPI.user_server,
            )
            .join(UsersForexAPI, UsersForexAPI.user_id == ForexUsers.user_id)
            .where(ForexUsers.is_active == 1)
        )
        dict_keys = ["user_id", "user_login", "user_password", "user_server"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_forex_signals(self, parent_signal_id: int) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                ForexSignals.id,
                ForexSignals.symbol,
                ForexSignals.type,
                ForexSignals.price,
                ForexSignals.parent_signal_id,
                ForexSignals.timestamp,
            ).where(
                (ForexSignals.parent_signal_id == parent_signal_id)
                | (ForexSignals.id == parent_signal_id)
            )
        )
        dict_keys = [
            "id",
            "symbol",
            "type",
            "price",
            "parent_signal_id",
            "zone",
            "timestamp",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_forex_users_order_history(self, user_id: int) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                ForexUsersOrderHistory.user_id,
                ForexUsersOrderHistory.order_type,
                ForexUsersOrderHistory.order_symbol,
                ForexUsersOrderHistory.order_volume,
                ForexUsersOrderHistory.order_tp_price,
                ForexUsersOrderHistory.order_sl_price,
                ForexUsersOrderHistory.order_price,
                ForexUsersOrderHistory.order_date,
                ForexUsersOrderHistory.signal_id,
            ).where(ForexUsersOrderHistory.user_id == user_id)
        )
        dict_keys = [
            "user_id",
            "order_type",
            "order_symbol",
            "order_volume",
            "order_tp_price",
            "order_sl_price",
            "order_price",
            "order_date",
            "signal_id",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_forex_users_order_tickets(
        self, parent_signal_id: int
    ) -> Dict[int, Dict[str, any]]:
        result = await self.session.execute(
            select(
                ForexUsersOrderHistory.user_id,
                ForexUsersOrderHistory.order_ticket,
                ForexUsersOrderHistory.order_volume,
                ForexUsersOrderHistory.order_type,
            ).where(ForexUsersOrderHistory.signal_id == parent_signal_id)
        )
        tickets_data = {}
        for row in result.fetchall():
            user_id = row[0]
            if user_id not in tickets_data:
                tickets_data[user_id] = {"tickets": [], "volume": 0, "order_type": ""}
            tickets_data[user_id]["tickets"].append(row[1])
            tickets_data[user_id]["volume"] = row[2]
            tickets_data[user_id]["order_type"] = row[3]
        return tickets_data

    async def forex_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(ForexUsers).where(ForexUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def forex_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(ForexUsers.is_active).where(ForexUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def forex_user_api_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(UsersForexAPI).where(UsersForexAPI.user_id == user_id)
        )
        return result.fetchone() is not None

    async def forex_signal_is_close(self, parent_signal_id: int) -> bool:
        result = await self.session.execute(
            select(ForexSignals).where(
                ForexSignals.parent_signal_id == parent_signal_id,
                ForexSignals.type == "close_all",
            )
        )
        return result.fetchone() is not None

    async def is_parent_signal_id(self, signal_id: int) -> bool:
        result = await self.session.execute(
            select(ForexSignals).where(
                ForexSignals.id == signal_id, ForexSignals.parent_signal_id.is_(None)
            )
        )
        return result.fetchone() is not None
