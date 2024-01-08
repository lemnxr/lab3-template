from pydantic import BaseModel, constr, conint, validator
from uuid import UUID
from datetime import datetime, date

from enums.status import ReservationStatus


class ReservationBase(BaseModel):
    username: constr(max_length=80)
    hotel_id: int | None
    status: ReservationStatus
    start_date: date
    end_date: date

    @validator('start_date', pre=True)
    def parse_start_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(
                v,
                '%Y-%m-%d'
            )
        return v
    
    @validator('end_date', pre=True)
    def parse_end_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(
                v,
                '%Y-%m-%d'
            )
        return v

class ReservationRequest(ReservationBase):
    hotel_id: int | None = None

class Reservation(ReservationBase):
    id: int
    reservation_uid: UUID
    payment_uid: UUID

class ReservationUpdate(BaseModel):
    status: ReservationStatus | None = None
    start_date: date | None = None
    end_date: date | None = None

    @validator('start_date', pre=True)
    def parse_start_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(
                v,
                '%Y-%m-%d'
            )
        return v
    
    @validator('end_date', pre=True)
    def parse_end_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(
                v,
                '%Y-%m-%d'
            )
        return v
