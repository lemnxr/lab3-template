from uuid import UUID
from models.reservation import ReservationModel
from cruds.interfaces.reservation import IReservationCRUD
from cruds.mocks.data import ReservationDataMock
from reservation_service.schemas.reservation import ReservationUpdate


class ReservationMockCRUD(IReservationCRUD, ReservationDataMock):
    async def get_all(
            self,
            offset: int = 1,
            limit: int = 100
        ):
        reservations = [
            ReservationModel(**item) for item in self._reservations
        ]
    
        return reservations[offset:limit]
    
    async def get_by_id(self, reservation_id: int):
        for item in self._reservations:
            if item["id"] == reservation_id:
                return ReservationModel(**item)
            
        return None
    
    async def get_by_uid(self, reservation_uid: UUID):
        for item in self._reservations:
            if item["reservation_uid"] == reservation_uid:
                return ReservationModel(**item)
            
        return None
    
    async def get_reservations_by_username(self, user_name: str):
        reservations = []

        for item in self._reservations:
            if item["username"] == user_name:
                reservations.append(ReservationModel(**item))
        
        if reservations != []:
            return reservations
        else:
            return None
    
    async def add(self, reservation: ReservationModel):   
        for item in self._reservations:
            if item["reservation_uid"] == reservation.reservation_uid:
                return None
                     
        self._reservations.append(
            {
                "username": reservation.username,
                "hotel_id": reservation.hotel_id,
                "status": reservation.status,
                "start_date": reservation.start_date,
                "end_date": reservation.end_date,
                "id": 1 if len(self._reservations) == 0
                    else self._reservations[-1]["id"] + 1,
                "reservation_uid": reservation.reservation_uid,
                "payment_uid": reservation.payment_uid
            },
        )
        
        return ReservationModel(**self._reservations[-1])
    
    async def patch(self, reservation: ReservationModel, reservation_update: ReservationUpdate):
        res = reservation
        res.status = reservation_update.status
        res.start_date = reservation_update.start_date
        res.end_date = reservation_update.end_date
        return res

    async def delete(self, reservation: ReservationModel):
        for i in range(len(self._reservations)):
            item = self._reservations[i]
            if item["id"] == reservation.id:
                deleted_reservation = self._reservations.pop(i)
                break

        return ReservationModel(**deleted_reservation)
    