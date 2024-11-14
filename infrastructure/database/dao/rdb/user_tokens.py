import time
from typing import Optional
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import UserTokens, UserServices


class UserTokensDAO(BaseDAO[UserTokens]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserTokens, session)

    async def bot_activation_token_exists(
        self, token: str, user_id: Optional[int] = None
    ) -> bool:
        query = select(UserTokens).where(UserTokens.token == token)
        if user_id:
            query = query.where(UserTokens.user_id == user_id)
        result = await self.session.execute(query)
        return result.fetchone() is not None

    async def set_user_bot_activation(self, user_id: int, services: list, days: int,
                                      token: str = None, order_id: int = None, date: int = None) -> int:
        if date is None:
            date = int(time.time())

        insert_user_token_stmt = insert(UserTokens).values(
            user_id=user_id,
            token=token,
            days=days,
            order_id=order_id,
            date=date
        )
        async with self.session.begin():
            result = await self.session.execute(insert_user_token_stmt)
            token_id = result.inserted_primary_key[0]

            for service in services:
                insert_user_service_stmt = insert(UserServices).values(
                    user_id=user_id,
                    service=service,
                    token_id=token_id
                )
                await self.session.execute(insert_user_service_stmt)

        return token_id
