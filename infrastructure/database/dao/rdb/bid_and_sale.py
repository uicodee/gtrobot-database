from typing import List, Dict

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    BidAndSaleUsers, BidAndSaleSymbols, BidAndSaleUserSymbols
)


class BidAndSaleDAO(BaseDAO[BidAndSaleUsers]):
    def __init__(self, session: AsyncSession):
        super().__init__(BidAndSaleUsers, session)

    async def get_active_users_with_symbol_id(self, symbol_id: int, tx_value: int) -> List[int]:
        result = await self.session.execute(
            select(BidAndSaleUsers.user_id)
            .join(BidAndSaleUserSymbols, BidAndSaleUserSymbols.user_id == BidAndSaleUsers.user_id)
            .where(
                BidAndSaleUsers.is_active == True,
                BidAndSaleUserSymbols.symbol_id == symbol_id,
                BidAndSaleUserSymbols.tx_value <= tx_value,
            )
        )
        return [row[0] for row in result.fetchall()]

    async def get_active_users(self) -> List[int]:
        result = await self.session.execute(
            select(BidAndSaleUsers.user_id)
            .where(BidAndSaleUsers.is_active == True)
        )
        return [row[0] for row in result.fetchall()]

    async def get_user_symbols(self, user_id: int) -> List[str]:
        result = await self.session.execute(
            select(BidAndSaleSymbols.name)
            .join(BidAndSaleUserSymbols, BidAndSaleUserSymbols.symbol_id == BidAndSaleSymbols.id)
            .where(BidAndSaleUserSymbols.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

    async def get_user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(BidAndSaleUsers)
            .where(BidAndSaleUsers.user_id == user_id)
        )
        return result.fetchone() is not None

    async def get_user_active_status(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(BidAndSaleUsers.is_active)
            .where(BidAndSaleUsers.user_id == user_id)
        )
        return bool(result.scalar())

    async def get_symbols(self) -> List[Dict[str, int]]:
        result = await self.session.execute(
            select(BidAndSaleSymbols.id, BidAndSaleSymbols.name)
        )
        return [{'id': row[0], 'name': row[1]} for row in result.fetchall()]

    async def get_symbol_id(self, name: str) -> int:
        result = await self.session.execute(
            select(BidAndSaleSymbols.id).where(BidAndSaleSymbols.name == name)
        )
        data = result.scalar()
        return data if data is not None else -1

    async def update_user_active_status(self, user_id: int, is_active: bool):
        await self.session.execute(
            update(BidAndSaleUsers)
            .where(BidAndSaleUsers.user_id == user_id)
            .values(is_active=is_active)
        )
        await self.session.commit()

    async def add_user(self, user_id: int, is_active: bool = True):
        await self.session.execute(
            insert(BidAndSaleUsers)
            .values(user_id=user_id, is_active=is_active)
        )
        await self.session.commit()

    async def add_user_symbols(self, data: list):
        await self.session.execute(
            insert(BidAndSaleUserSymbols),
            [{"user_id": user_id, "symbol_id": symbol_id, "tx_value": tx_value} for user_id, symbol_id, tx_value in data]
        )
        await self.session.commit()

    async def add_symbol(self, symbol: str):
        await self.session.execute(
            insert(BidAndSaleSymbols)
            .values(name=symbol)
        )
        await self.session.commit()

    async def del_user_symbols(self, data: list):
        await self.session.execute(
            delete(BidAndSaleUserSymbols),
            [{"user_id": user_id, "symbol_id": symbol_id} for user_id, symbol_id in data]
        )
        await self.session.commit()
