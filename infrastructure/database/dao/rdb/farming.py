import time
from typing import List, Dict

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    Accounts,
    HamsterAccountStatistics,
    HamsterUpgradePurchases,
    BlumAccountStatistics,
    TapswapAccountStatistics,
    HorizonAccountStatistics,
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

    async def account_status(self, account_id: int, user_id: int, is_active: bool):
        await self.session.execute(
            update(Accounts)
            .where(Accounts.id == account_id, Accounts.user_id == user_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def update_account(self, account_id: int, user_id: int, referral_token: str,
                             account_name: str, access_token: str, refresh_token: str = None,
                             is_active: int = 1, is_error: int = 0, date: int = None):
        if date is None:
            date = int(time.time())

        await self.session.execute(
            update(Accounts)
            .where(Accounts.id == account_id, Accounts.user_id == user_id)
            .values(
                referral_token=referral_token,
                account_name=account_name,
                access_token=access_token,
                refresh_token=refresh_token,
                is_active=is_active,
                is_error=is_error,
                date=date,
            )
        )
        await self.session.commit()

    async def insert_account(self, user_id: int, referral_token: str, account_name: str,
                             access_token: str, bot_name: str, refresh_token: str = None,
                             is_active: int = 1, is_error: int = 0, date: int = None):
        if date is None:
            date = int(time.time())

        result = await self.session.execute(
            insert(Accounts).values(
                user_id=user_id,
                referral_token=referral_token,
                account_name=account_name,
                access_token=access_token,
                refresh_token=refresh_token,
                bot_name=bot_name,
                is_active=is_active,
                is_error=is_error,
                date=date,
            )
        )
        await self.session.commit()

        return result.lastrowid

    async def insert_hamster_account_statistic(self, account_id: int, max_taps: int, earn_per_tap: int,
                                               earn_passive_per_hour: float, earn_passive_per_sec: float,
                                               taps_recover_per_sec: float, balance_coins: float,
                                               referral_count: int = 0, date: int = None):
        if date is None:
            date = int(time.time())

        result = await self.session.execute(
            insert(HamsterAccountStatistics).values(
                account_id=account_id,
                max_taps=max_taps,
                earn_per_tap=earn_per_tap,
                earn_passive_per_hour=earn_passive_per_hour,
                earn_passive_per_sec=earn_passive_per_sec,
                taps_recover_per_sec=taps_recover_per_sec,
                balance_coins=balance_coins,
                referral_count=referral_count,
                date=date,
            )
        )
        await self.session.commit()

        return result.lastrowid

    async def insert_hamster_upgrade_purchase(self, account_id: int, upgrade_id: str, upgrade_name: str,
                                              upgrade_level: int, upgrade_section: str,
                                              upgrade_price: float, date: int = None):
        if date is None:
            date = int(time.time())

        await self.session.execute(
            insert(HamsterUpgradePurchases).values(
                account_id=account_id,
                upgrade_id=upgrade_id,
                upgrade_name=upgrade_name,
                upgrade_level=upgrade_level,
                upgrade_section=upgrade_section,
                upgrade_price=upgrade_price,
                date=date,
            )
        )
        await self.session.commit()

    async def insert_blum_account_statistic(self, account_id: int, available_balance: float, play_passes: int,
                                            earnings_rate: float, limit_invitation: int, used_invitation: int,
                                            amount_for_claim: float, date: int = None):
        if date is None:
            date = int(time.time())

        result = await self.session.execute(
            insert(BlumAccountStatistics).values(
                account_id=account_id,
                available_balance=available_balance,
                play_passes=play_passes,
                earnings_rate=earnings_rate,
                limit_invitation=limit_invitation,
                used_invitation=used_invitation,
                amount_for_claim=amount_for_claim,
                date=date,
            )
        )
        await self.session.commit()

        return result.lastrowid

    async def insert_tapswap_account_statistic(self, account_id: int, shares: int, ligue: int, energy_level: int,
                                               charge_level: int, boost_energy_count: int, boost_turbo_count: int,
                                               stat_taps: int, stat_ref_in: int,
                                               stat_ref_out: int, stat_ref_cnt: int, stat_earned: int,
                                               stat_reward: int, stat_spent: int, date: int = None):
        if date is None:
            date = int(time.time())

        result = await self.session.execute(
            insert(TapswapAccountStatistics).values(
                account_id=account_id,
                shares=shares,
                ligue=ligue,
                energy_level=energy_level,
                charge_level=charge_level,
                boost_energy_count=boost_energy_count,
                boost_turbo_count=boost_turbo_count,
                stat_taps=stat_taps,
                stat_ref_in=stat_ref_in,
                stat_ref_out=stat_ref_out,
                stat_ref_cnt=stat_ref_cnt,
                stat_earned=stat_earned,
                stat_reward=stat_reward,
                stat_spent=stat_spent,
                date=date,
            )
        )
        await self.session.commit()

        return result.lastrowid

    async def insert_horizon_account_statistic(self, account_id: int,  last_sync_timestamp: int, last_tap_timestamp: int,
                                               last_boost_timestamp: int, boost_attempts: int, boost_taps: int,
                                               distance: float, delta: float, speed: float, referrals_count: int,
                                               is_banned: int, is_active: int, is_premium: int):
        result = await self.session.execute(
            insert(HorizonAccountStatistics).values(
                account_id=account_id,
                last_sync_timestamp=last_sync_timestamp,
                last_tap_timestamp=last_tap_timestamp,
                last_boost_timestamp=last_boost_timestamp,
                boost_attempts=boost_attempts,
                boost_taps=boost_taps,
                distance=distance,
                delta=delta,
                speed=speed,
                referrals_count=referrals_count,
                is_banned=is_banned,
                is_active=is_active,
                is_premium=is_premium,
            )
        )
        await self.session.commit()

        return result.lastrowid

    async def delete_account(self, account_id: int):
        await self.session.execute(
            delete(HamsterUpgradePurchases)
            .where(HamsterUpgradePurchases.account_id == account_id)
        )
        await self.session.execute(
            delete(HamsterAccountStatistics)
            .where(HamsterAccountStatistics.account_id == account_id)
        )
        await self.session.execute(
            delete(BlumAccountStatistics)
            .where(BlumAccountStatistics.account_id == account_id)
        )
        await self.session.execute(
            delete(Accounts)
            .where(Accounts.id == account_id)
        )

        await self.session.commit()
