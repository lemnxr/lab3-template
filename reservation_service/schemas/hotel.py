from pydantic import BaseModel, constr, conint
from uuid import UUID


class HotelBase(BaseModel):
    name: constr(max_length=255)
    country: constr(max_length=80)
    city: constr(max_length=80)
    address: constr(max_length=255)
    stars: conint(ge=1) | None = None
    price: conint(ge=1)

class HotelRequest(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    hotel_uid: UUID

class HotelUpdate(BaseModel):
    name: constr(max_length=255) | None = None
    country: constr(max_length=80) | None = None
    city: constr(max_length=80) | None = None
    address: constr(max_length=255) | None = None
    stars: conint(ge=1) | None = None
    price: conint(ge=1) | None = None
    