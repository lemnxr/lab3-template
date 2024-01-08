from abc import ABC, abstractmethod
from schemas.loyalty import CreateLoyaltyRequest


class ILoyaltyCRUD(ABC):
    @abstractmethod
    async def get_all_loyalties(
        self,
        page: int = 1,
        size: int = 100
    ) -> list[dict]:
        pass
    
    @abstractmethod
    async def get_loyalty_by_username(
        self,
        user_name: str
    ) ->list[dict]:
        pass

    @abstractmethod
    async def get_new_loyalty(
        self,
        loyalty: CreateLoyaltyRequest
    ) ->list[dict]:
        pass

    @abstractmethod
    async def increase_loyalty(
        self,
        id: int,
        reservation_count: int
    ) ->list[dict]:
        pass

    @abstractmethod
    async def decrease_loyalty(
        self,
        id: int,
        reservation_count: int
    ) ->list[dict]:
        pass
    