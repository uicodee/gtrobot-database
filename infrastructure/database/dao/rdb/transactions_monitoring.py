import time

import const
from typing import List, Dict

from sqlalchemy import select, update, insert, delete, func, exists, case
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    StocksBalance, Wallet, WalletBalances, PersonalWalletAssets, Follow, WalletTags, WalletsUsers, UserAPI, UserOrders,
    WalletInfo, Tags
)


class TransactionMonitoringDAO(BaseDAO[WalletsUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(WalletsUsers, session)

    async def get_stocks_balance(self, wallet_id: int):
        stmt = (
            select(StocksBalance)
            .join(Wallet, (Wallet.id == StocksBalance.wallet_id))
            .filter((Wallet.wallet_id == wallet_id) | (Wallet.parent_id == wallet_id))
        )
        result = await self.session.execute(stmt)

        stocks_balance = result.scalars().all()

        return stocks_balance if stocks_balance else None

    async def get_wallet_by_id(self, wallet_id: int):
        stmt = select(Wallet).filter(Wallet.id == wallet_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_wallet_addresses_by_parent_id(self, parent_id: int):
        stmt = select(Wallet.address).filter(Wallet.parent_id == parent_id)
        result = await self.session.execute(stmt)
        addresses = result.scalars().all()
        return addresses

    async def get_wallet_balance(self, wallet_id: int):
        stmt = (
            select(WalletBalances.balance)
            .join(Wallet, Wallet.id == WalletBalances.wallet_id)
            .filter((Wallet.wallet_id == wallet_id) | (Wallet.parent_id == wallet_id))
            .order_by(WalletBalances.created_at.desc())
            .group_by(WalletBalances.wallet_id)
        )
        result = await self.session.execute(stmt)
        balances = result.scalars().all()
        return sum(balances) if balances else None

    async def get_wallet_by_address(self, address: str):
        stmt = select(Wallet).filter(Wallet.address == address)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_wallet_id_by_address(self, address: str):
        stmt = select(Wallet.id).filter(Wallet.address == address)
        result = await self.session.execute(stmt)
        wallet_id = result.scalar()
        return wallet_id

    async def get_wallets(self):
        subquery = (
            select(WalletBalances.wallet_id, func.max(WalletBalances.id).label("max_id"))
            .group_by(WalletBalances.wallet_id)
            .alias("max_wallet_balances")
        )

        stmt = (
            select(
                Wallet.id,
                Wallet.address,
                Wallet.last_block_number,
                func.coalesce(WalletBalances.balance, 0).label("balance"),
                Wallet.network,
                Wallet.created_at,
                Wallet.parent_id,
                Wallet.is_personal_wallet,
            )
            .outerjoin(subquery, subquery.c.wallet_id == Wallet.id)
            .outerjoin(WalletBalances, WalletBalances.id == subquery.c.max_id)
            .outerjoin(Follow, Follow.wallet_id == Wallet.id)
            .filter((Follow.id.isnot(None)) | (Wallet.parent_id.isnot(None)))
            .group_by(
                Wallet.id,
                Wallet.address,
                Wallet.last_block_number,
                Wallet.network,
                Wallet.created_at,
                Wallet.parent_id,
                Wallet.is_personal_wallet,
                WalletBalances.balance,
            )
        )
        result = await self.session.execute(stmt)
        return result.fetchall()

    async def get_users_by_wallet(self, wallet_id: int):
        stmt = select(WalletsUsers.user_id).filter(WalletsUsers.wallet_id == wallet_id)
        result = await self.session.execute(stmt)
        return [row.user_id for row in result.scalars()]

    async def get_wallets_by_user_id(self, user_id: int):
        stmt = (
            select(Wallet.id, Wallet.address, Follow.name, Follow.info)
            .join(Follow, Follow.wallet_id == Wallet.id)
            .filter(Follow.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.fetchall()

    async def get_personal_wallet_assets(self, wallet_id: int):
        stmt = select(PersonalWalletAssets).filter(PersonalWalletAssets.wallet_id == wallet_id)
        result = await self.session.execute(stmt)
        assets = result.fetchall()
        return [dict(asset) for asset in assets]

    async def get_follow_wallet_ids(self, user_id: int = None,
                                    wallet_name: str = '',
                                    wallet_tags: list = None,
                                    wallet_network: str = None,
                                    wallet_address: str = '',
                                    is_full_search: bool = False,
                                    is_personal_wallet: bool = False):
        stmt = select(Wallet.id).distinct().join(Follow, Wallet.id == Follow.wallet_id, isouter=True)

        if not is_full_search:
            stmt = stmt.filter(Follow.user_id == user_id)

        if not user_id and not is_full_search:
            stmt = stmt.filter(Wallet.is_personal_wallet == is_personal_wallet)

        if wallet_name:
            stmt = stmt.filter(func.lower(Follow.name).like(func.lower(wallet_name)))

        if wallet_tags:
            stmt = stmt.join(WalletTags, Wallet.id == WalletTags.wallet_id).filter(
                WalletTags.tag_id.in_(wallet_tags)
            )

        if wallet_network:
            stmt = stmt.filter(Wallet.network == wallet_network)

        if wallet_address:
            stmt = stmt.filter(Wallet.address == wallet_address)

        if not is_full_search:
            stmt = stmt.order_by(Follow.created_at.desc())

        result = await self.session.execute(stmt)
        return [d[0] for d in result.fetchall()]

    async def get_wallet_ids(self, wallet_name: str = '', wallet_tags: list = None):
        wallet_name = f'%{wallet_name.lower()}%'

        stmt = select(Wallet.id).distinct().join(Follow, Wallet.id == Follow.wallet_id)
        stmt = stmt.filter(func.lower(Follow.name).like(func.lower(wallet_name)))

        if wallet_tags:
            stmt = stmt.join(WalletTags, Wallet.id == WalletTags.wallet_id).filter(
                WalletTags.tag.in_(wallet_tags)
            )

        result = await self.session.execute(stmt)

        return [wallet.id for wallet in result.scalars().all()]

    async def get_wallet_name_by_user(self, user_id: int, wallet_id: int):
        stmt = select(Follow.name).filter(Follow.user_id == user_id, Follow.wallet_id == wallet_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_wallet_name_by_address(self, user_id: int, address: str):
        stmt = (
            select(Follow.name)
            .filter(Follow.user_id == user_id)
            .join(Wallet, Wallet.id == Follow.wallet_id)
            .filter(Wallet.address == address)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_follow_users(self, address: str):
        stmt = (
            select(Follow.user_id)
            .join(Wallet, Wallet.id == Follow.wallet_id)
            .filter(Wallet.address == address)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def check_wallet_follow(self, user_id: int, wallet_id: int) -> bool:
        stmt = select(exists().where(Follow.user_id == user_id, Follow.wallet_id == wallet_id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_wallet_follow_count_by_user(self, user_id: int) -> int:
        stmt = select([func.count()]).select_from(Follow).filter(Follow.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_api_id(self, user_id: int) -> int:
        stmt = select(UserAPI.id).filter(UserAPI.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar() if result else None

    async def get_user_api_data(self, api_id: int) -> dict:
        stmt = select(
            UserAPI.id,
            UserAPI.user_id,
            UserAPI.api_key,
            UserAPI.api_secret,
            UserAPI.api_passphrase,
            UserAPI.user_exchange
        ).filter(UserAPI.id == api_id)
        result = await self.session.execute(stmt)
        row = result.fetchone()
        if row:
            dict_keys = ['id', 'user_id', 'api_key', 'api_secret', 'api_passphrase', 'user_exchange']
            return dict(zip(dict_keys, row))
        return {}

    async def check_order_existence(self, user_id: int, symbol: str):
        stmt = select(exists().where(UserOrders.user_id == user_id, UserOrders.symbol == symbol))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_follow_wallet_name_exists(self, user_id: int, name: str):
        stmt = select(exists().where(Follow.user_id == user_id, Follow.name == name))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_stock_balance(self, wallet_id: int, stock: str):
        stmt = select(StocksBalance.balance).filter(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock)
        result = await self.session.execute(stmt)
        row = result.fetchone()
        return row[0] if row else 0

    async def get_stock_quote(self, wallet_id: int, stock: str):
        stmt = select(StocksBalance.quote).filter(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock)
        result = await self.session.execute(stmt)
        row = result.fetchone()
        return row[0] if row else 0

    async def get_wallet_stock_symbols(self, wallet_id: int):
        stmt = (
            select(StocksBalance.stock)
            .filter(StocksBalance.wallet_id.in_(
                select(Wallet.id).filter((Wallet.id == wallet_id) | (Wallet.parent_id == wallet_id))))
            .order_by(StocksBalance.quote.desc())
        )
        result = await self.session.execute(stmt)
        return [stock[0] for stock in result.fetchall()]

    async def get_wallet_order_symbols(self, user_id: int):
        stmt = select(UserOrders.symbol).filter(UserOrders.user_id == user_id)
        result = await self.session.execute(stmt)
        return [symbol[0] for symbol in result.fetchall()]

    async def stock_balance_exists(self, wallet_id: int, stock: str):
        stmt = select(exists().where(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def wallet_data(self, wallet_id: int, user_id: int = 0):
        stmt = (
            select(
                Wallet.id,
                Follow.name,
                case(
                    (
                        (select([1]).filter(Wallet.parent_id == wallet_id).exists(), Wallet.address)
                    ),
                    else_=None
                ).label('address'),
                func.coalesce(func.sum(WalletBalances.balance), 0).label('balance'),
                case(
                    (
                        (select([True]).filter(Follow.wallet_id == Wallet.id, Follow.user_id == 0).exists(), True)
                    ),
                    else_=False
                ).label('user_check'),
                Wallet.network,
                func.group_concat(WalletTags.tag_id).label('tags'),
                Wallet.is_available_free
            )
            .outerjoin(Follow, (Follow.wallet_id == Wallet.id) & (Follow.user_id == user_id))
            .outerjoin(WalletTags, WalletTags.wallet_id == Wallet.id)
            .outerjoin(
                (select(
                    WalletBalances.wallet_id,
                    func.max(WalletBalances.created_at).label('max_created'),
                    WalletBalances.balance
                ).group_by(WalletBalances.wallet_id).alias('wb')),
                Wallet.id == WalletBalances.wallet_id
            )
            .filter(Wallet.id == wallet_id)
            .group_by(Wallet.id)
        )

        result = await self.session.execute(stmt)
        wallet_data_dict = {'miniDescription': {}, 'description': {}}

        for data in result:
            wallet_data_dict.update(dict(
                zip(['walletId', 'name', 'address', 'balance', 'isVerified', 'network', 'tags', 'isAvailableFree'],
                    data)))
            wallet_data_dict['tags'] = [int(tag.strip()) for tag in
                                        set(wallet_data_dict.get('tags', '').split(','))] if wallet_data_dict.get(
                'tags') else []
            wallet_data_dict['isVerified'] = bool(wallet_data_dict['isVerified'])
            wallet_data_dict['isAvailableFree'] = bool(wallet_data_dict['isAvailableFree'])

        for locale in const.LOCALES:
            wallet_data_dict['miniDescription'][locale] = None
            wallet_data_dict['description'][locale] = None

            stmt_info = select(WalletInfo.mini_description, WalletInfo.description).filter(
                WalletInfo.wallet_id == wallet_id,
                WalletInfo.locale == locale
            )
            result_info = await self.session.execute(stmt_info)
            if result_info:
                mini_desc, desc = result_info.fetchone()
                wallet_data_dict['miniDescription'][locale] = mini_desc
                wallet_data_dict['description'][locale] = desc

        return wallet_data_dict

    async def get_wallet_chart(self, wallet_id: int):
        stmt = (
            select(WalletBalances.created_at, WalletBalances.balance, WalletBalances.wallet_id)
            .filter(WalletBalances.wallet_id.in_(
                select(Wallet.id).filter((Wallet.id == wallet_id) | (Wallet.parent_id == wallet_id))
            ))
        )
        result = await self.session.execute(stmt)
        result = result.fetchall()

        wallets = {}
        for wallet in result:
            wallets.setdefault(wallet[2], []).append([wallet[0], wallet[1]])

        summed_result = []
        if wallets:
            first_wallet = list(wallets.keys())[0]
            summed_result = wallets[first_wallet]
            for wallet_data in summed_result:
                for w in wallets:
                    if w == first_wallet:
                        continue
                    for d in wallets[w]:
                        if abs(wallet_data[0] - d[0]) < 7200:
                            wallet_data[1] += d[1]
                            break
        return summed_result

    async def get_whale_tags(self) -> dict:
        tags_data = {}
        for locale in const.LOCALES:
            stmt = select(Tags.id, Tags.name, Tags.parent_id).filter(Tags.locale == locale)
            result = await self.session.execute(stmt)
            result = result.fetchall()

            for tag in result:
                tag_id = tag[0] if tag[2] is None else tag[2]
                if tag_id not in tags_data:
                    tags_data[tag_id] = {locale: tag[1]}
                else:
                    tags_data[tag_id][locale] = tag[1]

        return tags_data

    async def add_stocks_balance(self, wallet_id, stock, balance, quote):
        stmt = (
            update(StocksBalance)
            .filter(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock)
            .values(
                balance=StocksBalance.balance + balance,
                quote=StocksBalance.quote + quote
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def reduce_stocks_balance(self, wallet_id, stock, balance, quote):
        stmt = (
            update(StocksBalance)
            .filter(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock)
            .values(
                balance=StocksBalance.balance - balance,
                quote=StocksBalance.quote - quote
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_stocks_balance(self, wallet_id, stock, balance, quote):
        stmt = (
            update(StocksBalance)
            .filter(StocksBalance.wallet_id == wallet_id, StocksBalance.stock == stock)
            .values(
                balance=balance,
                quote=quote
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_wallet_last_blocks(self, wallet_id: int, last_blocks: str) -> None:
        stmt = (
            update(Wallet)
            .filter(Wallet.id == wallet_id)
            .values(last_block_number=last_blocks)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_wallet(self, wallet_id: int, name: str = None, last_block_number: str = None) -> None:
        stmt = (
            update(Wallet)
            .filter(Wallet.id == wallet_id)
            .values(name=name, last_block_number=last_block_number)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def set_wallet_balance(self, wallet_id: int, balance: float) -> None:
        stmt = (
            update(WalletBalances)
            .filter(WalletBalances.wallet_id == wallet_id)
            .values(balance=balance)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def add_wallet_last_block(self, wallet_id: int, last_block: str) -> None:
        stmt = (
            update(Wallet)
            .filter(Wallet.id == wallet_id)
            .values(last_block_number=last_block)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def reduce_wallet_balance(self, wallet_id: int, balance: float) -> None:
        stmt = (
            update(Wallet)
            .filter(Wallet.id == wallet_id)
            .values(balance=Wallet.balance - balance)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_user_api(self, api_id: int, api_key: str, api_secret: str,
                              api_passphrase: str, user_exchange: str = 'Binance') -> None:
        stmt = (
            update(UserAPI)
            .filter(UserAPI.id == api_id)
            .values(
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase,
                user_exchange=user_exchange
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_follow_name(self, user_id: int, wallet_id: int, wallet_name: str) -> None:
        stmt = (
            update(Follow)
            .filter(Follow.user_id == user_id, Follow.wallet_id == wallet_id)
            .values(name=wallet_name)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def insert_stocks_balance(self, data) -> None:
        stmt = insert(StocksBalance).values(data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_wallet(self, address: str, network: str = None, last_block_number: str = None) -> int:
        stmt = insert(Wallet).values(
            address=address,
            network=network,
            last_block_number=last_block_number
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.inserted_primary_key[0]

    async def create_follow(self, user_id: int, wallet_id: int, name: str, created_at: int = None):
        if not created_at:
            created_at = int(time.time())

        stmt = insert(Follow).values(
            user_id=user_id,
            wallet_id=wallet_id,
            name=name,
            created_at=created_at
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_user_api(self, user_id: int, api_key: str, api_secret: str, api_passphrase: str,
                              user_exchange: str = 'Binance'):
        stmt = insert(UserAPI).values(
            user_id=user_id,
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
            user_exchange=user_exchange
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_user_order(self, wallet_address: str, symbol: str, user_id: int, order_id: str,
                                order_amount: float, is_spot_order: bool = True, is_market: bool = True,
                                order_time: int = None):
        if not order_time:
            order_time = int(time.time())

        stmt = insert(UserOrders).values(
            wallet_address=wallet_address,
            symbol=symbol,
            user_id=user_id,
            order_id=order_id,
            order_time=order_time,
            order_amount=order_amount,
            is_spot_order=int(is_spot_order),
            is_market=int(is_market)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def insert_wallet_balance(self, wallet_id: int, balance: float, created_at: int = None) -> None:
        if not created_at:
            created_at = int(time.time())

        stmt = insert(WalletBalances).values(
            wallet_id=wallet_id,
            balance=balance,
            created_at=created_at
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_follow(self, user_id: int, wallet_id: int):
        stmt = (
            delete(Follow)
            .filter(Follow.user_id == user_id, Follow.wallet_id == wallet_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_not_followed_wallets(self):
        stmt = (
            delete(Wallet)
            .where(Wallet.id.notin_(select(Follow.wallet_id.distinct())))
            .where(Wallet.parent_id == None)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_stocks_for_not_existsing_wallets(self):
        stmt = (
            delete(StocksBalance)
            .where(StocksBalance.wallet_id.notin_(select(Wallet.id.distinct())))
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_wallet(self, wallet_id: int):
        stmt = delete(Wallet).where(Wallet.id == wallet_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_stock(self, wallet_id: int, stock: str):
        stmt = (
            delete(StocksBalance)
            .where(StocksBalance.wallet_id == wallet_id)
            .where(StocksBalance.stock == stock)
        )
        await self.session.execute(stmt)
        await self.session.commit()
