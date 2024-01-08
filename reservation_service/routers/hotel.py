from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import session
from typing import Annotated
from uuid import UUID

from config.db_connect import DB
from enums.response import ResponseClassHotel
from services.hotel import HotelService
from schemas.hotel import HotelRequest, HotelUpdate, Hotel
from cruds.interfaces.hotel import IHotelCRUD
from cruds.hotel import HotelCRUD

def get_hotel_crud() -> type[IHotelCRUD]:
    return HotelCRUD

router = APIRouter(
    prefix="/hotels",
    tags=["Hotel API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClassHotel.InvalidData.value
    }
)

hotel_database = DB()

@router.get("/", status_code=status.HTTP_200_OK,
            response_model=list[Hotel],
            responses={
                status.HTTP_200_OK: ResponseClassHotel.GetAll.value
            })
async def get_all(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
                    db: session = Depends(hotel_database.get_db),
                    page: Annotated[int, Query(ge=1)] = 1,
                    size: Annotated[int, Query(ge=1)] = 100):
    return await HotelService(hotelCRUD=hotelCRUD, db=db).get_all(page=page, size=size)


@router.get("/{id}", status_code=status.HTTP_200_OK,
            response_model=Hotel,
            responses={
                status.HTTP_200_OK: ResponseClassHotel.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClassHotel.NotFound.value
            })
async def get_by_id(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
                    id: int,
                    db: session = Depends(hotel_database.get_db)):
    return await HotelService(hotelCRUD=hotelCRUD, db=db).get_by_id(id)


@router.get("/uid/{hotel_uid}", status_code=status.HTTP_200_OK,
            response_model=Hotel,
            responses={
                status.HTTP_200_OK: ResponseClassHotel.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClassHotel.NotFound.value
            })
async def get_by_uid(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
                    hotel_uid: UUID,
                    db: session = Depends(hotel_database.get_db)):
    return await HotelService(hotelCRUD=hotelCRUD, db=db).get_by_uid(hotel_uid)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponseClassHotel.Add.value,
                 status.HTTP_409_CONFLICT: ResponseClassHotel.Conflict.value
             })
async def add(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
              hotel_request: HotelRequest,
              db: session = Depends(hotel_database.get_db)):
    hotel = await HotelService(hotelCRUD=hotelCRUD,db=db).add(hotel_request)
    return Response(status_code=status.HTTP_201_CREATED,  
                    headers={"Location": f"/api/v1/hotel/{hotel.hotel_uid}"}
                    )
    

@router.delete("/{hotel_uid}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponseClassHotel.Delete.value,
                   status.HTTP_404_NOT_FOUND: ResponseClassHotel.Delete.value
               })
async def delete(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
                 hotel_uid: UUID,
                 db: session = Depends(hotel_database.get_db)):
    await HotelService(hotelCRUD=hotelCRUD,db=db).delete(hotel_uid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{hotel_uid}", status_code=status.HTTP_200_OK,
              response_model=Hotel,
              responses={
                  status.HTTP_200_OK: ResponseClassHotel.Patch.value,
                  status.HTTP_404_NOT_FOUND: ResponseClassHotel.NotFound.value,
                  status.HTTP_409_CONFLICT: ResponseClassHotel.Conflict.value
              })
async def patch(hotelCRUD: Annotated[IHotelCRUD, Depends(get_hotel_crud)],
                hotel_uid: UUID,
                hotel_update: HotelUpdate,
                db: session = Depends(hotel_database.get_db)):
    return await HotelService(hotelCRUD=hotelCRUD,db=db).patch(hotel_uid, hotel_update)
