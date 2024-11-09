from .base import BaseModel
from sqlalchemy import Integer, Numeric, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column


class AdminSettings(BaseModel):
    __tablename__ = "admin_settings"

    exchange_usdt_balance: Mapped[float] = mapped_column(Numeric, default=0)
    request_counter: Mapped[int] = mapped_column(Integer, default=1)
    course_sum: Mapped[float] = mapped_column(Numeric, default=11250)
    task_counter: Mapped[int] = mapped_column(Integer, default=0)
    task_text: Mapped[str] = mapped_column(String, default="None")
    task_group_id: Mapped[int] = mapped_column(Integer, default=0)
    task_photo_id: Mapped[str] = mapped_column(String)
    is_quiz_active: Mapped[bool] = mapped_column(Boolean, default=False)
    quiz_mailing_text: Mapped[str] = mapped_column(
        Text,
        default="15 va undan yuqori bal yig’ganlarga yangi "
                "Trading Community ga imtiyoz bilan qoshilish imkoni beriladi."
                "\n\n<b>Batafsil malumot:</b> @Granduzb",
    )
