from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import SocialNetworksLinks


class SocialNetworksLinksDAO(BaseDAO[SocialNetworksLinks]):
    def __init__(self, session: AsyncSession):
        super().__init__(SocialNetworksLinks, session)

    async def get_user_post_links(self, user_id: int, date: str) -> List[str]:
        result = await self.session.execute(
            select(SocialNetworksLinks.user_link).where(
                SocialNetworksLinks.user_id == user_id,
                SocialNetworksLinks.is_profile == 0,
                SocialNetworksLinks.date == date,
            )
        )
        return [link for link in result.scalars().all()]

    async def link_exists(self, user_link: str) -> bool:
        result = await self.session.execute(
            select(SocialNetworksLinks).where(
                SocialNetworksLinks.user_link.ilike(user_link.lower())
            )
        )
        return result.fetchone() is not None
