from typing import Sequence, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import User


class UsersDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_all(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_status(self, user_id: int) -> User:
        result = await self.session.execute(
            select(User.status).where(User.id == user_id)
        )
        return result.scalar()

    async def get_count_users(self) -> Optional[int]:
        result = await self.session.execute(
            select(func.count()).select_from(User)
        )
        return result.scalar()

    async def get_user_locale(self, user_id: int) -> Optional[str]:
        result = await self.session.execute(
            select(User.locale).where(User.user_id == user_id)
        )
        return result.scalar()

    async def user_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.fetchone() is not None


