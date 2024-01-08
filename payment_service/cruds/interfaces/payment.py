from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from uuid import UUID

from models.payment import PaymentModel
from schemas.payment import PaymentUpdate


class IPaymentCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 100) -> list[PaymentModel]:
       pass
    
    @abstractmethod
    async def get_by_uid(self, payment_uid: UUID) -> PaymentModel | None:
        pass

    @abstractmethod
    async def add(self, payment: PaymentModel) -> PaymentModel | None:
        pass
    
    @abstractmethod
    async def delete(self, payment: PaymentModel) -> PaymentModel:
        pass
    
    @abstractmethod
    async def patch(self, payment: PaymentModel, payment_update: PaymentUpdate) -> PaymentModel | None:
        pass
