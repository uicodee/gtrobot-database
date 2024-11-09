from sqlalchemy import String, Integer, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class QuizResults(BaseModel):
    __tablename__ = "quiz_results"

    user_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    other: Mapped[str] = mapped_column(String)
    quiz_answers: Mapped[str] = mapped_column(String)
    correct_answers_num: Mapped[int] = mapped_column(Integer)
    incorrect_answers_num: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
