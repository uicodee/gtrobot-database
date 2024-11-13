from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import CoursePlaceholders


class CoursePlaceholdersDAO(BaseDAO[CoursePlaceholders]):
    def __init__(self, session: AsyncSession):
        super().__init__(CoursePlaceholders, session)

    async def get_kurs_placeholder_file_id(self, symbol: str) -> Optional[str]:
        result = await self.session.execute(
            select(CoursePlaceholders.file_id).where(CoursePlaceholders.symbol == symbol)
        )
        return result.scalar()
