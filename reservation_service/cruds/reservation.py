from uuid import UUID

from models.reservation import ReservationModel
from schemas.reservation import ReservationUpdate
from cruds.interfaces.reservation import IReservationCRUD


class ReservationCRUD(IReservationCRUD):
    async def get_all(self, offset: int = 0, limit: int = 100):
        return self._db.query(ReservationModel).offset(offset).limit(limit).all()
    
    async def get_reservations_by_username(self, user_name):
        return self._db.query(ReservationModel).filter(ReservationModel.username == user_name).all()

    async def get_by_uid(self, reservation_uid: UUID):
        return self._db.query(ReservationModel).filter(ReservationModel.reservation_uid == reservation_uid).first()

    async def add(self, reservation: ReservationModel):
        try:
            self._db.add(reservation)
            self._db.commit()
            self._db.refresh(reservation)
        except:
            return None
        
        return reservation
    
    async def delete(self, reservation: ReservationModel):
        self._db.delete(reservation)
        self._db.commit()
        
        return reservation

    async def patch(self, reservation: ReservationModel, reservation_update: ReservationUpdate):
        update_attributes = reservation_update.model_dump(exclude_unset=True)        

        for key, value in update_attributes.items():
            setattr(reservation, key, value)
        
        try:
            self._db.add(reservation)
            self._db.commit()
            self._db.refresh(reservation)
        except:
            return None
        
        return reservation
