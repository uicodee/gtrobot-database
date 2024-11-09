from .base import BaseModel
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class BlumAccountStatistics(BaseModel):
    __tablename__ = "blum_account_statistics"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    available_balance: Mapped[float] = mapped_column(Numeric)
    play_passes: Mapped[int] = mapped_column(Integer)
    earnings_rate: Mapped[float] = mapped_column(Numeric)
    limit_invitation: Mapped[int] = mapped_column(Integer)
    used_invitation: Mapped[int] = mapped_column(Integer)
    amount_for_claim: Mapped[float] = mapped_column(Numeric)
    date: Mapped[int] = mapped_column(Integer)
