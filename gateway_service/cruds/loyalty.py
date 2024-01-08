import requests
import json
from requests import Response
from enums.status import LoyaltyStatus

from cruds.interfaces.loyalty import ILoyaltyCRUD
from cruds.base import BaseCRUD
from schemas.loyalty import CreateLoyaltyRequest


class LoyaltyCRUD(ILoyaltyCRUD, BaseCRUD):
    def __init__(self):
        self.http_path = f'http://loyalty_service:8050/api/v1/'

    async def get_all_loyalties(
            self,
            page: int = 1,
            size: int = 100,
        ):
        response: Response = requests.get(
            url=f'{self.http_path}loyalties/?page={page}&size={size}'
        )
        return response.json()
        
    async def get_loyalty_by_username(
            self,
            user_name: str
    ):
        response: Response = requests.get(
            url=f'{self.http_path}loyalties/username/{user_name}'
        )

        if response.status_code == 404:
            return None
        else:
            return response.json()
    
    async def get_new_loyalty(
            self,
            loyalty: CreateLoyaltyRequest
    ):
        loyalty_data = {"username": f"{loyalty.username}", "status": f"{loyalty.status}", "discount": loyalty.discount, "reservation_count": loyalty.reservation_count}
        loyalty_data_json = json.dumps(loyalty_data)

        requests.post(url=f'{self.http_path}loyalties/', data=loyalty_data_json)
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
        
        requests.patch(url=f'{self.http_path}loyalties/{user_name}', data=loyalty_data_json)
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
        
        requests.patch(url=f'{self.http_path}loyalties/{user_name}', data=loyalty_data_json)
        return loyalty_data
    