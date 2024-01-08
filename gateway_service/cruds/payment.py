import requests
import json
from uuid import UUID
from requests import Response
from enums.status import PaymentStatus

from cruds.interfaces.payment import IPaymentCRUD
from cruds.base import BaseCRUD


class PaymentCRUD(IPaymentCRUD, BaseCRUD):
    def __init__(self):
        self.http_path = f'http://payment_service:8060/api/v1/'

    async def get_all_payments(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = requests.get(
            url=f'{self.http_path}payments/?page={page}&size={size}'
        )
        return response.json()
    
    async def get_payment_by_uid(
            self,
            payment_uid: UUID
    ):
        #response_list: Response = requests.get(url=f'{self.http_path}payments/')
        #print("payments_list:",response_list.json())
        #print("get_payment_uid:", payment_uid)
        response: Response = requests.get(
            url=f'{self.http_path}payments/{payment_uid}'
        )
        return response.json()
        
    async def get_new_payment(
            self,
            payment_uid: UUID,
            full_price: int
    ):
        payment_data = {"payment_uid": payment_uid, "status": PaymentStatus.Paid.value, "price": full_price}
        payment_data_json = json.dumps(payment_data)
        requests.post(url=f'{self.http_path}payments/', data=payment_data_json)

        return payment_data
    
    async def payment_cancel(
            self,
            payment_uid: UUID
    ):
        cancel_data = {"status": f"{PaymentStatus.Canceled.value}"}
        cancel_data_json = json.dumps(cancel_data)

        requests.patch(url=f'{self.http_path}payments/{payment_uid}', data=cancel_data_json)
        