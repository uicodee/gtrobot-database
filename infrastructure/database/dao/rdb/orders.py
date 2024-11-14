import time
from typing import List, Dict, Optional, Tuple

from sqlalchemy import select, update, insert, delete, func, join, case, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.dao.rdb import BaseDAO
from infrastructure.database.models import (
    UzumPayment,
    UzumAppPayment,
    PaymentNumbers,
    Purchases,
)


class OrdersDAO(BaseDAO[UzumPayment]):
    def __init__(self, session: AsyncSession):
        super().__init__(UzumPayment, session)

    async def get_uzum_payment_last_amount_and_order_id(
        self, user_id: int
    ) -> Tuple[Optional[float], Optional[str]]:
        result = await self.session.execute(
            select(UzumPayment.total_amount, UzumPayment.order_id)
            .where(UzumPayment.user_id == user_id)
            .order_by(UzumPayment.id.desc())
            .limit(1)
        )
        row = result.fetchone()
        return (row[0], row[1]) if row else (None, None)

    async def get_uzum_payment_order_id(self, user_id: int, db_order_id: int) -> str:
        result = await self.session.execute(
            select(UzumPayment.order_id).where(
                UzumPayment.user_id == user_id, UzumPayment.id == db_order_id
            )
        )
        return result.scalar()

    async def get_uzum_payment_order_data(
        self, order_id: str
    ) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                UzumPayment.id,
                UzumPayment.user_id,
                UzumPayment.first_name,
                UzumPayment.username,
                UzumPayment.last_operation_id,
                UzumPayment.order_id,
                UzumPayment.currency_code,
                UzumPayment.provider,
                UzumPayment.tariff_plan,
                UzumPayment.total_amount,
                UzumPayment.promo_code,
                UzumPayment.is_completed,
            ).where(UzumPayment.order_id == order_id)
        )

        dict_keys = [
            "id",
            "user_id",
            "first_name",
            "username",
            "operation_id",
            "order_id",
            "currency_code",
            "provider",
            "plan",
            "total_amount",
            "promo_code",
            "is_completed",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def uzum_payment_is_completed(self, order_id: str) -> bool:
        result = await self.session.execute(
            select(UzumPayment.is_completed).where(UzumPayment.order_id == order_id)
        )
        return result.scalar() or False

    async def get_uzum_app_payment_order_data(
        self, transaction_id: str
    ) -> Dict[str, Optional[str]]:
        result = await self.session.execute(
            select(
                UzumAppPayment.id,
                UzumAppPayment.phone_number,
                UzumAppPayment.plan,
                UzumAppPayment.total_amount,
                UzumAppPayment.transaction_id,
                UzumAppPayment.order_opening_time,
                UzumAppPayment.is_completed,
            ).where(UzumAppPayment.transaction_id == transaction_id)
        )

        dict_keys = [
            "id",
            "phone_number",
            "plan",
            "total_amount",
            "transaction_id",
            "order_opening_time",
            "is_completed",
        ]
        data = result.fetchone()
        return dict(zip(dict_keys, data)) if data else {}

    async def uzum_app_payment_is_completed(self, transaction_id: str) -> bool:
        result = await self.session.execute(
            select(UzumAppPayment.is_completed).where(
                UzumAppPayment.transaction_id == transaction_id
            )
        )
        return result.scalar() or False

    async def get_payment_number(self, user_id: int) -> int:
        result = await self.session.execute(
            select(PaymentNumbers.user_number).where(PaymentNumbers.user_id == user_id)
        )
        return result.scalar()

    async def user_payment_number_exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(PaymentNumbers).where(PaymentNumbers.user_id == user_id)
        )
        return result.first() is not None

    async def update_uzum_payment_is_completed(
        self, order_id: str, status: int = 1
    ) -> None:
        await self.session.execute(
            update(UzumPayment)
            .where(UzumPayment.order_id == order_id)
            .values(is_completed=status)
        )
        await self.session.commit()

    async def update_uzum_app_payment_is_completed(
        self, transaction_id: str, status: int = 1
    ) -> None:
        await self.session.execute(
            update(UzumAppPayment)
            .where(UzumAppPayment.transaction_id == transaction_id)
            .values(is_completed=status)
        )
        await self.session.commit()

    async def update_uzum_payment_last_operation_id(
        self, order_id: str, operation_id: str
    ) -> None:
        await self.session.execute(
            update(UzumPayment)
            .where(UzumPayment.order_id == order_id)
            .values(last_operation_id=operation_id)
        )
        await self.session.commit()

    async def update_payment_number(self, user_id: int, user_number: int) -> None:
        await self.session.execute(
            update(PaymentNumbers)
            .where(PaymentNumbers.user_id == user_id)
            .values(user_number=user_number)
        )
        await self.session.commit()

    async def update_uzum_transaction_id(
        self, order_id: str, transaction_id: str
    ) -> None:
        await self.session.execute(
            update(UzumPayment)
            .where(UzumPayment.order_id == order_id)
            .values(transaction_id=transaction_id)
        )
        await self.session.commit()

    async def set_uzum_payment(
        self,
        user_id: int,
        first_name: str,
        username: str,
        operation_id: str,
        order_id: str,
        currency_code: str,
        provider: str,
        tariff_plan: str,
        total_amount: int,
        promo_code: Optional[str] = None,
    ) -> int:
        result = await self.session.execute(
            insert(UzumPayment)
            .values(
                user_id=user_id,
                first_name=first_name,
                username=username,
                last_operation_id=operation_id,
                order_id=order_id,
                currency_code=currency_code,
                provider=provider,
                tariff_plan=tariff_plan,
                total_amount=total_amount,
                promo_code=promo_code,
                order_opening_time=int(time.time()),
            )
            .returning(UzumPayment.id)
        )
        await self.session.commit()
        return result.scalar()

    async def set_uzum_app_payment(
        self,
        phone_number: str,
        plan: str,
        total_amount: int,
        transaction_id: Optional[str] = None,
        order_opening_time: Optional[int] = None,
        is_completed: int = 0,
    ) -> int:
        result = await self.session.execute(
            insert(UzumAppPayment)
            .values(
                phone_number=phone_number,
                plan=plan,
                total_amount=total_amount,
                transaction_id=transaction_id,
                order_opening_time=order_opening_time or int(time.time()),
                is_completed=is_completed,
            )
            .returning(UzumAppPayment.id)
        )
        await self.session.commit()
        return result.scalar()

    async def set_payment_number(self, user_id: int, user_number: int) -> None:
        await self.session.execute(
            insert(PaymentNumbers).values(user_id=user_id, user_number=user_number)
        )
        await self.session.commit()

    async def set_new_purchase(
        self,
        user_id: int,
        provider: str,
        tariff_plan: str,
        total_amount: int,
        purchase_time: int,
        name: Optional[str] = None,
        username: Optional[str] = None,
        phone_number: Optional[str] = None,
        promo_code: Optional[str] = None,
        referral_user: Optional[str] = None,
        is_purchase: int = 1,
    ) -> int:
        result = await self.session.execute(
            insert(Purchases)
            .values(
                user_id=user_id,
                provider=provider,
                tariff_plan=tariff_plan,
                total_amount=total_amount,
                purchase_time=purchase_time,
                name=name,
                username=username,
                phone_number=phone_number,
                promo_code=promo_code,
                referral_user=referral_user,
                is_purchase=is_purchase,
            )
            .returning(Purchases.id)
        )
        await self.session.commit()
        return result.scalar()
