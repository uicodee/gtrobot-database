import time
from typing import List, Dict, Optional, Tuple

from sqlalchemy import select, update, insert, delete, func, join, case, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    MiningUsers,
    MiningTasks,
    MiningReferrals,
    MiningHistory,
    MiningSubscriptionOrders,
    UserMiningHistory,
    SubscribersMining,
    BudgetHistory,
    UserTasks,
    UserEarnings,
    UserWithdraws,
    SubscriptionOrders,
    UserPromoCodes,
    BalanceHistory,
    HoldingBalances,
    WithdrawTransactions,
    UserSubscriptions,
    UserExchanges,
)


class MiningDAO(BaseDAO[MiningUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(MiningUsers, session)

    async def get_mining_user_data(self, user_id: int) -> Dict[str, str]:
        end_subscription_date = int(time.time())

        result = await self.session.execute(
            select(
                MiningUsers.user_id,
                MiningUsers.referral_code,
                MiningUsers.balance,
                MiningUsers.daily_mining_balance,
                func.coalesce(SubscribersMining.subscription, "standard").label(
                    "subscription"
                ),
                MiningUsers.crypto_currency,
                MiningUsers.registration_date,
                func.count(MiningReferrals.referral_user_id).label("referral_count"),
            )
            .outerjoin(
                SubscribersMining,
                (MiningUsers.user_id == SubscribersMining.user_id)
                & (SubscribersMining.end_date > end_subscription_date),
            )
            .outerjoin(
                MiningReferrals, MiningUsers.user_id == MiningReferrals.referrer_user_id
            )
            .where(MiningUsers.user_id == user_id)
            .group_by(
                MiningUsers.user_id,
                MiningUsers.referral_code,
                MiningUsers.balance,
                MiningUsers.daily_mining_balance,
                SubscribersMining.subscription,
                MiningUsers.crypto_currency,
                MiningUsers.registration_date,
            )
        )

        dict_keys = [
            "user_id",
            "referral_code",
            "balance",
            "daily_mining_balance",
            "subscription",
            "crypto_currency",
            "registration_date",
            "referral_count",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_mining_user_referrals(self, user_id: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                MiningReferrals.referral_user_id,
                MiningReferrals.referral_date,
                MiningReferrals.referral_user_name,
                MiningUsers.user_profile_photo,
            )
            .join(MiningUsers, MiningUsers.user_id == MiningReferrals.referral_user_id)
            .where(MiningReferrals.referrer_user_id == user_id)
            .order_by(MiningReferrals.referral_date.desc())
        )

        dict_keys = [
            "referral_user_id",
            "referral_date",
            "referral_user_name",
            "referral_user_profile_photo",
        ]
        return [dict(zip(dict_keys, data)) for data in result.fetchall()]

    async def get_mining_active_tasks(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                MiningTasks.id,
                MiningTasks.task_text,
                MiningTasks.task_link,
                MiningTasks.task_group_id,
                MiningTasks.is_required,
            ).where(MiningTasks.is_active == True)
        )

        dict_keys = [
            "task_id",
            "task_text",
            "task_link",
            "task_group_id",
            "is_required",
        ]
        return [dict(zip(dict_keys, data)) for data in result.fetchall()]

    async def get_mining_all_tasks(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                MiningTasks.id,
                MiningTasks.task_text,
                MiningTasks.task_link,
                MiningTasks.task_group_id,
                MiningTasks.is_active,
            )
        )

        dict_keys = ["task_id", "task_text", "task_link", "task_group_id", "is_active"]
        return [dict(zip(dict_keys, data)) for data in result.fetchall()]

    async def get_mining_user_completed_task_ids(self, user_id: int) -> List[int]:
        result = await self.session.execute(
            select(MiningTasks.task_id).where(MiningTasks.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

    async def get_last_user_mining_data(
        self, user_id: int, mining_type: str
    ) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                UserMiningHistory.mining_id,
                UserMiningHistory.mining_date,
                UserMiningHistory.mining_type,
            )
            .where(
                UserMiningHistory.user_id == user_id,
                UserMiningHistory.mining_type == mining_type,
            )
            .order_by(UserMiningHistory.mining_date.desc())
            .limit(1)
        )

        dict_keys = ["mining_id", "mining_date", "mining_type"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_mining_end_message_not_sent(
        self, mining_type: str, mining_date: int
    ) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                UserMiningHistory.id,
                UserMiningHistory.user_id,
                func.coalesce(SubscribersMining.subscription, "standard").label(
                    "subscription"
                ),
                UserMiningHistory.end_message_sent,
            )
            .outerjoin(
                SubscribersMining,
                SubscribersMining.user_id == UserMiningHistory.user_id,
            )
            .where(
                UserMiningHistory.end_message_sent == False,
                UserMiningHistory.mining_type == mining_type,
                UserMiningHistory.mining_date < mining_date,
            )
        )

        dict_keys = ["id", "user_id", "subscription", "end_message_sent"]
        return [dict(zip(dict_keys, data)) for data in result.fetchall()]

    async def get_users_mining_data_by_id(self, mining_id: int) -> List[Dict[str, str]]:
        end_subscription_date = int(time.time())

        result = await self.session.execute(
            select(
                UserMiningHistory.id,
                UserMiningHistory.user_id,
                UserMiningHistory.mining_date,
                UserMiningHistory.mining_type,
                func.coalesce(SubscribersMining.subscription, "standard").label(
                    "subscription"
                ),
                MiningUsers.crypto_currency,
                MiningUsers.balance,
                func.count(MiningReferrals.referral_user_id).label("referral_count"),
            )
            .join(MiningUsers, MiningUsers.user_id == UserMiningHistory.user_id)
            .outerjoin(
                SubscribersMining,
                (UserMiningHistory.user_id == SubscribersMining.user_id)
                & (SubscribersMining.end_date > end_subscription_date),
            )
            .outerjoin(
                MiningReferrals, MiningUsers.user_id == MiningReferrals.referrer_user_id
            )
            .where(UserMiningHistory.mining_id == mining_id)
            .group_by(
                UserMiningHistory.user_id,
                UserMiningHistory.mining_date,
                UserMiningHistory.mining_type,
                MiningUsers.crypto_currency,
                MiningUsers.balance,
                SubscribersMining.subscription,
            )
        )

        dict_keys = [
            "mining_id",
            "user_id",
            "mining_date",
            "mining_type",
            "subscription",
            "crypto_currency",
            "balance",
            "referral_count",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_users_mining_data_by_mining_type(
        self, mining_type: str
    ) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                UserMiningHistory.id,
                UserMiningHistory.mining_id,
                UserMiningHistory.user_id,
                UserMiningHistory.mining_date,
                UserMiningHistory.mining_type,
            ).where(UserMiningHistory.mining_type == mining_type)
        )

        dict_keys = ["id", "mining_id", "user_id", "mining_date", "mining_type"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_current_mining_budget(
        self, budget_type: str = "regular"
    ) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                BudgetHistory.id,
                BudgetHistory.budget,
                BudgetHistory.budget_date,
                BudgetHistory.budget_type,
            )
            .where(BudgetHistory.budget_type == budget_type)
            .order_by(BudgetHistory.budget_date.desc())
            .limit(1)
        )

        dict_keys = ["id", "budget", "budget_date", "budget_type"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_mining_completed_task_users_id(self, task_id: int) -> List[int]:
        result = await self.session.execute(
            select(UserTasks.user_id).where(UserTasks.task_id == task_id)
        )
        return [row[0] for row in result.fetchall()]

    async def get_count_mining_users(self) -> int:
        result = await self.session.execute(select(func.count(MiningUsers.user_id)))
        return result.scalar() if result else 0

    async def get_mining_user_earning(self, user_id: int, mining_id: int) -> float:
        result = await self.session.execute(
            select(UserEarnings.earning).where(
                UserEarnings.user_id == user_id, UserEarnings.mining_id == mining_id
            )
        )
        return result.scalar() if result.scalar() else 0

    async def get_mining_user_earnings(self, mining_id: int) -> float:
        result = await self.session.execute(
            select(UserEarnings.earning).where(UserEarnings.mining_id == mining_id)
        )
        return sum(row[0] for row in result.fetchall())

    async def get_all_mining_history(self, mining_type: str) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                MiningHistory.id,
                MiningHistory.start_date,
                MiningHistory.end_date,
                MiningHistory.mining_type,
                MiningHistory.is_checked,
            ).where(MiningHistory.mining_type == mining_type)
        )

        dict_keys = ["id", "start_date", "end_date", "mining_type", "is_checked"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_top_earning_accounts(
        self, ticker_prices: Dict[str, float], top_count: int = 20
    ) -> List[Dict[str, str]]:
        dict_keys = [
            "user_id",
            "daily_mining_balance",
            "balance",
            "crypto_currency",
            "registration_date",
        ]
        users_data = []

        for ticker, price in ticker_prices.items():
            result = await self.session.execute(
                select(
                    MiningUsers.user_id,
                    MiningUsers.daily_mining_balance,
                    (MiningUsers.balance * price).label("balance"),
                    MiningUsers.crypto_currency,
                    MiningUsers.registration_date,
                )
                .where(MiningUsers.crypto_currency == ticker)
                .order_by(MiningUsers.balance.desc())
                .limit(top_count)
            )

            for row in result.fetchall():
                users_data.append(dict(zip(dict_keys, row)))

        users_data = sorted(users_data, key=lambda x: x["balance"], reverse=True)
        return users_data[:top_count]

    async def get_active_subscribers_mining_users(
        self, end_date: int
    ) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                SubscribersMining.id,
                SubscribersMining.user_id,
                SubscribersMining.start_date,
                SubscribersMining.end_date,
                SubscribersMining.subscription,
                SubscribersMining.end_message_sent,
            ).where(SubscribersMining.end_date > end_date)
        )

        dict_keys = [
            "id",
            "user_id",
            "start_date",
            "end_date",
            "subscription",
            "end_message_sent",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_subscribers_mining_end_message_not_sent(
        self, end_date: int
    ) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                SubscribersMining.id,
                SubscribersMining.user_id,
                SubscribersMining.start_date,
                SubscribersMining.end_date,
                SubscribersMining.subscription,
                SubscribersMining.end_message_sent,
            ).where(
                SubscribersMining.end_date < end_date,
                SubscribersMining.end_message_sent == False,
            )
        )

        dict_keys = [
            "id",
            "user_id",
            "start_date",
            "end_date",
            "subscription",
            "end_message_sent",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_mining_user_withdraws_not_sent(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                UserWithdraws.id,
                UserWithdraws.user_id,
                UserWithdraws.withdraw_source_currency,
                UserWithdraws.withdraw_source_amount,
                UserWithdraws.withdraw_currency,
                UserWithdraws.withdraw_amount,
                UserWithdraws.withdraw_address,
                UserWithdraws.withdraw_date,
                UserWithdraws.is_sent,
                UserWithdraws.is_checked,
                UserWithdraws.is_confirmed,
            ).where(UserWithdraws.is_sent == False)
        )

        dict_keys = [
            "withdraw_id",
            "user_id",
            "withdraw_source_currency",
            "withdraw_source_amount",
            "withdraw_currency",
            "withdraw_amount",
            "withdraw_address",
            "withdraw_date",
            "is_sent",
            "is_checked",
            "is_confirmed",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_mining_user_withdraws_not_checked(self) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                UserWithdraws.id,
                UserWithdraws.user_id,
                UserWithdraws.withdraw_source_currency,
                UserWithdraws.withdraw_source_amount,
                UserWithdraws.withdraw_currency,
                UserWithdraws.withdraw_amount,
                UserWithdraws.withdraw_address,
                UserWithdraws.withdraw_date,
                UserWithdraws.is_sent,
                UserWithdraws.is_checked,
                UserWithdraws.is_confirmed,
            ).where(UserWithdraws.is_checked == False)
        )

        dict_keys = [
            "withdraw_id",
            "user_id",
            "withdraw_source_currency",
            "withdraw_source_amount",
            "withdraw_currency",
            "withdraw_amount",
            "withdraw_address",
            "withdraw_date",
            "is_sent",
            "is_checked",
            "is_confirmed",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_mining_user_withdraw(self, withdraw_id: int) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                UserWithdraws.id,
                UserWithdraws.user_id,
                UserWithdraws.withdraw_source_currency,
                UserWithdraws.withdraw_source_amount,
                UserWithdraws.withdraw_currency,
                UserWithdraws.withdraw_amount,
                UserWithdraws.withdraw_address,
                UserWithdraws.withdraw_date,
                UserWithdraws.is_sent,
                UserWithdraws.is_confirmed,
            ).where(UserWithdraws.id == withdraw_id)
        )

        dict_keys = [
            "withdraw_id",
            "user_id",
            "withdraw_source_currency",
            "withdraw_source_amount",
            "withdraw_currency",
            "withdraw_amount",
            "withdraw_address",
            "withdraw_date",
            "is_sent",
            "is_confirmed",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_last_mining_data(self, mining_type: str) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                MiningHistory.id,
                MiningHistory.start_date,
                MiningHistory.end_date,
                MiningHistory.mining_type,
            )
            .where(
                MiningHistory.mining_type == mining_type,
                MiningHistory.is_checked == False,
            )
            .order_by(MiningHistory.start_date.desc())
            .limit(1)
        )

        dict_keys = ["mining_id", "start_date", "end_date", "mining_type"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_users_count_for_statistics(
        self, mining_type: str, offset: int = 4
    ) -> Dict[str, int]:
        current_mining_subquery = (
            select(MiningHistory.id)
            .where(
                MiningHistory.mining_type == mining_type,
                MiningHistory.is_checked == False,
            )
            .order_by(MiningHistory.start_date.desc())
            .limit(1)
            .scalar_subquery()
        )

        previous_mining_subquery = (
            select(MiningHistory.id)
            .where(MiningHistory.mining_type == mining_type)
            .order_by(MiningHistory.start_date.desc())
            .offset(offset)
            .limit(1)
            .scalar_subquery()
        )

        result = await self.session.execute(
            select(
                func.coalesce(
                    select(func.count(UserMiningHistory.user_id.distinct())).where(
                        UserMiningHistory.mining_id == current_mining_subquery
                    ),
                    0,
                ).label("current_mining_users_count"),
                func.coalesce(
                    select(func.count(UserMiningHistory.user_id.distinct())).where(
                        UserMiningHistory.mining_id == previous_mining_subquery
                    ),
                    0,
                ).label("previous_mining_users_count"),
            )
        )

        dict_keys = ["current_mining_users_count", "previous_mining_users_count"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def count_user_mining_history(self, user_id: int, mining_type: str) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(UserMiningHistory)
            .where(
                UserMiningHistory.user_id == user_id,
                UserMiningHistory.mining_type == mining_type,
            )
        )
        return result.scalar()

    async def mining_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(MiningUsers).where(MiningUsers.user_id == user_id)
        )
        return result.scalar() is not None

    async def user_is_mining(self, user_id: int, mining_id: int) -> bool:
        result = await self.session.execute(
            select(UserMiningHistory).where(
                UserMiningHistory.user_id == user_id,
                UserMiningHistory.mining_id == mining_id,
            )
        )
        return result.scalar() is not None

    async def subscription_order_exists(self, order_id: int) -> bool:
        result = await self.session.execute(
            select(SubscriptionOrders).where(SubscriptionOrders.order_id == order_id)
        )
        return result.scalar() is not None

    async def get_subscription_order(self, query_id: int) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                SubscriptionOrders.query_id,
                SubscriptionOrders.user_id,
                SubscriptionOrders.currency,
                SubscriptionOrders.total_amount,
                SubscriptionOrders.invoice_payload,
                SubscriptionOrders.shipping_option_id,
                SubscriptionOrders.date,
            ).where(SubscriptionOrders.query_id == query_id)
        )

        dict_keys = [
            "query_id",
            "user_id",
            "currency",
            "total_amount",
            "invoice_payload",
            "shipping_option_id",
            "date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def user_promo_code_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(UserPromoCodes)
            .where(UserPromoCodes.user_id == user_id)
            .order_by(UserPromoCodes.promo_code_date.desc())
            .limit(1)
        )
        return result.scalar() is not None

    async def promo_code_data(self, promo_code: str) -> Dict[str, str]:
        result = await self.session.execute(
            select(UserPromoCodes)
            .where(UserPromoCodes.promo_code == promo_code)
            .order_by(UserPromoCodes.promo_code_date.desc())
            .limit(1)
        )

        dict_keys = [
            "id",
            "user_id",
            "promo_code",
            "promo_code_sum",
            "is_used",
            "promo_code_date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def user_last_promo_code(self, user_id: int) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                UserPromoCodes.id,
                UserPromoCodes.user_id,
                UserPromoCodes.promo_code,
                UserPromoCodes.promo_code_sum,
                UserPromoCodes.is_used,
                UserPromoCodes.promo_code_date,
            )
            .where(UserPromoCodes.user_id == user_id)
            .order_by(UserPromoCodes.promo_code_date.desc())
            .limit(1)
        )

        dict_keys = [
            "id",
            "user_id",
            "promo_code",
            "promo_code_sum",
            "is_used",
            "promo_code_date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_last_subscriber_mining(self, user_id: int) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                SubscribersMining.id,
                SubscribersMining.user_id,
                SubscribersMining.start_date,
                SubscribersMining.end_date,
                SubscribersMining.subscription,
                SubscribersMining.end_message_sent,
            )
            .where(SubscribersMining.user_id == user_id)
            .order_by(SubscribersMining.end_date.desc())
            .limit(1)
        )

        dict_keys = [
            "id",
            "user_id",
            "start_date",
            "end_date",
            "subscription",
            "end_message_sent",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_users_without_profile_photo(self) -> List[int]:
        result = await self.session.execute(
            select(MiningUsers.user_id).where(MiningUsers.user_profile_photo == None)
        )
        return [row[0] for row in result.fetchall()]

    async def get_inactive_balances(
        self,
        ticker_prices: Dict[str, float],
        balance_date: int,
        min_usdt_balance: float = 1,
    ) -> List[Dict[str, str]]:
        dict_keys = [
            "user_id",
            "source_balance",
            "usdt_balance",
            "crypto_currency",
            "balance_date",
        ]
        users_data = []

        for ticker, price in ticker_prices.items():
            min_balance = min_usdt_balance / price
            result = await self.session.execute(
                select(
                    BalanceHistory.user_id,
                    MiningUsers.balance,
                    (MiningUsers.balance * price).label("usdt_balance"),
                    MiningUsers.crypto_currency,
                    BalanceHistory.balance_date,
                )
                .join(MiningUsers, BalanceHistory.user_id == MiningUsers.user_id)
                .where(
                    BalanceHistory.balance > min_balance,
                    BalanceHistory.crypto_currency == ticker,
                    BalanceHistory.balance_date < balance_date,
                    MiningUsers.balance >= BalanceHistory.balance,
                    MiningUsers.crypto_currency == BalanceHistory.crypto_currency,
                )
            )

            for row in result.fetchall():
                users_data.append(dict(zip(dict_keys, row)))

        return users_data

    async def get_holding_balance(
        self, user_id: int, max_holding_date: int, is_withdrawn: bool = False
    ) -> Dict[str, str]:
        result = await self.session.execute(
            select(
                HoldingBalances.id,
                HoldingBalances.user_id,
                HoldingBalances.balance,
                HoldingBalances.is_withdrawn,
                HoldingBalances.holding_date,
            )
            .where(
                HoldingBalances.user_id == user_id,
                HoldingBalances.holding_date > max_holding_date,
                HoldingBalances.is_withdrawn == is_withdrawn,
            )
            .order_by(HoldingBalances.holding_date.desc())
            .limit(1)
        )

        dict_keys = ["id", "user_id", "balance", "is_withdrawn", "holding_date"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_user_inactive_balance(
        self,
        user_id: int,
        crypto_currency: str,
        ticker_prices: Dict[str, float],
        min_usdt_balance: float = 1,
    ) -> Dict[str, str]:
        min_balance = min_usdt_balance / ticker_prices.get(crypto_currency, 0)
        result = await self.session.execute(
            select(
                BalanceHistory.user_id,
                BalanceHistory.balance,
                BalanceHistory.crypto_currency,
                BalanceHistory.balance_date,
            )
            .join(MiningUsers, MiningUsers.user_id == BalanceHistory.user_id)
            .where(
                BalanceHistory.user_id == user_id,
                BalanceHistory.balance > min_balance,
                MiningUsers.balance >= BalanceHistory.balance,
                MiningUsers.crypto_currency == BalanceHistory.crypto_currency,
            )
            .limit(1)
        )

        dict_keys = ["user_id", "balance", "crypto_currency", "balance_date"]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_user_holding_history(self, user_id: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                HoldingBalances.balance,
                HoldingBalances.holding_date,
                HoldingBalances.crypto_currency,
            ).where(HoldingBalances.user_id == user_id)
        )

        dict_keys = ["amount", "date", "crypto_currency"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_user_withdraws_history(self, user_id: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(
                UserWithdraws.withdraw_amount.label("amount"),
                UserWithdraws.withdraw_date.label("date"),
                UserWithdraws.withdraw_currency.label("crypto_currency"),
                case(
                    (UserWithdraws.is_checked == False, 0),
                    (
                        and_(
                            UserWithdraws.is_checked == True,
                            UserWithdraws.is_confirmed == True,
                        ),
                        1,
                    ),
                    (
                        and_(
                            UserWithdraws.is_checked == True,
                            UserWithdraws.is_confirmed == False,
                        ),
                        -1,
                    ),
                    else_=None,
                ).label("status"),
            ).where(UserWithdraws.user_id == user_id)
        )

        dict_keys = ["amount", "date", "crypto_currency", "status"]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_withdraw_transaction_id(self, withdraw_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(WithdrawTransactions.transaction_id).where(
                WithdrawTransactions.withdraw_id == withdraw_id
            )
        )
        return result.scalar()

    async def get_users_count_in_current_time(
        self, mining_type: str, from_date: int = None, is_unique: bool = False
    ) -> int:
        from_date = from_date or int(time.time())

        query = select(func.count(UserMiningHistory.id))
        if is_unique:
            query = query.group_by(UserMiningHistory.user_id)

        result = await self.session.execute(
            query.select_from(MiningHistory)
            .join(UserMiningHistory, UserMiningHistory.mining_id == MiningHistory.id)
            .where(
                MiningHistory.mining_type == mining_type,
                MiningHistory.end_date > from_date,
            )
        )

        return result.scalar() or 0

    async def get_users_earnings(self, from_date: int = 0) -> float:
        result = await self.session.execute(
            select(func.sum(UserEarnings.earning)).where(
                UserEarnings.earning < 10, UserEarnings.earning_date > from_date
            )
        )
        return result.scalar() or 0.0

    async def update_user_mining_crypto_currency(
        self, user_id: int, balance: float, crypto_currency: str
    ):
        await self.session.execute(
            update(MiningUsers)
            .where(MiningUsers.user_id == user_id)
            .values(balance=balance, crypto_currency=crypto_currency)
        )
        await self.session.commit()

    async def update_user_mining_balance(
        self, user_id: int, user_balance: float, crypto_currency: str
    ):
        await self.session.execute(
            update(MiningUsers)
            .where(MiningUsers.user_id == user_id)
            .values(balance=user_balance, crypto_currency=crypto_currency)
        )
        await self.session.commit()

    async def update_user_mining_balances(self, data: List[Tuple[float, str, int]]):
        for balance, crypto_currency, user_id in data:
            await self.session.execute(
                update(MiningUsers)
                .where(MiningUsers.user_id == user_id)
                .values(balance=balance, crypto_currency=crypto_currency)
            )
        await self.session.commit()

    async def update_user_daily_mining_balances(self, data: List[Tuple[float, int]]):
        for daily_balance, user_id in data:
            await self.session.execute(
                update(MiningUsers)
                .where(MiningUsers.user_id == user_id)
                .values(
                    daily_mining_balance=MiningUsers.daily_mining_balance
                    + daily_balance
                )
            )
        await self.session.commit()

    async def update_mining_history_is_checked(
        self, mining_id: int, is_checked: bool = True
    ):
        await self.session.execute(
            update(MiningHistory)
            .where(MiningHistory.id == mining_id)
            .values(is_checked=is_checked)
        )
        await self.session.commit()

    async def update_mining_task_status(self, task_id: int, is_active: bool = False):
        await self.session.execute(
            update(MiningTasks)
            .where(MiningTasks.id == task_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def update_mining_user_subscription(
        self, user_id: int, subscription: str = "standard"
    ):
        await self.session.execute(
            update(MiningUsers)
            .where(MiningUsers.user_id == user_id)
            .values(subscription=subscription)
        )
        await self.session.commit()

    async def update_mining_user_withdraw_sent_status(
        self, withdraw_id: int, is_sent: bool
    ):
        await self.session.execute(
            update(UserWithdraws)
            .where(UserWithdraws.id == withdraw_id)
            .values(is_sent=is_sent)
        )
        await self.session.commit()

    async def update_mining_user_withdraw_confirmed_status(
        self, withdraw_id: int, is_confirmed: bool
    ):
        await self.session.execute(
            update(UserWithdraws)
            .where(UserWithdraws.id == withdraw_id)
            .values(is_confirmed=is_confirmed)
        )
        await self.session.commit()

    async def update_mining_user_withdraw_checked_status(
        self, withdraw_id: int, is_checked: bool
    ):
        await self.session.execute(
            update(UserWithdraws)
            .where(UserWithdraws.id == withdraw_id)
            .values(is_checked=is_checked)
        )
        await self.session.commit()

    async def update_subscription_order_status(self, order_id: int, status: str):
        await self.session.execute(
            update(SubscriptionOrders)
            .where(SubscriptionOrders.order_id == order_id)
            .values(status=status)
        )
        await self.session.commit()

    async def update_subscribers_mining_end_message_sent(
        self, subscribers_mining_id: int, end_message_sent: bool
    ):
        await self.session.execute(
            update(SubscribersMining)
            .where(SubscribersMining.id == subscribers_mining_id)
            .values(end_message_sent=end_message_sent)
        )
        await self.session.commit()

    async def update_mining_end_message_sent(self, data: List[Tuple[bool, int]]):
        for end_message_sent, id_ in data:
            await self.session.execute(
                update(UserMiningHistory)
                .where(UserMiningHistory.id == id_)
                .values(end_message_sent=end_message_sent)
            )
        await self.session.commit()

    async def update_user_profile_photo(
        self, user_id: int, user_profile_photo: Optional[str] = None
    ):
        await self.session.execute(
            update(MiningUsers)
            .where(MiningUsers.user_id == user_id)
            .values(user_profile_photo=user_profile_photo)
        )
        await self.session.commit()

    async def update_holding_balance_is_withdrawn(
        self, balance_hold_id: int, is_withdrawn: bool = True
    ):
        await self.session.execute(
            update(HoldingBalances)
            .where(HoldingBalances.id == balance_hold_id)
            .values(is_withdrawn=is_withdrawn)
        )
        await self.session.commit()

    async def update_user_promo_code_status(
        self, promo_code_id: int, is_used: bool = True
    ):
        await self.session.execute(
            update(UserPromoCodes)
            .where(UserPromoCodes.id == promo_code_id)
            .values(is_used=is_used)
        )
        await self.session.commit()

    async def update_user_subscription(
        self,
        user_id: int,
        subscription: str,
        end_subscription_date: Optional[int] = None,
    ):
        if end_subscription_date:
            await self.session.execute(
                update(UserSubscriptions)
                .where(UserSubscriptions.user_id == user_id)
                .values(
                    subscription=subscription,
                    end_subscription_date=end_subscription_date,
                )
            )
        else:
            await self.session.execute(
                update(UserSubscriptions)
                .where(UserSubscriptions.user_id == user_id)
                .values(subscription=subscription)
            )
        await self.session.commit()

    async def set_mining_user(
        self,
        user_id: int,
        referral_code: str,
        user_profile_photo: Optional[str] = None,
        crypto_currency: str = "btc",
        registration_date: Optional[int] = None,
    ):
        registration_date = registration_date or int(time.time())
        await self.session.execute(
            insert(MiningUsers).values(
                user_id=user_id,
                referral_code=referral_code,
                user_profile_photo=user_profile_photo,
                crypto_currency=crypto_currency,
                registration_date=registration_date,
            )
        )
        await self.session.commit()

    async def set_mining_referral_user(
        self,
        referrer_user_id: int,
        referral_user_id: int,
        referral_user_name: str,
        referral_date: Optional[int] = None,
    ):
        referral_date = referral_date or int(time.time())
        await self.session.execute(
            insert(MiningReferrals).values(
                referrer_user_id=referrer_user_id,
                referral_user_id=referral_user_id,
                referral_user_name=referral_user_name,
                referral_date=referral_date,
            )
        )
        await self.session.commit()

    async def set_user_mining_history(
        self,
        mining_id: int,
        user_id: int,
        mining_type: str,
        mining_date: Optional[int] = None,
    ):
        mining_date = mining_date or int(time.time())
        await self.session.execute(
            insert(UserMiningHistory).values(
                mining_id=mining_id,
                user_id=user_id,
                mining_type=mining_type,
                mining_date=mining_date,
            )
        )
        await self.session.commit()

    async def set_user_mining_tasks(
        self, user_id: int, task_id: int, completion_date: Optional[int] = None
    ):
        completion_date = completion_date or int(time.time())
        await self.session.execute(
            insert(UserTasks).values(
                user_id=user_id, task_id=task_id, completion_date=completion_date
            )
        )
        await self.session.commit()

    async def set_mining_cycle(
        self, start_date: int, end_date: int, mining_type: str, is_checked: bool = False
    ):
        result = await self.session.execute(
            insert(MiningHistory)
            .values(
                start_date=start_date,
                end_date=end_date,
                mining_type=mining_type,
                is_checked=is_checked,
            )
            .returning(MiningHistory.id)
        )
        await self.session.commit()
        return result.scalar()

    async def set_mining_users_earnings(self, data: List[Tuple[int, int, float, int]]):
        await self.session.execute(
            insert(UserEarnings),
            [
                {
                    "user_id": user_id,
                    "mining_id": mining_id,
                    "earning": earning,
                    "earning_date": earning_date,
                }
                for user_id, mining_id, earning, earning_date in data
            ],
        )
        await self.session.commit()

    async def set_mining_budget(self, budget: float, budget_date: Optional[int] = None):
        budget_date = budget_date or int(time.time())
        await self.session.execute(
            insert(BudgetHistory).values(budget=budget, budget_date=budget_date)
        )
        await self.session.commit()

    async def set_mining_task(
        self,
        task_text: str,
        task_link: str,
        task_group_id: Optional[int] = None,
        is_required: bool = False,
    ):
        await self.session.execute(
            insert(MiningTasks).values(
                task_text=task_text,
                task_link=task_link,
                task_group_id=task_group_id,
                is_required=is_required,
            )
        )
        await self.session.commit()

    async def set_mining_subscribers_mining(
        self, user_id: int, start_date: int, end_date: int, subscription: str
    ):
        await self.session.execute(
            insert(SubscribersMining).values(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                subscription=subscription,
            )
        )
        await self.session.commit()

    async def set_mining_user_exchange(
        self,
        user_id: int,
        from_currency: str,
        to_currency: str,
        from_balance: float,
        to_balance: float,
        exchange_date: Optional[int] = None,
    ):
        exchange_date = exchange_date or int(time.time())
        async with self.session.begin():
            await self.session.execute(
                update(MiningUsers)
                .where(MiningUsers.user_id == user_id)
                .values(balance=to_balance, crypto_currency=to_currency)
            )
            await self.session.execute(
                insert(BalanceHistory).values(
                    user_id=user_id,
                    balance=from_balance,
                    crypto_currency=from_currency,
                    balance_date=exchange_date,
                )
            )
            await self.session.execute(
                insert(UserExchanges).values(
                    user_id=user_id,
                    from_currency=from_currency,
                    to_currency=to_currency,
                    from_balance=from_balance,
                    to_balance=to_balance,
                    exchange_date=exchange_date,
                )
            )

    async def set_mining_user_withdraw(
        self,
        user_id: int,
        source_currency: str,
        source_amount: float,
        withdraw_currency: str,
        withdraw_amount: float,
        withdraw_address: str,
        withdraw_date: Optional[int] = None,
        is_sent: bool = False,
        is_confirmed: bool = False,
        holding_id: Optional[int] = None,
    ):
        withdraw_date = withdraw_date or int(time.time())
        async with self.session.begin():
            await self.session.execute(
                update(MiningUsers)
                .where(MiningUsers.user_id == user_id)
                .values(balance=MiningUsers.balance - source_amount)
            )
            await self.session.execute(
                insert(BalanceHistory).values(
                    user_id=user_id,
                    balance=MiningUsers.balance,
                    crypto_currency=source_currency,
                    balance_date=withdraw_date,
                )
            )
            if holding_id:
                await self.session.execute(
                    update(HoldingBalances)
                    .where(HoldingBalances.id == holding_id)
                    .values(is_withdrawn=True)
                )
            await self.session.execute(
                insert(UserWithdraws).values(
                    user_id=user_id,
                    withdraw_source_currency=source_currency,
                    withdraw_source_amount=source_amount,
                    withdraw_currency=withdraw_currency,
                    withdraw_amount=withdraw_amount,
                    withdraw_address=withdraw_address,
                    withdraw_date=withdraw_date,
                    is_sent=is_sent,
                    is_confirmed=is_confirmed,
                )
            )

    async def set_mining_withdraw_transactions(
        self,
        withdraw_id: int,
        transaction_id: str,
        transaction_date: Optional[int] = None,
    ):
        transaction_date = transaction_date or int(time.time())
        await self.session.execute(
            insert(WithdrawTransactions).values(
                withdraw_id=withdraw_id,
                transaction_id=transaction_id,
                transaction_date=transaction_date,
            )
        )
        await self.session.commit()

    async def set_mining_subscription_order(
        self,
        query_id: int,
        user_id: int,
        currency: str,
        total_amount: float,
        invoice_payload: str,
        shipping_option_id: Optional[str] = None,
        date: Optional[int] = None,
    ):
        date = date or int(time.time())
        await self.session.execute(
            insert(SubscriptionOrders).values(
                query_id=query_id,
                user_id=user_id,
                currency=currency,
                total_amount=total_amount,
                invoice_payload=invoice_payload,
                shipping_option_id=shipping_option_id,
                date=date,
            )
        )
        await self.session.commit()

    async def create_user_subscription(
        self,
        user_id: int,
        subscription: str,
        end_subscription_date: int,
        order_id: Optional[int] = None,
        token_id: Optional[int] = None,
        purchase_date: Optional[int] = None,
    ):
        purchase_date = purchase_date or int(time.time())
        await self.session.execute(
            insert(UserSubscriptions).values(
                user_id=user_id,
                subscription=subscription,
                purchase_date=purchase_date,
                end_subscription_date=end_subscription_date,
                order_id=order_id,
                token_id=token_id,
            )
        )
        await self.session.commit()

    async def create_holding_balance(
        self,
        user_id: int,
        source_balance: float,
        usdt_balance: float,
        holding_date: Optional[int] = None,
    ):
        holding_date = holding_date or int(time.time())
        async with self.session.begin():
            await self.session.execute(
                update(MiningUsers)
                .where(MiningUsers.user_id == user_id)
                .values(balance=MiningUsers.balance - source_balance)
            )
            await self.session.execute(
                insert(BalanceHistory).values(
                    user_id=user_id,
                    balance=MiningUsers.balance,
                    crypto_currency=MiningUsers.crypto_currency,
                    balance_date=holding_date,
                )
            )
            await self.session.execute(
                insert(HoldingBalances).values(
                    user_id=user_id,
                    balance=usdt_balance,
                    is_withdrawn=False,
                    holding_date=holding_date,
                )
            )

    async def set_mining_user_balance_histories(
        self, data: List[Tuple[int, float, str, int]]
    ):
        await self.session.execute(
            insert(BalanceHistory),
            [
                {
                    "user_id": user_id,
                    "balance": balance,
                    "crypto_currency": crypto_currency,
                    "balance_date": balance_date,
                }
                for user_id, balance, crypto_currency, balance_date in data
            ],
        )
        await self.session.commit()

    async def del_mining_user_task(self, user_id: int, task_id: int) -> None:
        await self.session.execute(
            delete(UserTasks).where(
                UserTasks.user_id == user_id, UserTasks.task_id == task_id
            )
        )
        await self.session.commit()
