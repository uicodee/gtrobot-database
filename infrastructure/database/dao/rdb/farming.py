from typing import List, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    Accounts,
    HamsterAccountStatistics,
    HamsterUpgradePurchases,
    BlumAccountStatistics,
)


class FarmingDAO(BaseDAO[Accounts]):
    def __init__(self, session: AsyncSession):
        super().__init__(Accounts, session)

    async def account(self, account_id: int, user_id: int) -> Dict[str, any]:
        result = await self.session.execute(
            select(
                Accounts.id,
                Accounts.user_id,
                Accounts.referral_token,
                Accounts.account_name,
                Accounts.access_token,
                Accounts.refresh_token,
                Accounts.bot_name,
                Accounts.is_active,
                Accounts.is_error,
                Accounts.date,
            ).where(Accounts.id == account_id, Accounts.user_id == user_id)
        )
        dict_keys = [
            "id",
            "user_id",
            "referral_token",
            "account_name",
            "access_token",
            "refresh_token",
            "bot_name",
            "is_active",
            "is_error",
            "date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def accounts(self, user_id: int, bot_name: str) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                Accounts.id,
                Accounts.user_id,
                Accounts.referral_token,
                Accounts.account_name,
                Accounts.access_token,
                Accounts.refresh_token,
                Accounts.bot_name,
                Accounts.is_active,
                Accounts.is_error,
                Accounts.date,
            ).where(Accounts.user_id == user_id, Accounts.bot_name == bot_name)
        )
        dict_keys = [
            "id",
            "user_id",
            "referral_token",
            "account_name",
            "access_token",
            "refresh_token",
            "bot_name",
            "is_active",
            "is_error",
            "date",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def active_accounts(self, bot_name: str) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                Accounts.id,
                Accounts.user_id,
                Accounts.referral_token,
                Accounts.account_name,
                Accounts.access_token,
                Accounts.refresh_token,
                Accounts.bot_name,
                Accounts.is_active,
                Accounts.is_error,
                Accounts.date,
            ).where(Accounts.is_active == 1, Accounts.bot_name == bot_name)
        )
        dict_keys = [
            "id",
            "user_id",
            "referral_token",
            "account_name",
            "access_token",
            "refresh_token",
            "bot_name",
            "is_active",
            "is_error",
            "date",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def hamster_account_statistic(self, account_id: int) -> Dict[str, any]:
        result = await self.session.execute(
            select(
                HamsterAccountStatistics.id,
                HamsterAccountStatistics.account_id,
                HamsterAccountStatistics.max_taps,
                HamsterAccountStatistics.earn_per_tap,
                HamsterAccountStatistics.earn_passive_per_hour,
                HamsterAccountStatistics.earn_passive_per_sec,
                HamsterAccountStatistics.taps_recover_per_sec,
                HamsterAccountStatistics.balance_coins,
                HamsterAccountStatistics.referral_count,
                HamsterAccountStatistics.date,
            )
            .where(HamsterAccountStatistics.account_id == account_id)
            .order_by(HamsterAccountStatistics.date.desc())
            .limit(1)
        )
        dict_keys = [
            "id",
            "account_id",
            "max_taps",
            "earn_per_tap",
            "earn_passive_per_hour",
            "earn_passive_per_sec",
            "taps_recover_per_sec",
            "balance_coins",
            "referral_count",
            "date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def hamster_upgrade_purchases(
        self, account_id: int, page: int = 0, items_per_page: int = 25
    ) -> List[Dict[str, any]]:
        offset = (page - 1) * items_per_page
        result = await self.session.execute(
            select(
                HamsterUpgradePurchases.id,
                HamsterUpgradePurchases.account_id,
                HamsterUpgradePurchases.upgrade_id,
                HamsterUpgradePurchases.upgrade_name,
                HamsterUpgradePurchases.upgrade_level,
                HamsterUpgradePurchases.upgrade_section,
                HamsterUpgradePurchases.upgrade_price,
                HamsterUpgradePurchases.date,
            )
            .where(HamsterUpgradePurchases.account_id == account_id)
            .order_by(HamsterUpgradePurchases.date.desc())
            .limit(items_per_page)
            .offset(offset)
        )
        dict_keys = [
            "id",
            "account_id",
            "upgrade_id",
            "upgrade_name",
            "upgrade_level",
            "upgrade_section",
            "upgrade_price",
            "date",
        ]
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def blum_account_statistic(self, account_id: int) -> Dict[str, any]:
        result = await self.session.execute(
            select(
                BlumAccountStatistics.id,
                BlumAccountStatistics.account_id,
                BlumAccountStatistics.available_balance,
                BlumAccountStatistics.play_passes,
                BlumAccountStatistics.earnings_rate,
                BlumAccountStatistics.limit_invitation,
                BlumAccountStatistics.used_invitation,
                BlumAccountStatistics.amount_for_claim,
                BlumAccountStatistics.date,
            )
            .where(BlumAccountStatistics.account_id == account_id)
            .order_by(BlumAccountStatistics.date.desc())
            .limit(1)
        )
        dict_keys = [
            "id",
            "account_id",
            "available_balance",
            "play_passes",
            "earnings_rate",
            "limit_invitation",
            "used_invitation",
            "amount_for_claim",
            "date",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}
