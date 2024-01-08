from abc import ABC, abstractmethod
from uuid import UUID


class IReservationCRUD(ABC):
    @abstractmethod
    async def get_all_hotels(
        self,
        page: int = 1,
        size: int = 100
    ) -> list[dict]:
        pass
    
    @abstractmethod
    async def get_hotels_num(
        self
    ) -> int:
        pass

    @abstractmethod
    async def get_hotel_by_id(
        self,
        hotel_id: int
    ) -> list[dict]:
        pass

    @abstractmethod
    async def get_hotel_by_uid(
        self,
        hotel_uid: UUID
    ) -> list[dict]:
        pass

    @abstractmethod
    async def get_reservations_by_username(
        self,
        user_name: str
    ) -> list[dict]:
        pass

    @abstractmethod
    async def get_reservation_by_uid(
        self,
        reservation_uid: UUID
    ) -> list[dict]:
        pass

    @abstractmethod
    async def get_new_reservation(
        self,
    ) ->list[dict]:
        pass

    @abstractmethod
    async def reservation_cancel(
        self,
        reservation_uid: UUID
    ) ->list[dict]:
        pass
  