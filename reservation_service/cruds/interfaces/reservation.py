from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from uuid import UUID

from models.reservation import ReservationModel
from schemas.reservation import ReservationUpdate


class IReservationCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 100) -> list[ReservationModel]:
       pass

    @abstractmethod
    async def get_reservations_by_username(self, user_name: str) -> list[ReservationModel]:
       pass
    
    @abstractmethod
    async def get_by_uid(self, reservation_uid: UUID) -> ReservationModel | None:
        pass

    @abstractmethod
    async def add(self, reservation: ReservationModel) -> ReservationModel | None:
        pass
    
    @abstractmethod
    async def delete(self, reservation: ReservationModel) -> ReservationModel:
        pass
    
    @abstractmethod
    async def patch(self, reservation: ReservationModel, reservation_update: ReservationUpdate) -> ReservationModel | None:
        pass
