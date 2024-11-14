from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    Positions,
    AutoOrderUsersOrders,
    LeaderboardUsers,
    LeaderboardOrders,
    ClosedLeaderboardOrders,
)


class AutoOrderUsersDAO(BaseDAO[AutoOrderUsersOrders]):
    def __init__(self, session: AsyncSession):
        super().__init__(AutoOrderUsersOrders, session)

    async def del_auto_order_position(self, position_id: int) -> None:
        query = delete(Positions).where(Positions.id == position_id)
        await self.session.execute(query)

    async def del_auto_order_user_order(self, user_id: int, position_id: int) -> None:
        query = delete(AutoOrderUsersOrders).where(
            AutoOrderUsersOrders.user_id == user_id,
            AutoOrderUsersOrders.position_id == position_id,
        )
        await self.session.execute(query)

    async def del_auto_order_leaderboard_user(
        self, encrypted_uid: str, creator_user_id: int
    ) -> None:
        query = delete(LeaderboardUsers).where(
            LeaderboardUsers.encrypted_uid == encrypted_uid,
            LeaderboardUsers.user_id == creator_user_id,
        )
        await self.session.execute(query)

    async def del_new_order(self, order_id: int) -> None:
        query = delete(LeaderboardOrders).where(LeaderboardOrders.id == order_id)
        await self.session.execute(query)

    async def del_closed_leaderboard_order(self, order_id: int) -> None:
        query = delete(ClosedLeaderboardOrders).where(
            ClosedLeaderboardOrders.id == order_id
        )
        await self.session.execute(query)

    async def del_auto_order_user_history(self, user_id: int) -> None:
        query = delete(AutoOrderUsersOrders).where(
            AutoOrderUsersOrders.user_id == user_id
        )
        await self.session.execute(query)
