from pydantic import BaseModel
from enums.status import LoyaltyStatus


class LoyaltyInfoResponse(BaseModel):
    status: LoyaltyStatus
    discount: int
    reservation_count: int

class CreateLoyaltyRequest(LoyaltyInfoResponse):
    username: str
    