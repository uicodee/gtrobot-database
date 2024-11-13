from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import ActivatedUserSections


class ActivatedUserSectionsDAO(BaseDAO[ActivatedUserSections]):
    def __init__(self, session: AsyncSession):
        super().__init__(ActivatedUserSections, session)

    async def get_user_activated_sections(self, user_id: int) -> List[str]:
        result = await self.session.execute(
            select(ActivatedUserSections.section).where(
                ActivatedUserSections.user_id == user_id
            )
        )
        return [row[0] for row in result.fetchall()]

    async def user_section_is_activated(self, user_id: int, section: str) -> bool:
        result = await self.session.execute(
            select(ActivatedUserSections).where(
                ActivatedUserSections.user_id == user_id,
                ActivatedUserSections.section == section,
            )
        )
        return result.fetchone() is not None
