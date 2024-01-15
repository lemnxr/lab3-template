import requests
import json
from requests import Response
from enums.status import LoyaltyStatus
from fastapi import status

from cruds.interfaces.loyalty import ILoyaltyCRUD
from cruds.base import BaseCRUD
from schemas.loyalty import CreateLoyaltyRequest

from utils.settings import get_settings
from utils.curcuitBreaker import CircuitBreaker


class LoyaltyCRUD(ILoyaltyCRUD, BaseCRUD):
    def __init__(self):
        settings = get_settings()
        loyalty_host = settings["services"]["gateway"]["loyalty_host"]
        loyalty_port = settings["services"]["loyalty"]["port"]

        self.http_path = f'http://{loyalty_host}:{loyalty_port}/api/v1/'

    async def get_all_loyalties(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}loyalties/?page={page}&size={size}',
            http_method=requests.get
        )
        self._check_status_code(
            status_code=response.status_code,
            service_name="Loyalty Service"
        )

        return response.json()
        
    async def get_loyalty_by_username(
            self,
            user_name: str
    ):
        response: Response = CircuitBreaker.send_request(
            url=f'{self.http_path}loyalties/username/{user_name}',
            http_method=requests.get
        )
        # self._check_status_code(
        #      status_code=response.status_code,
        #      service_name="Loyalty Service"
        #      ) 

        if response.status_code == 404:
            return None
        else:
            self._check_status_code(
            status_code=response.status_code,
            service_name="Loyalty Service"
            )  
        return response.json()
    
    async def get_new_loyalty(
            self,
            loyalty: CreateLoyaltyRequest
    ):
        

        loyalty_data = {"username": f"{loyalty.username}", "status": f"{loyalty.status}", "discount": loyalty.discount, "reservation_count": loyalty.reservation_count}
        loyalty_data_json = json.dumps(loyalty_data)

        try:
            response: Response = requests.post(url=f'{self.http_path}loyalties/', data=loyalty_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE


        self._check_status_code(
            status_code=response.status_code,
            service_name="Loyalty Service"
        )
        return loyalty_data
    
    async def increase_loyalty(
            self,
            user_name: int,
            reservation_count: int
    ):
        reservation_count += 1

        if reservation_count >= 20:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Gold.value, "discount": 10}
        elif reservation_count >= 10:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Silver.value, "discount": 7}
        else:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Bronze.value, "discount": 5}
            
        loyalty_data_json = json.dumps(loyalty_data)

        try:
            response: Response = requests.patch(url=f'{self.http_path}loyalties/{user_name}', data=loyalty_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        self._check_status_code(
            status_code=response.status_code,
            service_name="Loyalty Service"
        )
        return loyalty_data
    
    async def decrease_loyalty(
            self,
            user_name: int,
            reservation_count: int
    ):
        reservation_count -= 1

        if reservation_count >= 20:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Gold.value, "discount": 10}
        elif reservation_count >= 10:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Silver.value, "discount": 7}
        else:
            loyalty_data = {"reservation_count": reservation_count, "status": LoyaltyStatus.Bronze.value, "discount": 5}
            
        loyalty_data_json = json.dumps(loyalty_data)
        
        try:
            response: Response = requests.patch(url=f'{self.http_path}loyalties/{user_name}', data=loyalty_data_json)
        except:
            response = Response()
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        self._check_status_code(
            status_code=response.status_code,
            service_name="Loyalty Service"
        )
        return loyalty_data
    