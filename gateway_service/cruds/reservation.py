import requests
import json
from uuid import UUID
from requests import Response
from enums.status import ReservationStatus
from datetime import datetime
from fastapi import status

from cruds.interfaces.reservation import IReservationCRUD
from cruds.base import BaseCRUD

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker


class ReservationCRUD(IReservationCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        reservation_host = settings["services"]["gateway"]["reservation_host"]
        reservation_port = settings["services"]["reservation"]["port"]
        self.http_path = f'http://{reservation_host}:{reservation_port}/api/v1/'

    async def get_all_hotels(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}hotels/?page={page}&size={size}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
        )

        return response.json()
        
    async def get_hotels_num(
            self
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}hotels/',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
        )

        return len(response.json())
    
    async def get_hotel_by_id(
            self,
            hotel_id: int
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}hotels/{hotel_id}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
        )

        return response.json()
    
    async def get_hotel_by_uid(
            self,
            hotel_uid: UUID
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}hotels/uid/{hotel_uid}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
        )

        return response.json()
    
    async def get_reservations_by_username(
            self,
            user_name: str
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}reservations/username/{user_name}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
        )

        return response.json()
    
    async def get_reservation_by_uid(
            self,
            reservation_uid: UUID
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}reservations/{reservation_uid}',
            http_method=requests.get
        )

        # if response.status_code == 404:
        #     return None
        # else:
        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
            )
            
        return response.json()
        
    async def get_new_reservation(
            self,
            username: str,
            hotel_id: int,
            res_status: str,
            start_date: datetime,
            end_date = datetime
    ):
        reservation_data = {"username": f"{username}", "hotel_id": f"{hotel_id}", "status": f"{res_status}", "start_date": f"{start_date}", "end_date": f"{end_date}"}
        reservation_data_json = json.dumps(reservation_data)

        try:
            response: Response = requests.post(url=f'{self.http_path}reservations/', data=reservation_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        self._check_status_code(
            status_code=response.status_code,
            service_name="Reservation Service"
            )
       
        location: str = response.headers["location"]

        uid = location.split("/")[-1]
    
        return uid
    
    async def reservation_cancel(
            self,
            reservation_uid: UUID
    ):
        cancel_data = {"status": f"{ReservationStatus.Canceled.value}"}
        cancel_data_json = json.dumps(cancel_data)
        
        try:
            response: Response = requests.patch(url=f'{self.http_path}reservations/{reservation_uid}', data=cancel_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
