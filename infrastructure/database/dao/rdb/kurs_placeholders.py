from typing import List, Dict
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import KursPlaceholders


class KursPlaceholdersDAO(BaseDAO[KursPlaceholders]):
    def __init__(self, session: AsyncSession):
        super().__init__(KursPlaceholders, session)

    async def set_kurs_placeholder(self, symbol: str, file_id: str):
        await self.session.execute(
            insert(KursPlaceholders).values(symbol=symbol, file_id=file_id)
        )
        await self.session.commit()
