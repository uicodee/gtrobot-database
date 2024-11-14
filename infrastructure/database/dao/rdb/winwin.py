import base64
from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy import select, func, case, and_, not_, text, join, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from dto.winwin import (
    UserLevels,
    UserRoot,
    RootUserVideo,
    UserStat,
    RootCPMReward,
    RootCPMLevel,
    VideoType,
    RootWithdraw,
    UserWithdraw,
    UserVideo,
    User,
    RootUnsentRequests,
    RootPPCLevel,
    RootPPCReward,
    RootPPSReward,
    RootPPSLevel,
    Conf,
    Video,
    LeaderboardMe,
    LeaderboardBoard,
)
from dto.winwin_admin import (
    TopEarningAccountsResponse,
    TopEarningAccount,
    UserBanData,
    PPCDataItem,
    PPSDataItem,
    UserMainAdminInfo,
    VideoTable,
)
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    WinWinUsers,
    UserVideos,
    UserPurchases,
    UserTransactions,
    TransactionTypes,
    CPMLevels,
    Videos,
    UserReferrals,
    PPCLevels,
    PPSLevels,
    VideoTypes,
    CPMRewards,
    UserWithdrawals,
    Requests,
    PPCRewards,
    PPSRewards,
    BannedUsers,
    LeaderboardsData,
    LeaderboardIDs
)


