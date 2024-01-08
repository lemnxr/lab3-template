from pydantic import BaseModel, conint
from uuid import UUID

from enums.status import PaymentStatus


class PaymentBase(BaseModel):
    payment_uid: UUID
    status: PaymentStatus
    price: conint(ge=1)

class PaymentRequest(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = None
    price: conint(ge=1) | None = None
    