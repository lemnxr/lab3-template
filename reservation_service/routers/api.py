from fastapi import APIRouter

from routers import hotel, reservation, health

router = APIRouter()
router.include_router(hotel.router)
router.include_router(reservation.router)
router.include_router(health.router)
