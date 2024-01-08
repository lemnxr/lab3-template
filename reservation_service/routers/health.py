from fastapi import APIRouter, status
from fastapi.responses import Response

from enums.response import ResponseClassHealth


router = APIRouter(
    prefix="/manage",
    tags=["ManageHealth"],
)

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={
        status.HTTP_200_OK: ResponseClassHealth.Health.value,
    }
)
async def health():
    return Response(
        status_code=status.HTTP_200_OK
    )
