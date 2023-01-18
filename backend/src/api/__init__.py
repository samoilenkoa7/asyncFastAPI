from fastapi import APIRouter

from .auth import router as auth_router
from .available_time import router as available_time_router
from .booking import router as booking_time_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(available_time_router)
router.include_router(booking_time_router)
