from typing import List
from sqlalchemy import select, update, insert, delete
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

    async def set_user_social_networks_link(self, user_id, is_profile, user_link, date):
        await self.session.execute(
            insert(SocialNetworksLinks).values(
                user_id=user_id, is_profile=is_profile, user_link=user_link, date=date
            )
        )
        await self.session.commit()

    async def del_social_networks_link(self, user_id: int, date: int):
        await self.session.execute(
            delete(SocialNetworksLinks).where(
                SocialNetworksLinks.user_id == user_id, SocialNetworksLinks.date == date
            )
        )
        await self.session.commit()

