from pydantic import BaseModel, conint, constr

from enums.status import LoyaltyStatus


class LoyaltyBase(BaseModel):
    username: constr(max_length=80)
    reservation_count: int
    status: LoyaltyStatus
    discount: int

class LoyaltyRequest(LoyaltyBase):
    reservation_count: int = 0
    status: LoyaltyStatus = 'BRONZE'

class Loyalty(LoyaltyBase):
    id: int

class LoyaltyUpdate(BaseModel):
    reservation_count: int | None = None
    status: LoyaltyStatus | None = None
    dicsount: int | None = None
    