from fastapi import APIRouter, Depends, status, Query, Header
from fastapi.responses import Response
from typing import Annotated
from uuid import UUID

from schemas.reservation import PaginationResponse, ReservationResponse, CreateReservationResponse, CreateReservationRequest
from schemas.loyalty import LoyaltyInfoResponse
from schemas.user import UserInfoResponse
from enums.response import ResponseClassGateway
from services.gateway import GatewayService
from cruds.interfaces.reservation import IReservationCRUD
from cruds.interfaces.payment import IPaymentCRUD
from cruds.interfaces.loyalty import ILoyaltyCRUD
from cruds.reservation import ReservationCRUD
from cruds.payment import PaymentCRUD
from cruds.loyalty import LoyaltyCRUD


def get_reservation_crud() -> type[IReservationCRUD]:
    return ReservationCRUD

def get_payment_crud() -> type[IPaymentCRUD]:
    return PaymentCRUD

def get_loyalty_crud() -> type[ILoyaltyCRUD]:
    return LoyaltyCRUD

router = APIRouter(
    tags=["Gateway API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClassGateway.InvalidData.value
    }
)

@router.get(
    "/hotels",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse,
    responses={
        status.HTTP_200_OK: ResponseClassGateway.GetAllHotels.value,
    }
)
async def get_all_hotels(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).get_all_hotels(page=page,size=size)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserInfoResponse,
    responses={
        status.HTTP_200_OK: ResponseClassGateway.GetUserInfo.value,
    }
)
async def get_user_info(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)]
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).get_user_info(user_name = X_User_Name)


@router.get(
    "/reservations",
    status_code=status.HTTP_200_OK,
    response_model=list[ReservationResponse],
    responses={
        status.HTTP_200_OK: ResponseClassGateway.GetUserReservations.value,
    }
)
async def get_user_reservations(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)]
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).get_user_reservations(user_name = X_User_Name)


@router.post(
    "/reservations",
    status_code=status.HTTP_200_OK,
    response_model=CreateReservationResponse,
    responses={
        status.HTTP_200_OK: ResponseClassGateway.ReserveHotel.value,
        status.HTTP_404_NOT_FOUND: ResponseClassGateway.HotelNotFound.value,
    }
)
async def reserve_hotel(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)],
    hotel_reservation_request: CreateReservationRequest
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).reserve_hotel(user_name = X_User_Name, hotel_reservation_request = hotel_reservation_request)


@router.get(
    "/reservations/{reservation_uid}",
    status_code=status.HTTP_200_OK,
    response_model=ReservationResponse,
    responses={
        status.HTTP_200_OK: ResponseClassGateway.GetReservationInfo.value,
        status.HTTP_404_NOT_FOUND: ResponseClassGateway.ReservationNotFound.value,
    }
)
async def get_reservation_info(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    reservation_uid: UUID,
    X_User_Name: Annotated[str, Header(max_length=80)]
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).get_reservation_info(user_name=X_User_Name, reservation_uid=reservation_uid)


@router.delete(
    "/reservations/{reservation_uid}",
    response_class=Response, 
    responses={
        status.HTTP_204_NO_CONTENT: ResponseClassGateway.ReservationCancel.value,
        status.HTTP_404_NOT_FOUND: ResponseClassGateway.ReservationNotFound.value,
    }
)
async def reservation_cancel(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    reservation_uid: UUID,
    X_User_Name: Annotated[str, Header(max_length=80)]
):
    await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).reservation_cancel(user_name = X_User_Name, reservation_uid=reservation_uid)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.get(
    "/loyalty",
    status_code=status.HTTP_200_OK,
    response_model=LoyaltyInfoResponse,
    responses={
        status.HTTP_200_OK: ResponseClassGateway.GetLoyalty.value,
    }
)
async def get_loyalty(
    reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
    paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
    loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
    X_User_Name: Annotated[str, Header(max_length=80)]
):
    return await GatewayService(
        reservationCRUD=reservationCRUD,
        paymentCRUD=paymentCRUD,
        loyaltyCRUD=loyaltyCRUD
    ).get_loyalty(user_name = X_User_Name)
