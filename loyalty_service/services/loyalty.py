from sqlalchemy.orm import Session

from models.loyalty import LoyaltyModel
from schemas.loyalty import LoyaltyRequest, LoyaltyUpdate
from exceptions.exceptions import NotFoundException, ConflictException
from cruds.interfaces.loyalty import ILoyaltyCRUD


class LoyaltyService():
    def __init__(self, loyaltyCRUD: type[ILoyaltyCRUD], db: Session):
        self._loyaltyCRUD = loyaltyCRUD(db)
        
    async def get_all(self, page: int = 1, size: int = 100):
        return await self._loyaltyCRUD.get_all(offset=(page-1)*size, limit=size)

    async def get_by_id(self, loyalty_id: int):
        loyalty = await self._loyaltyCRUD.get_by_id(loyalty_id)

        if loyalty == None:
            raise NotFoundException(prefix="Get Loyalty")
        return 
    
    async def get_by_username(self, user_name: str):
        loyalty = await self._loyaltyCRUD.get_by_username(user_name)

        if loyalty == None:
            raise NotFoundException(prefix="Get Loyalty")
        return loyalty
    
    async def add(self, loyalty_request: LoyaltyRequest):
        loyalty = LoyaltyModel(**loyalty_request.model_dump())
        loyalty = await self._loyaltyCRUD.add(loyalty)
        
        if loyalty == None:
            raise ConflictException(prefix="Add Loyalty")
        return loyalty
    
    async def delete(self, loyalty_id: int):
        loyalty = await self._loyaltyCRUD.get_by_id(loyalty_id)

        if loyalty == None:
            raise NotFoundException(prefix="Delete Loyalty")
        return await self._loyaltyCRUD.delete(loyalty)
    
    async def patch(self, username: str, loyalty_update: LoyaltyUpdate):
        loyalty = await self._loyaltyCRUD.get_by_username(username)

        if loyalty == None:
            raise NotFoundException(prefix="Update Loyalty")
    
        loyalty = await self._loyaltyCRUD.patch(loyalty, loyalty_update)

        if loyalty == None:
            raise ConflictException(prefix="Update Loyalty")
        return loyalty
