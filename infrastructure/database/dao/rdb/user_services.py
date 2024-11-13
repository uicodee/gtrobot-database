from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import UserServices, UserTokens


class UserServicesDAO(BaseDAO[UserServices]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserServices, session)

    async def get_last_user_service_ids(
        self, user_id: int, current_time: Optional[int] = None
    ) -> List[str]:
        if current_time is None:
            import time

            current_time = int(time.time())

        subquery = (
            select(UserTokens.id)
            .where(
                UserTokens.user_id == user_id,
                (UserTokens.days * 86400 + UserTokens.date) > current_time,
            )
            .limit(1)
        )

        result = await self.session.execute(
            select(UserServices.service).where(
                UserServices.user_id == user_id,
                UserServices.token_id == subquery.scalar_subquery(),
            )
        )
        return [row[0] for row in result.fetchall()]
