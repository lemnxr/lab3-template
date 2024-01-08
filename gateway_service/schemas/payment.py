from pydantic import BaseModel, conint
from enums.status import PaymentStatus


class PaymentInfo(BaseModel):
    status: PaymentStatus
    price: conint(ge=1)
