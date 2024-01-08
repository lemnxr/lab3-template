from fastapi import APIRouter

from routers import loyalty, health

router = APIRouter()
router.include_router(loyalty.router)
router.include_router(health.router)
