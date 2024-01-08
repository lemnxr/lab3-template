from sqlalchemy.orm import Session
from uuid import UUID

from models.payment import PaymentModel
from schemas.payment import PaymentRequest, PaymentUpdate
from exceptions.exceptions import NotFoundException, ConflictException
from cruds.interfaces.payment import IPaymentCRUD


class PaymentService():
    def __init__(self, paymentCRUD: type[IPaymentCRUD], db: Session):
        self._paymentCRUD = paymentCRUD(db)
        
    async def get_all(self, page: int = 1, size: int = 100):
        return await self._paymentCRUD.get_all(offset=(page-1)*size, limit=size)

    async def get_by_uid(self, payment_uid: UUID):
        payment = await self._paymentCRUD.get_by_uid(payment_uid)

        if payment == None:
            raise NotFoundException(prefix="Get Payment")
        return payment
    
    async def add(self, payment_request: PaymentRequest):
        payment = PaymentModel(**payment_request.model_dump())
        payment = await self._paymentCRUD.add(payment)

        if payment == None:
            raise ConflictException(prefix="Add Payment")
        return payment
    
    async def delete(self, payment_uid: UUID):
        payment = await self._paymentCRUD.get_by_uid(payment_uid)

        if payment == None:
            raise NotFoundException(prefix="Delete Payment")
        return await self._paymentCRUD.delete(payment)
    
    async def patch(self, payment_uid: UUID, payment_update: PaymentUpdate):
        payment = await self._paymentCRUD.get_by_uid(payment_uid)

        if payment == None:
            raise NotFoundException(prefix="Update Payment")
    
        payment = await self._paymentCRUD.patch(payment, payment_update)

        if payment == None:
            raise ConflictException(prefix="Update Payment")
        return payment
