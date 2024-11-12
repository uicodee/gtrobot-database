from typing import Sequence

from sqlalchemy import select
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
