from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import QuizResults


class ReferralsDAO(BaseDAO[QuizResults]):
    def __init__(self, session: AsyncSession):
        super().__init__(QuizResults, session)

    async def set_user_quiz_results(self, user_id, quiz_answers, correct_answers, incorrect_answers,
                                    first_name=None, last_name=None, other=None):
        await self.session.execute(
            insert(QuizResults).values(
                user_id=user_id,
                quiz_answers=quiz_answers,
                correct_answers=correct_answers,
                incorrect_answers=incorrect_answers,
                first_name=first_name,
                last_name=last_name,
                other=other
            )
        )
