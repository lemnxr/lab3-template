from uuid import UUID

from models.payment import PaymentModel
from schemas.payment import PaymentUpdate
from cruds.interfaces.payment import IPaymentCRUD


class PaymentCRUD(IPaymentCRUD):
    async def get_all(self, offset: int = 0, limit: int = 100):
        return self._db.query(PaymentModel).offset(offset).limit(limit).all()

    async def get_by_uid(self, payment_uid: UUID):
        print("uid:", payment_uid)
        return self._db.query(PaymentModel).filter(PaymentModel.payment_uid == payment_uid).first()

    async def add(self, payment: PaymentModel):
        try:
            self._db.add(payment)
            self._db.commit()
            self._db.refresh(payment)
        except:
            return None
        
        return payment
    
    async def delete(self, payment: PaymentModel):
        self._db.delete(payment)
        self._db.commit()
        
        return payment

    async def patch(self, payment: PaymentModel, payment_update: PaymentUpdate):
        update_attributes = payment_update.model_dump(exclude_unset=True)        

        for key, value in update_attributes.items():
            setattr(payment, key, value)
        
        try:
            self._db.add(payment)
            self._db.commit()
            self._db.refresh(payment)
        except:
            return None
        
        return payment
