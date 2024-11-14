from typing import List, Dict, Tuple, Optional
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    WinWinUsers, UserVideos, UserPurchases, UserTransactions, TransactionTypes, TopEarningAccount
)
from models.winwin_admin_models import TopEarningAccount, TopEarningAccountsResponse
from models.winwin_models import RootUserVideo


class WinWinDAO(BaseDAO[WinWinUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(WinWinUsers, session)

    async def user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(1).where(WinWinUsers.id == user_id)
        )
        return result.fetchone() is not None

    async def get_users_count(self) -> int:
        result = await self.session.execute(
            select(text("COUNT(*)")).select_from(WinWinUsers)
        )
        return int(result.scalar())

    async def get_videos_count(self) -> int:
        result = await self.session.execute(
            select(text("COUNT(*)")).select_from(UserVideos)
        )
        return int(result.scalar())

    async def get_purchases_count(self) -> int:
        result = await self.session.execute(
            select(text("COUNT(*)")).select_from(UserPurchases)
        )
        return int(result.scalar())

    async def get_balances_sum(self) -> Dict[str, float]:
        query = text("""
            WITH transaction_ids AS (
                SELECT
                    MAX(CASE WHEN type_name = 'cpm' THEN id END) AS cpm_id,
                    MAX(CASE WHEN type_name = 'pps' THEN id END) AS pps_id,
                    MAX(CASE WHEN type_name = 'ppc' THEN id END) AS ppc_id
                FROM transaction_types
            ),
            transaction_sums AS (
                SELECT
                    SUM(CASE WHEN ut.type_id = ti.cpm_id THEN ut.amount ELSE 0 END) AS cpm,
                    SUM(CASE WHEN ut.type_id = ti.pps_id THEN ut.amount ELSE 0 END) AS pps,
                    SUM(CASE WHEN ut.type_id = ti.ppc_id THEN ut.amount ELSE 0 END) AS ppc
                FROM user_transactions ut
                CROSS JOIN transaction_ids ti
            )
            SELECT
                ts.cpm AS cpm,
                ts.pps AS pps,
                ts.ppc AS ppc
            FROM transaction_sums ts
        """)
        result = await self.session.execute(query)
        row = result.fetchone()
        return dict(row) if row else {}

    async def get_top_earning_accounts(self, method: str, limit: int = 20, black_list: Tuple[int] = (), offset: int = 0) -> TopEarningAccountsResponse:
        black_list = black_list or tuple()
        query = text(f"""
            WITH transaction_ids AS (
                SELECT
                    MAX(CASE WHEN type_name = 'cpm' THEN id END) AS cpm_id,
                    MAX(CASE WHEN type_name = 'pps' THEN id END) AS pps_id,
                    MAX(CASE WHEN type_name = 'ppc' THEN id END) AS ppc_id
                FROM transaction_types
            ),
            transaction_sums AS (
                SELECT
                    ut.user_id,
                    SUM(CASE WHEN ut.type_id = ti.cpm_id THEN ut.amount ELSE 0 END) AS cpm,
                    SUM(CASE WHEN ut.type_id = ti.pps_id THEN ut.amount ELSE 0 END) AS pps,
                    SUM(CASE WHEN ut.type_id = ti.ppc_id THEN ut.amount ELSE 0 END) AS ppc,
                    SUM(CASE WHEN ut.amount > 0 THEN ut.amount ELSE 0 END) AS total_amount,
                    SUM(ut.amount) AS current_amount
                FROM user_transactions ut
                CROSS JOIN transaction_ids ti
                GROUP BY ut.user_id
            )
            SELECT
                ts.user_id,
                ts.cpm,
                ts.pps,
                ts.ppc,
                ts.total_amount,
                ts.current_amount
            FROM transaction_sums ts
            WHERE ts.user_id NOT IN :black_list
            ORDER BY {method} DESC
            LIMIT :limit OFFSET :offset
        """)
        result = await self.session.execute(query, {"black_list": black_list, "limit": limit, "offset": offset})
        accounts = [TopEarningAccount.parse_obj(dict(row)) for row in result.fetchall()]
        return TopEarningAccountsResponse(data=accounts)

    async def get_users_videos(self, video_type_id: int) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(UserVideos.id, UserVideos.video_id)
            .where(
                UserVideos.stopped_at.is_(None),
                UserVideos.moderated_at.isnot(None),
                UserVideos.is_accepted == 1,
                UserVideos.video_type_id == video_type_id
            )
        )
        return [dict(row) for row in result.fetchall()]

    async def get_user_video(self, user_video_id: int) -> RootUserVideo:
        result = await self.session.execute(
            select(
                UserVideos.id, UserVideos.video_id, UserVideos.user_id,
                UserVideos.video_type_id, UserVideos.stopped_at,
                UserVideos.moderated_at, UserVideos.is_accepted, UserVideos.created_at
            ).where(UserVideos.id == user_video_id)
        )
        data = result.fetchone()
        return RootUserVideo.parse_obj(dict(data)) if data else RootUserVideo()
