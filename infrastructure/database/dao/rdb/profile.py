from typing import List, Optional

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import Profile


class ProfilesDAO(BaseDAO[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session)

    async def get_users_with_profiles(self) -> List[int]:
        result = await self.session.execute(select(Profile.user_id))
        return [user_id for user_id in result.scalars().all()]

    async def get_user_terms_of_use(self, user_id: int) -> Optional[bool]:
        result = await self.session.execute(
            select(Profile.is_terms_of_use).where(Profile.user_id == user_id)
        )
        return bool(result.scalar()) if result.scalar() is not None else None

    async def get_user_profile(self, user_id: int) -> List[Optional[str]]:
        result = await self.session.execute(
            select(
                Profile.user_name,
                Profile.user_last_name,
                Profile.user_num,
                Profile.user_rating,
            ).where(Profile.user_id == user_id)
        )
        profile = result.fetchone()
        return list(profile) if profile else []

    async def get_is_request(self, user_id: int) -> Optional[bool]:
        result = await self.session.execute(
            select(Profile.is_request).where(Profile.user_id == user_id)
        )
        return bool(result.scalar()) if result.scalar() is not None else None

    async def get_user_balances(self, user_id: int) -> List[Optional[float]]:
        result = await self.session.execute(
            select(
                Profile.user_doge_balance,
                Profile.user_ton_balance,
                Profile.user_gtu_balance,
            ).where(Profile.user_id == user_id)
        )
        balances = result.fetchone()
        return list(balances) if balances else []

    async def user_rating(self, user_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(Profile.user_rating).where(Profile.user_id == user_id)
        )
        return result.scalar()

    async def get_profile_task_link_data(self, user_id: int) -> List[Optional[str]]:
        result = await self.session.execute(
            select(Profile.invite_link_id, Profile.invite_link).where(
                Profile.user_id == user_id
            )
        )
        link_data = result.fetchone()
        return list(link_data) if link_data else []

    async def user_profile_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        return result.fetchone() is not None

    async def update_user_request(self, user_id, is_request):
        await self.session.execute(
            update(Profile).where(Profile.user_id == user_id).values(is_request=is_request)
        )
        await self.session.commit()

    async def update_user_rating(self, user_id, user_rating):
        await self.session.execute(
            update(Profile).where(Profile.user_id == user_id).values(user_rating=user_rating)
        )
        await self.session.commit()

    async def update_user_balances(self, user_id, user_doge_balance, user_ton_balance, user_gtu_balance):
        await self.session.execute(
            update(Profile)
            .where(Profile.user_id == user_id)
            .values(
                user_doge_balance=user_doge_balance,
                user_ton_balance=user_ton_balance,
                user_gtu_balance=user_gtu_balance,
            )
        )
        await self.session.commit()

    async def update_user_terms_of_use(self, user_id, terms_of_use):
        await self.session.execute(
            update(Profile).where(Profile.user_id == user_id).values(is_terms_of_use=terms_of_use)
        )
        await self.session.commit()

    async def update_profile_task_link_data(self, user_id, invite_link_id, invite_link):
        await self.session.execute(
            update(Profile)
            .where(Profile.user_id == user_id)
            .values(invite_link_id=invite_link_id, invite_link=invite_link)
        )
        await self.session.commit()

    async def set_user_profile(self, user_id, user_num, user_name, user_last_name):
        await self.session.execute(
            insert(Profile).values(
                user_id=user_id,
                user_num=user_num,
                user_name=user_name,
                user_last_name=user_last_name,
            )
        )
        await self.session.commit()
