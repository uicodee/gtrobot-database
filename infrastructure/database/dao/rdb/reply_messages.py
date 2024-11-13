from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import ReplyMessages


class ReplyMessagesDAO(BaseDAO[ReplyMessages]):
    def __init__(self, session: AsyncSession):
        super().__init__(ReplyMessages, session)

    async def reply_message_data(self, copy_message_id: int) -> Optional[dict]:
        result = await self.session.execute(
            select(
                ReplyMessages.id,
                ReplyMessages.user_id,
                ReplyMessages.original_message_id,
                ReplyMessages.copy_message_id,
                ReplyMessages.reply_date,
                ReplyMessages.is_admin_reply
            ).where(ReplyMessages.copy_message_id == copy_message_id)
        )
        dict_keys = ['id', 'user_id', 'original_message_id', 'copy_message_id', 'reply_date', 'is_admin_reply']
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}
