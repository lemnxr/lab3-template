from enum import Enum


class PaymentStatus(str, Enum):
    Paid = 'PAID',
    Canceled = 'CANCELED'
