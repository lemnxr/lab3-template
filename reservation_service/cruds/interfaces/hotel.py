from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from uuid import UUID

from models.hotel import HotelModel
from schemas.hotel import HotelUpdate


class IHotelCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 100) -> list[HotelModel]:
       pass

    @abstractmethod
    async def get_by_id(self, hotel_id: int) -> HotelModel | None:
        pass
    
    @abstractmethod
    async def get_by_uid(self, hotel_uid: UUID) -> HotelModel | None:
        pass

    @abstractmethod
    async def add(self, hotel: HotelModel) -> HotelModel | None:
        pass
    
    @abstractmethod
    async def delete(self, hotel: HotelModel) -> HotelModel:
        pass
    
    @abstractmethod
    async def patch(self, hotel: HotelModel, hotel_update: HotelUpdate) -> HotelModel | None:
        pass
