from typing import List, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import P2PUsers, P2PPairs, P2PPairsExchange, AutoDeleteMessage


class P2PDAO(BaseDAO[P2PUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(P2PUsers, session)

    async def get_all_p2p_autodelete_messages(self) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                AutoDeleteMessage.user_id,
                AutoDeleteMessage.message_id,
                AutoDeleteMessage.current_time
            )
        )
        dict_keys = ['user_id', 'message_id', 'current_time']
        return [dict(zip(dict_keys, row)) for row in result.fetchall()]

    async def get_new_p2p_pair_data(self) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                P2PPairs.id, P2PPairs.profit, P2PPairs.asset_buy, P2PPairs.price_buy,
                P2PPairs.payment_buy, P2PPairs.asset_sell, P2PPairs.price_sell,
                P2PPairs.payment_sell, P2PPairs.exchange, P2PPairs.currency
            ).where(P2PPairs.is_post == 0)
        )
        dict_keys = ['id', 'profit', 'asset_buy', 'price_buy', 'payment_buy', 'asset_sell', 'price_sell',
                     'payment_sell', 'exchange', 'currency']
        return [dict(zip(dict_keys, map(str, row))) for row in result.fetchall()]

    async def get_new_p2p_pair_exchanges_data(self) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                P2PPairsExchange.id, P2PPairsExchange.profit, P2PPairsExchange.asset,
                P2PPairsExchange.price_buy, P2PPairsExchange.exchange_buy,
                P2PPairsExchange.price_sell, P2PPairsExchange.exchange_sell
            ).where(P2PPairsExchange.is_post == 0)
        )
        dict_keys = ['id', 'profit', 'asset', 'price_buy', 'exchange_buy', 'price_sell', 'exchange_sell']
        return [dict(zip(dict_keys, map(str, row))) for row in result.fetchall()]

    async def get_active_p2p_user_data(self) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                P2PUsers.user_id, P2PUsers.profit_percent, P2PUsers.exchanges
            ).where(
                (P2PUsers.is_active == 1) | (P2PUsers.is_active_exchanges == 1)
            )
        )
        dict_keys = ['user_id', 'profit_percent', 'exchanges']
        return [dict(zip(dict_keys, map(str, row))) for row in result.fetchall()]

    async def get_active_p2p_user_exchanges_data(self) -> List[Dict[str, any]]:
        result = await self.session.execute(
            select(
                P2PUsers.user_id, P2PUsers.profit_percent, P2PUsers.exchanges
            ).where(P2PUsers.is_active_exchanges == 1)
        )
        dict_keys = ['user_id', 'profit_percent', 'exchanges']
        return [dict(zip(dict_keys, map(str, row))) for row in result.fetchall()]

    async def get_p2p_user_exchanges_data(self, user_id: int) -> Optional[str]:
        result = await self.session.execute(
            select(P2PUsers.exchanges).where(P2PUsers.user_id == user_id)
        )
        return result.scalar()

    async def get_p2p_user_profit_data(self, user_id: int) -> Optional[float]:
        result = await self.session.execute(
            select(P2PUsers.profit_percent).where(P2PUsers.user_id == user_id)
        )
        return result.scalar()

    async def p2p_pair_exists(self, asset_buy: str, payment_buy: str, asset_sell: str, payment_sell: str,
                              exchange: str) -> bool:
        result = await self.session.execute(
            select(P2PPairs).where(
                P2PPairs.asset_buy == asset_buy,
                P2PPairs.payment_buy == payment_buy,
                P2PPairs.asset_sell == asset_sell,
                P2PPairs.exchange == exchange,
                P2PPairs.payment_sell == payment_sell
            )
        )
        return result.fetchone() is not None

    async def p2p_pair_exchange_exists(self, asset: str, exchange_buy: str, exchange_sell: str) -> bool:
        result = await self.session.execute(
            select(P2PPairsExchange).where(
                P2PPairsExchange.asset == asset,
                P2PPairsExchange.exchange_buy == exchange_buy,
                P2PPairsExchange.exchange_sell == exchange_sell
            )
        )
        return result.fetchone() is not None

    async def p2p_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(P2PUsers).where(P2PUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def p2p_user_is_active(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(P2PUsers.is_active).where(P2PUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def p2p_user_is_active_exchanges(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(P2PUsers.is_active_exchanges).where(P2PUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def update_p2p_pair_status(self, pair_id: int, is_post: bool = True) -> None:
        await self.session.execute(
            update(P2PPairs)
            .where(P2PPairs.id == pair_id)
            .values(is_post=is_post)
        )
        await self.session.commit()

    async def update_p2p_pair_exchange_status(self, pair_id: int, is_post: bool = True) -> None:
        await self.session.execute(
            update(P2PPairsExchange)
            .where(P2PPairsExchange.id == pair_id)
            .values(is_post=is_post)
        )
        await self.session.commit()

    async def update_p2p_pair_exchanges(self, user_id: int, exchanges: str) -> None:
        await self.session.execute(
            update(P2PUsers)
            .where(P2PUsers.user_id == user_id)
            .values(exchanges=exchanges)
        )
        await self.session.commit()

    async def update_p2p_exchanges_user_status(self, user_id: int, is_active: bool) -> None:
        await self.session.execute(
            update(P2PUsers)
            .where(P2PUsers.user_id == user_id)
            .values(is_active_exchanges=is_active)
        )
        await self.session.commit()

    async def update_p2p_user_percent(self, user_id: int, profit_percent: float) -> None:
        await self.session.execute(
            update(P2PUsers)
            .where(P2PUsers.user_id == user_id)
            .values(profit_percent=profit_percent)
        )
        await self.session.commit()

    async def update_p2p_user_status(self, user_id: int, is_active: bool) -> None:
        await self.session.execute(
            update(P2PUsers)
            .where(P2PUsers.user_id == user_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def update_p2p_user_statuses(self, user_id: int, is_active: bool = False) -> None:
        await self.session.execute(
            update(P2PUsers)
            .where(P2PUsers.user_id == user_id)
            .values(is_active=is_active, is_active_exchanges=is_active)
        )
        await self.session.commit()

    async def set_p2p_user_data(self, user_id: int, profit_percent: float) -> None:
        await self.session.execute(
            insert(P2PUsers).values(
                user_id=user_id,
                profit_percent=profit_percent
            )
        )
        await self.session.commit()

    async def set_p2p_pair_data(self, profit: float, asset_buy: str, price_buy: float,
                                payment_buy: str, asset_sell: str, price_sell: float,
                                payment_sell: str, exchange: str, currency: str) -> None:
        await self.session.execute(
            insert(P2PPairs).values(
                profit=profit,
                asset_buy=asset_buy,
                price_buy=price_buy,
                payment_buy=payment_buy,
                asset_sell=asset_sell,
                price_sell=price_sell,
                payment_sell=payment_sell,
                exchange=exchange,
                currency=currency
            )
        )
        await self.session.commit()

    async def set_p2p_pair_exchanges_data(self, profit: float, asset: str, price_buy: float, exchange_buy: str,
                                          price_sell: float, exchange_sell: str) -> None:
        await self.session.execute(
            insert(P2PPairsExchange).values(
                profit=profit,
                asset=asset,
                price_buy=price_buy,
                exchange_buy=exchange_buy,
                price_sell=price_sell,
                exchange_sell=exchange_sell
            )
        )
        await self.session.commit()

    async def set_p2p_autodelete_message(self, user_id: int, message_id: int, current_time: int) -> None:
        await self.session.execute(
            insert(P2PUsers).values(
                user_id=user_id,
                message_id=message_id,
                current_time=current_time
            )
        )
        await self.session.commit()

    async def del_p2p_autodelete_message(self, user_id: int, message_id: int) -> None:
        await self.session.execute(
            delete(P2PUsers)
            .where(P2PUsers.user_id == user_id, P2PUsers.message_id == message_id)
        )
        await self.session.commit()

    async def delete_old_p2p_pairs(self, currency: str = 'UZS', count_pairs: int = 1) -> None:
        result = await self.session.execute(
            select(P2PPairs.id)
            .where(P2PPairs.currency == currency)
            .order_by(P2PPairs.id)
            .limit(count_pairs)
        )
        ids_to_delete = [row[0] for row in result.fetchall()]
        if ids_to_delete:
            await self.session.execute(
                delete(P2PPairs).where(P2PPairs.id.in_(ids_to_delete))
            )
            await self.session.commit()

    async def delete_old_p2p_pairs_exchange(self, count_pairs: int = 1) -> None:
        result = await self.session.execute(
            select(P2PPairsExchange.id)
            .order_by(P2PPairsExchange.id)
            .limit(count_pairs)
        )
        ids_to_delete = [row[0] for row in result.fetchall()]
        if ids_to_delete:
            await self.session.execute(
                delete(P2PPairsExchange).where(P2PPairsExchange.id.in_(ids_to_delete))
            )
            await self.session.commit()

