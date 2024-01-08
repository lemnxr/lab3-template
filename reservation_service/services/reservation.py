from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from models.reservation import ReservationModel
from schemas.reservation import ReservationRequest, ReservationUpdate
from exceptions.exceptions import NotFoundException, ConflictException
from cruds.interfaces.reservation import IReservationCRUD


class ReservationService():
    def __init__(self, reservationCRUD: type[IReservationCRUD], db: Session):
        self._reservationCRUD = reservationCRUD(db)
        
    async def get_all(self, page: int = 1, size: int = 100):
        return await self._reservationCRUD.get_all(offset=(page-1)*size, limit=size)
    
    async def get_reservations_by_username(self, user_name: str):
        reservation_list = await self._reservationCRUD.get_reservations_by_username(user_name)

        for i in reservation_list:
            string_start_date = str(i.start_date)[:10]
            string_end_date = str(i.end_date)[:10]
            i.start_date = datetime.strptime(string_start_date, '%Y-%m-%d').date()
            i.end_date = datetime.strptime(string_end_date, '%Y-%m-%d').date()
        return await self._reservationCRUD.get_reservations_by_username(user_name)

    async def get_by_uid(self, reservation_uid: UUID):
        reservation = await self._reservationCRUD.get_by_uid(reservation_uid)

        if reservation == None:
            raise NotFoundException(prefix="Get Reservation")
        return reservation
    
    async def add(self, reservation_request: ReservationRequest):
        reservation = ReservationModel(**reservation_request.model_dump())
        reservation = await self._reservationCRUD.add(reservation)
        
        if reservation == None:
            raise ConflictException(prefix="Add Reservation")
        return reservation
    
    async def delete(self, reservation_uid: UUID):
        reservation = await self._reservationCRUD.get_by_uid(reservation_uid)

        if reservation == None:
            raise NotFoundException(prefix="Delete Reservation")
        return await self._reservationCRUD.delete(reservation)
    
    async def patch(self, reservation_uid: UUID, reservation_update: ReservationUpdate):
        reservation = await self._reservationCRUD.get_by_uid(reservation_uid)

        if reservation == None:
            raise NotFoundException(prefix="Update Reservation")
    
        reservation = await self._reservationCRUD.patch(reservation, reservation_update)

        if reservation == None:
            raise ConflictException(prefix="Update Reservation")
        return reservation
