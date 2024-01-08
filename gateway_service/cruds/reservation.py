import requests
import json
from uuid import UUID
from requests import Response
from enums.status import ReservationStatus
from datetime import datetime

from cruds.interfaces.reservation import IReservationCRUD
from cruds.base import BaseCRUD


class ReservationCRUD(IReservationCRUD, BaseCRUD):
    def __init__(self):
        self.http_path = f'http://reservation_service:8070/api/v1/'

    async def get_all_hotels(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = requests.get(
            url=f'{self.http_path}hotels/?page={page}&size={size}'
        )
        return response.json()
        
    async def get_hotels_num(
            self
    ):
        response: Response = requests.get(
            url=f'{self.http_path}hotels/'
        )
        return len(response.json())
    
    async def get_hotel_by_id(
            self,
            hotel_id: int
    ):
        response: Response = requests.get(
            url=f'{self.http_path}hotels/{hotel_id}'
        )
        return response.json()
    
    async def get_hotel_by_uid(
            self,
            hotel_uid: UUID
    ):
        response: Response = requests.get(
            url=f'{self.http_path}hotels/uid/{hotel_uid}'
        )
        return response.json()
    
    async def get_reservations_by_username(
            self,
            user_name: str
    ):
        response: Response = requests.get(
            url=f'{self.http_path}reservations/username/{user_name}'
        )
        return response.json()
    
    async def get_reservation_by_uid(
            self,
            reservation_uid: UUID
    ):
        response: Response = requests.get(
            url=f'{self.http_path}reservations/{reservation_uid}'
        )

        if response.status_code == 404:
            return None
        else:
            return response.json()
        
    async def get_new_reservation(
            self,
            username: str,
            hotel_id: int,
            status: str,
            start_date: datetime,
            end_date = datetime
    ):
        reservation_data = {"username": f"{username}", "hotel_id": f"{hotel_id}", "status": f"{status}", "start_date": f"{start_date}", "end_date": f"{end_date}"}
        reservation_data_json = json.dumps(reservation_data)

        response: Response = requests.post(url=f'{self.http_path}reservations/', data=reservation_data_json)
       
        location: str = response.headers["location"]

        uid = location.split("/")[-1]
    
        return uid
    
    async def reservation_cancel(
            self,
            reservation_uid: UUID
    ):
        cancel_data = {"status": f"{ReservationStatus.Canceled.value}"}
        cancel_data_json = json.dumps(cancel_data)

        requests.patch(url=f'{self.http_path}reservations/{reservation_uid}', data=cancel_data_json)
        