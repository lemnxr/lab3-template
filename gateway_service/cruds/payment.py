import requests
import json
from uuid import UUID
from requests import Response
from enums.status import PaymentStatus
from fastapi import status

from cruds.interfaces.payment import IPaymentCRUD
from cruds.base import BaseCRUD

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker


class PaymentCRUD(IPaymentCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        payment_host = settings["services"]["gateway"]["payment_host"]
        payment_port = settings["services"]["payment"]["port"]
        self.http_path = f'http://{payment_host}:{payment_port}/api/v1/'

    async def get_all_payments(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}payments/?page={page}&size={size}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Payment Service"
        )

        return response.json()
    
    async def get_payment_by_uid(
            self,
            payment_uid: UUID
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}payments/{payment_uid}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Payment Service"
        )

        return response.json()
        
    async def get_new_payment(
            self,
            payment_uid: UUID,
            full_price: int
    ):
        payment_data = {"payment_uid": payment_uid, "status": PaymentStatus.Paid.value, "price": full_price}
        payment_data_json = json.dumps(payment_data)

        try:
            response: Response = requests.post(url=f'{self.http_path}payments/', data=payment_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            
        self._check_status_code(
            status_code=response.status_code,
            service_name="Payment Service"
        )

        return payment_data
    
    async def payment_cancel(
            self,
            payment_uid: UUID
    ):
        cancel_data = {"status": f"{PaymentStatus.Canceled.value}"}
        cancel_data_json = json.dumps(cancel_data)

        try:
            response: Response = requests.patch(url=f'{self.http_path}payments/{payment_uid}', data=cancel_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        self._check_status_code(
            status_code=response.status_code,
            service_name="Payment Service"
        )
        
        