class WinWinDAO(BaseDAO[WinWinUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(WinWinUsers, session)

    async def user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(select(1).where(WinWinUsers.id == user_id))
        return result.fetchone() is not None

    async def get_users_count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(WinWinUsers)
        )
        return result.scalar()

    async def get_videos_count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(UserVideos)
        )
        return result.scalar()

    async def get_purchases_count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(UserPurchases)
        )
        return result.scalar()

    async def get_balances_sum(self) -> Dict[str, float]:
        transaction_ids = select(
            func.max(
                case([(TransactionTypes.type_name == "cpm", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "pps", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "ppc", TransactionTypes.id)])
            ),
        ).subquery()

        result = await self.session.execute(
            select(
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[0],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("cpm"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[1],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("pps"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[2],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("ppc"),
            )
        )
        row = result.fetchone()
        return {"cpm": row.cpm, "pps": row.pps, "ppc": row.ppc} if row else {}

    async def get_top_earning_accounts(
            self, method: str, limit: int = 20, black_list: Tuple[int] = (), offset: int = 0
    ) -> TopEarningAccountsResponse:
        black_list = black_list or tuple()

        transaction_ids = select(
            func.max(
                case([(TransactionTypes.type_name == "cpm", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "pps", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "ppc", TransactionTypes.id)])
            ),
        ).subquery()

        query = (
            select(
                UserTransactions.user_id,
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[0],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("cpm"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[1],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("pps"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[2],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("ppc"),
                func.sum(
                    case(
                        [(UserTransactions.amount > 0, UserTransactions.amount)],
                        else_=0,
                    )
                ).label("total_amount"),
                func.sum(UserTransactions.amount).label("current_amount"),
            )
            .group_by(UserTransactions.user_id)
            .having(not_(UserTransactions.user_id.in_(black_list)))
            .order_by(text(f"{method} DESC"))
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        accounts = [TopEarningAccount.parse_obj(dict(row)) for row in result.fetchall()]
        return TopEarningAccountsResponse(data=accounts)

    async def get_users_videos(self, video_type_id: int) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(UserVideos.id, UserVideos.video_id).where(
                UserVideos.stopped_at.is_(None),
                UserVideos.moderated_at.isnot(None),
                UserVideos.is_accepted == 1,
                UserVideos.video_type_id == video_type_id,
            )
        )
        return [dict(row) for row in result.fetchall()]

    async def get_user_video(self, user_video_id: int) -> RootUserVideo:
        result = await self.session.execute(
            select(
                UserVideos.id,
                UserVideos.video_id,
                UserVideos.user_id,
                UserVideos.video_type_id,
                UserVideos.stopped_at,
                UserVideos.moderated_at,
                UserVideos.is_accepted,
                UserVideos.created_at,
            ).where(UserVideos.id == user_video_id)
        )
        data = result.fetchone()
        return RootUserVideo.parse_obj(dict(data)) if data else RootUserVideo()

    async def get_user(self, user_id: int) -> UserRoot:
        result = await self.session.execute(
            select(
                WinWinUsers.id,
                WinWinUsers.name,
                WinWinUsers.phone_number,
                WinWinUsers.created_at,
            ).where(WinWinUsers.id == user_id)
        )
        data = result.fetchone()
        return UserRoot.parse_obj(dict(data)) if data else UserRoot()

    async def get_user_levels(self, user: UserRoot) -> UserLevels:
        cpm_level = (
            select(CPMLevels.id)
            .where(
                select(func.coalesce(func.sum(Videos.new_views), 0))
                .select_from(join(Videos, UserVideos, Videos.video_id == UserVideos.id))
                .where(
                    and_(
                        UserVideos.user_id == user.id,
                        Videos.created_at >= func.now() - CPMLevels.duration,
                    )
                )
                >= CPMLevels.min_views
            )
            .order_by(CPMLevels.min_views.desc())
            .limit(1)
        ).scalar_subquery()

        ppc_level = (
            select(PPCLevels.id)
            .where(
                select(func.count())
                .select_from(UserReferrals)
                .where(UserReferrals.user_id == user.id)
                >= PPCLevels.min_clicks
            )
            .order_by(PPCLevels.min_clicks.desc())
            .limit(1)
        ).scalar_subquery()

        pps_level = (
            select(PPSLevels.id)
            .where(
                select(func.count())
                .select_from(UserPurchases)
                .where(UserPurchases.user_id == user.id)
                >= PPSLevels.min_sales
            )
            .order_by(PPSLevels.min_sales.desc())
            .limit(1)
        ).scalar_subquery()

        result = await self.session.execute(
            select(
                cpm_level.label("cpm"), ppc_level.label("ppc"), pps_level.label("pps")
            )
        )
        data = result.fetchone()
        return UserLevels.parse_obj(dict(data)) if data else UserLevels()

    async def get_user_stat(self, user: UserRoot) -> UserStat:
        now = datetime.now()
        start_of_month_timestamp = int(datetime(now.year, now.month, 1).timestamp())

        transaction_ids = select(
            func.max(
                case([(TransactionTypes.type_name == "cpm", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "pps", TransactionTypes.id)])
            ),
            func.max(
                case([(TransactionTypes.type_name == "ppc", TransactionTypes.id)])
            ),
            func.max(
                case(
                    [
                        (
                            TransactionTypes.type_name == "canceled_withdraw",
                            TransactionTypes.id,
                        )
                    ]
                )
            ),
        ).subquery()

        transaction_sums = (
            select(
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[0],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("cpm"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[1],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("pps"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[2],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("ppc"),
                func.sum(
                    case(
                        [
                            (
                                UserTransactions.type_id == transaction_ids.c[3],
                                UserTransactions.amount,
                            )
                        ],
                        else_=0,
                    )
                ).label("canceled_withdraw"),
                func.sum(UserTransactions.amount).label("total_balance"),
            ).where(UserTransactions.user_id == user.id)
        ).subquery()

        monthly_views = (
            select(func.sum(Videos.new_views))
            .select_from(join(UserVideos, Videos, UserVideos.id == Videos.video_id))
            .where(
                and_(
                    UserVideos.user_id == user.id,
                    UserVideos.created_at >= start_of_month_timestamp,
                )
            )
        ).scalar_subquery()

        total_views = (
            select(func.sum(Videos.new_views))
            .select_from(join(UserVideos, Videos, UserVideos.id == Videos.video_id))
            .where(UserVideos.user_id == user.id)
        ).scalar_subquery()

        monthly_sales = (
            select(func.count())
            .select_from(UserPurchases)
            .where(
                and_(
                    UserPurchases.user_id == user.id,
                    UserPurchases.created_at >= start_of_month_timestamp,
                )
            )
        ).scalar_subquery()

        total_sales = (
            select(func.count())
            .select_from(UserPurchases)
            .where(UserPurchases.user_id == user.id)
        ).scalar_subquery()

        result = await self.session.execute(
            select(
                transaction_sums.c.cpm,
                transaction_sums.c.pps,
                transaction_sums.c.ppc,
                transaction_sums.c.canceled_withdraw,
                transaction_sums.c.total_balance,
                monthly_views.label("monthly_views"),
                total_views.label("total_views"),
                monthly_sales.label("monthly_sales"),
                total_sales.label("total_sales"),
            )
        )
        data = result.fetchone()
        return UserStat.parse_obj(dict(data)) if data else UserStat()

    async def get_user_videos(self, user: UserRoot) -> List[UserVideo]:
        video_alias = aliased(Videos)
        query = (
            select(
                UserVideos.id.label("id"),
                UserVideos.video_id,
                UserVideos.created_at,
                UserVideos.moderated_at,
                UserVideos.stopped_at,
                UserVideos.is_accepted,
                UserVideos.video_type_id,
                video_alias.title,
                video_alias.thumbnail,
                video_alias.duration,
                video_alias.video_url,
                video_alias.view_count,
                video_alias.like_count,
                video_alias.comment_count,
                video_alias.current_cpm_level,
                func.coalesce(func.sum(UserTransactions.amount), 0).label("earned"),
            )
            .join(
                video_alias, video_alias.video_id == UserVideos.video_id, isouter=True
            )
            .join(
                UserTransactions,
                UserTransactions.id == video_alias.transaction_id,
                isouter=True,
            )
            .where(UserVideos.user_id == user.id)
            .group_by(UserVideos.id, video_alias.video_id)
            .order_by(video_alias.created_at.desc())
        )
        result = await self.session.execute(query)
        return [UserVideo.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_user_withdrawals(self, user: UserRoot) -> List[UserWithdraw]:
        query = (
            select(UserWithdrawals)
            .where(UserWithdrawals.user_id == user.id)
            .order_by(UserWithdrawals.created_at.desc())
        )
        result = await self.session.execute(query)
        return [UserWithdraw.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_user_withdrawal(self, withdraw_id: int) -> RootWithdraw:
        query = select(UserWithdrawals).where(UserWithdrawals.id == withdraw_id)
        result = await self.session.execute(query)
        data = result.fetchone()
        return RootWithdraw.parse_obj(dict(data)) if data else RootWithdraw()

    async def get_user_data(self, user_id: int) -> User:
        def encode_user_id(user_id: int) -> str:
            return base64.b64encode(str(user_id).encode("utf-8")).decode("utf-8")

        user = await self.get_user(user_id)
        user.referral_code = encode_user_id(user_id)
        user.referral_link = f"https://t.me/GTRaibot?start={user.referral_code}"
        user.levels = await self.get_user_levels(user)
        user.videos = await self.get_user_videos(user)
        user.stat = await self.get_user_stat(user)
        user.withdrawals = await self.get_user_withdrawals(user)
        return user

    async def get_video_types(self) -> List[VideoType]:
        query = select(VideoTypes.id, VideoTypes.type_name)
        result = await self.session.execute(query)
        return [VideoType.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_cpm_data(self) -> List[RootCPMLevel]:
        async def get_cpm_rewards(cpm_level_id: int) -> List[RootCPMReward]:
            query = select(CPMRewards.video_type_id, CPMRewards.reward).where(
                CPMRewards.cpm_level_id == cpm_level_id
            )
            result = await self.session.execute(query)
            return [RootCPMReward.parse_obj(dict(row)) for row in result.fetchall()]

        query = select(CPMLevels.min_views, CPMLevels.duration)
        result = await self.session.execute(query)
        cpm_data = []
        for i, row in enumerate(result.fetchall()):
            _cpm = RootCPMLevel.parse_obj(dict(row))
            _cpm.rewards = await get_cpm_rewards(i + 1)
            cpm_data.append(_cpm)
        return cpm_data

    async def get_pps_data(self) -> List[RootPPSLevel]:
        async def get_pps_rewards(pps_level_id: int) -> RootPPSReward:
            query = select(
                PPSRewards.rate, PPSRewards.bonus_rate, PPSRewards.bonus_rate_min_price
            ).where(PPSRewards.pps_level_id == pps_level_id)
            result = await self.session.execute(query)
            data = result.fetchone()
            return RootPPSReward.parse_obj(dict(data)) if data else RootPPSReward()

        query = select(PPSLevels.min_sales)
        result = await self.session.execute(query)
        pps_data = []
        for i, row in enumerate(result.fetchall()):
            _pps = RootPPSLevel.parse_obj(dict(row))
            _pps.rewards = await get_pps_rewards(i + 1)
            pps_data.append(_pps)
        return pps_data

    async def get_ppc_data(self) -> List[RootPPCLevel]:
        async def get_ppc_rewards(ppc_level_id: int) -> RootPPCReward:
            query = select(
                PPCRewards.rate,
                PPCRewards.bonus_rate,
                PPCRewards.bonus_rate_min_activities,
            ).where(PPCRewards.ppc_level_id == ppc_level_id)
            result = await self.session.execute(query)
            data = result.fetchone()
            return RootPPCReward.parse_obj(dict(data)) if data else RootPPCReward()

        query = select(PPCLevels.min_clicks)
        result = await self.session.execute(query)
        ppc_data = []
        for i, row in enumerate(result.fetchall()):
            _ppc = RootPPCLevel.parse_obj(dict(row))
            _ppc.rewards = await get_ppc_rewards(i + 1)
            ppc_data.append(_ppc)
        return ppc_data

    async def get_conf(self) -> Conf:
        return Conf(
            cpm=await self.get_cpm_data(),
            pps=await self.get_pps_data(),
            ppc=await self.get_ppc_data(),
            video_types=await self.get_video_types(),
        )

    async def get_unsent_requests(self, request_type: str) -> List[RootUnsentRequests]:
        table = UserWithdrawals if request_type == "withdrawal" else UserVideos
        query = (
            select(table.user_id, table.id.label("source_id"))
            .join(Requests, Requests.source_id == table.id, isouter=True)
            .where(Requests.source_id.is_(None), table.moderated_at.is_(None))
        )
        result = await self.session.execute(query)
        return [RootUnsentRequests.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_unmoderated_data(self, request_type: str) -> List[int]:
        table = UserWithdrawals if request_type == "withdrawal" else UserVideos
        query = (
            select(table.id)
            .where(table.moderated_at.is_(None))
            .order_by(table.created_at.desc())
            .limit(5)
        )
        result = await self.session.execute(query)
        return [row[0] for row in result.fetchall()]

    async def get_transactions_chart(self, user_id: int, type_name: str = None) -> List:
        if type_name in ("pps", "ppc", "cpm"):
            query = (
                select(UserTransactions.created_at, UserTransactions.amount)
                .join(TransactionTypes, UserTransactions.type_id == TransactionTypes.id)
                .where(
                    UserTransactions.user_id == user_id,
                    TransactionTypes.type_name == type_name,
                    UserTransactions.amount > 0,
                )
                .order_by(UserTransactions.created_at.desc())
            )

        elif type_name == "earnings":
            query = (
                select(UserTransactions.created_at, UserTransactions.amount)
                .where(UserTransactions.user_id == user_id, UserTransactions.amount > 0)
                .order_by(UserTransactions.created_at.desc())
            )

        elif type_name == "views":
            query = (
                select(Videos.created_at, Videos.new_views)
                .join(UserVideos, UserVideos.id == Videos.video_id)
                .where(UserVideos.user_id == user_id)
                .order_by(Videos.created_at.desc())
            )

        elif type_name == "clients":
            query = (
                select(UserPurchases.created_at, text("1"))
                .where(UserPurchases.user_id == user_id)
                .order_by(UserPurchases.created_at.desc())
            )

        elif type_name == "clicks":
            query = (
                select(UserReferrals.created_at, text("1"))
                .where(UserReferrals.user_id == user_id)
                .order_by(UserReferrals.created_at.desc())
            )

        elif type_name == "active_clicks":
            query = (
                select(UserReferrals.created_at.label("first_activity"), text("1"))
                .join(
                    UserTransactions,
                    UserTransactions.id == UserReferrals.transaction_id,
                )
                .where(
                    UserReferrals.user_id == user_id, UserTransactions.on_holding == 0
                )
                .order_by(text("first_activity DESC"))
            )

        else:
            return []

        query = query.limit(1000)
        result = await self.session.execute(query)
        return [(row.created_at, row.amount) for row in result.fetchall()]

    async def get_leaderboard_top_by_level(
            self, method: str, level: int, limit: int = 10
    ) -> List[LeaderboardBoard]:
        subquery = (
            select(func.max(LeaderboardIDs.id))
            .where(LeaderboardIDs.method == method, LeaderboardIDs.level == level)
            .scalar_subquery()
        )

        query = (
            select(LeaderboardsData)
            .where(LeaderboardsData.leaderboard_id == subquery)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [LeaderboardBoard.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_leaderboard_top(
            self, method: str, limit: int = 10
    ) -> List[List[LeaderboardBoard]]:
        return [
            await self.get_leaderboard_top_by_level(method, 1, limit),
            await self.get_leaderboard_top_by_level(method, 2, limit),
            await self.get_leaderboard_top_by_level(method, 3, limit),
        ]

    async def get_leaderboard_me(self, method: str, user_id: int) -> LeaderboardMe:
        subquery = (
            select(func.min(LeaderboardsData.position))
            .where(
                LeaderboardsData.leaderboard_id.in_(
                    select(LeaderboardIDs.id).where(LeaderboardIDs.method == method)
                ),
                LeaderboardsData.id == user_id,
            )
            .scalar_subquery()
        )

        query = (
            select(LeaderboardsData, subquery.label("max_position"))
            .where(
                LeaderboardsData.leaderboard_id.in_(
                    select(LeaderboardIDs.id).where(LeaderboardIDs.method == method)
                ),
                LeaderboardsData.id == user_id,
            )
            .order_by(LeaderboardsData.created_at.desc())
        )

        result = await self.session.execute(query)
        data = result.fetchone()
        return LeaderboardMe.parse_obj(dict(data)) if data else LeaderboardMe()

    async def get_video_ids(
            self,
            user_id: int = None,
            order_type: str = "DESC",
            order_by: str = "created_at",
            status: str = None,
            limit: int = 10,
            offset: int = 0,
    ) -> List[int]:
        query = select(UserVideos.id)

        if status == "stopped":
            query = query.where(
                UserVideos.stopped_at.isnot(None), UserVideos.moderated_at.isnot(None)
            )
        elif status == "unstopped":
            query = query.where(
                UserVideos.stopped_at.is_(None), UserVideos.moderated_at.isnot(None)
            )
        elif status == "accepted":
            query = query.where(
                UserVideos.is_accepted == 1, UserVideos.moderated_at.isnot(None)
            )
        elif status == "unaccepted":
            query = query.where(
                UserVideos.is_accepted == 0, UserVideos.moderated_at.isnot(None)
            )
        elif status == "moderated":
            query = query.where(UserVideos.moderated_at.isnot(None))
        elif status == "unmoderated":
            query = query.where(UserVideos.moderated_at.is_(None))

        if user_id:
            query = query.where(UserVideos.user_id == user_id)

        query = (
            query.order_by(desc(order_by) if order_type == "DESC" else order_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [row[0] for row in result.fetchall()]

    async def get_video_table_data(self, video_id: str) -> VideoTable:
        query = (
            select(Videos, UserTransactions.amount)
            .join(
                UserTransactions,
                Videos.transaction_id == UserTransactions.id,
                isouter=True,
            )
            .join(UserVideos, UserVideos.video_id == video_id)
            .where(Videos.video_id == UserVideos.id)
        )

        result = await self.session.execute(query)
        return VideoTable(
            data=[Video.parse_obj(dict(row)) for row in result.fetchall()]
        )

    async def get_user_main_info_data(self, user_id) -> UserMainAdminInfo:
        user = UserMainAdminInfo.parse_obj(await self.get_user(user_id))
        user.levels = await self.get_user_levels(user)
        return user

    async def get_user_ppc_stat(self, user_id: int) -> PPCDataItem:
        all_users_query = select(func.count()).where(UserReferrals.user_id == user_id)
        active_users_query = select(
            func.count(func.distinct(UserReferrals.user_id))
        ).where(
            UserReferrals.referral_user_id.in_(
                select(UserReferrals.user_id).where(UserReferrals.user_id == user_id)
            )
        )

        all_users = await self.session.scalar(all_users_query)
        active_users = await self.session.scalar(active_users_query)
        return PPCDataItem(all_users=all_users, active_users=active_users)

    async def get_user_pps_stat(
            self, user_id: int = None, limit: int = 10, offset: int = 0
    ) -> List[PPSDataItem]:
        query = (
            select(UserPurchases, UserTransactions.amount.label("transaction_sum"))
            .join(
                UserTransactions,
                UserTransactions.id == UserPurchases.transaction_id,
                isouter=True,
            )
            .where(UserPurchases.purchase_sum > 0)
        )

        if user_id:
            query = query.where(UserPurchases.user_id == user_id)

        query = (
            query.order_by(UserPurchases.created_at.desc()).limit(limit).offset(offset)
        )
        result = await self.session.execute(query)
        return [PPSDataItem.parse_obj(dict(row)) for row in result.fetchall()]

    async def get_ban_data(self, user_id: int) -> UserBanData:
        query = select(BannedUsers).where(BannedUsers.user_id == user_id)
        result = await self.session.execute(query)
        data = result.fetchone()
        return UserBanData.parse_obj(dict(data)) if data else UserBanData()

    async def user_ban_exists(self, user_id: int) -> bool:
        query = select(1).where(BannedUsers.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar() is not None
