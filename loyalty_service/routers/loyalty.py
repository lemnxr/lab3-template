from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import session
from typing import Annotated

from config.db_connect import DB
from enums.response import ResponseClassLoyalty
from services.loyalty import LoyaltyService
from schemas.loyalty import LoyaltyRequest, LoyaltyUpdate, Loyalty
from cruds.interfaces.loyalty import ILoyaltyCRUD
from cruds.loyalty import LoyaltyCRUD

def get_loyalty_crud() -> type[ILoyaltyCRUD]:
    return LoyaltyCRUD

router = APIRouter(
    prefix="/loyalties",
    tags=["Loyalty API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClassLoyalty.InvalidData.value
    }
)

loyalty_database = DB()

@router.get("/", status_code=status.HTTP_200_OK,
            response_model=list[Loyalty],
            responses={
                status.HTTP_200_OK: ResponseClassLoyalty.GetAll.value
            })
async def get_all(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
                    db: session = Depends(loyalty_database.get_db),
                    page: Annotated[int, Query(ge=1)] = 1,
                    size: Annotated[int, Query(ge=1)] = 100):
    return await LoyaltyService(loyaltyCRUD=loyaltyCRUD, db=db).get_all(page=page, size=size)


@router.get("/{loyalty_id}", status_code=status.HTTP_200_OK,
            response_model=Loyalty,
            responses={
                status.HTTP_200_OK: ResponseClassLoyalty.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClassLoyalty.NotFound.value
            })
async def get_by_id(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
                    id: int,
                    db: session = Depends(loyalty_database.get_db)):
    return await LoyaltyService(loyaltyCRUD=loyaltyCRUD, db=db).get_by_id(id)

@router.get("/username/{user_name}", status_code=status.HTTP_200_OK,
            response_model=Loyalty,
            responses={
                status.HTTP_200_OK: ResponseClassLoyalty.GetByUsername.value,
                status.HTTP_404_NOT_FOUND: ResponseClassLoyalty.NotFound.value
            })
async def get_by_username(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
                    user_name: str,
                    db: session = Depends(loyalty_database.get_db)):
    return await LoyaltyService(loyaltyCRUD=loyaltyCRUD, db=db).get_by_username(user_name)

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponseClassLoyalty.Add.value,
                 status.HTTP_409_CONFLICT: ResponseClassLoyalty.Conflict.value
             })
async def add(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
              loyalty_request: LoyaltyRequest,
              db: session = Depends(loyalty_database.get_db)):
    loyalty = await LoyaltyService(loyaltyCRUD=loyaltyCRUD,db=db).add(loyalty_request)
    return Response(status_code=status.HTTP_201_CREATED,  
                    headers={"Location": f"/api/v1/loyalty/{loyalty.id}"}
                    )
    

@router.delete("/{loyalty_id}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponseClassLoyalty.Delete.value,
                   status.HTTP_404_NOT_FOUND: ResponseClassLoyalty.Delete.value
               })
async def delete(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
                 id: int,
                 db: session = Depends(loyalty_database.get_db)):
    await LoyaltyService(loyaltyCRUD=loyaltyCRUD,db=db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{username}", status_code=status.HTTP_200_OK,
              response_model=Loyalty,
              responses={
                  status.HTTP_200_OK: ResponseClassLoyalty.Patch.value,
                  status.HTTP_404_NOT_FOUND: ResponseClassLoyalty.NotFound.value,
                  status.HTTP_409_CONFLICT: ResponseClassLoyalty.Conflict.value
              })
async def patch(loyaltyCRUD: Annotated[ILoyaltyCRUD, Depends(get_loyalty_crud)],
                username: str,
                loyalty_update: LoyaltyUpdate,
                db: session = Depends(loyalty_database.get_db)):
    return await LoyaltyService(loyaltyCRUD=loyaltyCRUD,db=db).patch(username, loyalty_update)
