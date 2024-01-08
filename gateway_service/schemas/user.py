from pydantic import BaseModel
from schemas.reservation import ReservationResponse
from schemas.loyalty import LoyaltyInfoResponse


class UserInfoResponse(BaseModel):
    reservations: list[ReservationResponse]
    loyalty: LoyaltyInfoResponse
    