from enum import Enum

class LoyaltyStatus(str, Enum):
    Bronze = 'BRONZE',
    Silver = 'SILVER',
    Gold = 'GOLD'

class PaymentStatus(str, Enum):
    Paid = 'PAID',
    Canceled = 'CANCELED'

class ReservationStatus(str, Enum):
    Paid = 'PAID',
    Canceled = 'CANCELED'
    