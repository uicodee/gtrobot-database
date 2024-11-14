from typing import Tuple, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import UzumPayment, UzumAppPayment, PaymentNumbers


class OrdersDAO(BaseDAO[UzumPayment]):
    def __init__(self, session: AsyncSession):
        super().__init__(UzumPayment, session)

    async def get_uzum_payment_last_amount_and_order_id(self, user_id: int) -> Tuple[Optional[float], Optional[str]]:
        result = await self.session.execute(
            select(UzumPayment.total_amount, UzumPayment.order_id)
            .where(UzumPayment.user_id == user_id)
            .order_by(UzumPayment.id.desc())
            .limit(1)
        )
        data = result.fetchone()
        return data if data else (None, None)

    async def get_uzum_payment_order_id(self, user_id: int, db_order_id: int) -> Optional[str]:
        result = await self.session.execute(
            select(UzumPayment.order_id)
            .where(UzumPayment.user_id == user_id, UzumPayment.id == db_order_id)
        )
        return result.scalar()

    async def get_uzum_payment_order_data(self, order_id: str) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                UzumPayment.id, UzumPayment.user_id, UzumPayment.first_name, UzumPayment.username,
                UzumPayment.last_operation_id, UzumPayment.order_id, UzumPayment.currency_code,
                UzumPayment.provider, UzumPayment.tariff_plan, UzumPayment.total_amount,
                UzumPayment.promo_code, UzumPayment.is_completed
            ).where(UzumPayment.order_id == order_id)
        )
        dict_keys = ['id', 'user_id', 'first_name', 'username', 'operation_id', 'order_id', 'currency_code',
                     'provider', 'plan', 'total_amount', 'promo_code', 'is_completed']
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_uzum_app_payment_order_data(self, transaction_id: str) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                UzumAppPayment.id, UzumAppPayment.phone_number, UzumAppPayment.plan,
                UzumAppPayment.total_amount, UzumAppPayment.transaction_id,
                UzumAppPayment.order_opening_time, UzumAppPayment.is_completed
            ).where(UzumAppPayment.transaction_id == transaction_id)
        )
        dict_keys = ['id', 'phone_number', 'plan', 'total_amount', 'transaction_id', 'order_opening_time',
                     'is_completed']
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def get_payment_number(self, user_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(PaymentNumbers.user_number).where(PaymentNumbers.user_id == user_id)
        )
        return result.scalar()

    async def uzum_payment_is_completed(self, order_id: str) -> bool:
        result = await self.session.execute(
            select(UzumPayment.is_completed).where(UzumPayment.order_id == order_id)
        )
        return bool(result.scalar())

    async def uzum_app_payment_is_completed(self, transaction_id: str) -> bool:
        result = await self.session.execute(
            select(UzumAppPayment.is_completed).where(UzumAppPayment.transaction_id == transaction_id)
        )
        return bool(result.scalar())

    async def user_payment_number_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(PaymentNumbers).where(PaymentNumbers.user_id == user_id)
        )
        return result.fetchone() is not None
