from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import UserTokens


class UserTokensDAO(BaseDAO[UserTokens]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserTokens, session)

    async def bot_activation_token_exists(self, token: str, user_id: Optional[int] = None) -> bool:
        query = select(UserTokens).where(UserTokens.token == token)
        if user_id:
            query = query.where(UserTokens.user_id == user_id)
        result = await self.session.execute(query)
        return result.fetchone() is not None
