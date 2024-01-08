from copy import deepcopy
from datetime import datetime as dt

from cruds.mocks.reservation import ReservationMockCRUD
from cruds.mocks.data import ReservationDataMock
from services.reservation import ReservationService
from schemas.reservation import ReservationRequest, Reservation
from models.reservation import ReservationModel
from exceptions.exceptions import NotFoundException, ConflictException


reservationService = ReservationService(
    reservationCRUD=ReservationMockCRUD,
    db=None
)
correct_reservations = deepcopy(ReservationDataMock._reservations)


def model_into_dict(model: ReservationModel) -> dict:
    dictionary = model.__dict__
    del dictionary["_sa_instance_state"]
    return dictionary


async def test_get_all_reservations_success():
    try:
        reservations = await reservationService.get_all()

        assert len(reservations) == len(correct_reservations)
        for i in range(len(reservations)):
            assert model_into_dict(reservations[i]) == correct_reservations[i]
    except:
        assert False


async def test_get_reservation_by_uid_success():
    try:
        reservation = await reservationService.get_by_uid("dc716ca3-3b31-4375-a845-103c79d28b08")

        assert model_into_dict(reservation) == correct_reservations[0]
    except:
        assert False


async def test_get_reservation_by_id_not_found():
    try:
        await reservationService.get_by_uid("dc716ca3-3b31-4375-a845-111111111111")

        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_add_reservation_success():
    try:
        reservation = await reservationService.add(
            Reservation(
                username = "user",
                hotel_id = 1,
                status = "PAID",
                start_date = "2023-11-19",
                end_date = "2023-11-22",
                reservation_uid = "901dc631-ea2f-4ae6-8840-b66058cfd37d",
                id = 4,
                payment_uid = "6af4762c-763c-4038-81a2-a2d95263ddc0"
            ),
        )
        
        assert True
    except:
        assert False

async def test_add_reservation_conflict():
    try:
        reservation = await reservationService.add(
            Reservation(
                username = "user_not_found",
                hotel_id = 25,
                status = "PAID",
                start_date = "2023-11-19",
                end_date = "2023-11-22",
                reservation_uid = "901dc631-ea2f-4ae6-8840-b66058cfd37d",
                payment_uid = "6af4762c-763c-4038-81a2-a2d95263ddc0"
            ),
        )
        
        assert False
    except:
        assert True

async def test_delete_reservation_success():
    try:
        await reservationService.delete("801dc631-ea2f-4ae6-8840-b66058cfd37d")
        assert True
    except:
        assert False


async def test_delete_reservation_not_found():
    try:
        await reservationService.delete(10)
        
        assert False
    except NotFoundException:
        assert True
    except:
        assert False
