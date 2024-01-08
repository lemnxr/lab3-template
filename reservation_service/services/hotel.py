from sqlalchemy.orm import Session
from uuid import UUID

from models.hotel import HotelModel
from schemas.hotel import HotelRequest, HotelUpdate
from exceptions.exceptions import NotFoundException, ConflictException
from cruds.interfaces.hotel import IHotelCRUD


class HotelService():
    def __init__(self, hotelCRUD: type[IHotelCRUD], db: Session):
        self._hotelCRUD = hotelCRUD(db)
        
    async def get_all(self, page: int = 1, size: int = 100):
        return await self._hotelCRUD.get_all(offset=(page-1)*size, limit=size)
    
    async def get_by_id(self, hotel_id: int):
        hotel = await self._hotelCRUD.get_by_id(hotel_id)

        if hotel == None:
            raise NotFoundException(prefix="Get Hotel")
        return hotel

    async def get_by_uid(self, hotel_uid: UUID):
        hotel = await self._hotelCRUD.get_by_uid(hotel_uid)

        if hotel == None:
            raise NotFoundException(prefix="Get Hotel")
        return hotel
    
    async def add(self, hotel_request: HotelRequest):
        hotel = HotelModel(**hotel_request.model_dump())
        hotel = await self._hotelCRUD.add(hotel)
        
        if hotel == None:
            raise ConflictException(prefix="Add Hotel")
        return hotel
    
    async def delete(self, hotel_uid: UUID):
        hotel = await self._hotelCRUD.get_by_uid(hotel_uid)

        if hotel == None:
            raise NotFoundException(prefix="Delete Hotel")
        return await self._hotelCRUD.delete(hotel)
    
    async def patch(self, hotel_uid: UUID, hotel_update: HotelUpdate):
        hotel = await self._hotelCRUD.get_by_uid(hotel_uid)

        if hotel == None:
            raise NotFoundException(prefix="Update Hotel")
    
        hotel = await self._hotelCRUD.patch(hotel, hotel_update)

        if hotel == None:
            raise ConflictException(prefix="Update Hotel")
        return hotel
