from uuid import UUID

from models.hotel import HotelModel
from schemas.hotel import HotelUpdate
from cruds.interfaces.hotel import IHotelCRUD


class HotelCRUD(IHotelCRUD):
    async def get_all(self, offset: int = 0, limit: int = 100):
        return self._db.query(HotelModel).offset(offset).limit(limit).all()
    
    async def get_by_id(self, hotel_id: int):
        return self._db.query(HotelModel).filter(HotelModel.id == hotel_id).first()

    async def get_by_uid(self, hotel_uid: UUID):
        return self._db.query(HotelModel).filter(HotelModel.hotel_uid == hotel_uid).first()

    async def add(self, hotel: HotelModel):
        try:
            self._db.add(hotel)
            self._db.commit()
            self._db.refresh(hotel)
        except:
            return None
        
        return hotel
    
    async def delete(self, hotel: HotelModel):
        self._db.delete(hotel)
        self._db.commit()
        
        return hotel

    async def patch(self, hotel: HotelModel, hotel_update: HotelUpdate):
        update_attributes = hotel_update.model_dump(exclude_unset=True)        

        for key, value in update_attributes.items():
            setattr(hotel, key, value)
        
        try:
            self._db.add(hotel)
            self._db.commit()
            self._db.refresh(hotel)
        except:
            return None
        
        return hotel
