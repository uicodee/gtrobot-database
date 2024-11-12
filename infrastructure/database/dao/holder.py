from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO, UsersDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.user = UsersDAO(self.session)
