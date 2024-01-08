from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models.loyalty import LoyaltyModel
from schemas.loyalty import LoyaltyUpdate


class ILoyaltyCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 100) -> list[LoyaltyModel]:
       pass
    
    @abstractmethod
    async def get_by_id(self, loyalty_id: int) -> LoyaltyModel | None:
        pass

    @abstractmethod
    async def get_by_username(self, user_name: int) -> LoyaltyModel | None:
        pass

    @abstractmethod
    async def add(self, loyalty: LoyaltyModel) -> LoyaltyModel | None:
        pass
    
    @abstractmethod
    async def delete(self, loyalty: LoyaltyModel) -> LoyaltyModel:
        pass
    
    @abstractmethod
    async def patch(self, loyalty: LoyaltyModel, loyalty_update: LoyaltyUpdate) -> LoyaltyModel | None:
        pass
