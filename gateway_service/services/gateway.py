from uuid import UUID
from datetime import datetime

from cruds.interfaces.reservation import IReservationCRUD
from cruds.interfaces.payment import IPaymentCRUD
from cruds.interfaces.loyalty import ILoyaltyCRUD
from exceptions.exceptions import NotFoundException, ConflictException
from enums.status import ReservationStatus, PaymentStatus, LoyaltyStatus
from schemas.user import UserInfoResponse
from schemas.reservation import *
from schemas.payment import PaymentInfo
from schemas.loyalty import LoyaltyInfoResponse, CreateLoyaltyRequest


class GatewayService():
    def __init__(self,
                 reservationCRUD: type[IReservationCRUD],
                 paymentCRUD: type[IPaymentCRUD],
                 loyaltyCRUD: type[ILoyaltyCRUD]
                 ):
        self._reservationCRUD = reservationCRUD()
        self._paymentCRUD = paymentCRUD()
        self._loyaltyCRUD = loyaltyCRUD()

    async def get_all_hotels(self, page: int, size: int):
        hotels_list = await self._reservationCRUD.get_all_hotels(page=page, size=size)
        hotels_num = await self._reservationCRUD.get_hotels_num()
        hotels = []
        
        for hotel_dict in hotels_list:
            hotels.append(
                HotelResponse(
                    hotel_uid=hotel_dict["hotel_uid"],
                    name=hotel_dict["name"],
                    country=hotel_dict["country"],
                    city=hotel_dict["city"],
                    address=hotel_dict["address"],
                    stars=hotel_dict["stars"],
                    price=hotel_dict["price"]
                )
            )
        
        return PaginationResponse(
            page=page,
            pageSize=size,
            totalElements=hotels_num,
            items=hotels
        )
    
    async def __get_hotel_by_id(self, hotel_id: int):
        if hotel_id:
            hotel_dict = await self._reservationCRUD.get_hotel_by_id(hotel_id)
        else:
            hotel_dict = None
        return hotel_dict
    
    async def __get_hotel_by_uid(self, hotel_uid: UUID):
        if hotel_uid:
            hotel_dict = await self._reservationCRUD.get_hotel_by_uid(hotel_uid)
        else:
            hotel_dict = None
        return hotel_dict
    
    async def __get_payment_by_uid(self, payment_uid: UUID):
        if payment_uid:
            payment_dict = await self._paymentCRUD.get_payment_by_uid(payment_uid)
        else:
            payment_dict = None
        return payment_dict
    
    async def _get_user_reservations_hotels(self, user_name: str):
        reservations_list = await self._reservationCRUD.get_reservations_by_username(user_name=user_name)
        #print("username:",user_name)
        #print("reservations_list:",reservations_list)
        reservations = []

        for i in range(len(reservations_list)):
            #print("i:", i)
            #print(reservations_list[i]["payment_uid"])
            #print(reservations_list[i])
            hotel_dict = await self.__get_hotel_by_id(reservations_list[i]["hotel_id"])
            payment_dict = await self.__get_payment_by_uid(reservations_list[i]["payment_uid"])
            #print(reservation_dict)
            #print(payment_dict)
            hotel_info = HotelInfo(
                hotel_uid=hotel_dict["hotel_uid"],
                name=hotel_dict["name"],
                fullAddress=hotel_dict["country"]+", "+hotel_dict["city"]+", "+hotel_dict["address"],
                stars=hotel_dict["stars"]
                )
            
            payment_info = PaymentInfo(
                status=payment_dict["status"],
                price=payment_dict["price"]
                )

            reservations.append(
                ReservationResponse(
                    reservation_uid=reservations_list[i]["reservation_uid"],
                    hotel=hotel_info,
                    start_date=reservations_list[i]["start_date"],
                    end_date=reservations_list[i]["end_date"],
                    status=reservations_list[i]["status"],
                    payment=payment_info
                )
            )
        return reservations

    async def __get_loyalty_by_username(self, user_name: str):
        if user_name:
            loyalty_dict = await self._loyaltyCRUD.get_loyalty_by_username(user_name)
        else:
            loyalty_dict = None
        return loyalty_dict
    
    async def _get_user_loyalty(self, user_name: str):
        loyalty_dict = await self.__get_loyalty_by_username(user_name)

        if loyalty_dict == None:
            loyalty_dict = dict((await self._loyaltyCRUD.get_new_loyalty(
                CreateLoyaltyRequest(
                    username=user_name,
                    status=LoyaltyStatus.Bronze.value,
                    discount=5,
                    reservation_count=0
                    )
                )
            )
        )
        return loyalty_dict
    
    async def get_user_info(self, user_name: str):
        reservations = await self._get_user_reservations_hotels(user_name)
        loyalty = await self._get_user_loyalty(user_name)

        return UserInfoResponse(
            reservations=reservations,
            loyalty=loyalty
        )

    async def get_user_reservations(self, user_name: str):
        reservations = await self._get_user_reservations_hotels(user_name)
        return reservations
    
    async def reserve_hotel(self, user_name: str, hotel_reservation_request: CreateReservationRequest):
        hotel = await self.__get_hotel_by_uid(hotel_reservation_request.hotel_uid)

        if hotel == None:
            raise NotFoundException(prefix="Get Hotel")
        
        days = (hotel_reservation_request.end_date - hotel_reservation_request.start_date).days

        if days < 1:
            raise ConflictException(prefix="Reserve Hotel")
        
        new_reservation_uid = await self._reservationCRUD.get_new_reservation(
            username = user_name,
            hotel_id = hotel["id"],
            status = PaymentStatus.Paid.value,
            start_date = hotel_reservation_request.start_date,
            end_date = hotel_reservation_request.end_date
        )

        new_reservation = await self._reservationCRUD.get_reservation_by_uid(new_reservation_uid)

        full_price = int(hotel["price"]) * days

        loyalty = await self._get_user_loyalty(user_name)

        full_price = full_price * ((100 - int(loyalty["discount"])) / 100)

        new_payment = await self._paymentCRUD.get_new_payment(new_reservation["payment_uid"], full_price)
        new_loyalty = await self._loyaltyCRUD.increase_loyalty(loyalty["username"], loyalty["reservation_count"])

        return CreateReservationResponse(
                        reservation_uid=new_reservation_uid, 
                        hotel_uid=hotel["hotel_uid"],
                        start_date=hotel_reservation_request.start_date,
                        end_date=hotel_reservation_request.end_date,
                        discount=new_loyalty["discount"],
                        status=ReservationStatus.Paid.value,
                        payment=PaymentInfo(
                            status=new_payment["status"],
                            price=new_payment["price"])
                )

    async def get_reservation_info(self, user_name: str, reservation_uid: UUID):
        reservation = await self._reservationCRUD.get_reservation_by_uid(reservation_uid)

        if reservation == None:
            raise NotFoundException(prefix="Not Found")

        if reservation["username"] != user_name:
            raise NotFoundException(prefix="Incorrect username")
    
        hotel = await self.__get_hotel_by_id(reservation["hotel_id"])
        payment = await self.__get_payment_by_uid(reservation["payment_uid"])

        hotel_info = HotelInfo(
            hotel_uid=hotel["hotel_uid"],
            name=hotel["name"],
            fullAddress=hotel["country"]+", "+hotel["city"]+", "+hotel["address"],
            stars=hotel["stars"]
        )
            
        payment_info = PaymentInfo(
                status=payment["status"],
                price=payment["price"]
        )

        reservation_response = ReservationResponse(
                    reservation_uid=reservation["reservation_uid"],
                    hotel=hotel_info,
                    start_date=reservation["start_date"],
                    end_date=reservation["end_date"],
                    status=reservation["status"],
                    payment=payment_info
                )
        return reservation_response
    
    async def reservation_cancel(self, user_name: str, reservation_uid: UUID):
        reservation = await self._reservationCRUD.get_reservation_by_uid(reservation_uid)

        if reservation == None:
            raise NotFoundException(prefix="Not Found")

        if reservation["username"] != user_name:
            raise NotFoundException(prefix="Incorrect username")
        
        await self._reservationCRUD.reservation_cancel(reservation_uid)
        await self._paymentCRUD.payment_cancel(reservation["payment_uid"])

        loyalty = await self._get_user_loyalty(user_name)
        await self._loyaltyCRUD.decrease_loyalty(loyalty["username"], loyalty["reservation_count"])

        return reservation
    
    async def get_loyalty(self, user_name: str):
        loyalty = await self._get_user_loyalty(user_name)

        loyalty_info = LoyaltyInfoResponse(
            status=loyalty["status"],
            discount=loyalty["discount"],
            reservation_count=loyalty["reservation_count"]
        )
        return loyalty_info
    