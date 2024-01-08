from fastapi import APIRouter

from routers import payment, health

router = APIRouter()
router.include_router(payment.router)
router.include_router(health.router)
