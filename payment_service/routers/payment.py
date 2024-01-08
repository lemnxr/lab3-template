from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import session
from typing import Annotated
from uuid import UUID

from config.db_connect import DB
from enums.response import ResponseClassPayment
from services.payment import PaymentService
from schemas.payment import PaymentRequest, PaymentUpdate, Payment
from cruds.interfaces.payment import IPaymentCRUD
from cruds.payment import PaymentCRUD

def get_payment_crud() -> type[IPaymentCRUD]:
    return PaymentCRUD

router = APIRouter(
    prefix="/payments",
    tags=["Payment API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClassPayment.InvalidData.value
    }
)

payment_database = DB()

@router.get("/", status_code=status.HTTP_200_OK,
            response_model=list[Payment],
            responses={
                status.HTTP_200_OK: ResponseClassPayment.GetAll.value
            })
async def get_all(paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
                    db: session = Depends(payment_database.get_db),
                    page: Annotated[int, Query(ge=1)] = 1,
                    size: Annotated[int, Query(ge=1)] = 100):
    return await PaymentService(paymentCRUD=paymentCRUD, db=db).get_all(page=page, size=size)


@router.get("/{payment_uid}", status_code=status.HTTP_200_OK,
            response_model=Payment,
            responses={
                status.HTTP_200_OK: ResponseClassPayment.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClassPayment.NotFound.value
            })
async def get_by_uid(paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
                    payment_uid: UUID,
                    db: session = Depends(payment_database.get_db)):
    return await PaymentService(paymentCRUD=paymentCRUD, db=db).get_by_uid(payment_uid)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponseClassPayment.Add.value,
                 status.HTTP_409_CONFLICT: ResponseClassPayment.Conflict.value
             })
async def add(paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
              payment_request: PaymentRequest,
              db: session = Depends(payment_database.get_db)):
    payment = await PaymentService(paymentCRUD=paymentCRUD,db=db).add(payment_request)
    return Response(status_code=status.HTTP_201_CREATED,  
                    headers={"Location": f"/api/v1/payment/{payment.payment_uid}"}
                    )
    

@router.delete("/{payment_uid}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponseClassPayment.Delete.value,
                   status.HTTP_404_NOT_FOUND: ResponseClassPayment.Delete.value
               })
async def delete(paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
                 payment_uid: UUID,
                 db: session = Depends(payment_database.get_db)):
    await PaymentService(paymentCRUD=paymentCRUD,db=db).delete(payment_uid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{payment_uid}", status_code=status.HTTP_200_OK,
              response_model=Payment,
              responses={
                  status.HTTP_200_OK: ResponseClassPayment.Patch.value,
                  status.HTTP_404_NOT_FOUND: ResponseClassPayment.NotFound.value,
                  status.HTTP_409_CONFLICT: ResponseClassPayment.Conflict.value
              })
async def patch(paymentCRUD: Annotated[IPaymentCRUD, Depends(get_payment_crud)],
                payment_uid: UUID,
                payment_update: PaymentUpdate,
                db: session = Depends(payment_database.get_db)):
    return await PaymentService(paymentCRUD=paymentCRUD,db=db).patch(payment_uid, payment_update)
