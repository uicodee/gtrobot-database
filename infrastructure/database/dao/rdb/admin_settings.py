from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import AdminSettings


class AdminSettingsDAO(BaseDAO[AdminSettings]):
    def __init__(self, session: AsyncSession):
        super().__init__(AdminSettings, session)

    async def get_exchange_usdt(self) -> Optional[float]:
        result = await self.session.execute(select(AdminSettings.exchange_usdt_balance))
        return result.scalar()

    async def get_course_sum(self) -> Optional[float]:
        result = await self.session.execute(select(AdminSettings.course_sum))
        return result.scalar()

    async def get_exchange_request_counter(self) -> Optional[int]:
        result = await self.session.execute(select(AdminSettings.request_counter))
        return result.scalar()

    async def get_soc_task(self) -> List[Optional[str]]:
        result = await self.session.execute(
            select(
                AdminSettings.task_counter,
                AdminSettings.task_text,
                AdminSettings.task_group_id,
                AdminSettings.task_photo_id,
            )
        )
        task_data = result.fetchone()
        return list(task_data) if task_data else []
