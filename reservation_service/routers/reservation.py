from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import session
from typing import Annotated
from uuid import UUID

from config.db_connect import DB
from enums.response import ResponseClassReservation
from services.reservation import ReservationService
from schemas.reservation import ReservationRequest, ReservationUpdate, Reservation
from cruds.interfaces.reservation import IReservationCRUD
from cruds.reservation import ReservationCRUD

def get_reservation_crud() -> type[IReservationCRUD]:
    return ReservationCRUD

router = APIRouter(
    prefix="/reservations",
    tags=["Reservation API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClassReservation.InvalidData.value
    }
)

reservation_database = DB()

@router.get("/", status_code=status.HTTP_200_OK,
            response_model=list[Reservation],
            responses={
                status.HTTP_200_OK: ResponseClassReservation.GetAll.value
            })
async def get_all(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
                    db: session = Depends(reservation_database.get_db),
                    page: Annotated[int, Query(ge=1)] = 1,
                    size: Annotated[int, Query(ge=1)] = 100):
    return await ReservationService(reservationCRUD=reservationCRUD, db=db).get_all(page=page, size=size)

@router.get("/username/{user_name}", status_code=status.HTTP_200_OK,
            response_model=list[Reservation],
            responses={
                status.HTTP_200_OK: ResponseClassReservation.GetAll.value
            })
async def get_reservations_by_username(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
                                      user_name: str,
                                      db: session = Depends(reservation_database.get_db),
    ):
    return await ReservationService(reservationCRUD=reservationCRUD, db=db).get_reservations_by_username(user_name)

@router.get("/{reservation_uid}", status_code=status.HTTP_200_OK,
            response_model=Reservation,
            responses={
                status.HTTP_200_OK: ResponseClassReservation.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClassReservation.NotFound.value
            })
async def get_by_uid(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
                    reservation_uid: UUID,
                    db: session = Depends(reservation_database.get_db)):
    return await ReservationService(reservationCRUD=reservationCRUD, db=db).get_by_uid(reservation_uid)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponseClassReservation.Add.value,
                 status.HTTP_409_CONFLICT: ResponseClassReservation.Conflict.value
             })
async def add(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
              reservation_request: ReservationRequest,
              db: session = Depends(reservation_database.get_db)):
    reservation = await ReservationService(reservationCRUD=reservationCRUD,db=db).add(reservation_request)
    return Response(status_code=status.HTTP_201_CREATED,  
                    headers={"Location": f"/api/v1/reservation/{reservation.reservation_uid}"}
                    )
    

@router.delete("/{reservation_uid}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponseClassReservation.Delete.value,
                   status.HTTP_404_NOT_FOUND: ResponseClassReservation.Delete.value
               })
async def delete(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
                 reservation_uid: UUID,
                 db: session = Depends(reservation_database.get_db)):
    await ReservationService(reservationCRUD=reservationCRUD,db=db).delete(reservation_uid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{reservation_uid}", status_code=status.HTTP_200_OK,
              response_model=Reservation,
              responses={
                  status.HTTP_200_OK: ResponseClassReservation.Patch.value,
                  status.HTTP_404_NOT_FOUND: ResponseClassReservation.NotFound.value,
                  status.HTTP_409_CONFLICT: ResponseClassReservation.Conflict.value
              })
async def patch(reservationCRUD: Annotated[IReservationCRUD, Depends(get_reservation_crud)],
                reservation_uid: UUID,
                reservation_update: ReservationUpdate,
                db: session = Depends(reservation_database.get_db)):
    return await ReservationService(reservationCRUD=reservationCRUD,db=db).patch(reservation_uid, reservation_update)
