from enum import Enum


class ReservationStatus(str, Enum):
    Paid = 'PAID',
    Canceled = 'CANCELED'
    